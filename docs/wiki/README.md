# The connection graph

This directory is the repo's knowledge graph: which concepts exist, which
concepts point at each other, and which of those pointers are promises
not yet kept. The teaching model of this repo is cumulative — a topic's
"when is it useful" column points forward, its Scope points back — and
this wiki is where those threads are recorded so they live in the repo
instead of in someone's head.

- [`INDEX.md`](INDEX.md) is the graph: one row per node, one row per
  edge, each edge marked **delivered** or **promised** with the place it
  is stated.
- Node pages (added as nodes accumulate detail) carry anything that does
  not fit an index row: design notes, device lineage, cross-references.

## How it is maintained

- The main agent updates `INDEX.md` in the same change that lands a
  series: new node, promised edges it opens, promised edges it closes.
- The `connection-auditor` agent (`.claude/agents/connection-auditor.md`)
  audits the graph against the actual content — promised-but-missing,
  delivered-but-unrecorded, possible-but-unmade — before a series PR
  opens and whenever the next topic is being chosen.
- Edges cite where they are stated. An edge nobody can point to is a
  wish, not a connection.

## External research

Broader research material — clippings, paper notes, explorations that
are not repo-specific — lives in the maintainer's Obsidian vault at
`~/Obsidian/project-research`. This wiki deliberately stays repo-shaped:
its nodes are things the repo teaches or has promised to teach. When a
wiki thread grows beyond the repo (background reading, discarded
approaches), it belongs in the vault, with at most a pointer from here.
