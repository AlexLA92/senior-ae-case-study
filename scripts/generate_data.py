"""
Synthetic data generator for the Senior AE case study.
Produces 4 CSVs in data/raw/ with planted violations for the candidate to discover.
"""

import csv
import os
import random
from datetime import datetime, timedelta

import numpy as np
from faker import Faker

fake = Faker()
Faker.seed(42)
np.random.seed(42)
random.seed(42)

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ---------- constants ----------

REAL_SPONSORS = [
    "Sanofi",
    "Moderna",
    "AstraZeneca",
    "Pfizer",
    "Novartis",
    "Roche",
    "Johnson & Johnson",
    "Merck",
    "GSK",
    "Bristol-Myers Squibb",
    "AbbVie",
    "Eli Lilly",
    "Bayer",
    "Amgen",
    "Gilead Sciences",
    "Boehringer Ingelheim",
    "Takeda",
    "Novo Nordisk",
]

INDICATIONS = [
    "Non-Small Cell Lung Cancer",
    "Breast Cancer",
    "Type 2 Diabetes",
    "Rheumatoid Arthritis",
    "Chronic Kidney Disease",
    "Major Depressive Disorder",
    "Alzheimer's Disease",
    "Atopic Dermatitis",
    "Crohn's Disease",
    "Multiple Sclerosis",
    "Idiopathic Pulmonary Fibrosis",
    "Hepatitis B",
    "Prostate Cancer",
    "Asthma",
    "Heart Failure",
    "Sickle Cell Disease",
    "Obesity",
    "Migraine",
    "NASH",
    "Psoriasis",
]

COUNTRIES = [
    ("US", "United States"),
    ("FR", "France"),
    ("DE", "Germany"),
    ("GB", "United Kingdom"),
    ("ES", "Spain"),
    ("IT", "Italy"),
    ("JP", "Japan"),
    ("CA", "Canada"),
    ("AU", "Australia"),
    ("BR", "Brazil"),
    ("KR", "South Korea"),
    ("IN", "India"),
    ("MX", "Mexico"),
    ("ZA", "South Africa"),
    ("PL", "Poland"),
    ("NL", "Netherlands"),
    ("BE", "Belgium"),
    ("AR", "Argentina"),
    ("CL", "Chile"),
    ("TW", "Taiwan"),
    ("IL", "Israel"),
    ("CZ", "Czech Republic"),
    ("HU", "Hungary"),
    ("TH", "Thailand"),
    ("RU", "Russia"),
    ("CO", "Colombia"),
    ("PH", "Philippines"),
    ("EG", "Egypt"),
    ("SE", "Sweden"),
    ("DK", "Denmark"),
]

PHASES = ["Phase I", "Phase II", "Phase III", "Phase IV"]
TRIAL_STATUSES = ["recruiting", "active", "completed", "suspended"]

# ---------- sponsors ----------
# Column naming: createdAt (camelCase leak — should be created_at)


def generate_sponsors():
    rows = []
    for i, name in enumerate(REAL_SPONSORS, start=1):
        rows.append(
            {
                "sponsor_id": f"sp_{i:03d}",
                "sponsor_name": name,
                "createdAt": fake.date_between(
                    start_date="-5y", end_date="-2y"
                ).isoformat(),
            }
        )

    # Test data row
    rows.append(
        {
            "sponsor_id": "sp_099",
            "sponsor_name": "TEST",
            "createdAt": "2024-01-01",
        }
    )

    return rows


# ---------- trials ----------
# Column naming: trialName (camelCase leak — should be trial_name)


def generate_trials(sponsors):
    rows = []
    trial_id = 1
    real_sponsors = [s for s in sponsors if s["sponsor_name"] != "TEST"]

    # distribute ~150 trials across sponsors (weighted toward bigger pharma)
    weights = np.array([8, 6, 7, 9, 7, 8, 6, 7, 5, 6, 5, 6, 5, 4, 4, 5, 4, 5], dtype=float)
    weights = weights / weights.sum()

    for sponsor, count in zip(
        real_sponsors, np.random.multinomial(145, weights)
    ):
        for _ in range(count):
            start = fake.date_between(start_date="-3y", end_date="-6m")
            end = start + timedelta(days=random.randint(180, 1095))
            rows.append(
                {
                    "trial_id": f"tr_{trial_id:04d}",
                    "sponsor_id": sponsor["sponsor_id"],
                    "trialName": f"{fake.word().capitalize()}-{random.randint(100,999)}",
                    "indication": random.choice(INDICATIONS),
                    "phase": random.choice(PHASES),
                    "status": random.choice(TRIAL_STATUSES),
                    "start_date": start.isoformat(),
                    "end_date": end.isoformat(),
                }
            )
            trial_id += 1

    # a few test trials
    rows.append(
        {
            "trial_id": f"tr_{trial_id:04d}",
            "sponsor_id": "sp_099",
            "trialName": "TEST-TRIAL-001",
            "indication": "Test Indication",
            "phase": "Phase I",
            "status": "active",
            "start_date": "2024-01-01",
            "end_date": "2025-01-01",
        }
    )

    return rows


# ---------- sites ----------
# Column naming: siteName, countryCode (camelCase) but country_name (snake_case) — inconsistent!


def generate_sites():
    rows = []
    site_id = 1

    # distribute ~800 sites across 30 countries (US heavy, then EU, then rest)
    country_weights = np.array(
        [
            15, 8, 7, 7, 6, 6, 5, 5, 4, 4,  # US, FR, DE, GB, ES, IT, JP, CA, AU, BR
            3, 3, 3, 2, 3, 3, 2, 2, 2, 2,    # KR, IN, MX, ZA, PL, NL, BE, AR, CL, TW
            2, 2, 2, 1, 1, 1, 1, 1, 1, 1,    # IL, CZ, HU, TH, RU, CO, PH, EG, SE, DK
        ],
        dtype=float,
    )
    country_weights = country_weights / country_weights.sum()
    counts = np.random.multinomial(800, country_weights)

    for (code, name), count in zip(COUNTRIES, counts):
        for _ in range(count):
            rows.append(
                {
                    "site_id": f"si_{site_id:04d}",
                    "siteName": f"{fake.company()} Research Center",
                    "countryCode": code,
                    "country_name": f"country: {name}",
                }
            )
            site_id += 1

    return rows


# ---------- patient_trial_matches ----------
# No match_id — candidate must create a surrogate key
# Column naming: processedAt, reviewedAt, enrolledAt (camelCase leak)


def generate_matches(trials, sites):
    rows = []

    real_trials = [t for t in trials if not t["trialName"].startswith("TEST")]
    site_ids = [s["site_id"] for s in sites]

    for trial in real_trials:
        # each trial gets 50-600 patient matches
        n_matches = random.randint(50, 600)
        trial_sites = random.sample(site_ids, k=min(random.randint(5, 40), len(site_ids)))

        for _ in range(n_matches):
            processed_at = fake.date_time_between(
                start_date="-2y", end_date="now"
            )

            # funnel: processed -> reviewed (~60%) -> enrolled (~25% of reviewed)
            reviewed_at = None
            enrolled_at = None
            if random.random() < 0.60:
                reviewed_at = processed_at + timedelta(
                    days=random.randint(1, 30)
                )
                if random.random() < 0.25:
                    enrolled_at = reviewed_at + timedelta(
                        days=random.randint(1, 60)
                    )

            rows.append(
                {
                    "patient_id": f"pat_{random.randint(10000, 99999)}",
                    "trial_id": trial["trial_id"],
                    "site_id": f"SITE-{random.choice(trial_sites)}",
                    "processedAt": processed_at.isoformat(),
                    "reviewedAt": reviewed_at.isoformat() if reviewed_at else "",
                    "enrolledAt": enrolled_at.isoformat() if enrolled_at else "",
                }
            )

    # Plant one exact duplicate row (same patient+trial+site, same timestamps)
    dup_row = rows[42].copy()
    rows.append(dup_row)

    # Test patient rows
    for i in range(5):
        rows.append(
            {
                "patient_id": f"test_patient_{i}",
                "trial_id": real_trials[0]["trial_id"],
                "site_id": f"SITE-{site_ids[0]}",
                "processedAt": "2024-06-01T00:00:00",
                "reviewedAt": "",
                "enrolledAt": "",
            }
        )

    return rows


# ---------- write CSVs ----------


def write_csv(filename, rows, fieldnames):
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"  {filename}: {len(rows)} rows")


def main():
    print("Generating synthetic data...")

    sponsors = generate_sponsors()
    trials = generate_trials(sponsors)
    sites = generate_sites()
    matches = generate_matches(trials, sites)

    write_csv(
        "raw_sponsors.csv",
        sponsors,
        ["sponsor_id", "sponsor_name", "createdAt"],
    )
    write_csv(
        "raw_trials.csv",
        trials,
        [
            "trial_id",
            "sponsor_id",
            "trialName",
            "indication",
            "phase",
            "status",
            "start_date",
            "end_date",
        ],
    )
    write_csv(
        "raw_sites.csv",
        sites,
        ["site_id", "siteName", "countryCode", "country_name"],
    )
    write_csv(
        "raw_patient_trial_matches.csv",
        matches,
        [
            "patient_id",
            "trial_id",
            "site_id",
            "processedAt",
            "reviewedAt",
            "enrolledAt",
        ],
    )

    print("Done! CSVs written to data/raw/")


if __name__ == "__main__":
    main()
