from db_helper import get_all_tasks, get_tasks_types_cps_stats, get_tasks_by_type, get_tasks_task_status, get_tasks_reward_status, get_tasks_by_type_order_cps, get_tasks_by_type_count, get_cps_stats, get_tasks_cps_than

# 封装打印函数
def show_task(task):
    print(
        f"ID: {task['task_id']} | "
        f"任务名称: {task['task_name']} | "
        f"奖励: {task['reward_cps']} CPS | "
        f"类型: {task['task_type']} | "
        f"优先级: {task['priority']} | "
        f"截止日期: {task['due_date']} | "
        f"任务状态: {task['task_status']} | "
        f"奖励状态: {task['reward_status']}"
    )
# 封装：遍历+展示任务
def show_tasks(tasks):
    for task in tasks:
        show_task(task)

# 展示所有任务
def show_all_tasks(cursor):
    tasks = get_all_tasks(cursor)
    print("===== 所有的任务 =====")
    for task in tasks:
      show_task(task)

# 展示每种任务的的数量和总 CPS情况
def show_type_cps_stats(cursor):
    type_cps_stats = get_tasks_types_cps_stats(cursor)
    print("===== 每种任务的 数量 和 合计CPS 如下 =====")
    for row in type_cps_stats:
       print(
             f"任务类型: {row['task_type']} | "
             f"数量: {row['task_count']} | "
             f"总 CPS: {row['total_cps']} | "
             f"平均 CPS: {row['avg_cps']} | "
             f"最高 CPS: {row['max_cps']} | "
             f"最低 CPS: {row['min_cps']}"
            )    
       
# 展示指定任务类型下的任务
def show_task_by_type(cursor,task_type):
    task_types = get_tasks_by_type(cursor, task_type)
    print(f"===== 类型为 {task_type} 的任务如下 =====")
    for task in task_types:
      show_task(task)



# 展示任务状态为？的任务
def show_tasks_task_status(cursor,status):
    tasks_status = get_tasks_task_status(cursor,status)
    print(f"===== 所有任务状态为 {status} 的任务如下 =====")
    show_tasks(tasks_status)



# 展示奖励状态为？的任务
def show_tasks_reward_status(cursor,status):
    tasks_status = get_tasks_reward_status(cursor,status)
    print(f"===== 所有奖励状态为 {status} 的任务如下 =====")
    show_tasks(tasks_status)


def show_tasks_by_type_order_cps(cursor,task_type):
    tasks = get_tasks_by_type_order_cps(cursor, task_type)
    print(f"===== {task_type} 任务的详情如下(按CPS倒序排列) =====")
    show_tasks(tasks)


def show_tasks_by_type_count(cursor,task_type):
    task_by_type = get_tasks_by_type_count(cursor,task_type)
    if task_by_type is not None:
        print(f"任务类型: {task_by_type['task_type']} | 数量: {task_by_type['task_count']}")
    else:
        print("没有找到该类型任务。")

# 展示cps统计
def show_cps_stats(cursor):
    cps_stats = get_cps_stats(cursor)
    print("===== CPS 综合统计 =====")
    print(f"任务数量: {cps_stats['task_count']}")
    print(f"总 CPS: {cps_stats['total_cps']}")
    print(f"平均 CPS: {cps_stats['avg_cps']}")
    print(f"最高 CPS: {cps_stats['max_cps']}")
    print(f"最低 CPS: {cps_stats['min_cps']}")

def show_delete_task_result(is_deleted,task_id):
    if is_deleted == None:
        print(f"没有找到 ID 为 {task_id} 的任务，无法删除。")
        return

    print(f"===== 已删除 ID 为 {task_id} 的任务 =====")


# 19. 只查看总 CPS 大于 X 的任务类型
def show_tasks_cps_than(cursor, number):
    rows = get_tasks_cps_than(cursor,number)

    print(f"===== 总CPS大于 {number}  的任务类型 =====")
    for row in rows:
        print(f"任务类型: {row['task_type']} | 数量: {row['task_count']} | 总 CPS: {row['total_cps']}")

# 查看修改后的任务
def show_update_task_status(task, task_id, new_status):
    if task is None:
        print(f"没有找到 ID 为 {task_id} 的任务，未修改任何数据。")
        return

    print(f"===== 已将 ID 为 {task_id} 的任务状态修改为 {new_status}，如下所示 =====")
    show_task(task)
