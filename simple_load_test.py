#!/usr/bin/env python3
import requests
import time
import random
from concurrent.futures import ThreadPoolExecutor, as_completed

HOST = "http://localhost:5000"
EMAIL = "2818506630@qq.com"
PASSWORD = "123456"
USERS = 20
DURATION = 60  # 秒

# 登录获取 token
resp = requests.post(f"{HOST}/api/login", json={"email": EMAIL, "password": PASSWORD})
if resp.status_code != 200:
    print(f"登录失败: {resp.status_code} {resp.text}")
    exit(1)
token = resp.json().get("token")
headers = {"Authorization": f"Bearer {token}"}
print(f"登录成功，token: {token[:20]}...")

# 发送消息
def send_message(i):
    start = time.time()
    try:
        r = requests.post(f"{HOST}/api/chat/send",
                          json={"message": random.choice(["你好", "Bonjour", "教我法语", "苹果怎么说"])},
                          headers=headers,
                          timeout=120)
        elapsed = time.time() - start
        return {"id": i, "status": r.status_code, "elapsed": elapsed, "text": r.text[:100] if r.status_code != 200 else ""}
    except Exception as e:
        return {"id": i, "status": "error", "elapsed": time.time() - start, "error": str(e)}

# 预热：先发一条
send_message(0)

print(f"\n开始压测：{USERS} 并发用户，持续 {DURATION} 秒...")
start_time = time.time()
results = []
success = 0
failed = 0

with ThreadPoolExecutor(max_workers=USERS) as executor:
    futures = []
    while time.time() - start_time < DURATION:
        # 保持 USERS 个并发
        while len(futures) < USERS:
            future = executor.submit(send_message, len(futures))
            futures.append(future)

        # 收集完成的
        done = [f for f in futures if f.done()]
        for f in done:
            result = f.result()
            results.append(result)
            if result["status"] == 200:
                success += 1
            else:
                failed += 1
                if failed <= 5:
                    print(f"  失败示例: {result['status']} - {result.get('text', result.get('error', ''))[:100]}")
            futures.remove(f)

        time.sleep(0.1)

# 等待剩余的
for f in futures:
    result = f.result()
    results.append(result)
    if result["status"] == 200:
        success += 1
    else:
        failed += 1
        if failed <= 5:
            print(f"  失败示例: {result['status']} - {result.get('text', result.get('error', ''))[:100]}")

total = success + failed
elapsed_times = [r["elapsed"] for r in results if "error" not in r]
elapsed_times.sort()

print(f"\n===== 结果 =====")
print(f"总请求数: {total}")
print(f"成功: {success} ({100*success/total:.1f}%)")
print(f"失败: {failed} ({100*failed/total:.1f}%)")
if elapsed_times:
    print(f"响应时间 (ms):")
    print(f"  最小: {min(elapsed_times)*1000:.0f}")
    print(f"  中位数: {elapsed_times[len(elapsed_times)//2]*1000:.0f}")
    print(f"  95%: {elapsed_times[int(len(elapsed_times)*0.95)]*1000:.0f}")
    print(f"  最大: {max(elapsed_times)*1000:.0f}")
