import random
from models import GroupSlot, User

def assign_group(db):
    """为新用户分配组别，优先分配到当前人数最少的组（事务保护）"""
    slots = GroupSlot.query.all()
    if not slots:
        raise Exception("分组槽位未初始化")

    # 找出当前人数最少的组
    min_count = min(s.current_count for s in slots)
    candidates = [s for s in slots if s.current_count == min_count]

    # 从最少人的组中随机选一个
    chosen = random.choice(candidates)
    chosen.current_count += 1
    # 注意：不在这里 commit，调用方负责统一事务

    return chosen.group_type, chosen.avatar_type

def check_slot_balance():
    """检查分组槽位状态"""
    slots = GroupSlot.query.all()
    return [{'group_type': s.group_type, 'avatar_type': s.avatar_type, 'current': s.current_count, 'max': s.max_count} for s in slots]
