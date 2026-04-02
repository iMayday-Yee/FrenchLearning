import random
from models import GroupSlot, User

def assign_group(db):
    """为新用户分配组别，保证组别平衡"""
    available_slots = GroupSlot.query.filter(GroupSlot.current_count < GroupSlot.max_count).all()
    if not available_slots:
        raise Exception("所有分组槽位已满")

    chosen = random.choice(available_slots)
    chosen.current_count += 1
    db.session.commit()

    return chosen.group_type, chosen.avatar_type

def check_slot_balance():
    """检查分组槽位状态"""
    slots = GroupSlot.query.all()
    return [{'group_type': s.group_type, 'avatar_type': s.avatar_type, 'current': s.current_count, 'max': s.max_count} for s in slots]
