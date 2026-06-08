import sqlite3
import logging
from config import TASK_DB_FILE, TASK_PRIORITIES, DEFAULT_TASK_PRIORITY, DEFAULT_DUE_DATE
from task_helpers import is_valid_due_date, is_valid_due_date_range
from datetime import date, timedelta


def get_connection():
    connection = sqlite3.connect(TASK_DB_FILE)
    connection.row_factory = sqlite3.Row
    return connection


def create_tasks_table():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        task_id INTEGER PRIMARY KEY,
        task_name TEXT NOT NULL,
        reward_cps INTEGER NOT NULL,
        task_type TEXT NOT NULL,
        priority TEXT NOT NULL,
        due_date TEXT,
        task_status TEXT NOT NULL,
        reward_status TEXT NOT NULL
    )
    """)

    connection.commit()
    connection.close()


def row_to_task(row):
    return {
        "task_id": row["task_id"],
        "task_name": row["task_name"],
        "reward_cps": row["reward_cps"],
        "task_type": row["task_type"],
        "priority": row["priority"],
        "due_date": row["due_date"],
        "task_status": row["task_status"],
        "reward_status": row["reward_status"],
    }

def load_tasks_from_db():
    create_tasks_table()

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    SELECT 
        task_id,
        task_name,
        reward_cps,
        task_type,
        priority,
        due_date,
        task_status,
        reward_status
    FROM tasks
    ORDER BY task_id ASC
    """)

    rows = cursor.fetchall()
    connection.close()

    tasks = []

    for row in rows:
        tasks.append(row_to_task(row))

    logging.info(f"任务数据从 SQLite 读取成功，共 {len(tasks)} 条任务")
    return tasks


def load_tasks_from_json():
    return load_tasks_from_db()


def save_tasks_to_db(tasks):
    create_tasks_table()

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM tasks")

    for task in tasks:
        cursor.execute("""
        INSERT INTO tasks (
            task_id,
            task_name,
            reward_cps,
            task_type,
            priority,
            due_date,
            task_status,
            reward_status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            task["task_id"],
            task["task_name"],
            task["reward_cps"],
            task["task_type"],
            task["priority"],
            task["due_date"],
            task["task_status"],
            task["reward_status"],
        ))

    connection.commit()
    connection.close()

    logging.info(f"任务数据保存到 SQLite 成功，共 {len(tasks)} 条任务")


def save_tasks_to_json(tasks):
    save_tasks_to_db(tasks)

def insert_task_to_db(task):
    create_tasks_table()

    connection = get_connection()
    cursor = connection.cursor()

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
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        task["task_name"],
        task["reward_cps"],
        task["task_type"],
        task["priority"],
        task["due_date"],
        task["task_status"],
        task["reward_status"],
    ))

    new_task_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return new_task_id


# 获取指定id的任务
def get_tasks_by_type_from_db(task_type):
    create_tasks_table()

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    SELECT
        task_id,
        task_name,
        reward_cps,
        task_type,
        priority,
        due_date,
        task_status,
        reward_status
    FROM tasks
    WHERE task_type = ?
    ORDER BY task_id ASC
    """, (task_type,))

    rows = cursor.fetchall()
    connection.close()

    tasks = []

    for row in rows:
        tasks.append(row_to_task(row))

    return tasks



# 筛选优先级 查看任务
def get_tasks_by_priority_from_db(selected_priority):
    create_tasks_table()

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
          task_id,
          task_name,
          reward_cps,
          task_type,
          priority,
          due_date,
          task_status,
          reward_status
        FROM tasks
        WHERE priority = ?
        ORDER BY task_id ASC
        """,
        (selected_priority,))
    
    rows = cursor.fetchall()
    connection.close()

    tasks = []

    for row in rows:
        tasks.append(row_to_task(row))
    return tasks

# 按任务完成状态筛选
def get_tasks_by_status_from_db(selected_status):
    create_tasks_table()

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
          task_id,
          task_name,
          reward_cps,
          task_type,
          priority,
          due_date,
          task_status,
          reward_status
        FROM tasks
        WHERE task_status = ?
        ORDER BY task_id ASC
        """,
        (selected_status,))
    
    rows = cursor.fetchall()
    connection.close()

    tasks = []

    for row in rows:
        tasks.append(row_to_task(row))
    return tasks


# 按奖励完成状态筛选
def get_tasks_by_reward_status_from_db(selected_status):
    create_tasks_table()

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
          task_id,
          task_name,
          reward_cps,
          task_type,
          priority,
          due_date,
          task_status,
          reward_status
        FROM tasks
        WHERE reward_status = ?
        ORDER BY task_id ASC
        """,
        (selected_status,))
    
    rows = cursor.fetchall()
    connection.close()

    tasks = []

    for row in rows:
        tasks.append(row_to_task(row))
    return tasks


# 按时期筛选
def get_tasks_by_due_date_from_db(due_date_query):
    create_tasks_table()

    connection = get_connection()
    cursor = connection.cursor()

    if is_valid_due_date(due_date_query):
        cursor.execute("""
        SELECT
            task_id,
            task_name,
            reward_cps,
            task_type,
            priority,
            due_date,
            task_status,
            reward_status
        FROM tasks
        WHERE due_date = ?
        ORDER BY task_id ASC
        """, (due_date_query,))

    elif is_valid_due_date_range(due_date_query):
        date_parts = due_date_query.split("&")
        start_date = date_parts[0]
        end_date = date_parts[1]

        cursor.execute("""
        SELECT
            task_id,
            task_name,
            reward_cps,
            task_type,
            priority,
            due_date,
            task_status,
            reward_status
        FROM tasks
        WHERE due_date BETWEEN ? AND ?
        ORDER BY due_date ASC, task_id ASC
        """, (start_date, end_date))

    else:
        connection.close()
        return []

    rows = cursor.fetchall()
    connection.close()

    tasks = []

    for row in rows:
        tasks.append(row_to_task(row))

    return tasks



# 修改状态
def update_task_status_in_db(task_id, new_status):
    create_tasks_table()

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    UPDATE tasks
    SET task_status = ?
    WHERE task_id = ?
    """, (new_status, task_id))

    affected_rows = cursor.rowcount

    connection.commit()
    connection.close()

    return affected_rows > 0

# 修改任务状态
def update_reward_status_in_db(task_id, new_status):
    create_tasks_table()

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    UPDATE tasks
    SET reward_status = ?
    WHERE task_id = ?
    """, (new_status, task_id))

    affected_rows = cursor.rowcount

    connection.commit()
    connection.close()

    return affected_rows > 0


# 查询已过期任务
def get_overdue_tasks_from_db(today_text=None):
    create_tasks_table()

    if today_text is None:
        today_text = date.today().isoformat()

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    SELECT
        task_id,
        task_name,
        reward_cps,
        task_type,
        priority,
        due_date,
        task_status,
        reward_status
    FROM tasks
    WHERE due_date IS NOT NULL
      AND due_date < ?
    ORDER BY due_date ASC, task_id ASC
    """, (today_text,))

    rows = cursor.fetchall()
    connection.close()

    tasks = []

    for row in rows:
        tasks.append(row_to_task(row))

    return tasks


# 删除任务
def delete_task_from_db(task_id):
    create_tasks_table()

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    DELETE FROM tasks
    WHERE task_id = ?
    """, (task_id,))

    affected_rows = cursor.rowcount

    connection.commit()
    connection.close()

    return affected_rows > 0

# 查询未来指定天数内到期任务
def get_tasks_due_within_days_from_db(days=7, today_text=None):
    create_tasks_table()

    if today_text is None:
        today_date = date.today()
    else:
        today_date = date.fromisoformat(today_text)

    end_date = today_date + timedelta(days=days)

    start_text = today_date.isoformat()
    end_text = end_date.isoformat()

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    SELECT
        task_id,
        task_name,
        reward_cps,
        task_type,
        priority,
        due_date,
        task_status,
        reward_status
    FROM tasks
    WHERE due_date IS NOT NULL
      AND due_date BETWEEN ? AND ?
    ORDER BY due_date ASC, task_id ASC
    """, (start_text, end_text))

    rows = cursor.fetchall()
    connection.close()

    tasks = []

    for row in rows:
        tasks.append(row_to_task(row))

    return tasks


# 高级筛选
def get_tasks_advanced_from_db(
    task_type=None,
    task_status=None,
    reward_status=None,
    start_date=None,
    end_date=None,
    sort_option="不排序"
):
    create_tasks_table()

    connection = get_connection()
    cursor = connection.cursor()

    sql = """
    SELECT
        task_id,
        task_name,
        reward_cps,
        task_type,
        priority,
        due_date,
        task_status,
        reward_status
    FROM tasks
    """

    where_clauses = []
    params = []

    if task_type is not None:
        where_clauses.append("task_type = ?")
        params.append(task_type)

    if task_status is not None:
        where_clauses.append("task_status = ?")
        params.append(task_status)

    if reward_status is not None:
        where_clauses.append("reward_status = ?")
        params.append(reward_status)

    if start_date is not None and end_date is not None:
        where_clauses.append("due_date IS NOT NULL")
        where_clauses.append("due_date BETWEEN ? AND ?")
        params.append(start_date)
        params.append(end_date)

    if len(where_clauses) > 0:
        sql = sql + " WHERE " + " AND ".join(where_clauses)

    if sort_option == "按截止日期从近到远":
        sql = sql + " ORDER BY due_date IS NULL ASC, due_date ASC, task_id ASC"

    elif sort_option == "按截止日期从远到近":
        sql = sql + " ORDER BY due_date IS NULL ASC, due_date DESC, task_id ASC"

    elif sort_option == "按 CPS 奖励从高到低":
        sql = sql + " ORDER BY reward_cps DESC, task_id ASC"

    elif sort_option == "按 CPS 奖励从低到高":
        sql = sql + " ORDER BY reward_cps ASC, task_id ASC"

    elif sort_option == "按优先级排序 high > medium > low":
        sql = sql + """
        ORDER BY
            CASE priority
                WHEN 'high' THEN 1
                WHEN 'medium' THEN 2
                WHEN 'low' THEN 3
                ELSE 99
            END,
            task_id ASC
        """

    else:
        sql = sql + " ORDER BY task_id ASC"

    cursor.execute(sql, tuple(params))

    rows = cursor.fetchall()
    connection.close()

    tasks = []

    for row in rows:
        tasks.append(row_to_task(row))

    return tasks


# 任务统计
def get_task_stats_from_db():
    create_tasks_table()

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    SELECT
        COUNT(*) AS total_tasks,

        SUM(
            CASE
                WHEN task_status = '已完成' THEN 1
                ELSE 0
            END
        ) AS completed_tasks,

        SUM(
            CASE
                WHEN task_status = '未完成' THEN 1
                ELSE 0
            END
        ) AS unfinished_tasks,

        COALESCE(SUM(reward_cps), 0) AS total_cps,

        COALESCE(SUM(
            CASE
                WHEN task_status = '已完成' AND reward_status = '已领取'
                THEN reward_cps
                ELSE 0
            END
        ), 0) AS completed_cps,

        COALESCE(SUM(
            CASE
                WHEN task_status = '已完成' AND reward_status = '未领取'
                THEN reward_cps
                ELSE 0
            END
        ), 0) AS unclaim_cps,

        COALESCE(SUM(
            CASE
                WHEN task_status = '未完成'
                THEN reward_cps
                ELSE 0
            END
        ), 0) AS unfinished_cps

    FROM tasks
    """)

    row = cursor.fetchone()
    connection.close()

    return {
        "total_tasks": row["total_tasks"],
        "completed_tasks": row["completed_tasks"] or 0,
        "unfinished_tasks": row["unfinished_tasks"] or 0,
        "total_cps": row["total_cps"] or 0,
        "completed_cps": row["completed_cps"] or 0,
        "unclaim_cps": row["unclaim_cps"] or 0,
        "unfinished_cps": row["unfinished_cps"] or 0,
    }

def get_task_stats_by_type_from_db(task_type):
    create_tasks_table()

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    SELECT
        COUNT(*) AS total_tasks,

        SUM(
            CASE
                WHEN task_status = '已完成' THEN 1
                ELSE 0
            END
        ) AS completed_tasks,

        SUM(
            CASE
                WHEN task_status = '未完成' THEN 1
                ELSE 0
            END
        ) AS unfinished_tasks,

        COALESCE(SUM(reward_cps), 0) AS total_cps,

        COALESCE(SUM(
            CASE
                WHEN task_status = '已完成' AND reward_status = '已领取'
                THEN reward_cps
                ELSE 0
            END
        ), 0) AS completed_cps,

        COALESCE(SUM(
            CASE
                WHEN task_status = '已完成' AND reward_status = '未领取'
                THEN reward_cps
                ELSE 0
            END
        ), 0) AS unclaim_cps,

        COALESCE(SUM(
            CASE
                WHEN task_status = '未完成'
                THEN reward_cps
                ELSE 0
            END
        ), 0) AS unfinished_cps

    FROM tasks
    WHERE task_type = ?
    """, (task_type,))

    row = cursor.fetchone()
    connection.close()

    return {
        "task_type": task_type,
        "total_tasks": row["total_tasks"] or 0,
        "completed_tasks": row["completed_tasks"] or 0,
        "unfinished_tasks": row["unfinished_tasks"] or 0,
        "total_cps": row["total_cps"] or 0,
        "completed_cps": row["completed_cps"] or 0,
        "unclaim_cps": row["unclaim_cps"] or 0,
        "unfinished_cps": row["unfinished_cps"] or 0,
    }


# 清空任务
def clear_all_tasks_in_db():
    create_tasks_table()

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM tasks")

    connection.commit()
    connection.close()

    return True




def update_task_field_in_db(task_id, field_name, new_value):
    allowed_fields = {
        "task_name",
        "reward_cps",
        "task_type",
        "priority",
        "due_date",
        "task_status",
        "reward_status",
    }
# 定义被允许修改的字段，且判断函数中调用的field_name（即用户输入想修改的）在允许的字段内，否则报错。然后再将这个变量，弄在下面set里去定位修改的key
    if field_name not in allowed_fields:
        raise ValueError(f"不允许修改的字段: {field_name}")

    create_tasks_table()

    connection = get_connection()
    cursor = connection.cursor()

    sql = f"""
    UPDATE tasks
    SET {field_name} = ?
    WHERE task_id = ?
    """

    cursor.execute(sql, (new_value, task_id))

    affected_rows = cursor.rowcount

    connection.commit()
    connection.close()

    return affected_rows > 0

def repair_task_ids(tasks_data):
    max_task_id = 0

    for task in tasks_data:
        if "task_id" in task and isinstance(task["task_id"], int) and task["task_id"] > max_task_id:
            max_task_id = task["task_id"]

    next_id = max_task_id + 1
    has_repaired = False

    for task in tasks_data:
        if "task_id" not in task or not isinstance(task["task_id"], int):
            task["task_id"] = next_id
            next_id = next_id + 1
            has_repaired = True

        if "task_name" not in task or task["task_name"] == "":
            task["task_name"] = "未命名任务"
            has_repaired = True

        if "reward_cps" not in task or not isinstance(task["reward_cps"], int):
            task["reward_cps"] = 0
            has_repaired = True

        if "task_type" not in task:
            task["task_type"] = "社交任务"
            has_repaired = True

        if "task_status" not in task:
            task["task_status"] = "未完成"
            has_repaired = True

        if "reward_status" not in task:
            task["reward_status"] = "未领取"
            has_repaired = True

        if "priority" not in task or task["priority"] not in TASK_PRIORITIES:
            task["priority"] = DEFAULT_TASK_PRIORITY
            has_repaired = True

        if "due_date" not in task or not is_valid_due_date(task["due_date"]):
            task["due_date"] = DEFAULT_DUE_DATE
            has_repaired = True

    if has_repaired:
        save_tasks_to_db(tasks_data)
