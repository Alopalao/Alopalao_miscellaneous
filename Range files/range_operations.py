import time
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
    print("TAGS -> ", tags)
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

def range_intersection(
    ranges_a: list[list[int]],
    ranges_b: list[list[int]]
) -> list[list[int]]:
    """Returns the intersection between two list
    of ranges"""
    result = []
    a_i, b_i = 0, 0
    while a_i < len(ranges_a) and b_i < len(ranges_b):
        fst_a, snd_a = ranges_a[a_i]
        fst_b, snd_b = ranges_b[b_i]
        # Moving forward with non-intersection
        if snd_a < fst_b:
            a_i += 1
        elif snd_b < fst_a:
            b_i += 1
        else:
            # Intersection
            intersection_start = max(fst_a, fst_b)
            intersection_end = min(snd_a, snd_b)
            result.append([intersection_start, intersection_end])
            if snd_a < snd_b:
                a_i += 1
            else:
                b_i += 1
    return result

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

def range_addition(
    ranges_a: list[list[int]],
    ranges_b: list[list[int]]
) -> list[list[int]]:
    """Addition between two ranges.
    Simulates the addition between two sets
    Returns the result of the adittion and a boolean"""
    result = []
    a_i = b_i = 0
    len_a = len(ranges_a)
    len_b = len(ranges_b)
    while a_i < len_a or b_i < len_b:
        if (a_i < len_a and
                (b_i >= len_b or ranges_a[a_i][1] < ranges_b[b_i][0] - 1)):
            result.append(ranges_a[a_i])
            a_i += 1
        elif (b_i < len_b and
                (a_i >= len_a or ranges_b[b_i][1] < ranges_a[a_i][0] - 1)):
            result.append(ranges_b[b_i])
            b_i += 1
        # Intersection and continuos ranges
        else:
            new_range = [
                min(ranges_a[a_i][0], ranges_b[b_i][0]),
                max(ranges_a[a_i][1], ranges_b[b_i][1])
            ]
            a_i += 1
            b_i += 1
            while a_i < len_a or b_i < len_b:
                if a_i < len_a and (ranges_a[a_i][0] <= new_range[1] + 1):
                    new_range[1] = max(ranges_a[a_i][1], new_range[1])
                    a_i += 1
                elif b_i < len_b and (ranges_b[b_i][0] <= new_range[1] + 1):
                    new_range[1] = max(ranges_b[b_i][1], new_range[1])
                    b_i += 1
                # No more intersection
                else:
                    break
            result.append(new_range)
    return result

available_tags = [[7, 10], [13, 15], [20, 25]]
tags_ex = [[7, 9], [14, 15], [21, 23]]
#print(available_tags)
#b = [11, 13]
#print(b, " Adding -> ")
#add_tags(available_tags, b)
#print(available_tags)

# Record the start time
start_time = time.time()

for i in tags_ex:
    take_tags(available_tags, i)

# Record the end time
end_time = time.time()

print(available_tags)
# Calculate the elapsed time
elapsed_time = end_time - start_time
print("TIME -> ", elapsed_time)