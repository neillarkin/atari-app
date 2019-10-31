
def test_are_equal(actual, expected):
    """
    Test that two values are equal. Raises AssertionError if both values are
    not equal.

    `actual` is the actual value produced
    `expected` is the value that was supposed to be produced
    """
    assert expected == actual, "Expected {0}, got {1}".format(
        expected, actual)


def test_not_equal(a, b):
    """
    Test that two values are not equal. Raises AssertionError if both values
    are not equal.

    `a` is the actual value produced
    `b` is the value that was supposed to be produced
    """
    assert a != b, "Did not expect {0} but got {1}".format(a, b)


def test_is_in(collection, item):
    """
    Check to ensure that a given collection contains a given value. Raises
    AssertionError if `item` is not in `collection`

    `collection` is the collection to be tested
    `item` is the item that is being searched for
    """
    assert item in collection, "{0} does not contain {1}".format(
        collection, item)


def test_not_in(collection, item):
    """
    Check to ensure that a given collection does not contain a given value.
    Raises AssertionError if the `item` is found in `collection`

    `collection` is the collection in question
    `item` is the thing that we want to check for
    """
    assert item not in collection, "{0} is not in {1}".format(
        item, collection)


def test_between(upper_limit, lower_limit, actual):
    """
    Check to ensure that a number is between two other numbers. Raises
    AssertionError if the number is not between the other two numbers
    """
    assert lower_limit <= actual <= upper_limit, "{0} is not between {1} and {2}".format(actual, lower_limit, upper_limit)


# Test to fail the `test_are_equal` function
# test_are_equal(number_of_evens([1,2,3,4,5]), 2)

# Test to fail the `test_not_equal` function
# test_not_equal(0, 0)

# Test to fail the `test_is_in` function
# test_is_in([1], 2)

# Test to fail the `test_not_in` function
# test_not_in([1], 1)

# Test to fail the `test_between` function
test_between(10, 1, 200)