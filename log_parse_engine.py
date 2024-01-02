"""
该文件负责声网引擎相关的检测工作，包括如下检测内容：
done--1、相邻两次创建和相邻两次销毁引擎的间隔(warning)
    如果存在相邻两次创建或相邻两次销毁的时间间隔很短的情况,这块是有问题的需要check。
done--2、共创建或共销毁引擎多少次(info)
    会输出整个过程中引擎创建和销毁的次数
done--3、创建引擎和销毁引擎的次数是否匹配(warning)
    我们建议创建引擎和销毁引擎理论上应该是对应的,如果创建和销毁的次数不一致,那么需要check。
done--4、引擎是否存在多次创建和销毁的情况(warning)
    我们建议一个app的生命周期内最好只创建和销毁一次RtcEngine,所以如果是有多次的情况,需要check。
"""

from datetime import datetime
import re
import log_parse_util
import log_level
import log_constants

from log_parse_handle import LogHandle

# if __name__ == "__main__":
logHandle = LogHandle()

is_find = False

def check_engine_creation_and_destruction(t_lines):
    createTimestamps = []
    destroyTimestamps = []
    def process_engine_lines(keyword_lines, action_name):
        if keyword_lines:
            for line in keyword_lines:
                match = re.search(log_constants.TIME_PATTERN, line)
                if match:
                    extracted_time = match.group(1)
                    # 解析字符串为 datetime 对象
                    date_time = datetime.strptime(extracted_time, log_constants.DATA_FORMAT)
                    # 毫秒
                    milliseconds = int(date_time.timestamp() * 1000 + date_time.microsecond / 1000)
                    if '创建' == action_name:
                        createTimestamps.append(milliseconds)
                        if not is_find:
                            check_engine_intervals(createTimestamps, action_name)
                    elif '销毁' == action_name:
                        destroyTimestamps.append(milliseconds)
                        if not is_find:
                            check_engine_intervals(destroyTimestamps, action_name)
                    last_time = milliseconds
                    # logHandle.custom_print(log_level.LogLevel.INFO, f"在 {extracted_time} {action_name}声网引擎")
                    if logHandle.print_detail == "all":
                        logHandle.custom_print(log_level.LogLevel.INFO, f"  {line.strip()}")
                else:
                    logHandle.custom_print(log_level.LogLevel.ERROR, "解析时间信息的时候出错了")

    # 比较数组中的时间是否相近
    def check_engine_intervals(timestamps, action_name):
        for i in range(1, len(timestamps)):
            interval = timestamps[i] - timestamps[i - 1]
            if interval < 0.5:
                logHandle.custom_print(log_level.LogLevel.WARNING, f"存在两次{action_name}引擎的间隔小于500ms,请检查下是否需要频繁创建")
                logHandle.custom_print(log_level.LogLevel.WARNING, f"请检查{timestamps[i]}和{timestamps[i - 1]}这两次，这里只列举一次")
                global is_find
                is_find = True
                break

    engineKeyword_lines_init = [line for line in t_lines if re.search(log_constants.KEY_ENGINE_CREATE, line, re.IGNORECASE)]
    logHandle.custom_print(log_level.LogLevel.INFO, f"引擎共创建: {len(engineKeyword_lines_init)} 次")
    if (len(engineKeyword_lines_init) > 0):
        logHandle.custom_print(log_level.LogLevel.INFO, "创建引擎的详细信息如下")
    process_engine_lines(engineKeyword_lines_init, "创建")

    engineKeyword_lines_release = [line for line in t_lines if re.search(log_constants.KEY_ENGINE_DESTROY, line, re.IGNORECASE)]
    logHandle.custom_print(log_level.LogLevel.INFO, f"引擎共销毁: {len(engineKeyword_lines_release)} 次")
    if (len(engineKeyword_lines_release)):
        logHandle.custom_print(log_level.LogLevel.INFO, "销毁引擎的详细信息如下")
    process_engine_lines(engineKeyword_lines_release, "销毁")

    if len(engineKeyword_lines_init) != len(engineKeyword_lines_release):
        logHandle.custom_print(log_level.LogLevel.WARNING, "创建和销毁引擎的次数不匹配,请检查下。")

    if len(engineKeyword_lines_init) > 1 or len(engineKeyword_lines_release) > 1:
        logHandle.custom_print(log_level.LogLevel.WARNING, "提示：引擎的创建或销毁执行一次为最佳！")

    if len(engineKeyword_lines_init) == len(engineKeyword_lines_release):
        log_parse_util.has_adjacent_difference_one(createTimestamps, destroyTimestamps, "存在创建引擎和销毁引擎时间间隔很小的情况")
    else:
        log_parse_util.has_adjacent_difference_one2(createTimestamps, destroyTimestamps, "创建引擎和销毁引擎综合存在间隔很小的情况，检查即可")
    logHandle.custom_print(log_level.LogLevel.PARTING, "---- 以上是sdk引擎信息的体检报告 ----\n")