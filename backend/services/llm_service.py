import json
import re
import requests
from config import Config
from prompts.system_prompt import SYSTEM_PROMPT

SKIP_CONTENT_TYPES = {'audio', 'user_audio', 'thinking'}

def build_messages(user, study_day, today_messages, current_message):
    """构建发送给LLM的消息列表，只保留文本类消息"""
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    for msg in today_messages:
        if msg.content_type in SKIP_CONTENT_TYPES:
            continue
        content = msg.content
        if msg.content_type in ('word_audio', 'word_card'):
            try:
                w = json.loads(content)
                content = f"[单词: {w.get('french', '')} - {w.get('chinese', '')}]"
            except:
                continue
        if msg.role == 'assistant':
            messages.append({"role": "assistant", "content": content})
        else:
            messages.append({"role": "user", "content": content})

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
        "temperature": 0.7,
        "max_tokens": 512,
        "reasoning_split": True
    }

    try:
        response = requests.post(Config.LLM_API_URL, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        result = response.json()['choices'][0]['message']['content']
        print(f"LLM response: {result}")
        return result
    except Exception as e:
        print(f"LLM API error: {e}")
        return None

VALID_INTENTS = {'request_material', 'accept_learning', 'reject_learning', 'french_related_chat', 'unrelated_chat', 'other'}

def parse_llm_response(raw_text):
    """解析LLM返回的JSON响应"""
    # 去掉 <think>...</think> 思考块
    text = re.sub(r'<think>.*?</think>', '', raw_text, flags=re.DOTALL).strip()

    parsed = None
    try:
        parsed = json.loads(text)
    except:
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            try:
                parsed = json.loads(match.group())
            except:
                pass

    if not parsed or 'reply' not in parsed:
        # LLM 没有输出 JSON，直接把原文当作回复
        if text and len(text) < 200 and not text.startswith('{'):
            return {"intent": "french_related_chat", "reply": text}
        return {"intent": "other", "reply": "抱歉，我没有理解您的意思，可以再说一次吗？"}

    # 修正模型返回的非标准 intent
    intent = parsed.get('intent', 'other')
    if intent not in VALID_INTENTS:
        if any(k in intent for k in ['material', 'learn', 'study', 'request', 'start']):
            intent = 'request_material'
        elif any(k in intent for k in ['accept', 'agree', 'yes']):
            intent = 'accept_learning'
        elif any(k in intent for k in ['reject', 'refuse', 'decline']):
            intent = 'reject_learning'
        elif any(k in intent for k in ['french', 'grammar', 'language', 'vocab', 'chat']):
            intent = 'french_related_chat'
        elif any(k in intent for k in ['unrelated', 'off_topic']):
            intent = 'unrelated_chat'
        else:
            intent = 'french_related_chat'
    parsed['intent'] = intent

    return parsed

def get_system_prompt_for_group(group_type):
    """根据用户组别获取系统prompt"""
    return SYSTEM_PROMPT