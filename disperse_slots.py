#!/usr/bin/env python3
"""
分散过于集中的学习时间段（整点 -> XX:05~XX:30）
"""
import sqlite3
import os

DB_PATH = '/opt/FrenchLearning/backend/instance/french_study.db'


def show_distribution(cursor, title):
    print(f"\n{'='*50}")
    print(f"  {title}")
    print('='*50)
    cursor.execute("SELECT study_time_slot, COUNT(*) as cnt FROM users GROUP BY study_time_slot ORDER BY study_time_slot")
    rows = cursor.fetchall()
    total = sum(r[1] for r in rows)
    for slot, cnt in rows:
        bar = '█' * cnt
        print(f"  {slot}: {cnt:3d}人 {bar}")
    print(f"  总计: {total}人")
    print()


def main():
    if not os.path.exists(DB_PATH):
        print(f"数据库不存在: {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # 处理前分布
    show_distribution(cur, "处理前")

    # 找出整点用户
    cur.execute("SELECT id, study_time_slot FROM users WHERE study_time_slot LIKE '%:00'")
    rows = cur.fetchall()
    print(f"整点用户: {len(rows)} 人，将分散到 XX:05~XX:30\n")

    # 执行分散
    cur.execute("""
        UPDATE users SET study_time_slot =
          CASE id % 6
            WHEN 0 THEN substr(study_time_slot, 1, 3) || '05'
            WHEN 1 THEN substr(study_time_slot, 1, 3) || '10'
            WHEN 2 THEN substr(study_time_slot, 1, 3) || '15'
            WHEN 3 THEN substr(study_time_slot, 1, 3) || '20'
            WHEN 4 THEN substr(study_time_slot, 1, 3) || '25'
            WHEN 5 THEN substr(study_time_slot, 1, 3) || '30'
          END
        WHERE study_time_slot LIKE '%:00'
    """)
    conn.commit()
    print(f"已处理 {cur.rowcount} 条记录\n")

    # 处理后分布
    show_distribution(cur, "处理后")

    # 验证：还有没有整点的
    cur.execute("SELECT COUNT(*) FROM users WHERE study_time_slot LIKE '%:00'")
    remaining = cur.fetchone()[0]
    print(f"剩余整点用户: {remaining} 人 {'✅ 全部处理完毕' if remaining == 0 else '❌ 还有未处理的'}")

    conn.close()


if __name__ == '__main__':
    main()
