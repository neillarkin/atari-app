from byotest import *


def get_change(amount):
    """
    Takes the payment amount and returns the change

    `amount` the amount of money that we need to provide change for

    Returns a list of coin values
    """
    if amount == 0:
        return []
    
    if amount in [100, 50, 20, 10, 5, 2, 1]:
        return [amount]
    
    change = []
    for coin in [100, 50, 20, 10, 5, 2, 1]:
        if coin <= amount:
            amount -= coin
            change.append(coin)

    return change


#  Write our tests for our code
test_are_equal(get_change(0), [])
test_are_equal(get_change(1), [1])
test_are_equal(get_change(2), [2])
test_are_equal(get_change(5), [5])
test_are_equal(get_change(10), [10])
test_are_equal(get_change(20), [20])
test_are_equal(get_change(50), [50])
test_are_equal(get_change(100), [100])
test_are_equal(get_change(3), [2, 1])
test_are_equal(get_change(7), [5, 2])

print("All tests pass!")