import time

def detect_brute_force(log, redis_client):
    if log['event'] != 'login_fail':
        return None

    key = f"fail:{log['ip']}"
    count = redis_client.incr(key)
    redis_client.expire(key, 60)

    if count >= 5:
        return {
            "alert": "Brute Force Detected",
            "ip": log['ip'],
            "user": log['user'],
            "count": count,
            "timestamp": log['timestamp']
        }
    return None
