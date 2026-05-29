from config import TASK_TYPES
from storage import save_tasks_to_json
from task_helpers import has_task_len, find_task_index_by_id, get_next_task_id, filter_tasks_by_type
from views import show_task_detail, show_edit_menu, show_tasks, show_task_types, show_task_stats
from input_helper import get_yes_or_no, get_task_index, add_task_name, add_task_reward, add_task_type, get_task_id, get_type_index

# 封装函数：查找任务
def select_task(tasks_data, action_name):
    if not has_task_len(tasks_data, action_name):
        return None, None
    print("\n请选择查找任务的方式：")
    print("1. 按列表编号选择")
    print("2. 按任务ID选择")
    print("q. 返回主菜单")

    choice = input("请输入你的选择: ").strip()

    if choice == "q":
        print("已取消操作，返回主菜单。")
        return None, None

    if choice == "1":
        task_index = get_task_index(tasks_data, action_name)

        if task_index is None:
            return None, None

        task = tasks_data[task_index]

        return task_index, task

    elif choice == "2":
        show_tasks(tasks_data)

        task_id = get_task_id(action_name)

        if task_id is None:
            return None, None

        task_index = find_task_index_by_id(tasks_data, task_id)

        if task_index is None:
            print("未找到该任务ID对应的任务。")
            return None, None

        task = tasks_data[task_index]

        return task_index, task

    else:
        print("输入无效，返回主菜单。")
        return None, None
    
# 按类型查看任务
def show_tasks_by_type(tasks_data):
    if not has_task_len(tasks_data, "按类型查看"):
        return

    print("请选择要查看的任务类型：")

    show_task_types()

    type_index = get_type_index(TASK_TYPES, "查看")

    if type_index is None:
        return

    selected_task_type = TASK_TYPES[type_index]

    filtered_tasks = filter_tasks_by_type(tasks_data, selected_task_type)

    if len(filtered_tasks) == 0:
        print(f"暂无【{selected_task_type}】类型的任务。")
        return

    print(f"\n===== 【{selected_task_type}】任务列表 =====")
    show_tasks(filtered_tasks)

# 封装函数：修改任务
def edit_selected_task(task, tasks_data):
    print("\n你将要修改以下任务:")
    show_task_detail(task)

    show_edit_menu()

    edit_choice = input("请输入你的选择: ").strip()

    if edit_choice == "q":
        print("任务修改已取消，返回主菜单。")
        return

    if edit_choice == "1":
        new_name = add_task_name()

        if new_name is None:
            print("任务修改已取消，返回主菜单。")
            return

        confirm_edit = get_yes_or_no("确认修改任务名称吗？")

        if not confirm_edit:
            print("任务修改已取消，返回主菜单。")
            return

        task["task_name"] = new_name

    elif edit_choice == "2":
        new_reward = add_task_reward()

        if new_reward is None:
            print("任务修改已取消，返回主菜单。")
            return

        confirm_edit = get_yes_or_no("确认修改任务奖励吗？")

        if not confirm_edit:
            print("任务修改已取消，返回主菜单。")
            return

        task["reward_cps"] = new_reward

    elif edit_choice == "3":
        new_type = add_task_type()

        if new_type is None:
            print("任务修改已取消，返回主菜单。")
            return

        confirm_edit = get_yes_or_no("确认修改任务类型吗？")

        if not confirm_edit:
            print("任务修改已取消，返回主菜单。")
            return

        task["task_type"] = new_type

    elif edit_choice == "4":
        new_name = add_task_name()
        if new_name is None:
            print("任务修改已取消，返回主菜单。")
            return

        new_reward = add_task_reward()
        if new_reward is None:
            print("任务修改已取消，返回主菜单。")
            return

        new_type = add_task_type()
        if new_type is None:
            print("任务修改已取消，返回主菜单。")
            return

        confirm_edit = get_yes_or_no("确认修改全部任务信息吗？")

        if not confirm_edit:
            print("任务修改已取消，返回主菜单。")
            return

        task["task_name"] = new_name
        task["reward_cps"] = new_reward
        task["task_type"] = new_type

    else:
        print("输入无效，返回主菜单。")
        return

    save_tasks_to_json(tasks_data)

    print("\n任务修改成功！修改后的任务信息如下：")
    show_task_detail(task)

# 新增任务进到task_data
def add_task(tasks_data):
    task_name = add_task_name()
    if task_name is None:
           print("任务添加已取消，返回主菜单。")
           return

    task_reward = add_task_reward()

    if task_reward is None:
        print("任务添加已取消，返回主菜单")
        return

    task_type = add_task_type()
    if task_type is None:
        print("任务添加已取消，返回主菜单")
        return

    task = {
        "task_id": get_next_task_id(tasks_data),
        "task_name": task_name,
        "reward_cps": int(task_reward),
        "task_type": task_type,
        "task_status": "未完成",
        "reward_status": "未领取"
    }
    print("\n===== 新增任务 =====")
    show_task_detail(task)
    
    confirm_add_task = get_yes_or_no("请确认添加任务")
    if not confirm_add_task:
       print("已取消操作！")
       return
 
    tasks_data.append(task)
    save_tasks_to_json(tasks_data)
    print("任务新增成功！")
    return

# 完成任务
def complete_task(tasks_data):
    task_index, task = select_task(tasks_data, "完成任务")

    if task is None:
        return

    if task["task_status"] == "已完成":
        print("这个任务已经是已完成状态，无需重复操作。")
        return

    print("\n你将要完成以下任务: ")
    show_task_detail(task)

    complete_confirm = get_yes_or_no("确认完成该任务吗？")
    if not complete_confirm:
        print("已取消操作，返回主菜单。")
        return

    task["task_status"] = "已完成"
    save_tasks_to_json(tasks_data)
    print(f"任务【{task['task_name']}】已标记为已完成。")
    return


# 领取奖励
def claim_reward(tasks_data):
    task_index, task = select_task(tasks_data, "完成任务")

    if task is None:
        return
    
    if task["task_status"] == "未完成":
        print("任务未完成， 不能领取奖励")
        return

    if task["reward_status"] == "已领取":
        print("这个奖励已经领取过了， 无需重复领取")
        return

    print("\n你将要领取以下任务的奖励: ")
    show_task_detail(task)


    claim_confirm = get_yes_or_no("确认领取奖励码？")
    if not claim_confirm:
        print("已取消操作，返回主菜单。")
        return

    task["reward_status"] = "已领取"
    save_tasks_to_json(tasks_data)
    print(f"已领取【{task['task_name']}】的奖励，奖励金额为【{task['reward_cps']}】。")
    return

# 查找任务+修改任务
def select_edit_task(tasks_data):
    task_index, task = select_task(tasks_data, "修改")

    if task is None:
        return

    edit_selected_task(task, tasks_data)


# 根据id删除任务
def delete_one_task(tasks_data):
    task_index, task = select_task(tasks_data, "删除")

    if task is None:
        return

    print("\n你将要删除以下任务:")
    show_task_detail(task)

    confirm_delete = get_yes_or_no("请确认删除任务")

    if not confirm_delete:
        print("已取消删除，返回主菜单。")
        return

    deleted_task = tasks_data.pop(task_index)

    save_tasks_to_json(tasks_data)

    print(f"任务【{deleted_task['task_name']}】已删除。")

# 展示按任务类型的统计
def show_task_stats_by_type(tasks_data):
    if not has_task_len(tasks_data, "按类型统计"):
        return

    print("请选择要统计的任务类型：")

    show_task_types()

    type_index = get_type_index(TASK_TYPES, "统计")

    if type_index is None:
        return

    selected_task_type = TASK_TYPES[type_index]

    filtered_tasks = filter_tasks_by_type(tasks_data, selected_task_type)

    if len(filtered_tasks) == 0:
        print(f"暂无【{selected_task_type}】类型的任务，无法统计。")
        return

    print(f"\n===== 【{selected_task_type}】任务统计 =====")
    show_task_stats(filtered_tasks)

# 根据任务id查看详情
def show_selected_task_detail(tasks_data):
    task_index, task = select_task(tasks_data, "查看")

    if task is None:
        return

    print("\n===== 任务详情 =====")
    show_task_detail(task)

    # 清空所有任务
def clear_all_tasks(tasks_data):
    if not has_task_len(tasks_data,"清空"):
       return
    
    confirm_clear_all = get_yes_or_no("请确认删除所有任务")
    if not confirm_clear_all:
        print("已取消操作, 返回主菜单")
        return

    tasks_data.clear()
    save_tasks_to_json(tasks_data)
    print("所有任务已清空。")
    return