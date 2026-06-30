---
name: lakehouse-migration
description: Migrate analysts' SQL queries from the old data warehouse schema to the new Lakehouse schema. The SQL dialect is unchanged — only table names, column names, and the structural shape of the data differ, and the new schema rewards specific optimisations the old one did not. Use this skill whenever someone hands over a SQL query written against the old/legacy/warehouse/Redshift schema and wants it converted, ported, migrated, updated, or "made to work on the new tables" — even if they just paste a query and ask "can you fix this for the Lakehouse?" or "what's the new-schema version of this?". Also use it when someone asks why their old query is failing or returning nothing against the new tables, since the cause is almost always a schema change this skill knows about.
---

# SQL Lakehouse Migration

Analysts at Aurora are moving queries off the old data warehouse schema and onto the new Lakehouse schema. This skill translates a query from the old schema to the new one and flags anything the analyst needs to decide for themselves.

The SQL **dialect does not change** — same engine, same functions, same syntax. What changes is the *schema*: tables are renamed or split, columns are renamed, retyped, moved between tables, or dropped, and the new schema layout makes certain query patterns much cheaper (or much more expensive) than they were before. Translating the names is the easy 80%. The value of this skill is in the remaining 20%: getting the structural changes right and being honest about what you can't safely decide on the analyst's behalf.

## Before you start: load the reference material

Two reference files hold everything specific to this migration. **Read both before converting anything** — do not translate from memory or guesswork.

- `references/schema-mapping.md` — the authoritative old→new mapping: table renames and splits, column renames and type changes, columns that moved tables, and columns that were dropped or replaced. This is the source of truth. If it conflicts with your intuition, the file wins.
- `references/query-examples.md` — worked before/after pairs showing real old-schema queries next to their correct new-schema rewrites, with the optimisations applied. Treat these as patterns to generalise from, not just one-offs to copy. They are how you learn what "good" looks like on the new schema.

If a query touches something not covered by either file, that is exactly the kind of thing to flag (see below) rather than guess.

## The workflow

For each query an analyst gives you:

1. **Understand the original.** Read the old query and work out what it actually returns — the tables, joins, filters, and the grain of the result. You can't safely translate a query you don't understand.
2. **Map every reference.** Go through each table and column against `schema-mapping.md`. Rename what's renamed, repoint what moved, and note anything that has no clean equivalent.
3. **Apply the optimisations.** Using `query-examples.md` as your guide, rewrite the query in the shape the new schema rewards — not just a find-and-replace of names onto the old structure. The examples show what this means in practice.
4. **Produce the converted query.** Output valid SQL that an analyst can run. Keep it readable: preserve the original's aliases and formatting style where you reasonably can, so the analyst recognises their own query.
5. **Flag what needs human judgement.** Anywhere you had to make a non-obvious choice, lost information, or couldn't be certain, surface it explicitly (see next section). This is not optional and it is not padding — it is the difference between a query the analyst can trust and one that silently returns the wrong numbers.

## Output format

Always structure the response as:

### Converted query
The rewritten SQL in a single code block, ready to run.

### What changed
A short, plain list of the substantive changes — renamed tables/columns, joins that were restructured, optimisations applied. Keep it to what matters; don't narrate every trivial rename if there are many, summarise them ("all `dim_*` tables renamed per the new convention"). The point is to let the analyst see at a glance what happened to their query.

### ⚠️ Needs your judgement
Only include this section when there is something to flag — but be diligent about including it when there is. Each flag should say what the issue is and what the analyst should check or decide. Examples of things that belong here:

- **Ambiguous mappings** — an old column maps to more than one candidate in the new schema, and the right choice depends on intent you can't see.
- **Dropped or replaced data** — an old column/table has no equivalent, so part of the query's logic can't be carried over as-is.
- **Type changes that affect behaviour** — e.g. a column that was a string is now a date, changing how comparisons or formatting behave.
- **Semantic shifts** — the new table looks equivalent but has a different grain, default filter, or set of rows (e.g. soft-deleted records now included), so the same query may return different results.
- **Optimisations with a trade-off** — a rewrite is faster but changes ordering, null handling, or edge-case behaviour in a way the analyst should sign off on.
- **Anything not covered by the reference files** — if the query uses a table or column you can't find in the mapping, say so plainly rather than inventing a translation.

When in doubt, flag it. A false alarm costs the analyst ten seconds; a silent wrong answer can cost them a lot more.

## Principles

- **Correctness over cleverness.** A correct query that's slightly slower beats a fast one that's subtly wrong. Apply optimisations confidently when the examples support them, but never at the cost of changing results without flagging it.
- **The reference files are authoritative.** When your instinct disagrees with `schema-mapping.md`, the file is right and you are wrong. If the file seems wrong, flag that to the analyst — don't quietly override it.
- **Don't invent mappings.** If something isn't in the references, the honest move is to flag it, not to guess at a plausible-looking new-schema name.
- **Preserve the analyst's intent and style.** You're porting *their* query. Keep it recognisable so they can read, trust, and maintain it.
