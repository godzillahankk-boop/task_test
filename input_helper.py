
from config import TASK_TYPES, TASK_PRIORITIES, TASK_STATUS_OPTIONS, REWARD_STATUS_OPTIONS
from task_helpers import has_task_len, is_valid_due_date, is_valid_due_date_range
from views import show_filter_center_menu, show_task_priorities, show_task_types, show_tasks

DUE_DATE_CANCELLED = "__due_date_cancelled__"

# 封装函数：二次获取用户确认
def get_yes_or_no(message):
    while True:
        user_input = input(f"{message},确认yes, 取消no: ").strip()

        if user_input == "yes":
            return True

        if user_input == "no":
            return False

        print("输入无效，请输入 yes 或 no。")

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
    
# 封装函数：获取用户输入的任务index下标
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

# 封装函数：获取用户输入的任务优先级编号
def get_priority_index(options, action_name):
    priority_index = get_index_from_list(options, action_name, "优先级")
    return priority_index

# 封装函数：获取筛选中心任务类型选择
def get_task_type_filter():
    print("请选择要筛选的任务类型：")

    show_task_types()

    while True:
        user_input = input("请输入要筛选的类型编号, 输入q返回筛选中心: ").strip()

        if user_input == "q":
            print("已取消操作，返回筛选中心。")
            return None

        if not user_input.isdigit():
            print("输入无效，请输入数字编号。")
            continue

        number = int(user_input)

        if number < 1 or number > len(TASK_TYPES):
            print("类型编号不存在，请重新输入。")
            continue

        type_index = number - 1
        return TASK_TYPES[type_index]

# 封装函数：获取筛选中心任务优先级选择
def get_task_priority_filter():
    print("请选择要筛选的任务优先级：")

    show_task_priorities()

    while True:
        user_input = input("请输入要筛选的优先级编号, 输入q返回筛选中心: ").strip()

        if user_input == "q":
            print("已取消操作，返回筛选中心。")
            return None

        if not user_input.isdigit():
            print("输入无效，请输入数字编号。")
            continue

        number = int(user_input)

        if number < 1 or number > len(TASK_PRIORITIES):
            print("优先级编号不存在，请重新输入。")
            continue

        priority_index = number - 1
        return TASK_PRIORITIES[priority_index]

# 封装函数：获取筛选中心菜单选择
def get_filter_center_choice():
    show_filter_center_menu()
    user_input = input("请输入你的选择: ").strip()
    return user_input

# 封装函数：获取日期筛选条件
def get_due_date_filter_query():
    while True:
        due_date_query = input("请输入截止日期，格式 YYYY-MM-DD，或日期范围 YYYY-MM-DD&YYYY-MM-DD，输入q返回筛选中心: ").strip()

        if due_date_query == "q":
            print("已取消操作，返回筛选中心。")
            return None

        if is_valid_due_date(due_date_query) or is_valid_due_date_range(due_date_query):
            return due_date_query

        print("日期输入无效，请重新输入。")

# 封装函数：获取用户输入的任务完成状态
def get_task_status_filter():
    print("请选择任务完成状态：")

    for index, status in enumerate(TASK_STATUS_OPTIONS):
        print(f"{index + 1}. {status}")

    while True:
        user_input = input("请输入要筛选的状态编号, 输入q返回筛选中心: ").strip()

        if user_input == "q":
            print("已取消操作，返回筛选中心。")
            return None

        if not user_input.isdigit():
            print("输入无效，请输入数字编号。")
            continue

        number = int(user_input)

        if number < 1 or number > len(TASK_STATUS_OPTIONS):
            print("状态编号不存在，请重新输入。")
            continue

        status_index = number - 1
        return TASK_STATUS_OPTIONS[status_index]


# 封装函数：获取用户输入的奖励领取状态
def get_reward_status_filter():
    print("请选择奖励领取状态：")

    for index, status in enumerate(REWARD_STATUS_OPTIONS):
        print(f"{index + 1}. {status}")

    while True:
        user_input = input("请输入要筛选的状态编号, 输入q返回筛选中心: ").strip()

        if user_input == "q":
            print("已取消操作，返回筛选中心。")
            return None

        if not user_input.isdigit():
            print("输入无效，请输入数字编号。")
            continue

        number = int(user_input)

        if number < 1 or number > len(REWARD_STATUS_OPTIONS):
            print("状态编号不存在，请重新输入。")
            continue

        status_index = number - 1
        return REWARD_STATUS_OPTIONS[status_index]

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

# 添加任务优先级
def add_task_priority():
    print("请选择任务优先级：")

    show_task_priorities()

    priority_index = get_priority_index(TASK_PRIORITIES, "添加的任务优先级")
    if priority_index is None:
          return None
    selected_priority = TASK_PRIORITIES[priority_index]

    return selected_priority

# 添加任务截止日期
def add_task_due_date():
    while True:
        due_date = input("请输入任务截止日期，格式 YYYY-MM-DD，直接回车表示不设置截止日期，输入q返回主菜单: ").strip()

        if due_date == "q":
            print("已取消操作，返回主菜单。")
            return DUE_DATE_CANCELLED

        if due_date == "":
            return None

        if not is_valid_due_date(due_date):
            print("截止日期格式错误，请输入 YYYY-MM-DD 格式。")
            continue

        return due_date

# 封装函数：获取用户输入的任务id
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
