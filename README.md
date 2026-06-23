# Tipping Point Lab — Backend

Interactive climate tipping-point and media literacy application.
Django REST Framework backend — powers the Next.js frontend.

---

## Quick start

```bash
# 1. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure your database
#    Edit config/settings.py – PostgreSQL is the default.
#    For local zero-config dev, uncomment the SQLite block.

# 4. Run migrations
python manage.py migrate

# 5. Seed the database
python manage.py seed_tipping_points   # loads CSV → TippingPoint + relationships
python manage.py seed_metrics          # stat cards, CO₂ data, simulation scenarios

# 6. (Optional) create a superuser for /admin
python manage.py createsuperuser

# 7. Start the dev server
python manage.py runserver
```

API root: http://localhost:8000/api/

---

## Project structure

```
tipping_point_lab/
├── config/
│   ├── settings.py        Django settings (DB, CORS, DRF, paths)
│   ├── urls.py            Root URL config
│   └── wsgi.py
│
├── apps/
│   ├── tipping_points/    Core tipping-point cards, relationships, sources
│   │   ├── models.py      TippingPoint, TippingPointRelationship, SourceReference
│   │   ├── serializers.py Card + Detail serializers
│   │   ├── views.py       ReadOnly viewset + graph/relationships actions
│   │   ├── urls.py
│   │   ├── admin.py
│   │   └── management/commands/seed_tipping_points.py
│   │
│   ├── claims/            Media Literacy Lab
│   │   ├── models.py      ClimateClaim, EvidenceSentence, MisinformationTechnique
│   │   ├── serializers.py Quiz + Detail + AnswerCheck serializers
│   │   ├── views.py       Random quiz, answer-check, keyword search
│   │   ├── urls.py
│   │   └── admin.py
│   │
│   ├── simulator/         Domino Simulator
│   │   ├── models.py      SimulationRun, ActivatedNode, SimulationScenario
│   │   ├── services.py    DominoSimulationService (scoring engine)
│   │   ├── views.py       POST /run/, scenario list
│   │   ├── urls.py
│   │   └── admin.py
│   │
│   └── metrics/           Evidence Dashboard
│       ├── models.py      ClimateMetric, MetricDataPoint, StatisticCard
│       ├── serializers.py
│       ├── views.py
│       ├── urls.py
│       ├── admin.py
│       └── management/commands/seed_metrics.py
│
├── data/
│   └── tipping_point_seed_data.csv
│
└── requirements.txt
```

---

## API endpoints

### Tipping Points
| Method | URL | Description |
|--------|-----|-------------|
| GET | `/api/tipping-points/` | All cards (filterable by `?domain=`, `?severity=`, `?search=`) |
| GET | `/api/tipping-points/{slug}/` | Full detail page data |
| GET | `/api/tipping-points/{slug}/relationships/` | Incoming + outgoing graph edges |
| GET | `/api/tipping-points/graph/` | All nodes + edges (graph library format) |
| GET | `/api/tipping-points/by-domain/` | Counts grouped by domain |

### Claims (Media Literacy Lab)
| Method | URL | Description |
|--------|-----|-------------|
| GET | `/api/claims/` | All claims (quiz list view) |
| GET | `/api/claims/{id}/` | Full reveal (label + evidence) |
| GET | `/api/claims/random/?difficulty=medium` | Random redacted quiz card |
| POST | `/api/claims/{id}/check-answer/` | Evaluate user answer |
| GET | `/api/claims/search/?q=...` | Keyword search |
| GET | `/api/claims/techniques/` | All misinformation techniques |

### Simulator
| Method | URL | Description |
|--------|-----|-------------|
| POST | `/api/simulator/run/` | Run simulation (6 slider values) |
| GET | `/api/simulator/scenarios/` | Preset scenarios |
| GET | `/api/simulator/scenarios/{slug}/` | Scenario detail + default values |

### Metrics
| Method | URL | Description |
|--------|-----|-------------|
| GET | `/api/metrics/` | All time-series metrics |
| GET | `/api/metrics/{slug}/` | Metric + all data points |
| GET | `/api/metrics/stat-cards/` | Headline stat cards for dashboard |

---

## Simulator input/output

**POST /api/simulator/run/**

```json
{
  "misinformation":  70,
  "media_literacy":  30,
  "public_trust":    35,
  "policy_speed":    20,
  "emissions":       80,
  "resilience":      30,
  "save_run":        false
}
```

All values 0–100.

**Response:**
```json
{
  "trust_score":       28.5,
  "delay_risk":        74.2,
  "climate_pressure":  79.5,
  "risk_level":        "critical",
  "narrative":         "Under these conditions, widespread tipping-point activation...",
  "activated_nodes": [
    {
      "slug":             "warm_water_coral_reefs_dieoff",
      "name":             "Warm-water coral reef die-off",
      "domain":           "biosphere_ocean",
      "activation_score": 0.93,
      "triggered_by":     []
    }
  ],
  "interventions": [
    "Invest in media literacy education and public science communication.",
    "Accelerate policy timelines — delayed action compounds climate pressure non-linearly."
  ]
}
```

---

## Next steps (Phase 2 → 3)

- **Phase 3 (Frontend):** Wire the API into Next.js/React components. Start with the Tipping Point Explorer grid and detail pages.
- **Phase 5 (Claims data):** Download CLIMATE-FEVER JSON and write an import management command for ClimateClaim + EvidenceSentence. A starter loader shell is already scaffolded.
- **Phase 5 (Similarity search):** Swap the `claims/search/` keyword search for TF-IDF (`scikit-learn`) or sentence-transformer embeddings once the claims dataset is loaded.
- **Production:** Replace SQLite with PostgreSQL, set `DEBUG=False`, move `SECRET_KEY` to env var, add `gunicorn` + `nginx`.

---

## Disclaimer

This application is an educational simulation, not a predictive climate model.
Tipping-point relationships and scoring logic are intentionally simplified to demonstrate
cascading dynamics. All scientific references are provided for further reading.
