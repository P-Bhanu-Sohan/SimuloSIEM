def detect_privilege_escalation(log, redis_client):
    if log['event'] == 'login_fail':
        redis_client.setex(f"failed:{log['user']}@{log['ip']}", 120, 1)

    if log['event'] == 'sudo':
        key = f"failed:{log['user']}@{log['ip']}"
        if redis_client.exists(key):
            return {
                "alert": "Suspicious Privilege Escalation",
                "user": log['user'],
                "ip": log['ip'],
                "timestamp": log['timestamp']
            }
    return None
