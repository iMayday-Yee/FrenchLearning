# PRD：法语学习AI助手研究平台

## 一、项目概述

### 1.1 项目背景
这是一个管理学院博士生的调查研究项目。目的是研究**不同AI交互自主性风格**和**不同AI头像形象**对用户学习兴趣度、学习效果和用户粘性的影响。

### 1.2 产品定位
一个基于Web的法语学习聊天助手平台。用户通过浏览器（手机端或PC端）访问，与AI助手进行法语学习互动。每天推送3个法语单词（含拼写、词义、音频），用户可跟读并上传录音。

### 1.3 技术栈
- **前端**：Vue 3 + 响应式设计（同时适配移动端和PC端）
- **后端**：Python 3 + Flask
- **数据库**：SQLite（200用户规模够用，低内存开销，适合2核2G服务器）
- **LLM API**：硅基流动（SiliconFlow）提供的大模型API
- **服务器**：阿里云 2核2G ECS，通过公网IP直接访问（不使用域名）
- **通知渠道**：微信测试公众号模板消息 + 邮件（双通道，至少绑定一种）

### 1.4 规模与约束
- 最大用户数：200人
- 需考虑200人并发场景
- 学习周期：5天学习 + 测评 + 5天自主学习 = 共约11天活跃期
- 每用户每天最多20轮对话（1轮 = 用户发1条 + 助手回1条）
- 所有用户统一日期开始学习（由管理员在后台设定开放日期）

---

## 二、用户角色

### 2.1 被试用户（学习者）
- 通过注册页面注册
- 在浏览器中使用法语学习聊天功能
- 不知道自己被分到哪个实验组

### 2.2 管理员（研究人员）
- 通过后台管理页面操作
- 可设置学习开始日期、查看/导出所有实验数据
- 可管理每日单词列表和音频资源
- 可查看所有用户的分组情况、学习数据、对话记录

---

## 三、实验分组设计

### 3.1 交互风格分组（三组，用户不知情）

| 组别 | 名称 | 代号 | 交互特点 |
|------|------|------|----------|
| A组 | 低自主性组 | low | 助手被动等待，仅当用户主动发送类似"给我发法语练习音频"的请求时才发送学习材料 |
| B组 | 可调自主性组 | adjustable | 用户打开应用时，助手主动询问"您现在想要练习法语吗？我可以给您发送今天的练习音频"，用户同意后发送；拒绝则下次打开时再询问 |
| C组 | 高自主性组 | high | 用户打开应用时，助手直接发送"这是今天要练习的法语音频，你可以开始学习了"以及学习材料，无需询问 |

### 3.2 头像分组（两类）

| 类别 | 说明 |
|------|------|
| human | 类人形象头像 |
| robot | 机器人形象头像 |

### 3.3 分组规则
- 用户注册时系统自动随机分配到A/B/C中的一组
- 同时随机分配human或robot头像
- **必须保证平衡**：每个交互组内，human和robot各占一半
- 实现方式：预生成分组槽位。例如目标180人 → A组60人（30 human + 30 robot），B组60人（30 human + 30 robot），C组60人（30 human + 30 robot）。注册时从尚未满的槽位中随机选取一个分配。当某个槽位满了就不再分配该槽位。

---

## 四、注册流程

### 4.1 注册页面字段

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| 手机号 | text | 是 | 作为登录账号，唯一标识 |
| 邮箱 | email | 否 | 备用通知渠道（若未绑定微信则必填） |
| 密码 | password | 是 | 登录密码 |
| 姓名/昵称 | text | 是 | 显示用途 |
| 年龄 | number | 是 | 调研数据 |
| 性别 | select | 是 | 选项：男 / 女 / 其他 |
| 教育背景 | select | 是 | 选项：高中及以下 / 大专 / 本科 / 硕士 / 博士 |
| 对法语的兴趣程度 | select | 是 | 选项：非常感兴趣 / 比较感兴趣 / 一般 / 不太感兴趣 / 完全不感兴趣 |
| 法语学习基础 | select | 是 | 选项：零基础 / 了解少量单词 / 系统学习过一段时间 / 较为熟练 |
| 偏好学习时间段 | select | 是 | 选项：6:00-8:00 / 8:00-10:00 / 10:00-12:00 / 12:00-14:00 / 14:00-16:00 / 16:00-18:00 / 18:00-20:00 / 20:00-22:00 / 22:00-24:00 |

### 4.2 注册流程步骤

```
第1步：填写基本信息（上述所有字段） → 提交
       系统自动分组（用户不可见），创建用户记录
第2步：微信绑定页面
       展示带参数二维码（参数为user_id）
       用户用微信扫码关注测试公众号
       后端收到微信回调 → 绑定 user_id 与 openid
       前端每3秒轮询后端检查绑定状态，最多轮询60次（3分钟）
       绑定成功 → 自动跳转到第3步
       绑定超时或用户点击"跳过" → 检查是否已填写邮箱，是则允许跳过，否则提示必须绑定微信或填写邮箱
第3步：用户协议与隐私说明页 → 勾选同意后完成注册
第4步：注册完成页 → 显示"学习将于 X月X日 统一开始，届时请打开本页面开始学习"
```

### 4.3 用户协议内容要点（需展示给用户确认）
本研究将收集以下数据用于学术研究：
- 您主动发送消息的次数
- 您回复同意/拒绝接收学习材料的次数
- 您上传语音跟读的次数
- 您通过麦克风录音互动的次数
- 各组发音准确度评分的平均分差异（如有此功能）
- 所有聊天内容的完整记录
- 您的注册信息（年龄、性别、教育背景等）

所有数据仅用于学术研究，匿名处理后分析，不会泄露您的个人身份信息。

---

## 五、登录与学习开放控制

### 5.1 登录
- 登录方式：手机号 + 密码
- 登录后根据学习状态路由到对应页面

### 5.2 学习开放控制
- 管理员在后台设置一个"学习开始日期"（精确到日），例如 2026-04-07
- 在该日期的 06:00 之前，用户登录后看到等待页面："学习将于 X月X日 开始，请届时再来"
- 从该日期 06:00 起，学习功能正式开放
- 学习天数以自然日计算：开始日期为Day1，次日为Day2，以此类推
- Day1-Day5：每天推送3个新单词（第一阶段）
- Day5学习完成后：推送测评
- Day6-Day10：每天推送3个新单词（第二阶段，自主学习，形式与前5天完全一致，无最终测评）
- Day10之后：学习功能关闭，显示感谢页面

---

## 六、核心功能：聊天界面与学习流程

### 6.1 聊天界面设计

**布局**：类似常见即时通讯界面
- 顶部：助手名称"法语学习助手" + 头像（根据用户分组显示human或robot头像图片）
- 中部：聊天消息流（支持文字消息、音频播放器、单词卡片）
- 底部：文本输入框 + 发送按钮 + 录音按钮

**消息类型**：
1. **文本消息**：用户和助手的文字对话，普通聊天气泡样式
2. **单词卡片**：展示单词拼写 + 中文词义，高亮卡片样式（与普通文字消息视觉区分）
3. **音频消息**：可播放的音频条（用于发送法语单词标准发音音频，显示播放按钮 + 进度条）
4. **用户录音**：用户跟读后上传的录音，也显示为可播放的音频条，靠右显示

**响应式要求**：
- 移动端：全屏聊天界面，底部输入栏固定在屏幕底部
- PC端：居中卡片式布局（最大宽度约500px），模拟手机聊天体验

**整个学习周期内的聊天记录都在同一个页面中滚动显示**，不需要新开对话框。不同天的消息之间可显示一个日期分隔线（如"—— Day 3 · 4月9日 ——"）。

### 6.2 每日学习流程（按组别）

#### 6.2.1 A组（低自主性组）流程

```
用户打开应用 → 进入聊天界面（无任何助手主动消息）
用户什么都不说 → 助手不发任何内容
用户发送类似"给我发法语练习音频"/"我要学习"/"开始今天的课程"的消息
  → 后端将该消息发送给LLM，LLM判断意图为 "request_material"
  → 后端触发发送今日3个单词
  → 助手先回复一句引导文字："好的，这是今天要学习的3个法语单词，请跟着音频练习吧！"
  → 依次发送：单词1卡片 + 音频1、单词2卡片 + 音频2、单词3卡片 + 音频3
  → 末尾追加："以上是今天的3个单词，请跟着音频练习发音，你可以点击录音按钮录制跟读。"
用户跟读上传录音 → 后端记录 → 助手简短鼓励回复
```

#### 6.2.2 B组（可调自主性组）流程

```
用户打开应用 →
  后端检查今天状态：
    若今天已发送过学习材料 → 不做任何主动动作，正常聊天
    若今天未发送材料 → 助手自动发送模板消息：
      "您好！您现在想要练习法语吗？我可以给您发送今天的练习音频 😊"
      
用户回复肯定（LLM判断意图为 "accept_learning"）
  → 发送今日3个单词（同A组的发送流程）
  → 标记今天已发送

用户回复否定（LLM判断意图为 "reject_learning"）
  → 助手回复："好的，那等下次见面我再问您～"
  → 标记今天"本次会话已拒绝"
  → 下次触发"重新进入"事件时（见6.2.4），再次询问
```

#### 6.2.3 C组（高自主性组）流程

```
用户打开应用 →
  后端检查今天状态：
    若今天已发送过学习材料 → 不做任何主动动作
    若今天未发送材料 → 助手自动发送模板消息：
      "这是今天要练习的法语音频，你可以开始学习了！📚"
      + 立即依次发送今日3个单词卡片和音频
      + 标记今天已发送
      （C组不管用户是否跟读，今天都不再重复发送）
```

#### 6.2.4 "重新打开应用"检测逻辑（关键，影响B组和C组）

由于是Web应用，需要定义何为"重新打开"：

| 场景 | 是否算重新打开 |
|------|--------------|
| 用户关闭浏览器标签页后重新输入URL打开 | ✅ 是 |
| 用户刷新页面（F5） | ✅ 是 |
| 页面在后台超过5分钟后切回前台 | ✅ 是 |
| 页面在后台不足5分钟切回前台 | ❌ 否 |
| 手机锁屏后解锁回到页面，若间隔>5分钟 | ✅ 是 |

**前端实现**：
```javascript
// 在聊天页面Chat.vue中
let hiddenAt = null

document.addEventListener('visibilitychange', () => {
  if (document.hidden) {
    hiddenAt = Date.now()
  } else {
    if (hiddenAt && (Date.now() - hiddenAt) > 5 * 60 * 1000) {
      // 离开超过5分钟，视为重新进入，调用后端enter接口
      callStudyEnterAPI()
    }
    hiddenAt = null
  }
})

// 同时在 onMounted 中也调用 callStudyEnterAPI()（页面首次加载/刷新）
```

后端 `/api/study/enter` 收到请求后，根据用户分组和今日状态决定是否返回自动消息：
- A组：永远返回空（不主动发消息）
- B组：若今天未发送材料 → 返回询问消息
- C组：若今天未发送材料 → 返回学习材料（卡片+音频）

### 6.3 单词发送格式

每个单词发送为一组消息（助手连续发送）：

```
[单词卡片消息]
  📖 bonjour
  释义：你好

[音频消息]
  ▶ bonjour 发音音频  （可播放的音频条，点击播放）
```

三个单词依次发送完后，助手追加一条文本消息：
"以上是今天的3个单词，请跟着音频练习发音吧！你可以点击下方的🎤按钮录制你的跟读。"

### 6.4 用户跟读与录音

**录音流程**：
1. 用户点击底部的录音按钮
2. 首次使用时浏览器弹出麦克风权限请求（前端需处理权限被拒绝的提示）
3. 按住录音 或 点击开始/结束（两种交互方式均可，推荐点击式更适合移动端）
4. 录音完成后，前端将音频文件（webm格式）通过 `POST /api/chat/upload_audio` 上传
5. 前端在聊天界面中显示为用户的录音消息气泡
6. 后端返回助手的回复（鼓励文字 + 评分如有）

**后端处理**：
1. 保存原始音频文件，路径：`uploads/{user_id}/day{N}_{word_index}_{timestamp}.webm`
2. 进行有效性检测（见6.5）
3. 有效 → 跟练次数+1；无效 → 无效音频次数+1
4. 在LLM上下文中添加占位符：`[用户发送了单词"bonjour"的跟读录音]`（有效时）或 `[该录音无效（空白/无声）]`（无效时）
5. 调用LLM获取回复
6. 保存聊天记录
7. 对话轮次+1

### 6.5 音频有效性检测

使用 Python `pydub` 库分析上传的音频：
- 音频时长 < 0.5秒 → 无效
- 音频平均音量（dBFS）低于 -50dBFS → 无效（基本是静音）
- 其余情况 → 有效

无效音频仍保存原始文件（供研究人员审查），但不计入有效跟练次数。
助手对无效音频的回复由LLM生成（系统prompt中已指导），通常类似"好像没有听到您的声音呢，要不要再试一次？"。

### 6.6 发音评分（可选功能，视服务器资源而定）

**方案A（推荐尝试）- 调用语音转文字API比对**：
- 调用硅基流动或其他平台的Whisper语音转文字API
- 将用户录音转为文本
- 与目标法语单词做字符串相似度比对（归一化编辑距离）
- 映射为0-100分
- 评分结果随助手回复返回给用户，同时存入数据库

**方案B（保底）- 不评分**：
- 仅记录跟练次数和原始音频
- 测评阶段也只测词义理解，不测发音
- 助手收到有效录音后固定回复鼓励文字

**实现决策**：先开发方案B确保核心流程完整，再尝试接入方案A。如果2核2G服务器无法承载本地Whisper模型，则调用第三方API或直接使用方案B。

### 6.7 对话与LLM交互规则

#### 6.7.1 LLM调用流程

```
用户消息到达后端
  ↓
预处理（音频占位符替换、敏感内容检查等）
  ↓
从数据库加载今日聊天上下文（仅当天的消息记录）
  ↓
组装 messages 数组：system prompt + 今日历史消息 + 当前用户消息
  ↓
调用硅基流动 API
  ↓
解析返回的JSON（提取 intent 和 reply）
  ↓
根据 intent 执行业务逻辑（发送单词 / 记录拒绝 / 直接回复等）
  ↓
保存聊天记录 + 更新状态
  ↓
返回响应给前端
```

#### 6.7.2 上下文管理规则

- **每天的对话上下文独立**：不携带前一天的历史记录（节省token）
- 每次调用LLM时，从数据库加载当天所有消息作为上下文
- B组/C组的模板首条消息也要作为 assistant 角色的消息加入上下文
- 音频相关内容在上下文中以占位符形式表达，不发送真实音频数据

上下文结构示例：
```json
{
  "messages": [
    {"role": "system", "content": "（系统prompt，见6.7.3）"},
    {"role": "assistant", "content": "您好！您现在想要练习法语吗？我可以给您发送今天的练习音频"},
    {"role": "user", "content": "好的"},
    {"role": "assistant", "content": "好的，这是今天要学习的3个法语单词...（包含单词信息的文字描述）"},
    {"role": "user", "content": "[用户发送了单词\"bonjour\"的跟读录音]"},
    {"role": "assistant", "content": "练习得不错！继续加油！"}
  ]
}
```

#### 6.7.3 系统Prompt

以下为发送给LLM的系统prompt模板。后端根据用户所在组别动态生成最终prompt。

```
你是一个法语学习助手，你的唯一职责是帮助用户学习法语。请严格遵守以下规则：

【核心规则】
1. 你只讨论与法语学习相关的话题。
2. 如果用户发送的内容与法语学习完全无关（如闲聊天气、讲笑话、问其他知识），你必须固定回复："我是一个法语学习助手，目前只能和您聊与法语学习有关的内容哦～有什么法语问题都可以问我！"
3. 如果用户发送的内容与法语有一定关系但不在标准学习流程中（如感叹"今天单词好难"、问"法语难不难学"），你可以简短友好回复（不超过50字），然后引导继续练习。
4. 回复风格：友好、鼓励、简洁。

【关于音频占位符】
- 上下文中 [用户发送了单词"xxx"的跟读录音] 表示用户进行了跟读练习，请给予积极鼓励。
- [该录音无效（空白/无声）] 表示录音没有声音，请温和提醒重新录制。

【输出格式——严格遵守】
你的回复必须且只能是一个JSON对象，不要输出任何其他文字。格式：
{"intent": "分类标签", "reply": "给用户的回复文本"}

intent取值说明：
- "request_material"：用户请求获取今天的法语学习材料（如"给我发音频""我要学习""开始今天的课""发给我"等）
- "accept_learning"：用户同意开始学习（如"好的""行""可以""来吧""搞""OK"等肯定回答）
- "reject_learning"：用户拒绝学习（如"不了""现在不行""等会""不想""算了"等否定回答）
- "follow_up_practice"：用户发送了跟读录音
- "french_related_chat"：与法语有关的非标准流程闲聊
- "unrelated_chat"：与法语完全无关的内容
- "other"：无法归类
```

#### 6.7.4 后端对LLM回复的后处理逻辑（伪代码）

```python
def handle_llm_response(user, parsed_response, study_day):
    intent = parsed_response["intent"]
    reply_text = parsed_response["reply"]
    
    if intent == "request_material":
        # A组用户主动请求学习材料
        if not is_material_sent_today(user.id, study_day):
            words = get_daily_words(study_day)
            mark_material_sent(user.id, study_day)
            return build_material_response(reply_text, words)
        else:
            return [{"type": "text", "content": "今天的学习材料已经发送过啦，翻翻上面的消息看看？"}]
    
    elif intent == "accept_learning":
        # B组用户同意学习
        if not is_material_sent_today(user.id, study_day):
            words = get_daily_words(study_day)
            mark_material_sent(user.id, study_day)
            return build_material_response(reply_text, words)
        else:
            return [{"type": "text", "content": reply_text}]
    
    elif intent == "reject_learning":
        # B组用户拒绝学习
        mark_today_rejected(user.id, study_day)
        return [{"type": "text", "content": reply_text}]
    
    elif intent == "follow_up_practice":
        return [{"type": "text", "content": reply_text}]
    
    elif intent == "unrelated_chat":
        # 覆盖LLM回复，使用固定话术（双保险）
        return [{"type": "text", "content": "我是一个法语学习助手，目前只能和您聊与法语学习有关的内容哦～有什么法语问题都可以问我！"}]
    
    else:  # french_related_chat, other
        return [{"type": "text", "content": reply_text}]
```

#### 6.7.5 LLM返回格式容错

LLM可能不严格输出JSON，后端需要做容错：
```python
import json, re

def parse_llm_response(raw_text):
    # 尝试直接解析
    try:
        return json.loads(raw_text.strip())
    except:
        pass
    # 尝试从文本中提取JSON
    match = re.search(r'\{.*\}', raw_text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except:
            pass
    # 兜底：返回默认回复
    return {"intent": "other", "reply": "好的，请继续练习吧！"}
```

#### 6.7.6 每日对话轮次限制

- 每用户每天最多20轮（1轮 = 1次用户消息 + 1次助手回复）
- B/C组的模板首条消息不计入轮次
- 单词卡片和音频的发送不计入轮次（它们是材料推送，不是对话）
- 用户上传录音 + 助手回复计入1轮
- 达到20轮后，不再调用LLM，直接返回："今天的对话次数已用完啦，明天再来继续学习吧！😊"

---

## 七、通知系统

### 7.1 通知触发时机

每天在用户所选学习时间段的**起始时刻**发送一条通知。
例如：用户选择了 "8:00-10:00"，则每天 8:00 整发送通知。

**通知仅为提醒**，不影响学习功能的可用时间。用户在任何时间打开网页都能正常学习。

### 7.2 微信模板消息（主要渠道）

**绑定流程**（在注册阶段完成）：
1. 后端调用微信API生成带参数（user_id）的临时二维码
2. 前端展示二维码图片
3. 用户微信扫码 → 关注测试公众号 → 微信服务器推送事件到后端回调URL
4. 后端从回调事件中提取 openid + user_id（scene参数），存入数据库完成绑定
5. 前端每3秒轮询 `GET /api/bindcheck?user_id=xxx`，绑定成功后自动跳转

**定时发送通知**：
- 使用 APScheduler 定时任务，每小时整点执行
- 查找"study_time_slot起始小时 == 当前小时"且"已绑定微信（wechat_openid非空）"的用户
- 调用微信模板消息API `POST https://api.weixin.qq.com/cgi-bin/message/template/send`
- 消息内容包含跳转URL（学习平台地址），用户点击直接打开

**access_token管理**：
- 微信access_token有效期7200秒（2小时）
- 后端缓存access_token，每100分钟自动刷新一次
- 不能每次发消息都重新获取（会触发频率限制）

### 7.3 邮件通知（备用渠道）

- 对未绑定微信但填写了邮箱的用户，使用邮件通知
- 使用 Python `smtplib` + QQ邮箱或163邮箱SMTP服务
- 邮件标题："📖 今日法语学习提醒"
- 邮件正文：简短文字 + 学习平台URL链接
- 同样由APScheduler定时任务发送

### 7.4 两个微信测试号的使用说明

微信测试号每个最多支持100人关注。如果实验对象超过100人：
- 准备两个微信测试号（两个不同微信号分别注册测试号）
- 注册流程中，当第一个测试号关注数接近上限时，自动切换为展示第二个测试号的二维码
- 后端需记录每个用户绑定的是哪个测试号的openid，发送通知时使用对应测试号的access_token

---

## 八、每日单词数据管理

### 8.1 音频文件结构

```
backend/static/audio/
├── day1/
│   ├── 1-1.mp3
│   ├── 1-2.mp3
│   └── 1-3.mp3
├── day2/
│   ├── 2-1.mp3
│   ├── 2-2.mp3
│   └── 2-3.mp3
...
└── day10/
    ├── 10-1.mp3
    ├── 10-2.mp3
    └── 10-3.mp3
```

### 8.2 单词数据配置（words.json）

```json
[
  {
    "day": 1,
    "words": [
      {"index": 1, "french": "bonjour", "chinese": "你好", "audio": "day1/1-1.mp3"},
      {"index": 2, "french": "merci", "chinese": "谢谢", "audio": "day1/1-2.mp3"},
      {"index": 3, "french": "au revoir", "chinese": "再见", "audio": "day1/1-3.mp3"}
    ]
  }
]
```
（实际30个单词由项目方提供填入。Day1-5共15个单词用于测评，Day6-10共15个新单词。）

### 8.3 计算当前学习天数

```python
from datetime import date

def get_study_day(study_start_date_str):
    start = date.fromisoformat(study_start_date_str)
    delta = (date.today() - start).days + 1  # Day1起
    if delta < 1:
        return 0   # 尚未开始
    if delta > 10:
        return -1  # 已结束
    return delta
```

---

## 九、测评系统

### 9.1 触发条件

当用户处于Day5**且今天已发送过学习材料**时，测评入口出现。具体时机：
- Day5学习材料全部发送完后，助手最后追加一条消息：
  "恭喜你完成了5天的法语学习！🎉 点击下方按钮开始测评吧！"
  + 显示一个"开始测评"按钮
- 或者如果Day5用户没有主动学习（A组情况），则在Day6用户打开应用时，先检查是否需要补做Day5学习和测评
- 测评只做一次，完成后不再出现

### 9.2 测评页面设计（独立全屏页面 /assessment）

#### 词义选择题

- 共15题（Day1-Day5的全部15个单词）
- 题目顺序随机打乱
- 每题展示：一个法语单词 + 4个中文选项
- 4个选项 = 1个正确词义 + 3个干扰项（从其他14个单词的词义中随机抽取）
- 用户选择后自动进入下一题（不显示对错，防止学习效应影响测评）
- 进度条显示"3/15"
- 全部完成后计算成绩

#### 发音测试（仅在评分功能可用时）

- 词义测试结束后进入
- 逐个展示15个单词，要求录音跟读
- 每个录音实时评分
- 完成后计算发音平均分

#### 成绩计算

- 有发音测试：综合分 = 词义正确率×50% + 发音平均分×50%
- 无发音测试：综合分 = 词义正确率×100%
- 结果页展示分数 + 评语（如"优秀！""不错！""继续加油！"）

### 9.3 测评后

- 测评成绩存入 assessment_summary 表
- 返回聊天界面，Day6起继续第二阶段学习（新的15个单词，Day6-Day10）
- 第二阶段结束后无测评

---

## 十、数据库设计

### 10.1 users 表

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PRIMARY KEY AUTOINCREMENT | 用户ID |
| phone | VARCHAR(20) UNIQUE NOT NULL | 手机号 |
| email | VARCHAR(100) | 邮箱 |
| password_hash | VARCHAR(255) NOT NULL | 密码哈希 |
| nickname | VARCHAR(50) NOT NULL | 昵称 |
| age | INTEGER NOT NULL | 年龄 |
| gender | VARCHAR(10) NOT NULL | 性别 |
| education | VARCHAR(20) NOT NULL | 教育背景 |
| french_interest | VARCHAR(20) NOT NULL | 法语兴趣程度 |
| french_level | VARCHAR(20) NOT NULL | 法语学习基础 |
| study_time_slot | VARCHAR(10) NOT NULL | 偏好学习时间段起始时刻（如 "08:00"） |
| group_type | VARCHAR(20) NOT NULL | 交互组别：low / adjustable / high |
| avatar_type | VARCHAR(10) NOT NULL | 头像类型：human / robot |
| wechat_openid | VARCHAR(100) | 微信openid |
| wechat_account_index | INTEGER DEFAULT 0 | 绑定的是第几个测试号（0或1） |
| created_at | DATETIME DEFAULT CURRENT_TIMESTAMP | 注册时间 |

### 10.2 daily_status 表

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PRIMARY KEY AUTOINCREMENT | |
| user_id | INTEGER NOT NULL | 外键→users.id |
| study_day | INTEGER NOT NULL | 学习第几天（1-10） |
| date | DATE NOT NULL | 实际日期 |
| material_sent | BOOLEAN DEFAULT FALSE | 今天是否已发送学习材料 |
| rejected | BOOLEAN DEFAULT FALSE | 今天是否被用户拒绝过（B组用） |
| practice_count | INTEGER DEFAULT 0 | 今日有效跟练次数 |
| invalid_audio_count | INTEGER DEFAULT 0 | 今日无效音频次数 |
| conversation_rounds | INTEGER DEFAULT 0 | 今日已用对话轮次 |

唯一索引：(user_id, study_day)

### 10.3 chat_messages 表

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PRIMARY KEY AUTOINCREMENT | |
| user_id | INTEGER NOT NULL | |
| study_day | INTEGER NOT NULL | 学习第几天 |
| role | VARCHAR(10) NOT NULL | "user" / "assistant" |
| content_type | VARCHAR(20) NOT NULL | "text" / "word_card" / "audio" / "user_audio" / "system" |
| content | TEXT NOT NULL | 文本内容，或JSON（word_card类型存 {"french":"..","chinese":".."}），或文件路径 |
| is_template | BOOLEAN DEFAULT FALSE | 是否为模板消息（B/C组首条自动消息） |
| timestamp | DATETIME DEFAULT CURRENT_TIMESTAMP | |

索引：(user_id, study_day)

### 10.4 audio_records 表

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PRIMARY KEY AUTOINCREMENT | |
| user_id | INTEGER NOT NULL | |
| study_day | INTEGER NOT NULL | |
| word_index | INTEGER | 对应第几个单词（1/2/3），可为NULL（用户可能随时录音） |
| target_word | VARCHAR(50) | 目标法语单词 |
| audio_path | VARCHAR(255) NOT NULL | 音频文件服务器存储路径 |
| is_valid | BOOLEAN DEFAULT FALSE | 是否为有效录音 |
| score | FLOAT | 发音评分（0-100，可为NULL） |
| created_at | DATETIME DEFAULT CURRENT_TIMESTAMP | |

### 10.5 assessment_answers 表（每道题的回答）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PRIMARY KEY AUTOINCREMENT | |
| user_id | INTEGER NOT NULL | |
| word_french | VARCHAR(50) NOT NULL | 测试的法语单词 |
| correct_chinese | VARCHAR(50) NOT NULL | 正确词义 |
| user_choice | VARCHAR(50) NOT NULL | 用户选择的词义 |
| is_correct | BOOLEAN NOT NULL | 是否正确 |
| pronunciation_score | FLOAT | 发音评分（可NULL） |
| created_at | DATETIME DEFAULT CURRENT_TIMESTAMP | |

### 10.6 assessment_summary 表

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PRIMARY KEY AUTOINCREMENT | |
| user_id | INTEGER UNIQUE NOT NULL | |
| vocab_score | FLOAT NOT NULL | 词义正确率（0-100） |
| pronunciation_avg | FLOAT | 发音平均分（可NULL） |
| total_score | FLOAT NOT NULL | 综合分 |
| created_at | DATETIME DEFAULT CURRENT_TIMESTAMP | |

### 10.7 system_config 表

| 字段 | 类型 | 说明 |
|------|------|------|
| key | VARCHAR(50) PRIMARY KEY | 配置键 |
| value | TEXT NOT NULL | 配置值 |

默认配置项：
- `study_start_date`："2026-04-07"
- `max_daily_rounds`："20"
- `reenter_threshold_minutes`："5"

### 10.8 group_slots 表（分组平衡控制）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PRIMARY KEY AUTOINCREMENT | |
| group_type | VARCHAR(20) NOT NULL | low / adjustable / high |
| avatar_type | VARCHAR(10) NOT NULL | human / robot |
| max_count | INTEGER NOT NULL | 该槽位最大人数 |
| current_count | INTEGER DEFAULT 0 | 当前已分配人数 |

唯一索引：(group_type, avatar_type)

初始数据（以180人为例）：
```
(low, human, 30, 0)
(low, robot, 30, 0)
(adjustable, human, 30, 0)
(adjustable, robot, 30, 0)
(high, human, 30, 0)
(high, robot, 30, 0)
```

分配逻辑：从current_count < max_count的槽位中随机选一个，分配后current_count+1。

---

## 十一、API接口完整列表

### 11.1 认证模块

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| POST | /api/register | 用户注册 | 否 |
| POST | /api/login | 用户登录，返回JWT token | 否 |
| GET | /api/user/profile | 获取当前用户信息（头像类型等，不暴露组名） | 是 |

**POST /api/register 请求体**：
```json
{
  "phone": "13800138000",
  "email": "user@example.com",
  "password": "abc123",
  "nickname": "小明",
  "age": 22,
  "gender": "男",
  "education": "本科",
  "french_interest": "比较感兴趣",
  "french_level": "零基础",
  "study_time_slot": "08:00"
}
```

**POST /api/register 响应体**：
```json
{
  "code": 200,
  "user_id": 152,
  "message": "注册成功"
}
```

**POST /api/login 请求/响应**：
```json
// 请求
{"phone": "13800138000", "password": "abc123"}
// 响应
{"code": 200, "token": "eyJ...", "user_id": 152}
```

**GET /api/user/profile 响应**：
```json
{
  "user_id": 152,
  "nickname": "小明",
  "avatar_type": "human",
  "avatar_url": "/avatars/human.png",
  "study_start_date": "2026-04-07",
  "wechat_bindound": true
}
```

### 11.2 微信绑定模块

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| GET | /api/get_bind_qrcode | 获取绑定二维码URL，参数：user_id | 否 |
| GET | /api/bindcheck | 检查是否绑定成功，参数：user_id | 否 |
| GET | /wechat/callback | 微信服务器Token验证 | 否 |
| POST | /wechat/callback | 微信事件推送回调 | 否 |

### 11.3 学习状态模块

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| GET | /api/study/status | 获取当前学习状态 | 是 |
| POST | /api/study/enter | 用户进入/重新进入应用事件 | 是 |

**GET /api/study/status 响应**：
```json
{
  "study_day": 3,
  "phase": "learning",         // "not_started" / "learning" / "assessment" / "learning_phase2" / "completed"
  "material_sent_today": false,
  "remaining_rounds": 20,
  "need_assessment": false
}
```

**POST /api/study/enter 响应**：
```json
{
  "auto_messages": [
    {"type": "text", "content": "您好！您现在想要练习法语吗？我可以给您发送今天的练习音频 😊"}
  ]
}
```
（A组或无需自动消息时 auto_messages 为空数组）

### 11.4 聊天模块

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| POST | /api/chat/send | 发送文本消息 | 是 |
| POST | /api/chat/upload_audio | 上传跟读录音 | 是 |
| GET | /api/chat/history | 获取聊天记录，参数：day（可选，不传则返回当天） | 是 |
| GET | /api/study/words | 获取某天的单词数据，参数：day | 是 |

**POST /api/chat/send 请求**：
```json
{"content": "好的，我要开始学习了"}
```

**POST /api/chat/send 响应**：
```json
{
  "messages": [
    {"type": "text", "content": "好的，这是今天要学习的3个法语单词！"},
    {"type": "word_card", "content": {"french": "bonjour", "chinese": "你好"}},
    {"type": "audio", "content": {"url": "/static/audio/day1/1-1.mp3", "word": "bonjour"}},
    {"type": "word_card", "content": {"french": "merci", "chinese": "谢谢"}},
    {"type": "audio", "content": {"url": "/static/audio/day1/1-2.mp3", "word": "merci"}},
    {"type": "word_card", "content": {"french": "au revoir", "chinese": "再见"}},
    {"type": "audio", "content": {"url": "/static/audio/day1/1-3.mp3", "word": "au revoir"}},
    {"type": "text", "content": "以上是今天的3个单词，请跟着音频练习发音吧！"}
  ],
  "remaining_rounds": 19
}
```

**POST /api/chat/upload_audio**：
- Content-Type: multipart/form-data
- 字段：audio（文件）、word_index（可选，对应第几个单词）
- 响应同 /api/chat/send 格式

**GET /api/chat/history 响应**：
```json
{
  "messages": [
    {"id": 1, "role": "assistant", "type": "text", "content": "...", "timestamp": "2026-04-07T08:30:00"},
    {"id": 2, "role": "user", "type": "text", "content": "...", "timestamp": "2026-04-07T08:30:15"},
    ...
  ]
}
```

### 11.5 测评模块

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| GET | /api/assessment/check | 检查是否需要/可以进行测评 | 是 |
| GET | /api/assessment/questions | 获取测评题目 | 是 |
| POST | /api/assessment/submit | 提交测评答案 | 是 |
| GET | /api/assessment/result | 获取测评结果 | 是 |

**GET /api/assessment/questions 响应**：
```json
{
  "questions": [
    {
      "id": 1,
      "french": "bonjour",
      "options": ["你好", "谢谢", "再见", "早上好"],
      "audio_url": "/static/audio/day1/1-1.mp3"
    },
    ...
  ]
}
```
（15道题，选项已打乱，正确答案不标记——后端记录正确答案用于评分）

**POST /api/assessment/submit 请求**：
```json
{
  "answers": [
    {"question_id": 1, "user_choice": "你好"},
    {"question_id": 2, "user_choice": "谢谢"},
    ...
  ]
}
```

**POST /api/assessment/submit 响应**：
```json
{
  "vocab_score": 86.7,
  "pronunciation_avg": null,
  "total_score": 86.7,
  "correct_count": 13,
  "total_count": 15
}
```

### 11.6 管理后台模块

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| POST | /api/admin/login | 管理员登录 | 否 |
| GET | /api/admin/dashboard | 统计概览 | admin |
| GET | /api/admin/users | 获取所有用户（含分组信息） | admin |
| GET | /api/admin/export/chat | 导出聊天记录CSV | admin |
| GET | /api/admin/export/daily | 导出每日学习数据CSV | admin |
| GET | /api/admin/export/assessment | 导出测评成绩CSV | admin |
| GET | /api/admin/export/audio_list | 导出音频文件清单CSV | admin |
| POST | /api/admin/config | 更新系统配置 | admin |
| POST | /api/admin/notify | 手动发送通知给指定用户 | admin |

**导出CSV字段设计**：

聊天记录CSV：user_id, group_type, avatar_type, study_day, date, role, content_type, content, timestamp

每日学习数据CSV：user_id, group_type, avatar_type, study_day, date, material_sent, practice_count, invalid_audio_count, conversation_rounds

测评成绩CSV：user_id, group_type, avatar_type, nickname, age, gender, education, french_interest, french_level, vocab_score, pronunciation_avg, total_score

---

## 十二、前端页面与路由

### 12.1 路由表

```javascript
const routes = [
  { path: '/', component: Home },                    // 欢迎页，引导登录/注册
  { path: '/register', component: Register },         // 注册第1步：基本信息
  { path: '/bindwechat', component: BindWeChat },     // 注册第2步：微信绑定
  { path: '/agreement', component: Agreement },       // 注册第3步：用户协议
  { path: '/register-done', component: RegisterDone },// 注册第4步：完成
  { path: '/login', component: Login },               // 登录
  { path: '/chat', component: Chat, meta: { auth: true } },         // 聊天主界面
  { path: '/assessment', component: Assessment, meta: { auth: true } }, // 测评
  { path: '/result', component: Result, meta: { auth: true } },     // 测评结果
  { path: '/waiting', component: Waiting, meta: { auth: true } },   // 等待开始
  { path: '/completed', component: Completed, meta: { auth: true } },// 已结束
  { path: '/admin', component: AdminLogin },          // 管理员登录
  { path: '/admin/dashboard', component: AdminDashboard, meta: { admin: true } },
]
```

### 12.2 登录后路由守卫逻辑

```javascript
router.beforeEach(async (to, from) => {
  if (to.meta.auth && !store.token) {
    return '/login'
  }
  if (to.path === '/chat') {
    const status = await api.getStudyStatus()
    if (status.phase === 'not_started') return '/waiting'
    if (status.phase === 'completed') return '/completed'
    if (status.need_assessment) return '/assessment'
  }
})
```

### 12.3 核心组件列表

| 组件 | 说明 |
|------|------|
| ChatBubble.vue | 聊天气泡（区分用户/助手、不同消息类型） |
| WordCard.vue | 单词卡片展示（法语 + 中文释义） |
| AudioPlayer.vue | 音频播放组件（播放/暂停按钮 + 进度条） |
| AudioRecorder.vue | 录音组件（请求麦克风权限、录音、上传） |
| MessageList.vue | 消息列表（滚动、日期分隔线、自动滚动到底部） |
| AssessmentQuestion.vue | 测评单题组件（展示单词 + 4选项） |

### 12.4 前端状态管理

```javascript
// stores/user.js (Pinia)
export const useUserStore = defineStore('user', {
  state: () => ({
    token: localStorage.getItem('token') || '',
    userId: null,
    nickname: '',
    avatarType: '',  // "human" | "robot"
  }),
  actions: {
    setLogin(data) { ... },
    logout() { ... },
  }
})

// stores/study.js (Pinia)
export const useStudyStore = defineStore('study', {
  state: () => ({
    studyDay: 0,
    phase: 'not_started',
    materialSentToday: false,
    remainingRounds: 20,
    chatMessages: [],
    needAssessment: false,
  }),
  actions: {
    async fetchStatus() { ... },
    async loadHistory() { ... },
    appendMessage(msg) { ... },
  }
})
```

---

## 十三、后端定时任务

使用 APScheduler（BackgroundScheduler）。

### 13.1 每小时通知任务

```python
@scheduler.scheduled_job('cron', minute=0)
def send_scheduled_notifications():
    current_hour = datetime.now().hour
    if current_hour < 6:
        return
    
    study_day = get_study_day()
    if study_day <= 0 or study_day > 10:
        return  # 不在学习周期内，不发通知
    
    time_slot = f"{current_hour:02d}:00"
    users = User.query.filter_by(study_time_slot=time_slot).all()
    
    for user in users:
        if user.wechat_openid:
            send_wechat_notification(user)
        elif user.email:
            send_email_notification(user)
```

### 13.2 access_token刷新任务

```python
@scheduler.scheduled_job('interval', minutes=100)
def refresh_wechat_tokens():
    # 刷新所有测试号的access_token并缓存
    for account in wechat_accounts:
        token = fetch_access_token(account.app_id, account.app_secret)
        token_cache[account.index] = token
```

---

## 十四、部署架构

```
用户浏览器 ──HTTP──→ 阿里云ECS (公网IP:80)
                          │
                        Nginx
                      ┌───┴───┐
                      │       │
              静态文件  │   API反向代理
        /  → Vue dist/ │   /api/* → 127.0.0.1:5000
                       │   /wechat/* → 127.0.0.1:5000
                       │   /static/audio/* → 直接serve
                       │
                   Gunicorn + Gevent
                   (4 workers)
                       │
                   Flask App
                       │
              ┌────────┼────────┐
              │        │        │
           SQLite   硅基流动API  微信API
```

### Nginx配置要点

```nginx
server {
    listen 80;
    server_name _;
    client_max_body_size 10M;  # 允许上传音频

    # 前端静态文件
    location / {
        root /path/to/frontend/dist;
        try_files $uri $uri/ /index.html;  # Vue SPA路由
    }

    # 后端API
    location /api/ {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # 微信回调
    location /wechat/ {
        proxy_pass http://127.0.0.1:5000;
    }

    # 音频静态文件
    location /static/audio/ {
        alias /path/to/backend/static/audio/;
    }
    
    # 用户上传的录音（如果需要前端回放）
    location /uploads/ {
        alias /path/to/backend/uploads/;
    }
}
```

### Gunicorn配置

```python
# gunicorn_config.py
bind = "127.0.0.1:5000"
workers = 4
worker_class = "gevent"
timeout = 120  # LLM调用可能较慢
```

---

## 十五、管理后台

### 15.1 页面功能

**仪表盘**：
- 各组注册人数统计（A/B/C × human/robot）
- 今日活跃用户数
- 各组完成测评人数
- 当前学习天数

**用户列表**：
- 表格展示所有用户（ID、昵称、手机号、组别、头像类型、是否绑定微信、注册时间）
- 支持按组别筛选

**数据导出**：
- 四个导出按钮（聊天记录/每日数据/测评成绩/音频清单），点击下载CSV

**系统配置**：
- 学习开始日期设置
- 分组槽位容量调整

### 15.2 管理员认证

- 管理员账号密码在后端 config.py 中配置（或环境变量）
- 登录后返回独立的 admin_token
- 管理后台API通过 admin_token 认证

---

## 十六、项目目录结构

```
french-study-platform/
├── frontend/                          # Vue 3 前端项目
│   ├── public/
│   │   ├── avatars/
│   │   │   ├── human.png            # 类人头像（需设计/提供）
│   │   │   └── robot.png            # 机器人头像（需设计/提供）
│   │   └── favicon.ico
│   ├── src/
│   │   ├── api/
│   │   │   └── index.js             # axios封装，所有API请求
│   │   ├── components/
│   │   │   ├── ChatBubble.vue
│   │   │   ├── WordCard.vue
│   │   │   ├── AudioPlayer.vue
│   │   │   ├── AudioRecorder.vue
│   │   │   ├── MessageList.vue
│   │   │   └── AssessmentQuestion.vue
│   │   ├── views/
│   │   │   ├── Home.vue
│   │   │   ├── Register.vue
│   │   │   ├── BindWeChat.vue
│   │   │   ├── Agreement.vue
│   │   │   ├── RegisterDone.vue
│   │   │   ├── Login.vue
│   │   │   ├── Chat.vue              # 核心聊天页面
│   │   │   ├── Assessment.vue
│   │   │   ├── Result.vue
│   │   │   ├── Waiting.vue
│   │   │   ├── Completed.vue
│   │   │   └── admin/
│   │   │       ├── AdminLogin.vue
│   │   │       └── Dashboard.vue
│   │   ├── stores/
│   │   │   ├── user.js
│   │   │   └── study.js
│   │   ├── router/
│   │   │   └── index.js
│   │   ├── utils/
│   │   │   ├── audio.js              # 麦克风录音工具函数
│   │   │   └── request.js            # axios实例配置
│   │   ├── App.vue
│   │   └── main.js
│   ├── package.json
│   └── vite.config.js
│
├── backend/
│   ├── app.py                        # Flask应用入口 + APScheduler初始化
│   ├── config.py                     # 所有配置项
│   ├── models.py                     # SQLAlchemy数据库模型
│   ├── extensions.py                 # db、jwt等扩展实例
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py                   # /api/register, /api/login, /api/user/profile
│   │   ├── wechat.py                 # /api/get_bind_qrcode, /api/bindcheck, /wechat/callback
│   │   ├── study.py                  # /api/study/status, /api/study/enter, /api/study/words
│   │   ├── chat.py                   # /api/chat/send, /api/chat/upload_audio, /api/chat/history
│   │   ├── assessment.py             # /api/assessment/*
│   │   └── admin.py                  # /api/admin/*
│   ├── services/
│   │   ├── __init__.py
│   │   ├── llm_service.py            # 硅基流动API调用 + prompt构建 + 响应解析
│   │   ├── wechat_service.py         # 微信API封装（access_token管理、模板消息发送、二维码生成）
│   │   ├── email_service.py          # 邮件发送
│   │   ├── audio_service.py          # 音频有效性检测 + 发音评分（可选）
│   │   ├── notification_service.py   # 定时通知任务
│   │   └── group_service.py          # 分组分配逻辑
│   ├── prompts/
│   │   └── system_prompt.py          # 系统prompt模板
│   ├── data/
│   │   └── words.json                # 每日单词配置
│   ├── static/
│   │   └── audio/                    # 法语发音音频文件（按day分目录）
│   ├── uploads/                      # 用户录音存储目录（运行时创建）
│   ├── requirements.txt
│   └── gunicorn_config.py
│
├── nginx.conf                        # Nginx配置文件
├── deploy.sh                         # 部署脚本
└── README.md                         # 项目说明与部署指南
```

---

## 十七、配置文件详细内容

### 17.1 后端 config.py

```python
import os
from datetime import timedelta

class Config:
    # Flask
    SECRET_KEY = os.environ.get('SECRET_KEY', 'change-this-to-a-random-string')
    
    # 数据库
    SQLALCHEMY_DATABASE_URI = 'sqlite:///french_study.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-change-this')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=30)
    
    # 硅基流动 LLM API
    LLM_API_URL = "https://api.siliconflow.cn/v1/chat/completions"
    LLM_API_KEY = os.environ.get('LLM_API_KEY', '')
    LLM_MODEL = "deepseek-ai/DeepSeek-V2.5"  # 按硅基流动实际可用模型选择
    
    # 微信测试号（支持两个）
    WECHAT_ACCOUNTS = [
        {
            "app_id": os.environ.get('WECHAT_APP_ID_1', ''),
            "app_secret": os.environ.get('WECHAT_APP_SECRET_1', ''),
            "token": os.environ.get('WECHAT_TOKEN_1', 'fayuxiaozhushou1'),
            "template_id": os.environ.get('WECHAT_TEMPLATE_ID_1', ''),
        },
        {
            "app_id": os.environ.get('WECHAT_APP_ID_2', ''),
            "app_secret": os.environ.get('WECHAT_APP_SECRET_2', ''),
            "token": os.environ.get('WECHAT_TOKEN_2', 'fayuxiaozhushou2'),
            "template_id": os.environ.get('WECHAT_TEMPLATE_ID_2', ''),
        },
    ]
    
    # 邮件
    SMTP_SERVER = os.environ.get('SMTP_SERVER', 'smtp.qq.com')
    SMTP_PORT = int(os.environ.get('SMTP_PORT', 465))
    SMTP_USER = os.environ.get('SMTP_USER', '')
    SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD', '')  # QQ邮箱需使用授权码
    
    # 学习配置
    STUDY_START_DATE = '2026-04-07'
    MAX_DAILY_ROUNDS = 20
    REENTER_THRESHOLD_MINUTES = 5
    
    # 文件路径
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
    AUDIO_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'audio')
    
    # 管理员
    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin123change')
    
    # 分组配置
    GROUP_SLOTS = {
        'low': {'human': 30, 'robot': 30},
        'adjustable': {'human': 30, 'robot': 30},
        'high': {'human': 30, 'robot': 30},
    }
```

### 17.2 requirements.txt

```
flask==3.1.*
flask-cors==5.*
flask-sqlalchemy==3.*
flask-jwt-extended==4.*
flask-limiter==3.*
gunicorn==22.*
gevent==24.*
requests==2.*
APScheduler==3.*
pydub==0.25.*
PyJWT==2.*
python-dotenv==1.*
httpx==0.27.*
Werkzeug==3.*
```

---

## 十八、开发阶段规划（1周）

### Day 1-2：基础框架 + 核心聊天
- [ ] 前端Vue项目初始化 + 路由 + 状态管理
- [ ] 后端Flask项目初始化 + 数据库模型 + 数据库建表
- [ ] 注册/登录接口 + 前端页面
- [ ] 分组分配逻辑
- [ ] 聊天界面UI（消息列表 + 输入框 + 发送）
- [ ] LLM API对接（硅基流动调用封装 + 系统prompt + JSON解析）
- [ ] /api/chat/send 完整流程（含意图处理）

### Day 3-4：学习流程 + 音频 + 通知
- [ ] 每日单词推送逻辑（三组差异化流程）
- [ ] 单词卡片和音频播放组件
- [ ] /api/study/enter 接口（B/C组自动消息）
- [ ] 页面可见性检测（重新进入逻辑）
- [ ] 录音功能（AudioRecorder组件 + 上传接口）
- [ ] 音频有效性检测
- [ ] 微信绑定流程（二维码生成 + 回调 + 轮询）
- [ ] 邮件通知功能
- [ ] APScheduler定时通知任务

### Day 5：测评 + 管理后台
- [ ] 测评页面（15题词义选择）
- [ ] 测评提交 + 计分
- [ ] 管理后台登录 + 仪表盘
- [ ] 数据导出CSV接口

### Day 6：集成测试 + 修复
- [ ] 完整流程走通测试（注册→绑定→等待→学习Day1-5→测评→Day6-10→结束）
- [ ] 三组行为差异验证
- [ ] 响应式适配检查（手机端+PC端）
- [ ] Bug修复

### Day 7：部署 + 压测
- [ ] 阿里云服务器环境配置（Nginx + Python + Node.js）
- [ ] 前端build + 后端gunicorn部署
- [ ] 微信回调URL配置与验证
- [ ] 简单压力测试（模拟并发请求）
- [ ] 上传音频文件、配置单词数据
- [ ] 最终检查

---

## 十九、风险与注意事项

1. **2核2G服务器资源有限**：SQLite + gunicorn(4 workers) + 定时任务已经是基本负载。不建议在同一服务器上跑Whisper模型。发音评分建议使用第三方API或直接放弃。

2. **微信测试号限制**：每个测试号最多100人关注。200人实验需要两个测试号。需提前测试模板消息功能是否可用。

3. **LLM返回不稳定**：必须做JSON解析容错。建议在prompt中反复强调JSON格式要求，并在后端做多层解析兜底。

4. **浏览器录音兼容性**：MediaRecorder API在iOS Safari上有限制（需要iOS 14.3+）。建议优先测试目标用户群体最常用的浏览器。录音格式可能为webm（Chrome）或mp4（Safari），后端pydub需安装ffmpeg来处理多种格式。

5. **公网IP直连无HTTPS**：微信模板消息中的跳转URL可以是HTTP。但浏览器的麦克风权限在非HTTPS环境下可能被限制（Chrome要求HTTPS或localhost）。解决方案：申请免费SSL证书（如Let's Encrypt），或使用IP证书。如果实在无法配置HTTPS，需引导用户使用特定浏览器设置。**这是一个关键风险点，需优先解决。**

6. **SQLite并发写入**：200用户同时写入可能偶发锁定错误。确保使用WAL模式（`PRAGMA journal_mode=WAL`），并在代码中设置合理的busy_timeout。

7. **硅基流动API的速率限制和费用**：200用户 × 每天最多20轮 = 每天最多4000次API调用。需确认硅基流动的免费/付费额度是否足够。

8. **未认证APK安装（如果后续需要APP）**：当前方案已改为Web应用，不存在此问题。

9. **邮件可能进垃圾箱**：使用个人邮箱SMTP发送的通知邮件可能被归为垃圾邮件。建议邮件主题和内容尽量正式，减少垃圾邮件特征词。

10. **HTTPS与麦克风权限的补充说明**：如果无法配置HTTPS，可考虑：(a) 使用阿里云免费证书 + 临时域名；(b) 让用户在浏览器设置中手动允许HTTP站点使用麦克风（不推荐，操作复杂）；(c) 录音功能降级为文件上传（用户在手机录音APP中录制后上传文件）。
