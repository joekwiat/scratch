# Query Examples: Old → New (with optimisations)

> **Status: PLACEHOLDER.** Replace the examples below with real before/after pairs.
> These pairs teach the skill what a *good* new-schema query looks like — not just
> renamed names, but the optimisations the new Lakehouse schema rewards. The more
> representative the examples, the better the skill generalises.

Each example shows an old-schema query and its correct new-schema rewrite, plus a
note on what changed and why. Aim for examples that demonstrate the *optimisation
patterns*, not just trivial renames.

---

## Example 1: [short description of what this demonstrates]

**Old schema:**
```sql
SELECT cust_id, COUNT(*)
FROM old_schema.example_old_table
WHERE created >= '2024-01-01'
GROUP BY cust_id;
```

**New schema:**
```sql
SELECT customer_id, COUNT(*)
FROM new_schema.example_new_table
WHERE created_at >= TIMESTAMP '2024-01-01'
GROUP BY customer_id;
```

**What changed and why:**
- `cust_id` → `customer_id`, `created` → `created_at` (renames).
- `created_at` is now a timestamp, so the literal is compared as a timestamp
  rather than a string.
- *(Add the key optimisation this example is meant to teach, e.g. partition
  pruning, predicate pushdown, avoiding a now-unnecessary join, etc.)*

---

## Example 2: [the optimisation pattern this one is for]

**Old schema:**
```sql
-- old query here
```

**New schema:**
```sql
-- optimised new query here
```

**What changed and why:**
- ...

---

## Notes on optimisation patterns

A running list of the general optimisations the new schema rewards, distilled
from the examples above. This helps the skill apply them even to queries that
don't exactly match an example.

- *(e.g.)* Filter on the partition column to enable pruning.
- *(e.g.)* Prefer the pre-joined `fact_a` over re-joining the dimension tables.
