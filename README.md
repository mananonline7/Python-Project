# PrediMaint AI

Machine Learning based Predictive Maintenance portal built with Streamlit. Predicts bearing faults (Random Forest, trained on the CWRU bearing dataset) from vibration sensor features, and auto-generates maintenance work orders, inventory alerts, and notifications.

## Pages

- **Home** — executive dashboard / system status
- **Live Monitoring** — latest sensor reading from InfluxDB
- **Machine Learning Prediction** — runs the Random Forest model and logs a prediction
- **Maintenance Work Orders** — auto-generated work order for the latest fault
- **Inventory Management** — spare bearing stock levels
- **Email Notifications** — notification preview (demo only, does not send real email)
- **Tableau Analytics** — executive KPIs + embedded public Tableau dashboards

## Local setup

```bash
pip install -r requirements.txt
```

Copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml` and fill in your own InfluxDB credentials:

```toml
INFLUXDB_HOST = "http://localhost:8181"
INFLUXDB_DATABASE = "dissertation"
INFLUXDB_TOKEN = "your-influxdb-token-here"
```

Then run:

```bash
streamlit run 0_🏠_Home.py
```

## Deploying online

This app can be deployed for free on [Streamlit Community Cloud](https://streamlit.io/cloud):

1. Push this repo to GitHub.
2. On share.streamlit.io, create a new app pointing at `0_🏠_Home.py`.
3. In the app's **Settings → Secrets**, paste the same keys as `.streamlit/secrets.toml` (with your real InfluxDB credentials).

### Important limitation

The **Live Monitoring** and **Machine Learning Prediction** pages read live sensor data from an InfluxDB instance. If `INFLUXDB_HOST` points at `localhost`, it will only work when Streamlit and InfluxDB run on the same machine — a cloud-hosted app cannot reach a database on your own PC. To make those pages work online, host InfluxDB somewhere publicly reachable (e.g. [InfluxDB Cloud](https://www.influxdata.com/products/influxdb-cloud/)) and point `INFLUXDB_HOST` at that instance.

The other pages (Work Orders, Inventory, Email, Tableau Analytics) read from the bundled SQLite database (`data/predictive_maintenance.db`) and work fine on any host.

## Notes

- Never commit `.streamlit/secrets.toml` — it's gitignored. Only `.streamlit/secrets.toml.example` (placeholder values) is committed.
- `models/random_forest_model.pkl` was pickled with a specific scikit-learn version; if loading it fails after deployment, retrain and re-save the model with the scikit-learn version pinned in `requirements.txt`.

---

© 2026 PrediMaint AI | MSc Data Science Dissertation | Mohamed Irfan Ali | Arden University
