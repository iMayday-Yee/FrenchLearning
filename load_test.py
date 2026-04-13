import random
from locust import HttpUser, task, between

class ChatUser(HttpUser):
    wait_time = between(0.5, 1.5)

    def on_start(self):
        resp = self.client.post("/api/auth/login", json={
            "email": "2818506630@qq.com",
            "password": "123456"
        })
        self.token = resp.json().get("token")
        self.client.headers = {"Authorization": f"Bearer {self.token}"}

    @task
    def send_message(self):
        self.client.post("/api/chat/message", json={
            "message": random.choice(["你好", "Bonjour", "教我法语", "苹果用法语怎么说"])
        })
