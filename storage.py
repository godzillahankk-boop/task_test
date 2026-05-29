import json
from config import TASK_FILE


# 读取task.json的数据
def load_tasks_from_json(filename=TASK_FILE):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            tasks_data = json.load(file)
            return tasks_data

    except FileNotFoundError:
        return []

    except json.JSONDecodeError:
        print("task.json 文件内容不是合法 JSON，已使用空任务列表。")
        return []

# 保存任务到json
def save_tasks_to_json(tasks, filename=TASK_FILE):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(tasks, file, ensure_ascii=False, indent=2)

# 修复老数据的任务id
def repair_task_ids(tasks_data):
    max_task_id = 0

    for task in tasks_data:
        if "task_id" in task and task["task_id"] > max_task_id:
            max_task_id = task["task_id"]

    next_id = max_task_id + 1

    for task in tasks_data:
        if "task_id" not in task:
            task["task_id"] = next_id
            next_id = next_id + 1

    save_tasks_to_json(tasks_data)


