# Schema Mapping: Old Warehouse → New Lakehouse

> **Status: PLACEHOLDER.** Replace the examples below with the real mapping.
> This file is the authoritative source of truth for the migration. The skill is
> instructed to trust this file over its own intuition, so keep it accurate and
> complete.

This document maps the old data warehouse schema to the new Lakehouse schema.
The SQL dialect is unchanged; only the schema differs.

## Table mappings

| Old table | New table | Notes |
|-----------|-----------|-------|
| `old_schema.example_old_table` | `new_schema.example_new_table` | Straight rename. |
| `old_schema.wide_table` | `new_schema.fact_a` + `new_schema.fact_b` | Split into two; join on `id`. |

## Column mappings

For each table where columns changed, list old → new. Include type changes and
moves between tables explicitly, because those are the changes most likely to
cause silent wrong answers.

### `example_old_table` → `example_new_table`

| Old column | New column | Type change? | Notes |
|------------|------------|--------------|-------|
| `cust_id` | `customer_id` | no | Rename only. |
| `created` | `created_at` | `string` → `timestamp` | Compare as timestamp, not string. |
| `legacy_flag` | *(dropped)* | — | No equivalent. Flag to analyst. |

## Dropped / replaced

List anything in the old schema with no clean equivalent in the new one, so the
skill knows to flag rather than guess.

- `old_schema.example_old_table.legacy_flag` — removed; superseded by the
  `status` enum in `new_schema.example_new_table`.

## Semantic differences

Cases where a new table looks equivalent but behaves differently — different
grain, different default row set, soft-deletes now included, etc. These are
prime candidates for the skill's "needs your judgement" flags.

- *(example)* `new_schema.fact_a` includes soft-deleted rows by default; the old
  table excluded them. Add `WHERE is_deleted = false` to match old behaviour.
