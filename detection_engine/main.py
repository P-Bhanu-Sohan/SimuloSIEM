import json
import time
import psycopg2
from kafka import KafkaConsumer, KafkaProducer
import redis
import datetime
from rules.brute_force import detect_brute_force
from rules.sudo_after_fail import detect_privilege_escalation

# --- Service Setups ---
rules = [detect_brute_force, detect_privilege_escalation]

def connect_to_kafka():
    while True:
        try:
            consumer = KafkaConsumer(
                'raw-logs',
                bootstrap_servers='kafka:9092',
                group_id='detector',
                value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                consumer_timeout_ms=10000 # Timeout to allow checking connection status
            )
            producer = KafkaProducer(
                bootstrap_servers='kafka:9092',
                value_serializer=lambda m: json.dumps(m).encode('utf-8')
            )
            print("Successfully connected to Kafka")
            return consumer, producer
        except Exception as e:
            print(f"Could not connect to Kafka: {e}")
            time.sleep(5)

def connect_to_postgres():
    while True:
        try:
            conn = psycopg2.connect(
                host="postgres",
                database="simulosiem",
                user="user",
                password="password"
            )
            print("Successfully connected to PostgreSQL")
            return conn
        except psycopg2.OperationalError as e:
            print(f"Could not connect to PostgreSQL: {e}")
            time.sleep(5)

consumer, producer = connect_to_kafka()
r = redis.Redis(host='redis', port=6379, decode_responses=True)
print("Successfully connected to Redis")
pg_conn = connect_to_postgres()
pg_cursor = pg_conn.cursor()

print("Detection Engine is running and listening for logs...")

# --- Main Detection Loop ---
for msg in consumer:
    if not msg:
        print("Detection Engine: No message received from Kafka (timeout).")
        continue
    log = msg.value
    print(f"Detection Engine: Received log: {log.get('event')} from {log.get('ip')}")
    for rule in rules:
        print(f"Detection Engine: Applying rule {rule.__name__} to log.")
        alert = rule(log, r)
        if alert:
            # 1. Store in Redis (for the live UI)
            # Use a more specific key and set an expiration
            redis_key = f"alert:{alert.get('alert')}:{alert.get('ip')}:{alert.get('user')}"
            r.set(redis_key, json.dumps(alert), ex=300)  # Expire after 5 minutes

            # 2. Send to Kafka (for other potential services)
            producer.send("alerts", alert)

            # 3. Persist in PostgreSQL
            try:
                pg_cursor.execute(
                    """
                    INSERT INTO alerts (alert_type, ip, "user", count, timestamp)
                    VALUES (%s, %s, %s, %s, CAST(%s AS TIMESTAMP))
                    """,
                    (
                        alert.get('alert'),
                        alert.get('ip'),
                        alert.get('user'),
                        alert.get('count'),  # Handles cases where count is not present
                        datetime.datetime.fromisoformat(alert.get('timestamp')).strftime('%Y-%m-%d %H:%M:%S')
                    )
                )
                pg_conn.commit()
                print(f"[ALERT] Persisted to PostgreSQL: {alert}")
            except psycopg2.Error as e:
                print(f"Error inserting alert into PostgreSQL: {e}")
                pg_conn.rollback()
                # Simple reconnect logic
                if pg_conn.closed:
                    pg_conn = connect_to_postgres()
                    pg_cursor = pg_conn.cursor()

# Clean up connections
if pg_conn:
    pg_cursor.close()
    pg_conn.close()
if consumer:
    consumer.close()
if producer:
    producer.close()
