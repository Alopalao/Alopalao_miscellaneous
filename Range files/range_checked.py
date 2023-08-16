# a = [[10, 20], [800, 3000]]
# b = [[1, 13], [19, 801], [803, 808], [2000, 4096]]
def can_restrict(available: list[list[int, int]], new_restriction: list[list[int, int]]) -> bool:
    """Check if new_restriction can be applied when there is available"""
    """Returns an early False when a gap is detected"""
    """Simulates sliding window O(n)"""
    
    # Check [[1...]] and [[...4096]]
    if available[0][0] != 1:
        if not (new_restriction[0][0] == 1 and new_restriction[0][1] >= available[0][0]):
            return False
    if available[-1][1] != 4096:
        if not (new_restriction[-1][1] == 4096 and new_restriction[-1][0] <= available[-1][1]):
            return False

    # Corner case
    ava_n = len(available)
    if ava_n == 1:
        return True

    rest_n = len(new_restriction)
    bool_list = [False] * (ava_n-1)
    ava_i, rest_i, start = 0, 0, 0
    while rest_i < rest_n:
        if new_restriction[rest_i][0] <= available[ava_i][1]:
            while ava_i + 1 < ava_n:
                if new_restriction[rest_i][1] >= available[ava_i+1][0]:
                    if new_restriction[rest_i][1] <= available[ava_i+1][1]:
                        ava_i += 1
                        bool_list[start: ava_i] = [True] * (ava_i-start)
                        start = ava_i
                        break
                    else:
                        ava_i += 1
                elif new_restriction[rest_i][1] <= available[ava_i][1]:
                    break
                else:
                    return False
            rest_i += 1
        else:
            return False
    result = all(bool_list)
    return result

global_range = [1, 4096]

a = [[10, 20], [800, 3000], [4000, 4096]]
b = [[1, 13], [19, 801], [803, 808], [2000, 2060], [2999, 4000]]

result = can_restrict(a, b)
print("RESULT -> ", result)
