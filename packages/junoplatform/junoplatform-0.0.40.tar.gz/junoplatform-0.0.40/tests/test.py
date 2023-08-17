import redis
from redis.commands.json.path import Path

r = redis.Redis("192.168.101.157", 6379, 0, "myredis")
data = {"A": 123, "b":456}
r.json().set("k:1", "$", data)
a = r.json().get("k:1")

print(a)