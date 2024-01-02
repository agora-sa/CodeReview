"""
该文件检查mute相关的信息，包括如下：
1、muteLocalVideoStream相关
    统计muteLocalVideoStream这个操作一共执行了多少次 且打印详细信息（info）
    check最后一次执行mute操作的时间和详细信息（info）
2、muteLocalAudioStream相关
    统计muteLocalAudioStream这个操作一共执行了多少次 且打印详细信息（info）
    check最后一次执行mute操作的时间和详细信息（info）
3、muteRemoteVideoStream相关
    统计muteRemoteVideoStream这个操作一共执行了多少次 且打印详细信息（info）
    check最后一次执行mute操作的时间和详细信息（info）
4、muteRemoteAudioStream相关
    统计muteRemoteAudioStream这个操作一共执行了多少次 且打印详细信息（info）
    check最后一次执行mute操作的时间和详细信息（info）
"""

import re
import log_level
import log_constants
from log_parse_handle import LogHandle

# if __name__ == "__main__":
logHandle = LogHandle()

def check_av_mute_update(t_lines):
    check_mute_local_video(t_lines)
    check_mute_local_audio(t_lines)
    check_mute_romote_video(t_lines)
    check_mute_remote_audio(t_lines)
    logHandle.custom_print(log_level.LogLevel.PARTING, "---- 以上是订阅/发布流信息的体检报告 ----\n")

# 调用muteLocalVideoStream的次数及最后一个元素
def check_mute_local_video(t_lines):
    mutelvKeyword_lines = [line for line in t_lines if re.search(log_constants.KEY_MUTE_LOCAL_VIDEO, line, re.IGNORECASE)]
    mutelvKeyword_count = len(mutelvKeyword_lines)
    logHandle.custom_print(log_level.LogLevel.INFO, f"调用muteLocalVideoStream共: {mutelvKeyword_count} 次")

    if mutelvKeyword_count > 0:
        logHandle.custom_print(log_level.LogLevel.INFO, f"最后一次调用如下")
        logHandle.custom_print(log_level.LogLevel.INFO, f"{mutelvKeyword_lines[mutelvKeyword_count-1]}")

# 调用muteLocalAudioStream的次数及最后一个元素
def check_mute_local_audio(t_lines):
    mutelaKeyword_lines = [line for line in t_lines if re.search(log_constants.KEY_MUTE_LOCAL_AUDIO, line, re.IGNORECASE)]
    mutelaKeyword_count = len(mutelaKeyword_lines)
    logHandle.custom_print(log_level.LogLevel.INFO, f"调用muteLocalAudioStream共: {mutelaKeyword_count} 次")

    if mutelaKeyword_count > 0:
        logHandle.custom_print(log_level.LogLevel.INFO, f"最后一次调用如下")
        logHandle.custom_print(log_level.LogLevel.INFO, f"{mutelaKeyword_lines[mutelaKeyword_count-1]}")

# 调用muteRemoteVideoStream的次数及最后一个元素
def check_mute_romote_video(t_lines):
    mutervKeyword_lines = [line for line in t_lines if re.search(log_constants.KEY_MUTE_REMOTE_VIDEO, line, re.IGNORECASE)]
    mutervKeyword_count = len(mutervKeyword_lines)
    logHandle.custom_print(log_level.LogLevel.INFO, f"调用muteRemoteVideoStream共: {mutervKeyword_count} 次")

    if mutervKeyword_count > 0:
        logHandle.custom_print(log_level.LogLevel.INFO, f"最后一次调用如下")
        logHandle.custom_print(log_level.LogLevel.INFO, f"{mutervKeyword_lines[mutervKeyword_count-1]}")

# 调用muteRemoteAudioStream的次数及最后一个元素
def check_mute_remote_audio(t_lines):
    muteraKeyword_lines = [line for line in t_lines if re.search(log_constants.KEY_MUTE_REMOTE_AUDIO, line, re.IGNORECASE)]
    muteraKeyword_count = len(muteraKeyword_lines)
    logHandle.custom_print(log_level.LogLevel.INFO, f"调用muteLocalAudioStream共: {muteraKeyword_count} 次")

    if muteraKeyword_count > 0:
        logHandle.custom_print(log_level.LogLevel.INFO, f"最后一次调用如下")
        logHandle.custom_print(log_level.LogLevel.INFO, f"{muteraKeyword_lines[muteraKeyword_count-1]}")