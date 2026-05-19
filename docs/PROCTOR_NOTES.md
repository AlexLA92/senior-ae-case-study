# Proctor Notes — Senior AE Case Study

**For:** Alexandre + Barth  
**Prep:** Brief Barth 1 day ahead on planted violations + rubric.

## Protocol

- Alexandre drives intro + business context (5 min). Barth observes silently in Phase 1.
- Both can ask clarifying questions in Phase 2.
- Phase 3 (handoff write-up): leave the candidate alone for 20 min to write their handoff in the shared Notion page, return for a 5-min walk-through.
- **Before the session:** create a blank Notion page for the candidate's handoff and share it with them (guest editor access).
- Score independently on all 4 dimensions during the session. Compare after.
- AI tooling: Copilot + Continue extensions are pre-installed in the Codespace. Candidate can also use browser-based AI (Claude, ChatGPT, etc.). The brief explicitly encourages this — we're evaluating *how* they use AI, not *whether*.

---

## 6 Planted Violations

### 1. Duplicate row in raw data
- **Where:** `data/raw/raw_patient_trial_matches.csv` — one row duplicated (same `patient_id` + `trial_id`, different `match_id`)
- **Senior should:** Catch it during audit, add deduplication in `stg_patient_trial_matches` (e.g. `ROW_NUMBER() OVER (PARTITION BY patient_id, trial_id ORDER BY processed_at DESC)`)

### 2. No primary key on fact table
- **Where:** `pairing_funnel/models/marts/fct_patient_trial_matches.sql` + `models/marts/schema.yml`
- **What:** No `unique` or `not_null` test on `match_id` (or a surrogate key). No PK enforced.
- **Senior should:** Add `dbt_utils.generate_surrogate_key` or declare `match_id` as PK with `unique` + `not_null` tests

### 3. Test data left in source
- **Where:** `data/raw/raw_sponsors.csv` has `sponsor_name = 'TEST'` (sp_099). `raw_trials.csv` has a TEST trial. `raw_patient_trial_matches.csv` has `patient_id LIKE 'test_%'` rows.
- **Senior should:** Filter out test data in staging models (`WHERE sponsor_name != 'TEST'`, `WHERE patient_id NOT LIKE 'test_%'`), comment explaining why

### 4. Ambiguous country convention
- **Where:** `pairing_funnel/models/marts/dim_sites.sql` — both `country_code` and `country_name` exposed
- **What:** No documented convention on which is canonical for joins/reporting
- **Senior should:** Pick one for the exposure mart, document the choice, flag the ambiguity. Ideal: use `country_code` for joins, carry `country_name` for display.

### 5. Layering break — mart refs raw directly
- **Where:** `pairing_funnel/models/marts/fct_patient_trial_matches.sql` — line `select * from {{ ref('raw_patient_trial_matches') }}`
- **What:** The fact table skips the staging layer entirely, referencing the seed directly
- **Senior should:** Change to `{{ ref('stg_patient_trial_matches') }}` to respect the staging → marts layering

### 6. Missing tests in schema.yml
- **Where:** Individual `*.yml` files across `models/staging/` and `models/marts/`
- **What:** Columns are documented but no `unique`, `not_null`, or `relationships` tests on any PKs or FKs
- **Senior should:** Add `unique` + `not_null` on PKs, `relationships` tests between fact FKs and dim PKs

---

## Rubric — Score 1–4 per dimension (independently)

| Dimension | What it measures | 4 (Strong Yes) | 1 (Strong No) |
|---|---|---|---|
| **Modelling craft** | Clean staging→int→marts, tests in the right places, PKs, dedupe done right | Layered cleanly, tests cover relationships, PK chosen explicitly | Logic crammed into one model, no tests, raw refs hardcoded |
| **System thinking** | Catches planted issues in audit; sketches a coherent target before coding | Identifies ≥4/6 violations in audit, sketch maps cleanly to what they build | Misses most violations, jumps to code without sketching |
| **AI / tool fluency** | Decomposes problem before prompting; reads AI output critically; catches hallucinated columns | Uses AI as a thinking partner, sanity-checks every paste | Pastes AI output without reading, defends wrong output, or doesn't use AI at all |
| **Communication** | Verbalizes thinking, ticket is something we'd be happy to inherit | Ticket has the right context for a PM, lists assumptions + next steps, calls out unresolved issues | Ticket is one paragraph, no assumptions, no callouts |

**Overall verdict:** 4 Strong Yes / 3 Yes / 2 No / 1 Strong No

---

## What to Watch For

### Validation step

The brief asks the candidate to run `dbt build` cleanly and then query their exposure to answer: **"For Sanofi, which country has the highest enrollment rate?"**

```bash
duckdb pairing_funnel.duckdb -c "SELECT * FROM exposure_sponsor_funnel ORDER BY patients_enrolled DESC LIMIT 10;"
```

This confirms the model actually works end-to-end and the candidate can reason about the output (not just write SQL that compiles).

### Expected new model: `exposure_sponsor_funnel`

The candidate is asked to build `exposure_sponsor_funnel` in `models/activation/`. A good solution:
- Lives in `models/activation/exposure_sponsor_funnel.sql` (not in `marts/`)
- Refs `fct_patient_trial_matches` + `dim_trials` + `dim_sites` (not raw)
- Filters to Sanofi via a join to `dim_sponsors` or `dim_trials.sponsor_id`
- Aggregates by trial × country: `patients_processed`, `patients_reviewed`, `patients_enrolled`
- Has a companion `exposure_sponsor_funnel.yml` with an exposure declaration
- Has a companion yml with basic tests

### Green flags 🟢
- Draws the DAG before touching code
- Questions whether `country_code` or `country_name` is the right grain
- Adds tests that would actually catch regressions
- Explains trade-offs in the handoff (what they skipped and why)
- Uses AI to scaffold, but reads and edits the output
- Creates the model in `activation/` as instructed, not in `marts/`

### Red flags 🔴
- Doesn't notice the fact table refs raw directly
- No deduplication logic anywhere
- Builds the model without any tests
- Can't explain what their AI tool generated
- Notion handoff is just "I built the model" with no context

### Neutral / depends on explanation 🟡
- Skips some violations to focus on the new model (fine if explained)
- Doesn't use an intermediate layer (acceptable for this scope)
- Hardcodes sponsor name instead of parameterizing (expected for v1)
