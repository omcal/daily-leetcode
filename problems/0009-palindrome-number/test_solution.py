from .solution import Solution


def test_example_1():
    assert Solution().isPalindrome(121) is True


def test_negative_is_never_a_palindrome():
    assert Solution().isPalindrome(-121) is False


def test_trailing_zero_is_not_a_palindrome():
    assert Solution().isPalindrome(10) is False


def test_single_digit():
    assert Solution().isPalindrome(0) is True
    assert Solution().isPalindrome(7) is True
