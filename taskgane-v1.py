
import logging
from logger_config import setup_logger
from storage import load_tasks_from_json, repair_task_ids
from views import show_menu, show_tasks, show_task_stats
from task_actions import add_task, complete_task, claim_reward, select_edit_task, delete_one_task, show_task_stats_by_type, show_selected_task_detail, show_tasks_by_type, show_tasks_by_priority, show_overdue_tasks, show_tasks_due_within_7_days, task_filter_center, clear_all_tasks


# 主流程
def main():
    setup_logger()
    logging.info("Conso 任务奖励系统启动")
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
        "11": show_selected_task_detail,
        "12": show_tasks_by_priority,
        "13": show_overdue_tasks,
        "14": show_tasks_due_within_7_days,
        "15": task_filter_center
    }
    
    while True:
        show_menu()
        user_choice = input("请输入你的选择: ").strip()
        logging.info(f"用户选择菜单: {user_choice}")

        if user_choice == "q":
            logging.info("用户退出系统")
            print("已退出系统。")
            break

        action = menu_actions.get(user_choice)

        if action is None:
            print("输入无效，请重新输入。")
            logging.warning(f"用户输入了无效菜单: {user_choice}")
            continue

        try:
            logging.info(f"开始执行菜单功能: {user_choice}")
            action(tasks_data)
            logging.info(f"菜单功能执行完成: {user_choice}")

        except Exception as error:
            logging.exception(f"执行菜单功能失败: {user_choice}, 错误信息: {error}")
            print("功能执行出错，请检查日志 app.log。")

        # 如果选择6，action=get6=claim_reward....然后 action(tasks_data) = claim_reward(tasks_data)

if __name__ == "__main__":
    main()
