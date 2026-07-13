#!/usr/bin/env python3
r"""Konversi draf Markdown (v2/drafts) -> fragmen LaTeX (BookTEX/chapters).

Sumber naskah FINAL = v2/drafts/chNN/*.md (bukan lagi website/*.qmd).
Alur:
  1. Pilih berkas draf per bab (ch01 -> _v4_reflow, sisanya -> _v2).
  2. Pra-proses konvensi khas draf sebelum pandoc:
       - "# Bab N. Judul"      -> "# Judul"        (nomor bab otomatis)
       - "## N.N Judul"        -> "## Judul"       (nomor subbab otomatis)
       - "## Sintesis Bab N"   -> buka kotak \begin{sintesis}
       - blok "[GAMBAR N.N] ..." -> blok raw-LaTeX \begin{figure}\includegraphics
       - baris "Tabel N.N - ..." -> \tabeljudul{...}
  3. pandoc markdown -> latex (--listings, --top-level-division=chapter).
  4. Pasca-proses hasil pandoc:
       - paragraf "\textbf{Pendalaman: Judul.} isi" -> \begin{pendalaman}{Judul} isi \end{pendalaman}
       - tutup kotak \end{sintesis} di akhir berkas bila ada
       - batalkan escape di \lstinline
       - rapikan longtable lebar agar muat lebar teks B5

Pemakaian:
  python tools/md2tex.py            # semua bab (ch01..ch17)
  python tools/md2tex.py ch01 ch03  # bab tertentu
"""
from __future__ import annotations
import json, os, re, subprocess, sys, tempfile
from pathlib import Path

OUT_ROOT = Path(__file__).resolve().parents[1]              # .../BookTEX
CH_DIR   = OUT_ROOT / "chapters"
FIG_DIR  = OUT_ROOT / "figures"
# .../BookTEX -> NulisBuku -> "Buku 1"; draf ada di "Buku 1/v2/drafts"
DRAFT_DIR = OUT_ROOT.parents[1] / "v2" / "drafts"

# Lebar/tinggi cetak per figur mermaid (tools/size_figs.py) -- dihitung agar
# ukuran huruf label mendekati target tetap, dibatasi kotak halaman B5,
# bukan dipaksa selalu 0.92\linewidth (lihat catatan di size_figs.py).
_SIZES_PATH = FIG_DIR / "sizes.json"
FIG_SIZES: dict = json.loads(_SIZES_PATH.read_text(encoding="utf-8")) if _SIZES_PATH.exists() else {}

# Berkas draf per bab: ch01 memakai varian reflow, sisanya _draft_v2.
def draft_path(stem: str) -> Path:
    ch = stem  # "ch01"
    if ch == "ch01":
        return DRAFT_DIR / ch / "ch01_draft_v4_reflow.md"
    return DRAFT_DIR / ch / f"{ch}_draft_v2.md"


# --------------------------------------------------------------------------
# Util escape/inline untuk teks yang masuk langsung ke raw-LaTeX (caption dsb.)
# --------------------------------------------------------------------------
def md_inline_to_tex(s: str) -> str:
    r"""Konversi *emphasis* -> \emph{...}, `code` -> \texttt{...}, escape &%#."""
    s = s.strip()
    # `code`
    s = re.sub(r"`([^`]+)`", lambda m: r"\texttt{" + _esc(m.group(1)) + "}", s)
    # *italic* / _italic_ (non-greedy, hindari ** ganda)
    s = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"\\emph{\1}", s)
    s = re.sub(r"(?<!_)_([^_]+)_(?!_)", r"\\emph{\1}", s)
    # escape karakter khusus yang tersisa di teks biasa
    s = _esc(s, keep_backslash=True)
    return s


def _esc(s: str, keep_backslash: bool = False) -> str:
    for a, b in [("&", r"\&"), ("%", r"\%"), ("#", r"\#")]:
        s = s.replace(a, b)
    return s


# --------------------------------------------------------------------------
# Pra-proses Markdown
# --------------------------------------------------------------------------
GAMBAR_RE = re.compile(r"^\[GAMBAR\s+(\d+)\.(\d+)\]\s*$")
JUDUL_RE  = re.compile(r"^Judul:\s*(.*?)\s*$")
CHAP_RE   = re.compile(r"^#\s+Bab\s+\d+\.?\s*(.*)$")
SEC_RE    = re.compile(r"^(#{2,6})\s+(?:\d+\.\d+\.?\s+)?(.*)$")
SINTESIS_RE = re.compile(r"^#{2,6}\s+Sintesis\b", re.IGNORECASE)
BACAAN_RE   = re.compile(r"^#{2,6}\s+Bacaan\s+Lanjutan\b", re.IGNORECASE)
TABEL_RE  = re.compile(r"^(Tabel\s+\d+\.\d+)\s*[-–—]\s*(.*)$")


def preprocess(md: str, stem: str) -> tuple[str, bool]:
    """Kembalikan (markdown_terproses, ada_sitasi).

    Materi akhir bab dirakit berurutan: kotak Sintesis -> kotak Bacaan Lanjutan
    -> daftar Rujukan (bila ada sitasi). Kotak ditutup rapi sebelum blok berikut.
    """
    ch_num = int(re.sub(r"\D", "", stem))
    lines = md.splitlines()
    out: list[str] = []
    has_cite = "[@" in md
    open_box: str | None = None    # 'sintesis' | 'bacaan'

    def close_box() -> None:
        nonlocal open_box
        if open_box:
            out.extend(["", "```{=latex}", f"\\end{{{open_box}}}", "```", ""])
            open_box = None

    i, n = 0, len(lines)
    while i < n:
        line = lines[i]

        # --- kepala bab: buang "Bab N." ---
        mc = CHAP_RE.match(line)
        if mc:
            close_box()
            out.append(f"# {mc.group(1).strip()}")
            i += 1
            continue

        # --- Sintesis Bab N -> buka kotak sintesis ---
        if SINTESIS_RE.match(line):
            close_box()
            out.extend(["", "```{=latex}", "\\begin{sintesis}", "```", ""])
            open_box = "sintesis"
            i += 1
            continue

        # --- Bacaan Lanjutan -> buka kotak bacaan ---
        if BACAAN_RE.match(line):
            close_box()
            out.extend(["", "```{=latex}", "\\begin{bacaan}", "```", ""])
            open_box = "bacaan"
            i += 1
            continue

        # --- kepala subbab lain: buang nomor "N.N" ---
        ms = SEC_RE.match(line)
        if ms:
            close_box()
            out.append(f"{ms.group(1)} {ms.group(2).strip()}")
            i += 1
            continue

        # --- blok [GAMBAR N.N] ---
        mg = GAMBAR_RE.match(line)
        if mg:
            fig = int(mg.group(2))
            img = f"ch{ch_num:02d}-fig-{fig}"
            caption = ""
            i += 1
            while i < n and lines[i].strip() != "":
                mj = JUDUL_RE.match(lines[i])
                if mj and not caption:
                    caption = mj.group(1).rstrip(".")
                i += 1
            cap_tex = md_inline_to_tex(caption)
            sz = FIG_SIZES.get(img)
            if sz:
                incl = f"\\includegraphics[width={sz['width_mm']}mm]{{{img}}}"
            else:
                # Tak ada di sizes.json (mis. plot PNG bukan-mermaid): batasi
                # lebar & tinggi maksimum, jangan pernah paksa selebar teks.
                incl = f"\\includegraphics[width=0.92\\linewidth,height=119mm,keepaspectratio]{{{img}}}"
            out += [
                "", "```{=latex}",
                "\\begin{figure}[tbp]\\centering",
                incl,
                f"\\caption{{{cap_tex}}}",
                f"\\label{{fig:{img}}}",
                "\\end{figure}",
                "```", "",
            ]
            continue

        # --- baris judul tabel "Tabel N.N - ..." ---
        mt = TABEL_RE.match(line)
        if mt:
            title = f"{mt.group(1)} — {md_inline_to_tex(mt.group(2))}"
            out += ["", "```{=latex}", f"\\tabeljudul{{{title}}}", "```", ""]
            i += 1
            continue

        out.append(line)
        i += 1

    close_box()

    # Daftar Rujukan per bab (citeproc mengisi div #refs dengan karya terkutip).
    if has_cite:
        out.extend(["", "```{=latex}", "\\rujukanheading", "```",
                    "", "::: {#refs}", ":::", ""])

    return "\n".join(out) + "\n", has_cite


# --------------------------------------------------------------------------
# pandoc
# --------------------------------------------------------------------------
BIB = OUT_ROOT / "references.bib"


def run_pandoc(md: str) -> str:
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as f:
        f.write(md); tmp = f.name
    try:
        cmd = ["pandoc", tmp,
               "-f", "markdown+lists_without_preceding_blankline+raw_attribute",
               "-t", "latex", "--listings",
               "--top-level-division=chapter", "--wrap=preserve"]
        if BIB.exists():
            cmd += ["--citeproc", f"--bibliography={BIB}"]
        res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
        if res.returncode != 0:
            raise RuntimeError(res.stderr)
        return res.stdout
    finally:
        os.unlink(tmp)


# --------------------------------------------------------------------------
# Pasca-proses LaTeX
# --------------------------------------------------------------------------
def match_brace(s: str, open_idx: int) -> int:
    """Diberi indeks '{', kembalikan indeks '}' pasangannya."""
    depth = 0
    for k in range(open_idx, len(s)):
        if s[k] == "{":
            depth += 1
        elif s[k] == "}":
            depth -= 1
            if depth == 0:
                return k
    return len(s) - 1


def wrap_pendalaman(tex: str) -> str:
    r"""Paragraf diawali \textbf{Pendalaman: Judul.} -> kotak pendalaman."""
    needle = "\\textbf{Pendalaman:"
    idx = 0
    while True:
        m = tex.find(needle, idx)
        if m < 0:
            break
        brace_open = tex.find("{", m)
        j = match_brace(tex, brace_open)
        inner = tex[brace_open + 1:j]                    # "Pendalaman: Judul."
        title = inner[len("Pendalaman:"):].strip()
        if title.endswith("."):
            title = title[:-1]
        para_end = tex.find("\n\n", j)
        if para_end < 0:
            para_end = len(tex)
        body = tex[j + 1:para_end].strip()
        repl = f"\\begin{{pendalaman}}{{{title}}}\n{body}\n\\end{{pendalaman}}"
        tex = tex[:m] + repl + tex[para_end:]
        idx = m + len(repl)
    return tex


# Batalkan escape LaTeX di dalam \lstinline (isinya verbatim).
_LST_UNESCAPE = [
    (r"\textbackslash{}", "\\"), (r"\textasciitilde{}", "~"),
    (r"\textasciicircum{}", "^"),
    (r"\_", "_"), (r"\%", "%"), (r"\#", "#"), (r"\&", "&"),
    (r"\$", "$"), (r"\{", "{"), (r"\}", "}"),
]
_LSTINLINE = re.compile(r"\\lstinline(?P<d>.)(?P<c>.*?)(?P=d)")


def fix_inline_code(tex: str) -> str:
    def repl(m: re.Match) -> str:
        c = m.group("c")
        for a, b in _LST_UNESCAPE:
            c = c.replace(a, b)
        return f"\\lstinline{m.group('d')}{c}{m.group('d')}"
    return _LSTINLINE.sub(repl, tex)


_MINIPAGE_OPEN = re.compile(r"\\begin\{minipage\}\[[bt]\]\{[^}]*\}(\\raggedright|\\centering|\\raggedleft)?")

# Identifier kode panjang tanpa spasi (mis. "StratifiedGroupKFold") tak punya
# titik potong baris di dalam \lstinline -> meluber ke kolom sebelah pada
# sel tabel sempit. Untuk sel tabel saja, ganti dengan \texttt{\seqsplit{...}}
# yang boleh dipenggal di sembarang huruf.
_LSTINLINE_ANY = re.compile(r"\\passthrough\{\\lstinline(?P<d>.)(?P<c>.*?)(?P=d)\}")


def _tex_escape_verbatim(s: str) -> str:
    s = s.replace("\\", r"\textbackslash{}")
    for a, b in [("_", r"\_"), ("%", r"\%"), ("#", r"\#"), ("&", r"\&"),
                 ("$", r"\$"), ("{", r"\{"), ("}", r"\}"),
                 ("^", r"\^{}"), ("~", r"\~{}")]:
        s = s.replace(a, b)
    return s


def break_long_inline_code(text: str) -> str:
    r"""Dalam sel tabel: \lstinline!TokenPanjangTanpaSpasi! -> \texttt{\seqsplit{...}}."""
    def repl(m: re.Match) -> str:
        c = m.group("c")
        if len(c) > 13 and " " not in c:
            return "\\texttt{\\seqsplit{" + _tex_escape_verbatim(c) + "}}"
        return m.group(0)
    return _LSTINLINE_ANY.sub(repl, text)


# Istilah seperti "node2vec/DeepWalk" atau "GCN/GAT/GraphSAGE" tak punya
# spasi di sekitar "/" -> tak ada titik potong baris -> meluber ke kolom
# sebelah pada sel tabel sempit. \slash (bawaan kernel LaTeX) mencetak "/"
# tapi mengizinkan baris dipotong di situ. Lewati span \lstinline/\texttt/
# \url yang sudah verbatim/dilindungi agar "/" di dalamnya tak tersentuh.
_PROTECTED_SPAN = re.compile(
    r"\\lstinline(.)(?:(?!\1).)*\1"
    r"|\\texttt\{(?:[^{}]|\{[^{}]*\})*\}"
    r"|\\url\{[^}]*\}"
)


def allow_slash_breaks(text: str) -> str:
    out, last = [], 0
    for m in _PROTECTED_SPAN.finditer(text):
        out.append(text[last:m.start()].replace("/", "\\slash{}"))
        out.append(m.group(0))
        last = m.end()
    out.append(text[last:].replace("/", "\\slash{}"))
    return "".join(out)


_TEXLEN_STRIP = re.compile(r"\\slash\{\}|\\[a-zA-Z]+\*?|[{}\\]")
_WORDBREAK = re.compile(r"[\s_/]+")


def _visual_len_text(cell: str) -> str:
    r"""Teks tampak sel: buang perintah/kurung LaTeX, gabung baris jadi satu."""
    cell = cell.replace("\n", " ")
    cell = cell.replace("\\slash{}", "/")
    cell = _TEXLEN_STRIP.sub("", cell)
    return cell.strip()


def _visual_len(cell: str) -> int:
    return len(_visual_len_text(cell))


def _longest_unbreakable(text: str) -> int:
    r"""Token terpanjang yang benar2 tak bisa dilipat baris: pisah di spasi,
    '_' dan '/' juga, karena tabel mengizinkan potong baris di keduanya
    (lihat \renewcommand{\_} dan allow_slash_breaks di convert_longtable)."""
    words = [w for w in _WORDBREAK.split(text) if w]
    return max((len(w) for w in words), default=0)


def _split_row_cells(row: str, ncol: int) -> list[str] | None:
    r"""Pecah satu baris tabel di '&' level-atas (abaikan '\&' dan '&' dalam {})."""
    cells, cur, depth, i = [], [], 0, 0
    while i < len(row):
        ch = row[i]
        if ch == "\\" and i + 1 < len(row):
            cur.append(row[i:i + 2]); i += 2; continue
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
        if ch == "&" and depth == 0:
            cells.append("".join(cur)); cur = []; i += 1; continue
        cur.append(ch); i += 1
    cells.append("".join(cur))
    return cells if len(cells) == ncol else None


def estimate_col_ratios(body: str, ncol: int, floor: float = 0.16, ceil: float = 0.52) -> list[float]:
    r"""Lebar kolom proporsional terhadap panjang isi rata-rata, bukan sama rata.

    Tabel pandoc default membagi kolom sama rata (\real{0.3333} dst.) walau
    satu kolom berisi label singkat dan kolom lain berisi kalimat panjang --
    hasilnya kolom label terlalu lebar, kolom kalimat terlalu sempit/padat.
    """
    totals = [0] * ncol
    counts = [0] * ncol
    maxword = [0] * ncol
    for row in re.split(r"\\\\(?:\[[^\]]*\])?", body):
        # baris header sering tergabung satu segmen dengan "\toprule" (mis.
        # "\toprule\n\nInvoiceNo & ... \\") -- skip-if-startswith akan
        # membuang seluruh sel header, bukan cuma penandanya. Buang cuma
        # tokennya, biarkan sisa teks (isi sel) tetap terhitung.
        for tok in ("\\toprule", "\\midrule", "\\bottomrule", "\\endhead", "\\noalign{}"):
            row = row.replace(tok, "")
        row = row.strip()
        if not row or "&" not in row:
            continue
        cells = _split_row_cells(row, ncol)
        if cells is None:
            continue
        for idx, c in enumerate(cells):
            vlen = _visual_len(c)
            totals[idx] += vlen
            counts[idx] += 1
            maxword[idx] = max(maxword[idx], _longest_unbreakable(_visual_len_text(c)))
    # Sel dengan kalimat panjang tapi satu token tunggal tanpa spasi (mis.
    # header nama kolom "InvoiceDate") tak boleh dinilai sempit hanya karena
    # rata-rata sel di kolom itu pendek -- token itu sendiri tak bisa dilipat.
    weights = [
        max((totals[i] / counts[i]) if counts[i] else 1.0, maxword[i])
        for i in range(ncol)
    ]
    if sum(weights) <= 0:
        weights = [1.0] * ncol
    total = sum(weights)
    ratios = [w / total for w in weights]

    # Floor per kolom, bukan satu angka global: tabel lebar (mis. 8 kolom
    # pratinjau data) tak bisa dijatah floor absolut 0.16/kolom (8*0.16>1,
    # dan bahkan versi diskalakan 0.85/ncol masih bisa memangkas kolom di
    # bawah kebutuhan nyata token terpanjangnya, mis. header "InvoiceDate").
    # Dasar floor: proporsi maxword kolom itu sendiri terhadap total maxword
    # semua kolom -- menjamin lebar sebanding kebutuhan token tak terpotong
    # itu, lalu dibatasi juga oleh floor absolut default untuk tabel sempit.
    maxword_total = sum(maxword) or ncol
    col_floor = [
        min(floor, 0.98 * maxword[i] / maxword_total) if maxword[i] else 0.0
        for i in range(ncol)
    ]
    ceil = max(ceil, max(col_floor))

    # Water-filling: kunci kolom yang melanggar floor/ceil, sebar ulang sisanya
    # proporsional -- clamp lalu renormalize satu langkah bisa membuat kolom
    # yang baru dinaikkan ke floor turun lagi di bawah floor.
    locked = {}
    free = set(range(ncol))
    for _ in range(ncol):
        remaining = 1.0 - sum(locked.values())
        free_total = sum(ratios[i] for i in free)
        violated = None
        for i in free:
            share = (ratios[i] / free_total) * remaining if free_total > 0 else remaining / len(free)
            if share < col_floor[i]:
                violated = (i, col_floor[i])
                break
            if share > ceil:
                violated = (i, ceil)
                break
        if violated is None:
            break
        i, bound = violated
        locked[i] = bound
        free.discard(i)
    remaining = 1.0 - sum(locked.values())
    free_total = sum(ratios[i] for i in free)
    final = [0.0] * ncol
    for i in locked:
        final[i] = locked[i]
    for i in free:
        final[i] = (ratios[i] / free_total) * remaining if free_total > 0 else remaining / max(len(free), 1)

    final = [round(r, 3) for r in final]
    final[-1] = round(final[-1] + (1.0 - sum(final)), 3)
    return final


def convert_longtable(block: str) -> str:
    r"""Ubah longtable pandoc -> tabularx (kolom X melebar, teks melipat).

    Semua tabel dirender pada satu ukuran huruf tetap (\small); sel yang
    berisi kalimat panjang melipat ke beberapa baris alih-alih memaksa
    seluruh tabel diperkecil (adjustbox scale-down membuat ukuran huruf
    tak seragam antar tabel — itulah yang diganti di sini).
    """
    # 1) buang spesifikasi kolom p{...} pandoc, hitung jumlah kolom.
    b = block.find("[]{")
    open_brace = b + 2
    close = match_brace(block, open_brace)
    colspec = block[open_brace + 1:close]
    ncol = colspec.count(">{")
    content = block[close + 1:]
    content = content[:content.rfind("\\end{longtable}")]

    # 2) bersihkan perkakas longtable + minipage bungkus sel.
    for tok in ("\\endfirsthead", "\\endhead", "\\endlastfoot", "\\noalign{}"):
        content = content.replace(tok, "")
    content = _MINIPAGE_OPEN.sub("", content)
    content = content.replace("\\end{minipage}", "")
    content = content.replace("\\bottomrule", "")     # dipasang ulang di akhir

    if ncol == 0:  # cadangan: hitung dari baris pertama berisi '&'
        for ln in content.splitlines():
            if "&" in ln:
                ncol = ln.count("&") + 1
                break
        ncol = max(ncol, 1)

    # 3) rapikan baris kosong beruntun.
    lines = [ln for ln in content.splitlines()]
    body = "\n".join(lines).strip()
    body = break_long_inline_code(body)
    body = allow_slash_breaks(body)

    # Pengenal panjang (mis. "hari_sejak_transaksi_terakhir") tanpa spasi tak
    # punya titik potong baris -> overfull hbox. Izinkan potong sehabis "_".
    # Tabel: huruf lebih kecil dari teks utama (footnotesize) dan baris rapat
    # (arraystretch + linespread di-reset lokal, tak ikut 1.12 teks utama).
    # xltabular (bukan tabularx) dipakai agar tabel panjang boleh terpotong
    # antar-halaman -- pada trim 15.5x23cm, beberapa router/peta tabel lebih
    # tinggi dari satu halaman penuh; tabularx polos akan meluber diam-diam
    # ke luar batas fisik halaman (baris terakhir hilang, tak tercetak).
    # \endhead menandai header (toprule+judul+midrule) agar terulang tiap
    # potongan halaman.
    #
    # Lebar kolom proporsional (calc: p{(\linewidth-gap)*\real{rasio}}),
    # bukan X sama rata -- kolom berisi label singkat jadi sempit, kolom
    # berisi kalimat panjang jadi lega. \tabcolsep dipakai preamble.tex.
    ratios = estimate_col_ratios(body, ncol)
    gap = 2 * (ncol - 1)
    colspec_x = " ".join(
        f">{{\\raggedright\\arraybackslash}}p{{(\\linewidth-{gap}\\tabcolsep)*\\real{{{r:.3f}}}}}"
        for r in ratios
    )
    header, sep, rows = body.partition("\\midrule")
    if sep:
        body = f"{header}{sep}\n\\endhead\n{rows}"
    return (
        "\\par\\vspace{3pt}\\noindent\n"
        "\\begingroup\\renewcommand{\\arraystretch}{1.0}%\n"
        "\\scriptsize\\linespread{1}\\selectfont\n"
        "\\renewcommand{\\_}{\\textunderscore\\hspace{0pt}}%\n"
        f"\\begin{{xltabular}}{{\\linewidth}}{{@{{}}{colspec_x.strip()}@{{}}}}\n"
        f"{body}\n"
        "\\bottomrule\n"
        "\\end{xltabular}\\endgroup\\par\\vspace{5pt}\n"
    )


def reflow_tables(tex: str) -> str:
    r"""Ganti tiap longtable dengan tabular auto-fit; sisanya tak tersentuh."""
    out, i = [], 0
    pat = "\\begin{longtable}"
    while True:
        j = tex.find(pat, i)
        if j < 0:
            out.append(tex[i:]); break
        out.append(tex[i:j])
        end = tex.find("\\end{longtable}", j) + len("\\end{longtable}")
        out.append(convert_longtable(tex[j:end]))
        i = end
    return "".join(out)


def postprocess(tex: str) -> str:
    tex = fix_inline_code(tex)
    tex = wrap_pendalaman(tex)
    tex = reflow_tables(tex)
    return tex


# --------------------------------------------------------------------------
def convert_chapter(stem: str) -> None:
    src = draft_path(stem)
    if not src.exists():
        print(f"  {stem}: LEWAT — draf tidak ditemukan: {src}")
        return
    md = src.read_text(encoding="utf-8")
    pre, has_cite = preprocess(md, stem)
    body = run_pandoc(pre)
    body = postprocess(body)

    header = (
        "% ==========================================================================\n"
        f"% {stem}.tex — dihasilkan dari v2/drafts oleh tools/md2tex.py\n"
        f"% Sumber: {src.relative_to(OUT_ROOT.parents[1])}\n"
        "% Boleh disunting manual; menjalankan md2tex.py lagi akan menimpa.\n"
        "% ==========================================================================\n"
    )
    out = CH_DIR / f"{stem}.tex"
    out.write_text(header + body, encoding="utf-8")
    npend = body.count("\\begin{pendalaman}")
    nfig  = body.count("\\begin{figure}")
    nbaca = body.count("\\begin{bacaan}")
    print(f"  {stem}: {nfig} gambar, {npend} pendalaman, bacaan={'ya' if nbaca else 'tidak'}, "
          f"sitasi={'ya' if has_cite else 'tidak'}, {len(body.splitlines())} baris")


def main() -> None:
    CH_DIR.mkdir(exist_ok=True)
    stems = [a for a in sys.argv[1:] if not a.startswith("-")] or [f"ch{n:02d}" for n in range(1, 18)]
    print(f"Konversi {len(stems)} bab dari {DRAFT_DIR} -> {CH_DIR}")
    for s in stems:
        convert_chapter(s)
    print("Selesai.")


if __name__ == "__main__":
    main()
