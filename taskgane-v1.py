import json
TASK_FILE = "task.json"
TASK_TYPES = ["社交任务", "浏览任务", "游戏任务", "邀请任务"]


# 封装函数：判断任务是否为空
def has_task_len(tasks_data,action_name):
    if len(tasks_data) == 0:
        print(f"暂无任务，无法{action_name}。")
        return False
    return True

# 封装函数：打印单个任务详情
def show_task_detail(task):
    print(f"任务id: {task['task_id']}")
    print(f"任务名称: {task['task_name']}")
    print(f"任务奖励: {task['reward_cps']} CPS")
    print(f"任务类型: {task['task_type']}")
    print(f"任务状态: {task['task_status']}")
    print(f"奖励状态: {task['reward_status']}")

# 封装函数：判断菜单栏的输入合法性（q退出、非数字、超出范围）
def get_index_from_list(data_list, action_name, item_name):
    while True:
        user_input = input(f"请输入要{action_name}的{item_name}编号, 输入q返回主菜单: ").strip()

        if user_input == "q":
            print("已取消操作，返回主菜单。")
            return None

        if not user_input.isdigit():
            print("输入无效，请输入数字编号。")
            continue

        number = int(user_input)

        if number < 1 or number > len(data_list):
            print(f"{item_name}编号不存在，请重新输入。")
            continue

        index = number - 1
        return index

# 封装函数：获取用户输入的任务编号
def get_task_index(tasks_data, action_name):
    if not has_task_len(tasks_data, action_name):
        return None

    show_tasks(tasks_data)
    task_index = get_index_from_list(tasks_data, action_name, "任务")

    return task_index

# 封装函数：获取用户输入的任务类型编号
def get_type_index(options, action_name):
    option_index = get_index_from_list(options, action_name, "类型")
    return option_index

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


# 封装函数：二次获取用户确认
def get_yes_or_no(message):
    while True:
        user_input = input(f"{message},确认yes, 取消no: ").strip()

        if user_input == "yes":
            return True

        if user_input == "no":
            return False

        print("输入无效，请输入 yes 或 no。")

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

# 封装函数：展示任务类型
def show_task_types():
    for index, task_type in enumerate(TASK_TYPES):
        print(f"{index + 1}. {task_type}")

# 封装函数：筛选任务类型，返回对应list
def filter_tasks_by_type(tasks_data, selected_task_type):
    filtered_tasks = []

    for task in tasks_data:
        if task["task_type"] == selected_task_type:
            filtered_tasks.append(task)

    return filtered_tasks



# 展示编辑详情菜单栏
def show_edit_menu():
    print("\n请选择要修改的内容：")
    print("1. 修改任务名称")
    print("2. 修改任务奖励 CPS")
    print("3. 修改任务类型")
    print("4. 修改全部信息")
    print("q. 返回主菜单")


# 添加任务名称
def add_task_name():
    while True: 
        task_name = input("请输入任务名称(输入q返回主菜单):").strip()
        if task_name == "q":
            return None
        if task_name == "":
            print("任务名称不能为空，请重新输入。")
        else:
            return task_name

# 添加任务奖励CPS
def add_task_reward():
    while True:
        task_reward = input("请输入任务奖励 CPS 数量(输入q返回主菜单):").strip()
        if task_reward == "q":
            return None
        if not task_reward.isdigit():
            print("CPS 奖励必须是数字，请重新输入。")
            continue
        if int(task_reward) <= 0:    
            print("CPS 奖励必须大于0, 请重新输入。")
            continue
        else:
            return int(task_reward)

# 添加任务类型
def add_task_type():
    print("请选择任务类型：")

    show_task_types()

    task_index = get_type_index(TASK_TYPES, "添加的任务类型")
    if task_index is None:
          return None
    selected_task_type = TASK_TYPES[task_index]

    return selected_task_type

# 新增任务自动生成task_id
def get_next_task_id(tasks_data):
    if len(tasks_data) == 0:
        return 1

    max_task_id = 0

    for task in tasks_data:
        if task["task_id"] > max_task_id:
            max_task_id = task["task_id"]

    return max_task_id + 1

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
    
# 展示已添加的任务列表
def show_tasks(tasks_data):
    if not has_task_len(tasks_data, "查看"):
       return

    print("\n当前任务列表如下:")

    for index, task in enumerate(tasks_data, start=1):
        print(f"{index}. ID: {task['task_id']} | 任务名称: {task['task_name']} | 奖励: {task['reward_cps']} CPS | 任务类型: {task['task_type']} |  任务状态: {task['task_status']} | 奖励状态：{task['reward_status']}")

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

# 遍历task，找出对应id的task
def find_task_by_id(tasks_data, task_id):
    for task in tasks_data:
        if task["task_id"] == task_id:
            return task
    return None

# 找到对应task_id的任务的下标index
def find_task_index_by_id(tasks_data, task_id):
    for index, task in enumerate(tasks_data):
        if task["task_id"] == task_id:
            return index

    return None

# 封装函数：输入任务id
def get_task_id(action_name):
    while True:
        user_input = input(f"请输入要{action_name}的任务ID, 输入q返回主菜单: ").strip()

        if user_input == "q":
            print("已取消操作，返回主菜单。")
            return None

        if not user_input.isdigit():
            print("任务ID必须是数字，请重新输入。")
            continue

        return int(user_input)

# 根据任务id查看详情
def show_selected_task_detail(tasks_data):
    task_index, task = select_task(tasks_data, "查看")

    if task is None:
        return

    print("\n===== 任务详情 =====")
    show_task_detail(task)

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

# 主流程
def main():
    tasks_data = load_tasks_from_json()
    repair_task_ids(tasks_data)
    
    while True:
      show_menu()
      user_choice = input("请输入你的选择: ").strip()
      if user_choice == "1":
        add_task(tasks_data)

      elif user_choice == "2":
        show_tasks(tasks_data)

      elif user_choice == "3":
        clear_all_tasks(tasks_data)
    
      elif user_choice == "4":
        delete_one_task(tasks_data)
    
      elif user_choice == "5":
        complete_task(tasks_data)
    
      elif user_choice == "6":
        claim_reward(tasks_data)

      elif user_choice == "7":
        show_task_stats(tasks_data)

      elif user_choice == "8":
        show_tasks_by_type(tasks_data)

      elif user_choice == "9":
        show_task_stats_by_type(tasks_data)

      elif user_choice == "10":
        select_edit_task(tasks_data)

      elif user_choice == "11":
        show_selected_task_detail(tasks_data)



      elif user_choice == "q":
        print("已退出系统。")
        break
      else:
        print("输入无效，请重新输入。")

if __name__ == "__main__":
    main()