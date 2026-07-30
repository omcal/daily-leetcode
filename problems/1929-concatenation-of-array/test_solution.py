from .solution import Solution


def test_example_1():
    assert Solution().getConcatenation([1, 2, 1]) == [1, 2, 1, 1, 2, 1]


def test_example_2():
    assert Solution().getConcatenation([1, 3, 2, 1]) == [1, 3, 2, 1, 1, 3, 2, 1]


def test_single_element():
    assert Solution().getConcatenation([7]) == [7, 7]


def test_input_is_not_mutated():
    nums = [1, 2, 3]
    Solution().getConcatenation(nums)
    assert nums == [1, 2, 3]
