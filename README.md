# Senior Analytics Engineer, Product — technical case study (90 min)

## Context

A product squad is building an embedded dashboard for sponsors. For a given sponsor, they want to show — per trial and per country — how many patients moved through the funnel: **processed → reviewed → enrolled**.

You'll work on a stub dbt project (`dbt/`) running on DuckDB in a pre-configured Codespace. The project compiles and runs but contains real-world hygiene issues.

## Getting started (~10 min)

**1. Fork the repo** — Click the **Fork** button at the top-right of this page. This creates your own copy.

**2. Open a Codespace** — On your fork, click **Code → Codespaces → Create codespace on main**. Wait ~2 min for the setup to complete.

**3. Verify it works** — In the Codespace terminal:

```bash
cd dbt

# Install dependencies (should already be done by setup, but just in case)
dbt deps

# ✅ dbt build should pass (12 models + seeds, 0 errors)
dbt build

# ✅ you can query the data
duckdb dbt_case_study.duckdb -c "SELECT COUNT(*) FROM dim_sponsors;"
# Expected: 19
```

If either fails, run the setup manually:

```bash
cd /workspaces/dbt-duckdb-starter
python scripts/generate_data.py
cp data/raw/*.csv dbt/seeds/
cp dbt/profiles.yml ~/.dbt/profiles.yml
cd dbt
dbt deps
dbt build
```

**4. Read the rest of this README** before starting.

## What to do

### 1. Audit — no AI (~20 min)

Read the repo. Flag everything that's wrong — naming, architecture, data quality, testing. Walk us through what you find.

At ~20 min we'll ask: **"If you had to start fixing this right now, what would you prioritize first and why?"**

**No AI tools for this phase** — we want to see your instincts.

### 2. Fix, build & document — AI encouraged (~45 min)

Now use whatever AI tools you want. Your goal:

1. **Fix** the issues that matter most
2. **Build** a new model `exposure_sponsor_funnel` for **one sponsor (Sanofi)** with the columns the dashboard needs. Place it in an `activation` layer (i.e. `models/activation/`). Declare it as a [dbt exposure](https://docs.getdbt.com/docs/build/exposures). Add the tests that matter.
3. **Document** as you go — write an executive summary in the Notion page we've shared with you: what you shipped, key assumptions, and recommended next steps.

**You're done when `dbt build` passes and you can query your exposure to answer: "For Sanofi, which country has the highest enrollment rate?"**

### 3. Walk-through (~15 min)

We'll rejoin and you'll walk us through your work: what you found, what you fixed, what you built, and what you'd do next.

## Deliverable

Push your work to a branch on your fork and share the branch URL in your Notion handoff.

```bash
git checkout -b fix/case-study
git add -A
git commit -m "Case study: fixes + exposure_sponsor_funnel"
git push -u origin fix/case-study
```

## Rules

- **Phase 1 (audit): no AI tools.** Just you and the code.
- **Phase 2 (fix, build, document): AI encouraged.** Use whatever you'd use on the job — GitHub Copilot is available in the Codespace, and you can use any browser-based AI tool (Claude, ChatGPT, etc.) in a separate tab. To open Copilot Chat in the Codespace: press `Ctrl+Shift+I` (or `Cmd+Shift+I` on Mac), or click the chat icon in the left sidebar. Copilot Free gives you 50 completions/month — more than enough for this session. You can check your usage at https://github.com/settings/copilot/features.
- **Share your screen at all times** so we can follow along.
- Ask us questions if you feel blocked — we're here to help, not to watch you struggle.
- Working code wins over comprehensive code. Trade-offs are fair; explain them in your Notion document.

## Time-box yourself

This is designed for 90 minutes. Don't go over. Incomplete work with clear trade-offs is better than complete work that took 3 hours.
