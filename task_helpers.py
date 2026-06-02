

from datetime import date, timedelta


# 封装函数：校验任务截止日期格式
def is_valid_due_date(date_text):
    if date_text is None:
        return True

    if not isinstance(date_text, str):
        return False

    try:
        parsed_date = date.fromisoformat(date_text)
    except ValueError:
        return False

    return parsed_date.isoformat() == date_text


def get_today(today=None):
    if today is None:
        return date.today()

    if isinstance(today, date):
        return today

    return date.fromisoformat(today)


# 封装函数：校验任务截止日期范围格式
def is_valid_due_date_range(date_range_text):
    if not isinstance(date_range_text, str):
        return False

    date_parts = date_range_text.split("&")

    if len(date_parts) != 2:
        return False

    start_date_text = date_parts[0]
    end_date_text = date_parts[1]

    if not is_valid_due_date(start_date_text) or not is_valid_due_date(end_date_text):
        return False

    start_date = date.fromisoformat(start_date_text)
    end_date = date.fromisoformat(end_date_text)

    return start_date <= end_date


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


# 封装函数：筛选已过期任务
def filter_overdue_tasks(tasks_data, today=None):
    filtered_tasks = []
    today_date = get_today(today)

    for task in tasks_data:
        due_date = task.get("due_date")

        if due_date is None or not is_valid_due_date(due_date):
            continue

        if date.fromisoformat(due_date) < today_date:
            filtered_tasks.append(task)

    return filtered_tasks


# 封装函数：筛选未来指定天数内到期任务
def filter_tasks_due_within_days(tasks_data, days=7, today=None):
    filtered_tasks = []
    today_date = get_today(today)
    end_date = today_date + timedelta(days=days)

    for task in tasks_data:
        due_date = task.get("due_date")

        if due_date is None or not is_valid_due_date(due_date):
            continue

        parsed_due_date = date.fromisoformat(due_date)

        if today_date <= parsed_due_date <= end_date:
            filtered_tasks.append(task)

    return filtered_tasks


# 封装函数：按截止日期精确或范围筛选任务
def filter_tasks_by_due_date(tasks_data, due_date_query):
    filtered_tasks = []

    if is_valid_due_date(due_date_query):
        for task in tasks_data:
            due_date = task.get("due_date")

            if due_date is not None and due_date == due_date_query:
                filtered_tasks.append(task)

        return filtered_tasks

    if is_valid_due_date_range(due_date_query):
        date_parts = due_date_query.split("&")
        start_date = date.fromisoformat(date_parts[0])
        end_date = date.fromisoformat(date_parts[1])

        for task in tasks_data:
            due_date = task.get("due_date")

            if due_date is None or not is_valid_due_date(due_date):
                continue

            parsed_due_date = date.fromisoformat(due_date)

            if start_date <= parsed_due_date <= end_date:
                filtered_tasks.append(task)

    return filtered_tasks


# 封装函数：按任务完成状态筛选任务
def filter_tasks_by_task_status(tasks_data, selected_status):
    filtered_tasks = []

    for task in tasks_data:
        if task["task_status"] == selected_status:
            filtered_tasks.append(task)

    return filtered_tasks


# 封装函数：按奖励领取状态筛选任务
def filter_tasks_by_reward_status(tasks_data, selected_status):
    filtered_tasks = []

    for task in tasks_data:
        if task["reward_status"] == selected_status:
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
