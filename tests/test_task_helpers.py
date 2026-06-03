import pytest
from task_helpers import calculate_task_stats, get_next_task_id, find_task_index_by_id, filter_tasks_by_type, filter_tasks_by_priority, is_valid_due_date, is_valid_due_date_range, filter_overdue_tasks, filter_tasks_due_within_days, filter_tasks_by_due_date, filter_tasks_by_task_status, filter_tasks_by_reward_status, filter_tasks_advanced, sort_tasks
from input_helper import get_advanced_due_date_range_filter, DUE_DATE_CANCELLED

@pytest.fixture
def sample_tasks():
    return [
        {
            "task_id": 1,
            "task_name": "task A",
            "reward_cps": 100,
            "task_type": "社交任务",
            "priority": "high",
            "due_date": None,
            "task_status": "未完成",
            "reward_status": "未领取"
        },
        {
            "task_id": 2,
            "task_name": "task B",
            "reward_cps": 200,
            "task_type": "游戏任务",
            "priority": "medium",
            "due_date": "2026-06-10",
            "task_status": "已完成",
            "reward_status": "未领取"
        },
        {
            "task_id": 3,
            "task_name": "task C",
            "reward_cps": 300,
            "task_type": "邀请任务",
            "priority": "low",
            "due_date": "2026-06-11",
            "task_status": "已完成",
            "reward_status": "已领取"
        }
    ]

@pytest.fixture
def non_continuous_tasks():
    return [
        {
            "task_id": 1,
            "task_name": "task A",
            "reward_cps": 100,
            "task_type": "社交任务",
            "task_status": "未完成",
            "reward_status": "未领取"
        },
        {
            "task_id": 3,
            "task_name": "task C",
            "reward_cps": 300,
            "task_type": "邀请任务",
            "task_status": "已完成",
            "reward_status": "已领取"
        },
        {
            "task_id": 8,
            "task_name": "task H",
            "reward_cps": 800,
            "task_type": "游戏任务",
            "task_status": "未完成",
            "reward_status": "未领取"
        }
    ]


#-----------------------------


# 空数据测试
def test_empty_tasks():
    stats = calculate_task_stats([])
    assert stats is None

    test_id = get_next_task_id([])
    assert test_id == 1

    filtered_tasks = filter_tasks_by_type([], "游戏任务")
    assert filtered_tasks == []

    filtered_tasks = filter_tasks_by_priority([], "high")
    assert filtered_tasks == []

    task_index = find_task_index_by_id([], 2)
    assert task_index is None

# 异常边界测试
def test_edge_tasks(sample_tasks):
    task_index = find_task_index_by_id(sample_tasks, 999)
    assert task_index is None

    filtered_tasks = filter_tasks_by_type(sample_tasks, "浏览任务")
    assert len(filtered_tasks) == 0

    filtered_tasks = filter_tasks_by_priority(sample_tasks, "high")
    assert len(filtered_tasks) == 1



def test_get_next_task_id_non_continuous(non_continuous_tasks):
    test_id = get_next_task_id(non_continuous_tasks)
    assert test_id == 9

# 测试下一个任务id
def test_get_next_task_id(sample_tasks):
    test_id = get_next_task_id(sample_tasks)
    assert test_id == 4

# 测试 filter_tasks_by_type 函数，使用参数化测试不同任务类型的筛选结果
@pytest.mark.parametrize(
    "task_type, expected_count, expected_names",
    [
        ("社交任务", 1, ["task A"]),
        ("游戏任务", 1, ["task B"]),
        ("邀请任务", 1, ["task C"]),
        ("浏览任务", 0, []),
    ]
)

# 测试筛选并返回对应任务类型
def test_filter_tasks_by_type(sample_tasks, task_type, expected_count, expected_names):
    filtered_tasks = filter_tasks_by_type(sample_tasks, task_type)

    assert len(filtered_tasks) == expected_count

    task_names = []

    for task in filtered_tasks:
        task_names.append(task["task_name"])

    assert task_names == expected_names


# 测试筛选并返回对应任务优先级
@pytest.mark.parametrize(
    "priority, expected_count, expected_names",
    [
        ("high", 1, ["task A"]),
        ("medium", 1, ["task B"]),
        ("low", 1, ["task C"]),
    ]
)
def test_filter_tasks_by_priority(sample_tasks, priority, expected_count, expected_names):
    filtered_tasks = filter_tasks_by_priority(sample_tasks, priority)

    assert len(filtered_tasks) == expected_count

    task_names = []

    for task in filtered_tasks:
        task_names.append(task["task_name"])

    assert task_names == expected_names


@pytest.mark.parametrize(
    "date_text, expected",
    [
        ("2026-06-10", True),
        ("2026/06/10", False),
        ("2026-13-01", False),
        ("", False),
        (None, True),
    ]
)
def test_is_valid_due_date(date_text, expected):
    assert is_valid_due_date(date_text) == expected


def test_filter_overdue_tasks():
    tasks_data = [
        {"task_id": 1, "task_name": "overdue", "due_date": "2026-06-09"},
        {"task_id": 2, "task_name": "today", "due_date": "2026-06-10"},
        {"task_id": 3, "task_name": "no due date", "due_date": None},
        {"task_id": 4, "task_name": "future", "due_date": "2026-06-11"},
    ]

    filtered_tasks = filter_overdue_tasks(tasks_data, today="2026-06-10")

    task_names = []

    for task in filtered_tasks:
        task_names.append(task["task_name"])

    assert task_names == ["overdue"]


def test_filter_tasks_due_within_days():
    tasks_data = [
        {"task_id": 1, "task_name": "yesterday", "due_date": "2026-06-09"},
        {"task_id": 2, "task_name": "today", "due_date": "2026-06-10"},
        {"task_id": 3, "task_name": "within 7 days", "due_date": "2026-06-15"},
        {"task_id": 4, "task_name": "day 7", "due_date": "2026-06-17"},
        {"task_id": 5, "task_name": "day 8", "due_date": "2026-06-18"},
        {"task_id": 6, "task_name": "no due date", "due_date": None},
    ]

    filtered_tasks = filter_tasks_due_within_days(tasks_data, today="2026-06-10")

    task_names = []

    for task in filtered_tasks:
        task_names.append(task["task_name"])

    assert task_names == ["today", "within 7 days", "day 7"]


def test_filter_tasks_by_due_date_exact():
    tasks_data = [
        {"task_id": 1, "task_name": "no due date", "due_date": None},
        {"task_id": 2, "task_name": "target A", "due_date": "2026-06-10"},
        {"task_id": 3, "task_name": "other", "due_date": "2026-06-11"},
        {"task_id": 4, "task_name": "target B", "due_date": "2026-06-10"},
    ]

    filtered_tasks = filter_tasks_by_due_date(tasks_data, "2026-06-10")

    task_names = []

    for task in filtered_tasks:
        task_names.append(task["task_name"])

    assert task_names == ["target A", "target B"]


def test_filter_tasks_by_due_date_range():
    tasks_data = [
        {"task_id": 1, "task_name": "before", "due_date": "2026-06-09"},
        {"task_id": 2, "task_name": "start", "due_date": "2026-06-10"},
        {"task_id": 3, "task_name": "middle", "due_date": "2026-06-15"},
        {"task_id": 4, "task_name": "end", "due_date": "2026-06-17"},
        {"task_id": 5, "task_name": "after", "due_date": "2026-06-18"},
        {"task_id": 6, "task_name": "no due date", "due_date": None},
    ]

    filtered_tasks = filter_tasks_by_due_date(tasks_data, "2026-06-10&2026-06-17")

    task_names = []

    for task in filtered_tasks:
        task_names.append(task["task_name"])

    assert task_names == ["start", "middle", "end"]


@pytest.mark.parametrize(
    "date_range_text, expected",
    [
        ("2026-06-10&2026-06-17", True),
        ("2026/06/10&2026-06-17", False),
        ("2026-06-18&2026-06-10", False),
        ("abc", False),
    ]
)
def test_is_valid_due_date_range(date_range_text, expected):
    assert is_valid_due_date_range(date_range_text) == expected


@pytest.mark.parametrize(
    "selected_status, expected_names",
    [
        ("未完成", ["task A"]),
        ("已完成", ["task B", "task C"]),
    ]
)
def test_filter_tasks_by_task_status(sample_tasks, selected_status, expected_names):
    filtered_tasks = filter_tasks_by_task_status(sample_tasks, selected_status)

    task_names = []

    for task in filtered_tasks:
        task_names.append(task["task_name"])

    assert task_names == expected_names


@pytest.mark.parametrize(
    "selected_status, expected_names",
    [
        ("未领取", ["task A", "task B"]),
        ("已领取", ["task C"]),
    ]
)
def test_filter_tasks_by_reward_status(sample_tasks, selected_status, expected_names):
    filtered_tasks = filter_tasks_by_reward_status(sample_tasks, selected_status)

    task_names = []

    for task in filtered_tasks:
        task_names.append(task["task_name"])

    assert task_names == expected_names


@pytest.fixture
def advanced_filter_tasks():
    return [
        {
            "task_id": 1,
            "task_name": "social unfinished",
            "reward_cps": 100,
            "task_type": "社交任务",
            "priority": "medium",
            "due_date": "2026-06-10",
            "task_status": "未完成",
            "reward_status": "未领取"
        },
        {
            "task_id": 2,
            "task_name": "game completed",
            "reward_cps": 200,
            "task_type": "游戏任务",
            "priority": "high",
            "due_date": "2026-06-15",
            "task_status": "已完成",
            "reward_status": "未领取"
        },
        {
            "task_id": 3,
            "task_name": "invite completed",
            "reward_cps": 300,
            "task_type": "邀请任务",
            "priority": "low",
            "due_date": "2026-06-20",
            "task_status": "已完成",
            "reward_status": "已领取"
        },
        {
            "task_id": 4,
            "task_name": "browse no date",
            "reward_cps": 400,
            "task_type": "浏览任务",
            "priority": "medium",
            "due_date": None,
            "task_status": "未完成",
            "reward_status": "未领取"
        }
    ]


def get_task_names(tasks_data):
    task_names = []

    for task in tasks_data:
        task_names.append(task["task_name"])

    return task_names


def test_filter_tasks_advanced_by_type_only(advanced_filter_tasks):
    filtered_tasks = filter_tasks_advanced(advanced_filter_tasks, task_type="社交任务")

    assert get_task_names(filtered_tasks) == ["social unfinished"]


def test_filter_tasks_advanced_by_status_only(advanced_filter_tasks):
    filtered_tasks = filter_tasks_advanced(advanced_filter_tasks, task_status="已完成")

    assert get_task_names(filtered_tasks) == ["game completed", "invite completed"]


def test_filter_tasks_advanced_by_date_only(advanced_filter_tasks):
    filtered_tasks = filter_tasks_advanced(
        advanced_filter_tasks,
        start_date="2026-06-10",
        end_date="2026-06-15"
    )

    assert get_task_names(filtered_tasks) == ["social unfinished", "game completed"]


def test_filter_tasks_advanced_with_multiple_conditions(advanced_filter_tasks):
    filtered_tasks = filter_tasks_advanced(
        advanced_filter_tasks,
        task_type="游戏任务",
        task_status="已完成",
        reward_status="未领取",
        start_date="2026-06-10",
        end_date="2026-06-17"
    )

    assert get_task_names(filtered_tasks) == ["game completed"]


def test_filter_tasks_advanced_without_matching_result(advanced_filter_tasks):
    filtered_tasks = filter_tasks_advanced(
        advanced_filter_tasks,
        task_type="社交任务",
        task_status="已完成",
        reward_status="已领取"
    )

    assert filtered_tasks == []


def test_get_advanced_due_date_range_filter_with_single_date(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "2026-06-05")

    start_date, end_date = get_advanced_due_date_range_filter()

    assert start_date == "2026-06-05"
    assert end_date == "2026-06-05"


def test_get_advanced_due_date_range_filter_with_date_range(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "2026-06-01&2026-06-07")

    start_date, end_date = get_advanced_due_date_range_filter()

    assert start_date == "2026-06-01"
    assert end_date == "2026-06-07"


def test_get_advanced_due_date_range_filter_with_empty_input(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "   ")

    start_date, end_date = get_advanced_due_date_range_filter()

    assert start_date is None
    assert end_date is None


def test_get_advanced_due_date_range_filter_with_cancel(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "q")

    start_date, end_date = get_advanced_due_date_range_filter()

    assert start_date == DUE_DATE_CANCELLED
    assert end_date == DUE_DATE_CANCELLED


def test_get_advanced_due_date_range_filter_retries_invalid_date(monkeypatch):
    user_inputs = iter(["2026/06/05", "2026-06-05"])
    monkeypatch.setattr("builtins.input", lambda _: next(user_inputs))

    start_date, end_date = get_advanced_due_date_range_filter()

    assert start_date == "2026-06-05"
    assert end_date == "2026-06-05"


def test_sort_tasks_without_sorting_keeps_order(advanced_filter_tasks):
    sorted_tasks = sort_tasks(advanced_filter_tasks, "不排序")

    assert get_task_names(sorted_tasks) == [
        "social unfinished",
        "game completed",
        "invite completed",
        "browse no date"
    ]


def test_sort_tasks_by_due_date_nearest_first_puts_none_last(advanced_filter_tasks):
    sorted_tasks = sort_tasks(advanced_filter_tasks, "按截止日期从近到远")

    assert get_task_names(sorted_tasks) == [
        "social unfinished",
        "game completed",
        "invite completed",
        "browse no date"
    ]


def test_sort_tasks_by_due_date_farthest_first_puts_none_last(advanced_filter_tasks):
    sorted_tasks = sort_tasks(advanced_filter_tasks, "按截止日期从远到近")

    assert get_task_names(sorted_tasks) == [
        "invite completed",
        "game completed",
        "social unfinished",
        "browse no date"
    ]


def test_sort_tasks_by_reward_high_to_low(advanced_filter_tasks):
    sorted_tasks = sort_tasks(advanced_filter_tasks, "按 CPS 奖励从高到低")

    assert get_task_names(sorted_tasks) == [
        "browse no date",
        "invite completed",
        "game completed",
        "social unfinished"
    ]


def test_sort_tasks_by_reward_low_to_high(advanced_filter_tasks):
    sorted_tasks = sort_tasks(advanced_filter_tasks, "按 CPS 奖励从低到高")

    assert get_task_names(sorted_tasks) == [
        "social unfinished",
        "game completed",
        "invite completed",
        "browse no date"
    ]


def test_sort_tasks_by_priority(advanced_filter_tasks):
    sorted_tasks = sort_tasks(advanced_filter_tasks, "按优先级排序 high > medium > low")

    assert get_task_names(sorted_tasks) == [
        "game completed",
        "social unfinished",
        "browse no date",
        "invite completed"
    ]



# 测试find_task_index_by_id函数，使用参数化测试不同的task_id和预期的index结果
@pytest.mark.parametrize(
    "task_id, expected_index",
    [
        (1, 0),
        (2, 1),
        (3, 2),
        (999, None),
    ]
)
# 遍历tasks_data，找到对应id任务的下标index
def test_find_task_index_by_id(sample_tasks, task_id, expected_index):
    task_index = find_task_index_by_id(sample_tasks, task_id)
    assert task_index == expected_index


@pytest.mark.parametrize(
    "tasks_data, expected_stats",
    [
        (
            [
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
            ],
            {
                "total_tasks": 3,
                "completed_tasks": 2,
                "unfinished_tasks": 1,
                "total_cps": 600,
                "completed_cps": 300,
                "unclaim_cps": 200,
                "unfinished_cps": 100
            }
        ),
        (
            [
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
                    "task_status": "未完成",
                    "reward_status": "未领取"
                }
            ],
            {
                "total_tasks": 2,
                "completed_tasks": 0,
                "unfinished_tasks": 2,
                "total_cps": 300,
                "completed_cps": 0,
                "unclaim_cps": 0,
                "unfinished_cps": 300
            }
        ),
        (
            [
                {
                    "task_id": 1,
                    "task_name": "task A",
                    "reward_cps": 100,
                    "task_type": "社交任务",
                    "task_status": "已完成",
                    "reward_status": "未领取"
                },
                {
                    "task_id": 2,
                    "task_name": "task B",
                    "reward_cps": 200,
                    "task_type": "游戏任务",
                    "task_status": "已完成",
                    "reward_status": "未领取"
                }
            ],
            {
                "total_tasks": 2,
                "completed_tasks": 2,
                "unfinished_tasks": 0,
                "total_cps": 300,
                "completed_cps": 0,
                "unclaim_cps": 300,
                "unfinished_cps": 0
            }
        ),
        (
            [
                {
                    "task_id": 1,
                    "task_name": "task A",
                    "reward_cps": 100,
                    "task_type": "社交任务",
                    "task_status": "已完成",
                    "reward_status": "已领取"
                },
                {
                    "task_id": 2,
                    "task_name": "task B",
                    "reward_cps": 200,
                    "task_type": "游戏任务",
                    "task_status": "已完成",
                    "reward_status": "已领取"
                }
            ],
            {
                "total_tasks": 2,
                "completed_tasks": 2,
                "unfinished_tasks": 0,
                "total_cps": 300,
                "completed_cps": 300,
                "unclaim_cps": 0,
                "unfinished_cps": 0
            }
        )
    ]
)
def test_calculate_task_stats_with_multiple_cases(tasks_data, expected_stats):
    stats = calculate_task_stats(tasks_data)

    assert stats == expected_stats
