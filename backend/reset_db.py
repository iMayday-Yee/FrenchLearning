"""清空所有数据表内容（保留表结构），重新初始化种子数据"""
import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), 'instance', 'french_study.db')

if not os.path.exists(db_path):
    print(f'数据库不存在: {db_path}')
    exit(1)

conn = sqlite3.connect(db_path)
cur = conn.cursor()

# 获取所有表名
cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
tables = [row[0] for row in cur.fetchall()]

print(f'找到 {len(tables)} 张表: {", ".join(tables)}')
print()

for table in tables:
    cur.execute(f'SELECT COUNT(*) FROM {table}')
    count = cur.fetchone()[0]
    cur.execute(f'DELETE FROM {table}')
    print(f'  {table}: 删除 {count} 条记录')

conn.commit()
conn.close()

print('\n所有数据已清空。重启服务后会自动重新初始化种子数据（system_config、group_slots、wechat_accounts）。')
