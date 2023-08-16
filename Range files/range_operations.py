def next_tag(available:list[list[int]]) -> int:
    # Take next available tag
    if not available:
        # Not available tags
        return None
    
    first_tag = available[-1][1]
    available[-1][1] -= 1
    if available[-1][1] == available[-1][0]:
        available.pop()

    return first_tag

def is_available_log(available:list[list[int]], tags:list[int]) -> (bool, int):
    # Is range AVAILABLE to be taken?, which range
    lo = 0
    hi = len(available)
    while lo < hi:
        mid = (lo+hi)//2
        if available[mid][0] <= tags[0]:
            if available[mid][1] >= tags[1]:
                return True, mid
            lo = mid + 1
        elif available[mid][0] > tags[0]:
            hi = mid
    return False, None

def take_tags(available:list[list[int]], tags:list[int]) -> None:
    # Take RANGE from available, if possible (detects error)
    flag, i = is_available_log(available, tags)
    if flag is False:
        # tags not available
        return None

    if available[i][0] == tags[0]:
        if available[i][1] == tags[1]:
            available.pop(i)
        else:
            available[i: i+1] = [[tags[1], available[i][1]]]
    elif available[i][1] == tags[1]:
        available[i: i+1] = [[available[i][0], tags[0]]]
    else:
        available[i: i+1] = [[available[i][0], tags[0]], [tags[1], available[i][1]]]

def is_available_n_tuple(available:list[list[int]], tags:list[int]) -> (bool, int):
    # Is range AVAILABLE to be taken?
    for index in range(0, len(available)):
        if available[index][0] <= tags[0]:
            if available[index][1] >= tags[1]:
                return True, index
    return False, None

def is_unavailable_restrictive(available:list[list[int]], tags:list[int]) -> (bool, int):
    # Is unavailable, 
    # Negative value or 0 for tags is not possible
    # Values higher than 4096 are not possible
    # Restrictive because it cares if a value is really un_available
    n = len(available)
    if available[0][0] >= tags[1]:
        return True, 0
    
    for index in range(1, len(available)):
        if available[index][0] >= tags[1]:
            if available[index-1][1] <= tags[0]:
                return True, index
            return False, None
            
    if available[n-1][1] <= tags[0]:
        return True, n
    return False, None

def add_tags(available:list[list[int]], tags:list[int]) -> None:
    # Add RANGE to available, if possible
    # Example available = [[7, 10], [13, 15]]
    flag, i = is_unavailable_restrictive(available, tags)
    if flag is False:
        # Not possible
        return None
    n = len(available)
    if i == 0:
        # tags [1,7]
        if available[i][0] == tags[1]:
            available[i][0] = tags[0]
        # tags [1,3]
        available.insert(0, tags)

    elif i == n:
        # tags [15,301]
        if available[i-1][1] == tags[0]:
            available[i-1][1] = tags[1]
        # tags [200,301]
        available.append(tags)

    else:
        # tags [10, 13]
        if available[i-1][1] == tags[0] and available[i][0] == tags[1]:
            available[i-1:i+1] = [[available[i-1][0], available[i][1]]]
        # tags [10, 11]
        elif available[i-1][1] == tags[0]:
            available[i-1][1] = tags[1]
        # tags [11, 13]
        elif available[i][0] == tags[1]:
            available[i][0] = tags[0]
        # tags [11, 12]
        else:
            available.insert(i, tags)

def is_included (rtc_range: list[int, int], avb_range: list[int, int]) -> bool:
    """Determines if avb_range is included on rtc_range"""
    if rtc_range[0] <= avb_range[0] and rtc_range[1] >= avb_range[1]:
        return True
    return False

def subtract_ranges(restriction: list[list[int, int]], available: list[list[int, int]]) -> list[list[int, int]]:
    """Substract ranges list[list[int]]'s.
    This method does not catch error and `available` is expected
    to be included in `restriction` with no exceptions.
    Big O(n) as sliding window"""
    jndex, index = 0, 0
    n = len(available)
    result = [restriction[index]]
    while jndex < n:
        if is_included(result[-1], available[jndex]):
            if result[-1] == available[jndex]:
                result.pop()
            elif result[-1][0] == available[jndex][0]:
                result[-1] = [available[jndex][1], result[-1][1]]
            elif result[-1][1] == available[jndex][1]:
                result[-1] = [result[-1][0], available[jndex][0]]
            else:
                result[-1:] = [
                    [result[-1][0], available[jndex][0]],
                    [available[jndex][1], result[-1][1]]
                ]
            jndex += 1
        else:
            index += 1
            result.append(restriction[index])
    any_left = restriction[index+1:]
    if any_left:
        result.append(any_left)
    return result

available_tags = [[7, 10], [13, 15], [20, 25]]
print(available_tags)
b = [11, 13]
print(b, " Adding -> ")
add_tags(available_tags, b)
print(available_tags)