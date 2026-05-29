


# 封装函数：遍历所有任务的类型，返回已有类型
def filter_tasks_by_type(tasks_data, selected_task_type):
    filtered_tasks = []

    for task in tasks_data:
        if task["task_type"] == selected_task_type:
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