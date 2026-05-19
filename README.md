# Senior Analytics Engineer, Product — technical case study (90 min)

You'll receive a stub dbt project (`pairing_funnel/`) running on DuckDB in a pre-configured Codespace. The project compiles and runs but contains real-world hygiene issues.

## Context

A product squad is building an embedded dashboard for sponsors. For a given sponsor, they want to show — per trial and per country — how many patients moved through the funnel: **processed → reviewed → enrolled**.

## What to do

### 1. Audit (0–25 min)

Read the repo. Flag what's wrong. Sketch how you'd model this cleanly (Excalidraw / paper).

### 2. Fix + build (25–70 min)

Fix the 2–3 issues that matter most. Then build a new model `exposure_sponsor_funnel` for **one sponsor (Sanofi)** with the columns the dashboard needs. Place it in an `activation` layer (i.e. `models/activation/`). Declare it as a [dbt exposure](https://docs.getdbt.com/docs/build/exposures). Add the tests that matter.

### 3. Validate

Your work is done when:
- `dbt build` passes with no errors
- You can query your exposure and answer: **"For Sanofi, which country has the highest enrollment rate?"**

```bash
# Query the exposure directly
cd pairing_funnel
duckdb pairing_funnel.duckdb -c "SELECT * FROM exposure_sponsor_funnel ORDER BY patients_enrolled DESC LIMIT 10;"
```

### 4. Handoff (70–90 min)

Write your handoff in the Notion page we've shared with you. Summarize what you shipped, your assumptions, what you didn't fix and why, what you'd do next. Write it as if a PM and another engineer will read it tomorrow.

## Rules

- **AI tools and internet are encouraged.** Use whatever you'd use on the job — GitHub Copilot is available in the Codespace, and you can use any browser-based AI tool (Claude, ChatGPT, etc.) in a separate tab. We want to see how you collaborate with AI, not whether you can type SQL from memory.
- Working code wins over comprehensive code. Trade-offs are fair; explain them in the Notion handoff.
- Talk through your thinking as you go.

## How to run

If you're in Codespace, everything is pre-baked. Otherwise:

```bash
# Generate synthetic data
python scripts/generate_data.py

# Copy seeds into dbt project
cp data/raw/*.csv pairing_funnel/seeds/

# Install dbt packages
cd pairing_funnel
dbt deps

# Run everything
dbt build
```

## Time-box yourself

This is designed for 90 minutes. Don't go over. Incomplete work with clear trade-offs is better than complete work that took 3 hours.
