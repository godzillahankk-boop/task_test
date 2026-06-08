from config import TASK_TYPES, TASK_PRIORITIES
from task_helpers import has_task_len, calculate_filter_stats
from storage import get_task_stats_from_db




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
    print("12. 按任务优先级查看任务")
    print("13. 查看已过期任务")
    print("14. 查看未来 7 天内到期任务")
    print("15. 任务筛选中心")
    print("16. 高级筛选任务")
    print("q. 退出系统")

# 展示任务筛选中心菜单
def show_filter_center_menu():
    print("\n===== 任务筛选中心 =====")
    print("1. 按任务类型筛选")
    print("2. 按任务优先级筛选")
    print("3. 按截止日期筛选")
    print("4. 按完成状态筛选")
    print("5. 按奖励领取状态筛选")
    print("q. 返回主菜单")

# 展示筛选结果
def show_filter_result(title, tasks_data):
    if len(tasks_data) == 0:
        print("暂无符合条件的任务。")
        return

    print(f"\n===== {title} =====")
    show_tasks(tasks_data)

# 展示高级筛选结果
def show_advanced_filter_result(tasks_data):
    print("\n===== 高级筛选结果 =====")

    if len(tasks_data) == 0:
        print("暂无符合条件的任务。")
    else:
        show_tasks(tasks_data)

    stats = calculate_filter_stats(tasks_data)

    print("\n===== 筛选结果统计 =====")
    print(f"任务总数: {stats['total_tasks']}")
    print(f"已完成数量: {stats['completed_tasks']}")
    print(f"未完成数量: {stats['unfinished_tasks']}")
    print(f"总奖励 CPS: {stats['total_cps']}")
    print(f"可领取 CPS: {stats['unclaim_cps']}")

# 封装函数：展示截止日期
def format_due_date(due_date):
    if due_date is None:
        return "无"

    return due_date

# 封装函数：打印单个任务详情
def show_task_detail(task):
    print(f"任务id: {task['task_id']}")
    print(f"任务名称: {task['task_name']}")
    print(f"任务奖励: {task['reward_cps']} CPS")
    print(f"任务类型: {task['task_type']}")
    print(f"任务优先级: {task['priority']}")
    print(f"任务截止日期: {format_due_date(task['due_date'])}")
    print(f"任务状态: {task['task_status']}")
    print(f"奖励状态: {task['reward_status']}")

# 展示编辑详情菜单栏
def show_edit_menu():
    print("\n请选择要修改的内容：")
    print("1. 修改任务名称")
    print("2. 修改任务奖励 CPS")
    print("3. 修改任务类型")
    print("4. 修改任务优先级")
    print("5. 修改截止日期")
    print("6. 修改全部信息")
    print("q. 返回主菜单")

# 封装函数：获取并展示任务类型
def show_task_types():
    for index, task_type in enumerate(TASK_TYPES):
        print(f"{index + 1}. {task_type}")

# 封装函数：获取并展示任务优先级
def show_task_priorities():
    for index, priority in enumerate(TASK_PRIORITIES):
        print(f"{index + 1}. {priority}")

# 展示统计结果
def show_task_stats(tasks_data):
    stats = get_task_stats_from_db()

    if stats["total_tasks"] == 0:
        print("暂无任务，无法统计。")
        return

    print("\n===== 任务统计 =====")
    print(f"总任务数: {stats['total_tasks']}")
    print(f"已完成任务数: {stats['completed_tasks']}")
    print(f"未完成任务数: {stats['unfinished_tasks']}")
    print(f"总 CPS 奖励: {stats['total_cps']}")
    print(f"已领取 CPS: {stats['completed_cps']}")
    print(f"可领取 CPS: {stats['unclaim_cps']}")
    print(f"未完成 CPS: {stats['unfinished_cps']}")



# 展示已添加的任务列表
def show_tasks(tasks_data):
    if not has_task_len(tasks_data, "查看"):
       return

    print("\n当前任务列表如下:")

    for index, task in enumerate(tasks_data, start=1):
        print(f"{index}. ID: {task['task_id']} | 任务名称: {task['task_name']} | 奖励: {task['reward_cps']} CPS | 任务类型: {task['task_type']} | 优先级: {task['priority']} | 截止日期: {format_due_date(task['due_date'])} | 任务状态: {task['task_status']} | 奖励状态：{task['reward_status']}")
