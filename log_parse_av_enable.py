
import re
import log_level
import log_constants
from log_parse_handle import LogHandle

# if __name__ == "__main__":
logHandle = LogHandle()

# 主要检查一些比较耗时的操作
def check_av_enable(t_lines):

    check_enable_local_video(t_lines)
    check_enable_local_audio(t_lines)
    check_enable_audio(t_lines)
    check_enable_video(t_lines)
    check_disable_audio(t_lines)
    check_disable_video(t_lines)
    logHandle.custom_print(log_level.LogLevel.PARTING, "---- 以上是av_enable信息的体检报告 ----\n")
    

# 调用enableLocalVideo的次数及最后一个元素
def check_enable_local_video(t_lines):
    elvKeyword_lines = [line for line in t_lines if re.search(log_constants.KEY_ENABLE_LOCAL_VIDEO, line, re.IGNORECASE)]
    evlKeyword_count = len(elvKeyword_lines)
    logHandle.custom_print(log_level.LogLevel.INFO, f"调用enableLocalVideo共: {evlKeyword_count} 次")
    print_over_time_warning(evlKeyword_count, "enableLocalVideo")

    if evlKeyword_count > 0:
        logHandle.custom_print(log_level.LogLevel.INFO, f"最后一次调用信息如下\n {elvKeyword_lines[evlKeyword_count-1]}")

# 调用enableLocalAudio的次数及最后一个元素
def check_enable_local_audio(t_lines):
    elaKeyword_lines = [line for line in t_lines if re.search(log_constants.KEY_ENABLE_LOCAL_AUDIO, line, re.IGNORECASE)]
    elaKeyword_count = len(elaKeyword_lines)
    logHandle.custom_print(log_level.LogLevel.INFO, f"调用enableLocalAudio共: {elaKeyword_count} 次")
    print_over_time_warning(elaKeyword_count, "enableLocalAudio")

    if elaKeyword_count > 0:
        logHandle.custom_print(log_level.LogLevel.INFO, "最后一次调用如下")
        logHandle.custom_print(log_level.LogLevel.INFO, f"{elaKeyword_lines[elaKeyword_count-1]}")

# 调用enableAudio的次数及最后一个元素
def check_enable_audio(t_lines):
    eaKeyword_lines = [line for line in t_lines if re.search(log_constants.KEY_ENABLE_AUDIO, line, re.IGNORECASE)]
    eaKeyword_count = len(eaKeyword_lines)
    logHandle.custom_print(log_level.LogLevel.INFO, f"调用enableAudio共: {eaKeyword_count} 次")
    print_over_time_warning(eaKeyword_count, "enableAudio")

    if eaKeyword_count > 0:
        logHandle.custom_print(log_level.LogLevel.INFO, f"最后一次调用如下")
        logHandle.custom_print(log_level.LogLevel.INFO, f"{eaKeyword_lines[eaKeyword_count-1]}")

# 调用enableVideo的次数及最后一个元素
def check_enable_video(t_lines):
    evKeyword_lines = [line for line in t_lines if re.search(log_constants.KEY_ENABLE_VIDEO, line, re.IGNORECASE)]
    evKeyword_count = len(evKeyword_lines)
    logHandle.custom_print(log_level.LogLevel.INFO, f"调用enableVideo共: {evKeyword_count} 次")
    print_over_time_warning(evKeyword_count, "enableVideo")

    if evKeyword_count > 0:
        logHandle.custom_print(log_level.LogLevel.INFO, f"最后一次调用如下")
        logHandle.custom_print(log_level.LogLevel.INFO, f"{evKeyword_lines[evKeyword_count-1]}")

# 调用disableAudio的次数及最后一个元素
def check_disable_audio(t_lines):
    daKeyword_lines = [line for line in t_lines if re.search(log_constants.KEY_DISABLE_AUDIO, line, re.IGNORECASE)]
    daKeyword_count = len(daKeyword_lines)
    logHandle.custom_print(log_level.LogLevel.INFO, f"调用disableAudio共: {daKeyword_count} 次")
    print_over_time_warning(daKeyword_count, "disableAudio")

    if daKeyword_count > 0:
        logHandle.custom_print(log_level.LogLevel.INFO, f"最后一次调用如下")
        logHandle.custom_print(log_level.LogLevel.INFO, f"{daKeyword_lines[daKeyword_count-1]}")

# 调用disableVideo的次数及最后一个元素
def check_disable_video(t_lines):
    daKeyword_lines = [line for line in t_lines if re.search(log_constants.KEY_DISABLE_VIDEO, line, re.IGNORECASE)]
    daKeyword_count = len(daKeyword_lines)
    logHandle.custom_print(log_level.LogLevel.INFO, f"调用disableVideo共: {daKeyword_count} 次")
    print_over_time_warning(daKeyword_count, "disableVideo")

    if daKeyword_count > 0:
        logHandle.custom_print(log_level.LogLevel.INFO, f"最后一次调用如下")
        logHandle.custom_print(log_level.LogLevel.INFO, f"{daKeyword_lines[daKeyword_count-1]}")

# 检查这些api的调用次数是否超过了某一个值，超过后警告
def print_over_time_warning(count, apiStr):
    if (count > 5):
        logHandle.custom_print(log_level.LogLevel.WARNING, f"检查下是否有必要频繁调用{apiStr}接口")