
from storage import load_tasks_from_json, repair_task_ids
from views import show_menu, show_tasks, show_task_stats
from task_actions import add_task, complete_task, claim_reward, select_edit_task, delete_one_task, show_task_stats_by_type, show_selected_task_detail, show_tasks_by_type, clear_all_tasks


# 主流程
def main():
    tasks_data = load_tasks_from_json()
    repair_task_ids(tasks_data)

    menu_actions = {
        "1": add_task,
        "2": show_tasks,
        "3": clear_all_tasks,
        "4": delete_one_task,
        "5": complete_task,
        "6": claim_reward,
        "7": show_task_stats,
        "8": show_tasks_by_type,
        "9": show_task_stats_by_type,
        "10": select_edit_task,
        "11": show_selected_task_detail
    }
    
    while True:
        show_menu()
        user_choice = input("请输入你的选择: ").strip()

        if user_choice == "q":
            print("已退出系统。")
            break

        action = menu_actions.get(user_choice)

        if action is None:
            print("输入无效，请重新输入。")
            continue

        action(tasks_data)

        # 如果选择6，action=get6=claim_reward....然后 action(tasks_data) = claim_reward(tasks_data)

if __name__ == "__main__":
    main()