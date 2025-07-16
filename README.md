
# SimuloSIEM 🛡️

**SimuloSIEM** is a lightweight, containerized Security Information and Event Management (SIEM) simulation platform. It uses Kafka for log streaming, Vector.dev for log parsing, Redis for caching, PostgreSQL for storage, and Python-based detection engines to identify suspicious activity — all visualized through Grafana dashboards.

---

## 📈 Project Overview

SimuloSIEM ingests synthetic security logs, simulates detection of threats like brute force attacks and privilege escalation, and visualizes system health in real-time. It's ideal for learning distributed systems, security monitoring, and streaming pipelines.

---

## 🗺️ System Architecture

```mermaid
graph TD
  A[Log Generator (Python)] --> B[Kafka (raw-logs topic)]
  B --> C[Vector.dev (Parser)]
  C --> D[PostgreSQL (Structured Storage)]
  C --> E[Redis (Cache)]
  E --> F[Detection Engine (Python)]
  F --> G[Kafka (alerts topic)]
  F --> H[Redis (Alert Cache)]
  D --> I[Grafana Dashboard]
  H --> I
```

---

## ⚙️ Tech Stack

| Component         | Technology           |
|------------------|----------------------|
| Log Ingestion     | Kafka, Zookeeper     |
| Log Parsing       | Vector.dev           |
| Streaming + Cache | Redis                |
| Storage           | PostgreSQL           |
| Detection Engine  | Python (modular rules)|
| Containerization  | Docker, Docker Compose |
| Visualization     | Grafana              |

---

## 📂 Folder Structure

```
simulosiem/
├── docker-compose.yml
├── log_generator/
│   └── generate_logs.py
├── vector/
│   └── vector.yaml
├── detection_engine/
│   ├── main.py
│   └── rules/
│       ├── brute_force.py
│       └── escalation.py
├── redis/
├── postgres/
├── grafana/
│   └── dashboards/
│       └── simulosiem.json
└── README.md
```

---

## 🚨 Detection Rules (Examples)

- **Brute Force Detection**: >5 failed logins from same IP in 60 seconds.
- **Privilege Escalation**: `sudo` used from a previously unauthorized user.
- **Recon Activity**: Multiple suspicious endpoint hits or known sensitive paths.

---

## 🐳 Running SimuloSIEM

> Make sure Docker and Docker Compose are installed.

```bash
git clone https://github.com/yourname/simulosiem.git
cd simulosiem
docker-compose up --build
```

Services:
- Kafka: `localhost:9092`
- Redis: `localhost:6379`
- PostgreSQL: `localhost:5432`
- Grafana: `http://localhost:3000` (login: `admin/admin`)

---

## 📊 Grafana Dashboards

SimuloSIEM includes real-time dashboards for:
- Top source IPs
- Live alert stream
- Time-series alert counts
- Brute-force attempts

You can import the `grafana/dashboards/simulosiem.json` manually if needed.

---

## 🧠 Future Ideas

- IP geolocation enrichment
- Sigma-like rule interface
- Web UI with FastAPI + React
- Alerting via Slack/Telegram
- Kibana or Loki integration (optional)

---

## 📜 License

MIT License. For educational use only.

---

## 🤝 Contributing
PRs welcome! Check the `issues` tab or open a discussion for ideas.

