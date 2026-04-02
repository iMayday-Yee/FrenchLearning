import json
import re
import requests
from config import Config
from prompts.system_prompt import SYSTEM_PROMPT

def build_messages(user, study_day, today_messages, current_message):
    """构建发送给LLM的消息列表"""
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    for msg in today_messages:
        if msg.is_template or msg.role == 'assistant':
            messages.append({"role": "assistant", "content": msg.content})
        else:
            messages.append({"role": "user", "content": msg.content})

    messages.append({"role": "user", "content": current_message})
    return messages

def call_llm(messages):
    """调用硅基流动LLM API"""
    headers = {
        "Authorization": f"Bearer {Config.LLM_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": Config.LLM_MODEL,
        "messages": messages,
        "temperature": 0.7
    }

    try:
        response = requests.post(Config.LLM_API_URL, headers=headers, json=payload, timeout=120)
        response.raise_for_status()
        result = response.json()['choices'][0]['message']['content']
        print(f"LLM response: {result}")
        return result
    except Exception as e:
        print(f"LLM API error: {e}")
        return None

def parse_llm_response(raw_text):
    """解析LLM返回的JSON响应"""
    try:
        return json.loads(raw_text.strip())
    except:
        pass

    match = re.search(r'\{.*\}', raw_text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except:
            pass

    return {"intent": "other", "reply": "好的，请继续练习吧！"}

def get_system_prompt_for_group(group_type):
    """根据用户组别获取系统prompt"""
    return SYSTEM_PROMPT