from task_helpers import calculate_task_stats, get_next_task_id, find_task_index_by_id, filter_tasks_by_type

tasks_data = [
        {
            "task_id": 1,
            "task_name": "task A",
            "reward_cps": 100,
            "task_type": "社交任务",
            "task_status": "未完成",
            "reward_status": "未领取"
        },
        {
            "task_id": 2,
            "task_name": "task B",
            "reward_cps": 200,
            "task_type": "游戏任务",
            "task_status": "已完成",
            "reward_status": "未领取"
        },
        {
            "task_id": 3,
            "task_name": "task C",
            "reward_cps": 300,
            "task_type": "邀请任务",
            "task_status": "已完成",
            "reward_status": "已领取"
        }
    ]

# 空数据测试
def test_empty_tasks():
    stats = calculate_task_stats([])
    assert stats is None

    test_id = get_next_task_id([])
    assert test_id == 1

    filtered_tasks = filter_tasks_by_type([], "游戏任务")
    assert filtered_tasks == []

    task_index = find_task_index_by_id([], 2)
    assert task_index is None

# 异常边界测试
def test_edge_tasks():
    task_index = find_task_index_by_id(tasks_data, 999)
    assert task_index is None

    filtered_tasks = filter_tasks_by_type(tasks_data, "浏览任务")
    assert len(filtered_tasks) == 0

# 测试任务统计结果
def test_calculate_task_stats():
    stats = calculate_task_stats(tasks_data)

    assert stats["total_tasks"] == 3, f"总任务数统计错误，实际是 {stats['total_tasks']}，预期是 3"
    assert stats["completed_tasks"] == 2
    assert stats["unfinished_tasks"] == 1
    assert stats["total_cps"] == 600
    assert stats["completed_cps"] == 300
    assert stats["unclaim_cps"] == 200
    assert stats["unfinished_cps"] == 100

# 测试下一个任务id
def test_get_next_task_id():
    test_id = get_next_task_id(tasks_data)
    assert test_id == 4



# 测试筛选并返回对应任务类型
def test_filter_tasks_by_type():
    filtered_tasks = filter_tasks_by_type(tasks_data,"游戏任务")
    assert filtered_tasks == [
                {
            "task_id": 2,
            "task_name": "task B",
            "reward_cps": 200,
            "task_type": "游戏任务",
            "task_status": "已完成",
            "reward_status": "未领取"
        },
    ]



# 遍历tasks_data，找到对应id任务的下标index
def test_find_task_index_by_id():
    task_index = find_task_index_by_id(tasks_data, 2)
    assert task_index == 1


# 封装测试运行器
# def run_test(test_func):
    #try:
        #test_func()
        #print(f"{test_func.__name__} 通过测试")
        #return True
    #except AssertionError:
        #print(f"{test_func.__name__} 测试失败")
        #return False

# 测试主流程
#def main():

    #test_functions = [
        #test_empty_tasks,
        #test_edge_tasks,
        #test_calculate_task_stats,
        #test_get_next_task_id,
        #test_filter_tasks_by_type,
        #test_find_task_index_by_id
    #]

    #passed_count = 0
    #failed_count = 0

    #for test_func in test_functions:
        #result = run_test(test_func)

        #if result:
            #passed_count = passed_count + 1
        #else:
            #failed_count = failed_count + 1

    #print("\n===== 测试结果汇总 =====")
    #print(f"通过数量: {passed_count}")
    #print(f"失败数量: {failed_count}")

#if __name__ == "__main__":
    #main()
