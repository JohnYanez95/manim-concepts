# The connection graph

This directory is the repo's knowledge graph: which concepts exist, which
concepts point at each other, and which of those pointers are promises
not yet kept. The teaching model of this repo is cumulative — a topic's
"when is it useful" column points forward, its Scope points back — and
this wiki is where those threads are recorded so they live in the repo
instead of in someone's head.

- [`INDEX.md`](INDEX.md) is the graph: one row per node, one row per
  edge, each edge marked **delivered** or **promised** with the place it
  is stated. Its `Last audited:` stamp is the commit the graph was last
  reconciled against — the auditor diffs from it.
- [`log.md`](log.md) is the **append-only** record of graph operations —
  series landing, audits applied, schema changes. Every graph operation
  appends an entry at the bottom; existing entries are never edited or
  reordered, and corrections get their own new entry.
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

## Scope boundary

This wiki deliberately stays repo-shaped: its nodes are things the repo
teaches or has promised to teach. Background reading, clippings, and
explorations that are not repo-specific do not belong here — when a wiki
thread grows beyond the repo, it leaves the repo. The wiki is also
**screen-shaped**: the study-guide track *reads* the graph (glue
transitions are authored from edge citations) but never writes it —
print deliveries are recorded in their plans, not here (plan 012).
