from typing import Optional

# a = [[10, 20], [800, 3000]]
# b = [[1, 13], [19, 801], [803, 808], [2000, 4096]]
def can_restrict(available: list[list[int, int]], new_restriction: list[list[int, int]]) -> Optional[str]:
    """Check if new_restriction can be applied when there is available"""
    """Returns an early False when a gap is detected"""
    """Simulates sliding window O(n)"""
    
    # Check [[1...]] and [[...4096]]
    if available[0][0] != 1:
        if not (new_restriction[0][0] == 1 and new_restriction[0][1] + 1 >= available[0][0]):
            print(f"There is a gap at the beginning: available_tag:{available[0]} and tag_range:{new_restriction[0]}. "\
                  f"Tags can be {[1, 4095]}")
            return False
    if available[-1][1] != 4095:
        if not (new_restriction[-1][1] == 4095 and new_restriction[-1][0] <= available[-1][1] + 1):
            print(f"There is a gap at the end: available_tag:{available[-1]} and tag_range:{new_restriction[-1]}. "\
                  f"Tags can be {[1, 4095]}")
            return False

    # Corner case
    ava_n = len(available)
    if ava_n == 1:
        return True

    rest_n = len(new_restriction)
    ava_i, rest_i = 0, 0
    while rest_i < rest_n:
        if new_restriction[rest_i][0] <= available[ava_i][1] + 1:
            #print(1)
            while ava_i + 1 < ava_n:
                #print(new_restriction[rest_i], " - ", available[ava_i])
                #print(3)
                if new_restriction[rest_i][1] + 1 >= available[ava_i+1][0]:
                    #print(4)
                    ava_i += 1
                elif new_restriction[rest_i][1] <= available[ava_i][1]:
                    #print(5)
                    break
                else:
                    #print(6)
                    print(f"Gap detected available_tag:{[available[ava_i], available[ava_i+1]]} and tag_range:{new_restriction[rest_i]}")
                    return False
            rest_i += 1
        else:
            #print(2)
            print(f"Gap detected available_tag:{[available[ava_i], available[ava_i+1]]} and tag_range:{new_restriction[rest_i]}")
            return False
    return True

#a = [[4, 5], [7,9], [11, 16], [21, 24]]
#b = [[1,3], [8,10], [12,15], [18,19], [24,30]]
def range_intersection(available, tag_ranges):
    """Checks for intersection between list of ranges"""
    result = []
    ava_i, tag_i = 0, 0
    
    while ava_i < len(available) and tag_i < len(tag_ranges):
        fst_ava, snd_ava = available[ava_i]
        fst_tag, snd_tag = tag_ranges[tag_i]

        # Moving forward with non-intersection
        if snd_ava < fst_tag:
            ava_i += 1
        elif snd_tag < fst_ava:
            tag_i += 1
        else:
            # Intersection
            intersection_start = max(fst_ava, fst_tag)
            intersection_end = min(snd_ava, snd_tag)
            result.append([intersection_start, intersection_end])
            
            if snd_ava < snd_tag:
                ava_i += 1
            else:
                tag_i += 1
    return result
global_range = [1, 4095]

#a = [[4, 5], [7,9], [11, 16], [21, 24]]
#b = [[1,3], [8,10], [12,15], [18,19], [24,30]]

#a = [[4, 5], [11, 14], [21, 24]]
#b = [[1, 3], [6, 20], [24, 30]]

#a = [[1, 30], [50, 60], [80, 90], [100, 150]]
#b = [[25, 55], [59, 79], [91, 120], [130, 4095]]

a = [[3, 5], [7,9], [11, 16], [21, 23], [25,25], [27,28], [30,30]]
b = [[1,3],[6,6],[8,8],[10,10],[12,13],[15,15],[17,20],[22,30]]

print(range_intersection(a, b))
print(can_restrict(a,b))
