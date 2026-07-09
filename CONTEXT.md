# Learn Matt Pocock Skills

A bilingual (English/Chinese) reading site that turns Matt Pocock's agent skills into side-by-side HTML reference pages, organized as a skill map tracing the "idea → ship" workflow.

## Language

**Skill map**:
The single landing page (`index.html`) that renders every translated skill as a node on a stylized highway diagram. It is the site's only entry point — a reader reaches any skill page by following a link from here.
_Avoid_: homepage, index, landing page (too generic — "skill map" names the diagram metaphor the page actually embodies)

**Mainline**:
The vertical sequence of skill nodes on the skill map that traces the promoted engineering workflow from idea to shipped code (`ask-matt` → `grill-with-docs` → `prototype`/`handoff` → `to-spec` → `to-tickets` → `implement`/`tdd` → `code-review`). Mainline nodes sit on the highway's center road.
_Avoid_: flow, pipeline, workflow (those describe the process; "mainline" names the visual spine on the map)

**Foundation layer**:
The row of dashed nodes beneath the mainline on the skill map holding vocabulary skills (`domain-modeling`, `codebase-design`) that underpin the mainline rather than sit on it. A foundation skill is consulted by mainline skills, not stepped through in sequence.
_Avoid_: base layer, vocabulary row, supporting skills

**Skill page**:
A bilingual HTML page generated from one skill's `SKILL.md` by the `bilingual-html` skill, living at `./<skill-name>/SKILL.html`. It shows a frontmatter table at the top, then paragraph-aligned English-left / Chinese-right columns. Every skill page links back to the skill map.
_Avoid_: doc page, article, translation page

**Attached document**:
A bilingual HTML page generated from a non-`SKILL.md` markdown file within a skill's source directory (e.g. `LOGIC.md`, `tests.md`, `AGENT-BRIEF.md`). An attached document never appears as a node on the skill map; it is reached only via the navigation link inside its parent skill page.
_Avoid_: sub-page, secondary page, companion doc

**Bilingual pair**:
The atomic layout unit of a skill page: one Markdown paragraph rendered as a `.pair` containing `.col-en` (the verbatim English source) and `.col-zh` (the Chinese translation), aligned at the paragraph level. Pairs stack vertically; they never mix paragraphs.
_Avoid_: row, translation block, parallel text block

**Translation glossary**:
The file at `docs/glossary.md` that fixes the Chinese rendering of cross-skill terms so that nine parallel translation workers stay consistent. It is a translation anchor table, distinct from this file — it records "how to render a source term," not "what a domain concept IS."
_Avoid_: terminology table, term list, dictionary

## Relationships

- The **skill map** links to every **skill page**, and only to skill pages — never directly to an **attached document**.
- A **skill page** links back to the **skill map** and, when the skill has them, forward to its **attached documents**.
- An **attached document** links back to its parent **skill page** and onward to the **skill map** — the three-layer navigation is `skill map → skill page → attached document`.
- **Mainline** and **foundation layer** skills are both shown as nodes on the **skill map**; the difference is topological (on the highway vs. beneath it), not navigational.
- Every **skill page** and **attached document** is composed of **bilingual pairs**.
- The **translation glossary** constrains the `.col-zh` content of every **bilingual pair** across all pages.
