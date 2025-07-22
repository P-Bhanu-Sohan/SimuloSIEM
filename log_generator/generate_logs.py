from kafka import KafkaProducer
import json, random, time, datetime

producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)
print("Log Generator: Successfully connected to Kafka producer.")

users = ["alice", "bob", "charlie", "diana", "eve", "frank", "grace", "heidi", "ivan", "judy", "root", "admin"]
ips = [f"192.168.1.{i}" for i in range(10, 100)] + [f"10.0.0.{i}" for i in range(1, 20)]
events = [
    "login_success", "login_fail", "sudo", "file_access", "network_scan",
    "malware_detected", "port_scan", "data_exfiltration", "system_boot",
    "service_start", "service_stop", "config_change", "user_add", "user_delete"
]
services = ["web_server", "database", "auth_service", "file_server", "mail_server", "dns_server"]

def generate_log():
    event_weights = [
        10,  # login_success
        5,   # login_fail
        3,   # sudo
        7,   # file_access
        2,   # network_scan
        1,   # malware_detected
        2,   # port_scan
        1,   # data_exfiltration
        4,   # system_boot
        6,   # service_start
        6,   # service_stop
        3,   # config_change
        1,   # user_add
        1    # user_delete
    ]
    return {
        "timestamp": datetime.datetime.now().isoformat(),
        "user": random.choice(users),
        "ip": random.choice(ips),
        "event": random.choices(events, weights=event_weights)[0],
        "service": random.choice(services)
    }

while True:
    log = generate_log()
    producer.send("raw-logs", log)
    print(f"Log Generator: Sent log: {log.get('event')} from {log.get('ip')}")
    time.sleep(0.2)  # 5 logs/sec
