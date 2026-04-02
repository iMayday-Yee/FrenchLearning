# 法语学习助手 - 数据库表结构文档

## 概述

本项目使用 SQLite 数据库，通过 SQLAlchemy ORM 进行管理。数据库文件位于 `backend/french_study.db`。

---

## 表结构

### 1. users（用户表）

存储用户基本信息。

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | Integer | PK, 自增 | 用户唯一标识 |
| phone | String(20) | UNIQUE, NOT NULL | 手机号，用于登录 |
| email | String(100) | - | 电子邮箱（可选） |
| password_hash | String(255) | NOT NULL | 密码哈希值 |
| nickname | String(50) | NOT NULL | 昵称 |
| age | Integer | NOT NULL | 年龄 |
| gender | String(10) | NOT NULL | 性别 |
| education | String(20) | NOT NULL | 学历 |
| french_interest | String(20) | NOT NULL | 学习法语的目的/兴趣 |
| french_level | String(20) | NOT NULL | 当前法语水平 |
| study_time_slot | String(10) | NOT NULL | 偏好的学习时间段 |
| group_type | String(20) | NOT NULL | 分组类型：low / adjustable / high |
| avatar_type | String(10) | NOT NULL | 头像类型：human / robot |
| wechat_openid | String(100) | - | 微信 OpenID（绑定后填充） |
| wechat_account_index | Integer | DEFAULT 0 | 微信账号索引（用于区分多账号） |
| created_at | DateTime | DEFAULT utcnow | 注册时间 |

**索引**：`phone` 字段有唯一索引

---

### 2. daily_status（每日学习状态表）

记录用户每天的学习进度和统计。

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | Integer | PK, 自增 | 记录唯一标识 |
| user_id | Integer | FK(users.id), NOT NULL | 关联的用户ID |
| study_day | Integer | NOT NULL | 学习天数（1-10） |
| date | Date | NOT NULL | 学习日期 |
| material_sent | Boolean | DEFAULT False | 当天是否已发送学习材料 |
| rejected | Boolean | DEFAULT False | 用户是否拒绝了学习 |
| practice_count | Integer | DEFAULT 0 | 有效跟读练习次数 |
| invalid_audio_count | Integer | DEFAULT 0 | 无效录音次数（空白/无声） |
| conversation_rounds | Integer | DEFAULT 0 | 对话轮次（每发送一次消息/录音 +1） |

**唯一约束**：`user_id` + `study_day` 组合唯一

**索引**：`idx_user_study_day(user_id, study_day)`

---

### 3. chat_messages（聊天消息表）

存储所有对话记录。

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | Integer | PK, 自增 | 消息唯一标识 |
| user_id | Integer | FK(users.id), NOT NULL | 发送用户ID |
| study_day | Integer | NOT NULL | 所属学习天数 |
| role | String(10) | NOT NULL | 角色：user / assistant |
| content_type | String(20) | NOT NULL | 消息类型：text / word_card / audio / user_audio / word_audio / thinking / system |
| content | Text | NOT NULL | 消息内容（文本或JSON字符串） |
| is_template | Boolean | DEFAULT False | 是否为模板消息 |
| timestamp | DateTime | DEFAULT utcnow | 发送时间 |

**索引**：`idx_user_study_day(user_id, study_day)`

**content_type 说明**：
- `text`：普通文本消息
- `word_card`：单词卡片（旧版，已被 word_audio 替代）
- `audio`：音频消息（范例发音）
- `user_audio`：用户录音消息
- `word_audio`：组合消息类型（单词+音频+录音按钮），包含 JSON：`{"french", "chinese", "audio_url", "word_index"}`
- `thinking`：思考中状态提示
- `system`：系统消息

---

### 4. audio_records（录音记录表）

存储用户跟读录音文件信息。

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | Integer | PK, 自增 | 记录唯一标识 |
| user_id | Integer | FK(users.id), NOT NULL | 关联的用户ID |
| study_day | Integer | NOT NULL | 录音所属学习天数 |
| word_index | Integer | - | 对应的单词索引（0, 1, 2） |
| target_word | String(50) | - | 目标单词 |
| audio_path | String(255) | NOT NULL | 录音文件存储路径 |
| is_valid | Boolean | DEFAULT False | 录音是否有效（非空白/无声） |
| score | Float | - | 评分（预留字段） |
| created_at | DateTime | DEFAULT utcnow | 创建时间 |

**文件存储路径格式**：`uploads/{user_id}/{study_day}/{word_index}_{timestamp}.webm`

---

### 5. assessment_answers（评估答案表）

存储第5天和第10天测评的答题记录。

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | Integer | PK, 自增 | 记录唯一标识 |
| user_id | Integer | FK(users.id), NOT NULL | 关联的用户ID |
| word_french | String(50) | NOT NULL | 法语单词 |
| correct_chinese | String(50) | NOT NULL | 正确中文含义 |
| user_choice | String(50) | NOT NULL | 用户选择的中文 |
| is_correct | Boolean | NOT NULL | 是否回答正确 |
| pronunciation_score | Float | - | 发音评分（预留字段） |
| created_at | DateTime | DEFAULT utcnow | 答题时间 |

---

### 6. assessment_summary（评估汇总表）

存储用户测评总分。

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | Integer | PK, 自增 | 记录唯一标识 |
| user_id | Integer | FK(users.id), UNIQUE, NOT NULL | 关联的用户ID |
| vocab_score | Float | NOT NULL | 词汇得分 |
| pronunciation_avg | Float | - | 平均发音分 |
| total_score | Float | NOT NULL | 总分 |
| created_at | DateTime | DEFAULT utcnow | 评测时间 |

---

### 7. system_config（系统配置表）

存储系统级配置参数。

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| key | String(50) | PK | 配置项名称 |
| value | Text | NOT NULL | 配置值 |

**现有配置项**：

| key | value 示例 | 说明 |
|-----|-----------|------|
| study_start_date | 2026-04-02 | 学习开始日期 |
| max_daily_rounds | 20 | 每日最大对话轮次 |
| reenter_threshold_minutes | 5 | 重新进入聊天的阈值（分钟） |

---

### 8. group_slots（分组槽位表）

管理不同分组和头像类型的用户槽位。

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | Integer | PK, 自增 | 记录唯一标识 |
| group_type | String(20) | NOT NULL | 分组类型：low / adjustable / high |
| avatar_type | String(10) | NOT NULL | 头像类型：human / robot |
| max_count | Integer | NOT NULL | 最大槽位数 |
| current_count | Integer | DEFAULT 0 | 当前已占用槽位 |

**唯一约束**：`group_type` + `avatar_type` 组合唯一

**默认配置**（3组 x 2种头像 = 6条记录）：
- low/human: 30槽
- low/robot: 30槽
- adjustable/human: 30槽
- adjustable/robot: 30槽
- high/human: 30槽
- high/robot: 30槽

---

## 表关系图

```
users (1) ─────< daily_status (N)
    │
    ├────< chat_messages (N)
    │
    ├────< audio_records (N)
    │
    └────< assessment_answers (N)
            │
            └──── assessment_summary (1)
```

---

## 常用查询示例

### 查询用户某天的学习状态
```sql
SELECT * FROM daily_status WHERE user_id = ? AND study_day = ?;
```

### 查询用户某天的所有对话
```sql
SELECT * FROM chat_messages WHERE user_id = ? AND study_day = ? ORDER BY timestamp;
```

### 查询用户的所有录音
```sql
SELECT * FROM audio_records WHERE user_id = ? ORDER BY created_at DESC;
```

### 查询某分组剩余槽位
```sql
SELECT (max_count - current_count) AS remaining FROM group_slots WHERE group_type = 'high' AND avatar_type = 'human';
```

---

## 注意事项

1. **数据清理**：目前没有实现自动数据清理机制，长时间运行后数据量会持续增长
2. **录音文件**：数据库只存储文件路径，录音文件实际存储在 `uploads/` 目录下
3. **并发安全**：SQLite 在高并发写入时可能有锁等待问题，当前实现为简单场景设计
4. **评分字段**：`score` 和 `pronunciation_score` 字段目前预留，暂无实际功能
