from datetime import datetime
import re

import log_level
import log_parse_util
import log_constants
from log_parse_handle import LogHandle

# if __name__ == "__main__":
logHandle = LogHandle()

# 频道操作相关
# 1、相邻两次加入和相邻两次离开频道的时间间隔
# 2、共加入或离开频道多少次
# 3、加入频道和离开频道的次数是否匹配
def check_channel_join_and_leave(t_lines):
    joinTimestamps = []
    leaveTimestamps = []
    def process_channel_lines(keyword_lines, action_name):
        if keyword_lines:
            for line in keyword_lines:
                match = re.search(log_constants.TIME_PATTERN, line)
                if match:
                    extracted_time = match.group(1)
                    # 解析字符串为 datetime 对象
                    date_time = datetime.strptime(extracted_time, log_constants.DATA_FORMAT)
                    # 毫秒
                    milliseconds = int(date_time.timestamp() * 1000 + date_time.microsecond / 1000)

                    if '加入' == action_name:
                        joinTimestamps.append(milliseconds)
                        check_channel_intervals(joinTimestamps, action_name)
                    elif '离开' == action_name:
                        leaveTimestamps.append(milliseconds)
                        check_channel_intervals(leaveTimestamps, action_name)
                
                    # logHandle.custom_print(log_level.LogLevel.INFO, f"在 {extracted_time} {action_name}声网频道")
                    if logHandle.print_detail == "all":
                        logHandle.custom_print(log_level.LogLevel.INFO, f" {line.strip()}")
                else:
                    print("解析时间的时候出错了！")

    # 比较数组中的时间是否相近
    def check_channel_intervals(timestamps, action_name):
        for i in range(1, len(timestamps)):
            interval = timestamps[i] - timestamps[i - 1]
            if interval < 0.5:
                logHandle.custom_print(log_level.LogLevel.WARNING, f"存在两次{action_name}频道的间隔小于500ms的情况,请检查下。")

    joinChannel_lines = [line for line in t_lines if re.search(log_constants.KEY_JOIN_CHANNEL, line, re.IGNORECASE)]
    logHandle.custom_print(log_level.LogLevel.INFO, f"共加入频道: {len(joinChannel_lines)} 次")
    if (len(joinChannel_lines) > 0):
        logHandle.custom_print(log_level.LogLevel.INFO, f"加入频道的详细信息如下")
    process_channel_lines(joinChannel_lines, "加入")

    successKeyword_lines = [line for line in t_lines if re.search(log_constants.KEY_JOIN_SUCCESS, line, re.IGNORECASE)]
    success_count = len(successKeyword_lines)
    logHandle.custom_print(log_level.LogLevel.INFO, f"加入频道成功共: {success_count} 次")
    if (success_count == len(joinChannel_lines)):
        logHandle.custom_print(log_level.LogLevel.INFO, "加入频道成功次数 = 加入频道次数，此项忽略")
    else:
        logHandle.custom_print(log_level.LogLevel.WARNING, "加入频道成功次数!=加入频道次数,请检查频道是否加入成功,可以看下onError回调中的原因")

    leaveChannel_lines = [line for line in t_lines if re.search(log_constants.KEY_LEAVE_CHANNEL, line, re.IGNORECASE)]
    logHandle.custom_print(log_level.LogLevel.INFO, f"共离开频道: {len(leaveChannel_lines)} 次")
    if (len(leaveChannel_lines) > 0):
        logHandle.custom_print(log_level.LogLevel.INFO, f"离开频道的详细信息如下")
    process_channel_lines(leaveChannel_lines, "离开")

    if len(joinChannel_lines) != len(leaveChannel_lines):
        logHandle.custom_print(log_level.LogLevel.WARNING, "加入和离开频道的次数不匹配，请检查下。")

    if len(joinChannel_lines) == len(leaveChannel_lines):
        log_parse_util.has_adjacent_difference_one(joinTimestamps, joinTimestamps, "存在加入频道和离开频道时间间隔很小的情况")
    else:
        log_parse_util.has_adjacent_difference_one2(joinTimestamps, joinTimestamps, "加入频道和离开频道综合存在间隔很小的情况，检查即可")
    logHandle.custom_print(log_level.LogLevel.PARTING, "---- 以上是频道信息的体检报告 ----\n")