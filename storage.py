import json
import os
import logging
from config import TASK_FILE, TASK_PRIORITIES, DEFAULT_TASK_PRIORITY, DEFAULT_DUE_DATE
from task_helpers import is_valid_due_date


# 读取task.json的数据
def load_tasks_from_json(filename=TASK_FILE):
    if not os.path.exists(filename):
        logging.info(f"数据文件不存在，将使用空的任务列表")
        return []

    try:
        with open(filename, "r", encoding="utf-8") as file:
            tasks = json.load(file)

        if not isinstance(tasks, list):
            logging.warning(f"任务数据格式异常，期望 list, 实际不是 list, 已重置为空列表")
            print("任务数据格式异常，已重置为空列表")
            return []
        
        logging.info(f"任务数据读取成功，共 {len(tasks)} 条任务")
        return tasks
        

    except json.JSONDecodeError:
        logging.warning(f"任务数据文件损坏或为空，已重置为空列表")
        print("任务数据文件损坏或为空，已重置为空列表")
        return []

# 保存任务到json
def save_tasks_to_json(tasks, filename=TASK_FILE):
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(tasks, file, ensure_ascii=False, indent=2)

        logging.info(f"任务数据保存成功，共 {len(tasks)} 条任务")

    except Exception:
        logging.exception(f"任务数据保存失败: {filename}")
        raise

# 修复老数据
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
        save_tasks_to_json(tasks_data)
