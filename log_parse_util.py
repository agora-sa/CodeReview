import log_level
from log_parse_handle import LogHandle

# if __name__ == "__main__":
logHandle = LogHandle()


# 判断两个数组中的元素是否存在对位接近的情况
def has_adjacent_difference_one(arr1, arr2, text):
    for elem1, elem2 in zip(arr1, arr2):
        if abs(elem1 - elem2) < 2:
            logHandle.custom_print(log_level.LogLevel.WARNING, f"{text}")
            return True
    return False

# 两个数组混合哦安段是否存在接近的情况
def has_adjacent_difference_one2(arr1, arr2, text):
    for elem1 in arr1:
        for elem2 in arr2:
            if abs(elem1 - elem2) == 1:
                logHandle.custom_print(log_level.LogLevel.WARNING, f"{text}")
                return True
    return False