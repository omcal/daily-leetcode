from .solution import Solution


def test_example_1():
    assert Solution().search([-1, 0, 3, 5, 9, 12], 9) == 4


def test_example_2_missing_target():
    assert Solution().search([-1, 0, 3, 5, 9, 12], 2) == -1


def test_single_element():
    assert Solution().search([5], 5) == 0
    assert Solution().search([5], -5) == -1


def test_empty_list():
    assert Solution().search([], 1) == -1


def test_target_at_each_end():
    nums = [-1, 0, 3, 5, 9, 12]
    assert Solution().search(nums, -1) == 0
    assert Solution().search(nums, 12) == 5


def test_finds_every_element():
    nums = [-8, -3, 0, 2, 7, 11, 40, 41]
    for index, value in enumerate(nums):
        assert Solution().search(nums, value) == index
