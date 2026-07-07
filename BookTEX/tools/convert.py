#!/usr/bin/env python3
r"""Konversi bab Quarto (.qmd) -> fragmen LaTeX (.tex) untuk BookTEX.

Alur:
  1. Buang YAML front matter bila ada.
  2. Ekstrak setiap blok ```{mermaid} secara berurutan; ganti dengan blok
     raw-LaTeX \begin{figure}...\includegraphics...\caption. Ambil teks
     caption dari baris '%%| fig-cap:'.
  3. Salin PNG mermaid yang sudah dirender (figure-docx/mermaid-figure-K.png)
     ke figures/chNN-fig-K.png sesuai urutan kemunculan.
  4. Sisanya (prosa, matematika, kode) dialirkan lewat pandoc ->
     --top-level-division=chapter --listings, sehingga:
        #   -> \chapter    ##  -> \section    ### -> \subsection (tak bernomor)

Pemakaian:
  python tools/convert.py            # semua bab
  python tools/convert.py ch03 ch07  # bab tertentu
"""
from __future__ import annotations
import hashlib, json, os, re, shutil, subprocess, sys, tempfile
from pathlib import Path

# Penanda pemisah kepala (metadata) dan isi otomatis dalam .tex.
BODY_MARK = "% >>>>> ISI OTOMATIS (jangan hapus baris ini) >>>>>"

ROOT      = Path(__file__).resolve().parents[2]          # .../NulisBuku
QMD_DIR   = ROOT / "website" / "chapters"
OUT_ROOT  = Path(__file__).resolve().parents[1]          # .../BookTEX
CH_DIR    = OUT_ROOT / "chapters"
FIG_DIR   = OUT_ROOT / "figures"
FIGSRC_DIR = FIG_DIR / "_src"          # sumber mermaid per bab (untuk reverse-sync)

FENCE_OPEN  = re.compile(r'^(`{3,})\{mermaid\}?\s*$')
FIGCAP      = re.compile(r'^\s*%%\|\s*fig-cap:\s*(.*?)\s*$')
YAML_DELIM  = re.compile(r'^---\s*$')


def sha1(s: str) -> str:
    return hashlib.sha1(s.encode("utf-8")).hexdigest()[:12]


def read_existing(tex_path: Path) -> tuple[str | None, str | None, str | None]:
    """Kembalikan (qmd_hash, tex_hash, body) dari .tex lama, atau (None,None,None)."""
    if not tex_path.exists():
        return None, None, None
    txt = tex_path.read_text(encoding="utf-8")
    qh = re.search(r"% qmd-sha1: (\w+)", txt)
    th = re.search(r"% tex-sha1: (\w+)", txt)
    body = txt.split(BODY_MARK + "\n", 1)[1] if BODY_MARK + "\n" in txt else None
    return (qh.group(1) if qh else None,
            th.group(1) if th else None,
            body)


def strip_frontmatter(lines: list[str]) -> list[str]:
    if lines and YAML_DELIM.match(lines[0]):
        for i in range(1, len(lines)):
            if YAML_DELIM.match(lines[i]):
                return lines[i + 1:]
    return lines


def clean_caption(raw: str) -> str:
    raw = raw.strip().strip('"').strip("'")
    # lolos-kan karakter khusus LaTeX yang umum muncul di caption
    for a, b in [('&', r'\&'), ('%', r'\%'), ('#', r'\#'), ('_', r'\_')]:
        raw = raw.replace(a, b)
    return raw


def extract_mermaid(lines: list[str], stem: str) -> tuple[list[str], list[dict]]:
    """Ganti blok mermaid dengan blok raw-LaTeX. Kembalikan (baris_baru, daftar_gambar).

    Tiap gambar: {"k", "img", "caption", "src"} — 'src' = isi mentah blok mermaid
    (termasuk baris %%|) supaya reverse-sync bisa memulihkan diagram hidup di web.
    """
    out: list[str] = []
    figures: list[dict] = []
    i, n = 0, len(lines)
    while i < n:
        m = FENCE_OPEN.match(lines[i])
        if not m:
            out.append(lines[i]); i += 1; continue
        fence = m.group(1)
        caption = ""
        src: list[str] = []
        i += 1
        while i < n and lines[i].rstrip() != fence:
            cm = FIGCAP.match(lines[i])
            if cm and not caption:
                caption = clean_caption(cm.group(1))
            src.append(lines[i])
            i += 1
        i += 1  # lewati fence penutup
        k = len(figures) + 1
        img = f"{stem}-fig-{k}"
        figures.append({"k": k, "img": img, "caption": caption, "src": src})
        cap = f"\\caption{{{caption}}}" if caption else ""
        out += [
            "",
            "```{=latex}",
            "\\begin{figure}[htbp]\\centering",
            f"\\includegraphics[width=\\linewidth,height=0.72\\textheight,keepaspectratio]{{{img}}}",
            cap,
            f"\\label{{fig:{img}}}",
            "\\end{figure}",
            "```",
            "",
        ]
    return out, figures


def copy_pngs(stem: str, n_fig: int) -> list[int]:
    """Salin mermaid-figure-K.png -> figures/chNN-fig-K.png. Kembalikan indeks yang hilang."""
    src_dir = QMD_DIR / f"{stem}_files" / "figure-docx"
    missing = []
    for k in range(1, n_fig + 1):
        src = src_dir / f"mermaid-figure-{k}.png"
        if src.exists():
            shutil.copyfile(src, FIG_DIR / f"{stem}-fig-{k}.png")
        else:
            missing.append(k)
    return missing


# Karakter yang di-escape pandoc tapi harus mentah di dalam \lstinline (verbatim).
_LST_UNESCAPE = [
    (r"\textbackslash{}", "\\"), (r"\textasciitilde{}", "~"),
    (r"\textasciicircum{}", "^"),
    (r"\_", "_"), (r"\%", "%"), (r"\#", "#"), (r"\&", "&"),
    (r"\$", "$"), (r"\{", "{"), (r"\}", "}"),
]
_LSTINLINE = re.compile(r"\\lstinline(?P<d>.)(?P<c>.*?)(?P=d)")


def fix_inline_code(tex: str) -> str:
    r"""Batalkan escape LaTeX di dalam \lstinline!...! (isinya verbatim)."""
    def repl(m: re.Match) -> str:
        c = m.group("c")
        for a, b in _LST_UNESCAPE:
            c = c.replace(a, b)
        return f"\\lstinline{m.group('d')}{c}{m.group('d')}"
    return _LSTINLINE.sub(repl, tex)


def run_pandoc(md: str) -> str:
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as f:
        f.write(md); tmp = f.name
    try:
        res = subprocess.run(
            ["quarto", "pandoc", tmp,
             "-f", "markdown+lists_without_preceding_blankline", "-t", "latex",
             "--listings", "--top-level-division=chapter", "--wrap=preserve"],
            capture_output=True, text=True, encoding="utf-8",
        )
        if res.returncode != 0:
            raise RuntimeError(res.stderr)
        return fix_inline_code(res.stdout)
    finally:
        os.unlink(tmp)


def convert_chapter(stem: str, force: bool = False) -> None:
    qmd = QMD_DIR / f"{stem}.qmd"
    tex_path = CH_DIR / f"{stem}.tex"
    qmd_text = qmd.read_text(encoding="utf-8")
    cur_qmd_hash = sha1(qmd_text)
    old_qmd_hash, old_tex_hash, old_body = read_existing(tex_path)

    # Keputusan tulis-ulang (dilewati bila --force tidak diberikan):
    if not force and old_qmd_hash is not None:
        if old_qmd_hash == cur_qmd_hash:
            print(f"  {stem}: dilewati — .qmd tak berubah sejak generasi terakhir.")
            return
        # .qmd berubah; kalau .tex sudah disunting manual, jangan timpa diam-diam.
        if old_body is not None and sha1(old_body) != old_tex_hash:
            print(f"  {stem}: DILEWATI — .qmd berubah TAPI .tex sudah disunting manual. "
                  f"Pakai --force untuk menimpa (suntingan akan hilang).")
            return

    lines = strip_frontmatter(qmd_text.splitlines())
    new_lines, figures = extract_mermaid(lines, stem)
    missing = copy_pngs(stem, len(figures))
    body = run_pandoc("\n".join(new_lines) + "\n")

    # Sidecar: simpan sumber mermaid agar reverse-sync bisa memulihkan diagram hidup.
    FIGSRC_DIR.mkdir(exist_ok=True)
    sidecar = {f["img"]: {"caption": f["caption"], "src": f["src"]} for f in figures}
    (FIGSRC_DIR / f"{stem}.json").write_text(
        json.dumps(sidecar, ensure_ascii=False, indent=1), encoding="utf-8")

    header = (
        "% ==========================================================================\n"
        f"% {stem}.tex — dihasilkan otomatis dari website/chapters/{stem}.qmd\n"
        "% Boleh disunting manual. 'sync' hanya menimpa bila .qmd berubah DAN .tex\n"
        "% belum disunting; kalau keduanya berubah, dilewati (pakai --force).\n"
        f"% qmd-sha1: {cur_qmd_hash}\n"
        f"% tex-sha1: {sha1(body)}\n"
        "% ==========================================================================\n"
        f"{BODY_MARK}\n"
    )
    tex_path.write_text(header + body, encoding="utf-8")

    note = f" | PNG hilang: {missing}" if missing else ""
    print(f"  {stem}: {len(figures)} gambar, {len(body.splitlines())} baris tex{note}")


def status_chapter(stem: str) -> str:
    """Ringkas keadaan satu bab: apakah .qmd/.tex berubah sejak generasi terakhir."""
    qmd = QMD_DIR / f"{stem}.qmd"
    tex_path = CH_DIR / f"{stem}.tex"
    if not qmd.exists():
        return f"  {stem:5} —  .qmd tidak ada"
    cur_qmd_hash = sha1(qmd.read_text(encoding="utf-8"))
    old_qmd_hash, old_tex_hash, old_body = read_existing(tex_path)
    if old_qmd_hash is None:
        return f"  {stem:5} [BARU]     .tex belum dibuat -> sync akan membuatnya"
    qmd_changed = old_qmd_hash != cur_qmd_hash
    tex_edited  = old_body is not None and sha1(old_body) != old_tex_hash
    if not qmd_changed and not tex_edited:
        return f"  {stem:5} [sinkron]  qmd & tex sama seperti generasi terakhir"
    if qmd_changed and not tex_edited:
        return f"  {stem:5} [QMD]      .qmd berubah -> sync akan regen .tex (aman)"
    if not qmd_changed and tex_edited:
        return f"  {stem:5} [TEX]      .tex disunting manual -> sync membiarkannya (aman)"
    return f"  {stem:5} [BENTROK]  .qmd & .tex sama-sama berubah -> putuskan manual (--force menimpa .tex)"


def print_status(stems: list[str]) -> None:
    print("Status sinkronisasi qmd <-> tex:\n")
    for s in stems:
        print(status_chapter(s))
    print("\nKeterangan: [QMD]=edit di website, [TEX]=edit di LaTeX, "
          "[BENTROK]=dua-duanya diedit (perlu keputusan).")


def main() -> None:
    FIG_DIR.mkdir(exist_ok=True); CH_DIR.mkdir(exist_ok=True)
    args = sys.argv[1:]
    force = "--force" in args
    stems = [a for a in args if not a.startswith("-")] or [f"ch{n:02d}" for n in range(1, 18)]
    if "--status" in args:
        print_status(stems)
        return
    print(f"Konversi {len(stems)} bab -> {CH_DIR}" + (" (--force)" if force else ""))
    for s in stems:
        convert_chapter(s, force=force)
    print("Selesai.")


if __name__ == "__main__":
    main()
