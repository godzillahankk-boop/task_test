from config import TASK_TYPES
from task_helpers import has_task_len




# 展示主菜单
def show_menu():
    print("\n===== Conso 任务奖励系统 =====")
    print("1. 新增任务")
    print("2. 查看任务列表")
    print("3. 删除所有任务")
    print("4. 删除指定任务")
    print("5. 完成指定任务")
    print("6. 领取任务奖励")
    print("7. 查看任务统计")
    print("8. 按任务类型查看任务")
    print("9. 按任务类型统计")
    print("10. 修改指定任务")
    print("11. 搜索任务详情")
    print("q. 退出系统")

# 封装函数：打印单个任务详情
def show_task_detail(task):
    print(f"任务id: {task['task_id']}")
    print(f"任务名称: {task['task_name']}")
    print(f"任务奖励: {task['reward_cps']} CPS")
    print(f"任务类型: {task['task_type']}")
    print(f"任务状态: {task['task_status']}")
    print(f"奖励状态: {task['reward_status']}")

# 展示编辑详情菜单栏
def show_edit_menu():
    print("\n请选择要修改的内容：")
    print("1. 修改任务名称")
    print("2. 修改任务奖励 CPS")
    print("3. 修改任务类型")
    print("4. 修改全部信息")
    print("q. 返回主菜单")

# 封装函数：获取并展示任务类型
def show_task_types():
    for index, task_type in enumerate(TASK_TYPES):
        print(f"{index + 1}. {task_type}")



# 展示任务列表统计
def show_task_stats(tasks_data):

    if not has_task_len(tasks_data,"统计"):
        return
    
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

    print("\n===== 任务统计 =====")
    print(f"总任务数: {total_tasks}")
    print(f"已完成任务数: {completed_tasks}")
    print(f"未完成任务数: {unfinished_tasks}")
    print(f"总 CPS 奖励: {total_cps}")
    print(f"已领取 CPS: {completed_cps}")
    print(f"可领取 CPS: {unclaim_cps}")
    print(f"未完成 CPS: {unfinished_cps}")

# 展示已添加的任务列表
def show_tasks(tasks_data):
    if not has_task_len(tasks_data, "查看"):
       return

    print("\n当前任务列表如下:")

    for index, task in enumerate(tasks_data, start=1):
        print(f"{index}. ID: {task['task_id']} | 任务名称: {task['task_name']} | 奖励: {task['reward_cps']} CPS | 任务类型: {task['task_type']} |  任务状态: {task['task_status']} | 奖励状态：{task['reward_status']}")
