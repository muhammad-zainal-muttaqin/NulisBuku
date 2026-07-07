# General First-Pass Revision Instructions for All Chapters

Revise each chapter as a coherent reference-book chapter rather than a collection of independently generated subchapters. At this stage, prioritize chapter structure, conceptual coverage, consistency, readability, and narrative flow. Detailed technical claims will receive separate technical review and subsequent revision.

---

## 1. Strengthen the chapter opening

Each chapter must open with a standalone introductory section — several paragraphs placed before the first numbered subsection. This section is not a subsection itself and carries no subsection number or heading.

The introduction should present a clear and realistic motivating problem. It should explain:

- why the chapter topic matters;
- what limitation exists in the raw data, basic representation, or conventional approach;
- what practical or analytical decisions the chapter will help the reader make;
- what can go wrong when those decisions are handled poorly.

Do not begin only with a definition, historical overview, list of techniques, or description of the chapter contents.

Where appropriate, return to the opening problem later in the chapter so that the chapter has a clear conceptual arc.

---

## 2. Organize the chapter around reader questions

Each chapter should be written with a small number of clear objectives in mind — but these should not appear as a formal section. Before revising, identify the principal questions the chapter should answer:

- What is this technique or representation?
- Why and when is it useful?
- What alternatives are available?
- How should the reader choose among them?
- What assumptions and risks are involved?
- How should its contribution be evaluated?

These questions should guide the chapter structure, not be presented to the reader.

---

## 3. Ensure a deliberate conceptual progression

Organize the chapter so that it progresses logically through:

1. the motivating problem and core idea;
2. the principal techniques or representation choices;
3. important design decisions and trade-offs;
4. limitations, risks, and failure modes;
5. evaluation or validation considerations;
6. an integrated example, case, or synthesis.

The exact structure may differ by chapter, but the sequence should feel intentional. Check that every subchapter has a distinct function. Remove or merge subchapters that repeat the same explanation under different headings.

---

## 4. Use one recurring example or integrated case where appropriate

Where feasible, use one recurring dataset, scenario, or application to connect several parts of the chapter. Small examples from multiple domains may still be used to clarify individual concepts, but they should not make the chapter feel fragmented.

The integrated case should emphasize reasoning, representation choices, comparison, and evaluation — not detailed implementation.

---

## 5. Improve transitions between subchapters

Explicitly revise the transitions between subchapters. Each transition should explain why the next topic follows from the previous one. Avoid abrupt shifts that make the chapter read as a sequence of independent articles.

Remove repeated introductory statements such as:

- "Dalam rekayasa fitur..."
- "Pada data dunia nyata..."
- "Salah satu tantangan utama..."
- "Bagian ini akan membahas..."

Use chapter-level continuity rather than restarting the explanation in every subchapter.

---

## 6. Include a decision-oriented comparison

Each chapter must contain at least one table or figure that helps readers choose among techniques. Depending on the chapter, compare aspects such as:

- suitable data or problem types;
- assumptions;
- strengths and limitations;
- interaction with model families;
- validation or leakage risks.

The comparison should support practical decision-making rather than merely restate definitions.

---

## 7. Add a concise chapter synthesis

End each chapter with a short synthesis of its central principles and decisions. It should not simply repeat subsection headings or redefine terms. A useful synthesis states:

- when a technique is appropriate;
- what assumptions it introduces;
- what trade-offs matter most;
- what should be validated;
- which alternatives should be considered.

Keep this section compact.

---

## 8. Do not add formal learning activities at this stage

Do not add:

- explicit learning objectives;
- review questions or exercises;
- notebook walkthroughs;
- mini-project instructions;
- repository references that depend on unfinished materials.

Existing references to notebooks or projects should be removed, generalized, or marked for later integration.

---

## 9. Control length and repetition

During revision, remove:

- duplicated definitions;
- repeated motivations or risk warnings;
- examples that do not add a new insight;
- long lists of techniques without interpretation;
- excessive mathematical detail not needed for understanding;
- verbose transitions and generic concluding paragraphs.

Where possible, replace repeated prose with a compact table or figure.

---

## 10. Distinguish essential coverage from optional enrichment

Include a component only when it is important to the chapter's subject. Modern models or recent methods should not be added merely to make the chapter appear current — include them only when they change the reader's understanding or decision process.

---

## 11. Maintain reference-book orientation

Write for readers who may consult the chapter selectively. To support this:

- use informative subsection headings;
- define chapter-specific terminology clearly;
- provide concise cross-references to earlier or later chapters where needed;
- explain enough context for the chapter to stand on its own.

A brief opening sentence may indicate relevant prerequisite concepts or related chapters, but do not create a formal prerequisite block.

---

## 12. Separate chapter integration from technical review

This first-pass revision should focus on:

- chapter-level coherence and completeness;
- placement of concepts and removal of duplication;
- consistency of terminology;
- quality of examples and transitions;
- decision support and chapter synthesis.

Do not attempt to resolve uncertain technical details. Where a statement requires verification or specialist judgment, leave it as-is — technical claims will be reviewed separately in a subsequent pass with human oversight.
