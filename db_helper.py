# 封装任务打印函数


# 3. 创建 tasks 表
def create_tasks_table(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        task_id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_name TEXT NOT NULL,
        reward_cps INTEGER NOT NULL,
        task_type TEXT NOT NULL,
        priority TEXT NOT NULL,
        due_date TEXT,
        task_status TEXT NOT NULL,
        reward_status TEXT NOT NULL
    )
    """)

# 5. 插入几条测试数据
def insert_demo_tasks(cursor, connection):
    cursor.execute("""
    INSERT INTO tasks (
        task_name,
        reward_cps,
        task_type,
        priority,
        due_date,
        task_status,
        reward_status
    )
    VALUES (
        'follow us',
        100,
        '社交任务',
        'medium',
        '2026-06-05',
        '未完成',
        '未领取'
    )
    """)

    cursor.execute("""
    INSERT INTO tasks (
        task_name,
        reward_cps,
        task_type,
        priority,
        due_date,
        task_status,
        reward_status
    )
    VALUES (
        'play game',
        300,
        '游戏任务',
        'low',
        '2026-06-10',
        '未完成',
        '未领取'
    )
    """)

    cursor.execute("""
    INSERT INTO tasks (
        task_name,
        reward_cps,
        task_type,
        priority,
        due_date,
        task_status,
        reward_status
    )
    VALUES (
        'invite friends',
        800,
        '邀请任务',
        'high',
        '2026-08-01',
        '已完成',
        '未领取'
    )
    """)

    connection.commit()



# 4. 清空旧测试数据，避免每次运行重复插入
def reset_demo_data(cursor, connection):
    cursor.execute("DELETE FROM tasks") # 负责执行删除任务
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='tasks'")# 重置自增id，防止无限扩大
    connection.commit() # 提交修改



# 7. 查询所有任务
def get_all_tasks(cursor):
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    return tasks


# 18. 统计每种任务的的数量和CPS情况
def get_tasks_types_cps_stats(cursor):
    cursor.execute("""
    SELECT 
     task_type,
      COUNT(*) AS task_count,
      SUM(reward_cps) AS total_cps,
      AVG(reward_cps) AS avg_cps,
      MAX(reward_cps) AS max_cps,
      MIN(reward_cps) AS min_cps
    FROM tasks
    GROUP BY task_type
    """)

    rows = cursor.fetchall()
    return rows

# 8. 查询指定任务类型
def get_tasks_by_type(cursor, task_type):
    cursor.execute(
        "SELECT * FROM tasks WHERE task_type = ?",
        (task_type,)
    )

    tasks = cursor.fetchall()
    return tasks

# 9. 查询任务状态为？的任务
def get_tasks_task_status(cursor,status):
    cursor.execute("""
    SELECT * 
    FROM tasks 
    WHERE task_status= ?
    """,(status,))
    tasks = cursor.fetchall()
    return tasks

# 9. 查询奖励状态为？的任务
def get_tasks_reward_status(cursor,status):
    cursor.execute("""
    SELECT * 
    FROM tasks 
    WHERE reward_status= ?
    """,(status,))
    tasks = cursor.fetchall()
    return tasks

# 10. 按类型查询任务后，再按cps倒序排列
def get_tasks_by_type_order_cps(cursor, task_type):
    cursor.execute("""
    SELECT *
    FROM tasks
    WHERE task_type = ?
    ORDER BY reward_cps DESC
    """, (task_type,))

    tasks = cursor.fetchall()
    return tasks

def get_tasks_cps_than(cursor, number):
    cursor.execute("""
    SELECT 
      task_type,
      COUNT(*) AS task_count,
      SUM(reward_cps) as total_cps
    FROM tasks
    GROUP BY task_type
    HAVING total_cps > ?
    ORDER BY total_cps DESC
    """,
        (str(number),))
    
    rows = cursor.fetchall()
    return rows

# 12. 统计单个任务类型数量
def get_tasks_by_type_count(cursor,task_type):
    cursor.execute("""
    SELECT 
        task_type, 
        COUNT(*) AS task_count
    FROM tasks
    WHERE task_type = ?
    GROUP BY task_type
    """, 
    (task_type,)
    )
    row = cursor.fetchone()
    return row

# 查询所有cps统计
def get_cps_stats(cursor):
    cursor.execute("""
    SELECT 
        COUNT(*) AS task_count,
        SUM(reward_cps) AS total_cps,
        AVG(reward_cps) AS avg_cps,
        MAX(reward_cps) AS max_cps,
        MIN(reward_cps) AS min_cps
    FROM tasks
    """)

    stats = cursor.fetchone()
    return stats

# 14. 修改任务状态
def update_task_status(cursor,connection,task_id,new_status):
    cursor.execute("""
    UPDATE tasks
    SET task_status = ?
    WHERE task_id = ?
    """, (new_status, task_id))

    connection.commit()

    if cursor.rowcount == 0:
        return None
    else:
        cursor.execute("""
        SELECT *
        FROM tasks
        WHERE task_id = ?
        """, (task_id,))

        task = cursor.fetchone()

        return task

# 15. 删除指定任务，并展示新的表
def delete_task_by_id(cursor, connection, task_id):
    cursor.execute("""
    DELETE FROM tasks
    WHERE task_id = ?
    """, (task_id,))

    connection.commit()

    if cursor.rowcount == 0:
        return None

    return task_id

