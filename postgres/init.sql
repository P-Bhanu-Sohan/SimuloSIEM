CREATE TABLE IF NOT EXISTS logs (
    id INTEGER NULL,
    timestamp TIMESTAMP,
    "user" TEXT,
    ip TEXT,
    event TEXT,
    service TEXT
);

CREATE TABLE IF NOT EXISTS alerts (
    id SERIAL PRIMARY KEY,
    alert_type TEXT,
    ip TEXT,
    "user" TEXT,
    count INTEGER,
    timestamp TIMESTAMP
);