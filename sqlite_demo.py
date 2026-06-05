import sqlite3
from db_helper import create_tasks_table, reset_demo_data, insert_demo_tasks, update_task_status, delete_task_by_id
from db_views import show_all_tasks, show_task_by_type, show_tasks_task_status, show_tasks_reward_status, show_tasks_by_type_order_cps, show_type_cps_stats, show_cps_stats, show_tasks_cps_than, show_update_task_status, show_delete_task_result

def main():
    # 1. 连接 SQLite 数据库：如果 tasks.db 不存在，SQLite 会自动创建这个文件
    connection = sqlite3.connect("tasks.db")
    connection.row_factory = sqlite3.Row

    # 2. 创建 cursor：cursor 可以理解成“数据库操作员”，负责执行 SQL
    cursor = connection.cursor()

    create_tasks_table(cursor)
    reset_demo_data(cursor, connection)
    insert_demo_tasks(cursor, connection)


    show_all_tasks(cursor)
    show_task_by_type(cursor, "游戏任务")
    show_tasks_task_status(cursor, "未完成")
    show_tasks_reward_status(cursor, "未领取")
    show_tasks_by_type_order_cps(cursor, "游戏任务")
    show_type_cps_stats(cursor)
    show_cps_stats(cursor)
    show_tasks_cps_than(cursor, 200)
    updated_task = update_task_status(cursor, connection, 2, "已完成")
    show_update_task_status(updated_task, 2, "已完成")

    is_deleted = delete_task_by_id(cursor, connection, 4)
    show_delete_task_result(is_deleted, 4)



    connection.close()

if __name__ == "__main__":
    main()
