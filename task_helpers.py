

# 封装函数：遍历所有任务的类型，返回已有类型的任务列表字典
def filter_tasks_by_type(tasks_data, selected_task_type):
    filtered_tasks = []

    for task in tasks_data:
        if task["task_type"] == selected_task_type:
            filtered_tasks.append(task)

    return filtered_tasks

# 封装函数：遍历所有任务的优先级，返回对应优先级的任务列表
def filter_tasks_by_priority(tasks_data, selected_priority):
    filtered_tasks = []

    for task in tasks_data:
        if task["priority"] == selected_priority:
            filtered_tasks.append(task)

    return filtered_tasks

# 封装函数：遍历task，找出对应id的task
def find_task_by_id(tasks_data, task_id):
    for task in tasks_data:
        if task["task_id"] == task_id:
            return task
    return None

# 遍历tasks_data，找到对应id任务的下标index
def find_task_index_by_id(tasks_data, task_id):
    for index, task in enumerate(tasks_data):
        if task["task_id"] == task_id:
            return index

    return None

# 封装函数：遍历tasks_data，判断tasks_data长度是否=0，即判断是否有任务存在，否则无法action
def has_task_len(tasks_data,action_name):
    if len(tasks_data) == 0:
        print(f"暂无任务，无法{action_name}。")
        return False
    return True

# 遍历tasks_data，在最大的任务id后面，自动生成新的任务id
def get_next_task_id(tasks_data):
    if len(tasks_data) == 0:
        return 1

    max_task_id = 0

    for task in tasks_data:
        if task["task_id"] > max_task_id:
            max_task_id = task["task_id"]

    return max_task_id + 1

# 展示任务列表统计
def calculate_task_stats(tasks_data):
    if not has_task_len(tasks_data,"统计"):
        return None
    
    total_tasks = len(tasks_data)
    completed_tasks = 0
    unfinished_tasks = 0
    total_cps = 0
    completed_cps = 0
    unclaim_cps = 0
    unfinished_cps = 0

    for task in tasks_data:
        reward_cps = task["reward_cps"]
        total_cps = total_cps + reward_cps

        if task["task_status"] == "已完成" and task["reward_status"] == "已领取":
            completed_tasks = completed_tasks + 1
            completed_cps = completed_cps + reward_cps
        elif task["task_status"] == "已完成" and task["reward_status"] == "未领取":
            completed_tasks = completed_tasks + 1
            unclaim_cps = unclaim_cps + reward_cps
        elif task["task_status"] == "未完成" and task["reward_status"] == "未领取":
    
            unfinished_tasks = unfinished_tasks + 1
            unfinished_cps = unfinished_cps + reward_cps
    stats = {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "unfinished_tasks": unfinished_tasks,
        "total_cps": total_cps,
        "completed_cps": completed_cps,
        "unclaim_cps": unclaim_cps,
        "unfinished_cps": unfinished_cps
    }

    return stats
