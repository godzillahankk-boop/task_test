import sqlite3

conn = sqlite3.connect('tasks.db')   # 把路径改成你文件的实际路径
cursor = conn.cursor()

# 查看所有表
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cursor.fetchall())

# 查看 tasks 表的数据
cursor.execute("SELECT * FROM tasks LIMIT 10;")
for row in cursor.fetchall():
    print(row)

conn.close()