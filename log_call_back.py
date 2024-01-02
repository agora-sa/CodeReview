import re
import log_level
import log_constants
from datetime import datetime
from log_parse_handle import LogHandle

# if __name__ == "__main__":
logHandle = LogHandle()

# 声网回调相关的体检
def check_agora_call_back(t_lines):
    # 检查onFirstRemoteAudioFrame
    check_first_remote_audio(t_lines)
    # 检查onFirstRemoteVideoFrame
    check_first_remote_video(t_lines)
    # 检查onFirstRemoteAudioDecoded
    check_first_remote_audio_decoded(t_lines)
    # 检查onFirstRemoteVideoDecoded
    check_first_remote_video_decoded(t_lines)
    # 检查onUserJoined
    check_user_joined(t_lines)
    # 检查成功切换用户角色
    check_changed_role_success(t_lines)

def check_first_remote_audio(t_lines):
    check_first_remote_av(t_lines, log_constants.KEY_ON_FIRST_REMOTE_AUDIO, "音频首帧")

def check_first_remote_video(t_lines):
    check_first_remote_av(t_lines, log_constants.KEY_ON_FIRST_REMOTE_VIDEO, "视频首帧")

def check_first_remote_audio_decoded(t_lines):
    check_first_remote_av(t_lines, log_constants.KEY_ON_FIRST_REMOTE_AUDIO_DECODED, "音频首帧解码")

def check_first_remote_video_decoded(t_lines):
    check_first_remote_av(t_lines, log_constants.KEY_ON_FIRST_REMOTE_VIDEO_DECODED, "视频首帧解码")
    

# 检测关于音视频首帧渲染和首帧回调的相关信息
def check_first_remote_av(t_lines, key, text):
    fraKeyword_lines = [line for line in t_lines if re.search(key, line, re.IGNORECASE)]
    fraKeyword_count = len(fraKeyword_lines)
    if fraKeyword_count < 1:
        if key == log_constants.KEY_ON_FIRST_REMOTE_AUDIO:
            logHandle.custom_print(log_level.LogLevel.WARNING, f"没有收到{text},请检查是否调用了setupRemoteAudio或者是否成功加入频道")
        elif key == log_constants.KEY_ON_FIRST_REMOTE_VIDEO:
            logHandle.custom_print(log_level.LogLevel.WARNING, f"没有收到{text},请检查是否调用了setupRemoteVideo或者是否成功加入频道")
        elif key == log_constants.KEY_ON_FIRST_REMOTE_AUDIO_DECODED:
            logHandle.custom_print(log_level.LogLevel.WARNING, f"没有收到{text},可能是没收到远端的音频流或者是收到后解码失败，或者是否成功加入频道？")
        elif key == log_constants.KEY_ON_FIRST_REMOTE_VIDEO_DECODED:
            logHandle.custom_print(log_level.LogLevel.WARNING, f"没有收到{text},可能是没收到远端的视频流或者是收到后解码失败，或者是否成功加入频道？")
        return
    logHandle.custom_print(log_level.LogLevel.WARNING, f"收到{text}{fraKeyword_count}次")

    fraTimestamps = []
    if fraKeyword_lines:
            if logHandle.print_detail != "all":
                match = re.search(log_constants.TIME_PATTERN, fraKeyword_lines[fraKeyword_count - 1])
                if match:
                    extracted_time = match.group(1)
                    # 解析字符串为 datetime 对象
                    date_time = datetime.strptime(extracted_time, log_constants.DATA_FORMAT)
                    # 毫秒
                    milliseconds = int(date_time.timestamp() * 1000 + date_time.microsecond / 1000)
                    fraTimestamps.append(milliseconds)
                    check_engine_intervals(fraTimestamps)
                    logHandle.custom_print(log_level.LogLevel.WARNING, f"最后一次收到{text}是在:{date_time}")
                return
            logHandle.custom_print(log_level.LogLevel.INFO, "{text}的信息如下")
            for line in fraKeyword_lines:
                logHandle.custom_print(log_level.LogLevel.INFO, f"{line}")

# 检查远端用户加入房间
def check_user_joined(t_lines):
    userId = []
    fraKeyword_lines = [line for line in t_lines if re.search(log_constants.KEY_ON_USER_JOINED, line, re.IGNORECASE)]
    fraKeyword_count = len(fraKeyword_lines)
    if fraKeyword_count < 1:
        logHandle.custom_print(log_level.LogLevel.WARNING, "没有远端用户加入过房间")
        return
    logHandle.custom_print(log_level.LogLevel.INFO, f"共有{fraKeyword_count}条远端加入房间的信息")

    for line in fraKeyword_lines:
        logHandle.custom_print(log_level.LogLevel.INFO, f"{line}")
        # 使用正则表达式匹配 userId 的值
        match = re.search(r'userId:"([^"]+)"', line)
        if match:
            # 获取匹配到的 userId
            user_id = match.group(1)
            userId.append(user_id)
            # print(f'userId: {user_id}')
        else:
            logHandle.custom_print(log_level.LogLevel.ERROR, 'No match found.')

    # 找出不同的值和其数量
    count_unique, unique_values = find_unique_values(userId)
    if count_unique > 1:
        logHandle.custom_print(log_level.LogLevel.INFO, f"有{count_unique}个远端的用户加入过房间,userid如下")
        print(unique_values)
    else:
        logHandle.custom_print(log_level.LogLevel.INFO, f"只有 {count_unique} 个远端的用户uid={unique_values[0]} 加入过房间")


# 找出userid的数组中有几个用户，分别都是谁
def find_unique_values(arr):
    unique_values = set(arr)
    count_unique = len(unique_values)
    return count_unique, list(unique_values)

# 检测角色切换成功的通知回调
# ChannelProxy::onChangeRoleSuccess->onClientRoleChanged(this:0x7f1177ac00, oldRole:1, newRole:1, newRoleLatencyLevel:2)
def check_changed_role_success(t_lines):
    crsKeyword_lines = [line for line in t_lines if re.search(log_constants.KEY_ON_CHANGED_ROLE_SUCCESS, line, re.IGNORECASE)]
    crsKeyword_count = len(crsKeyword_lines)
    if crsKeyword_count < 1:
        logHandle.custom_print(log_level.LogLevel.WARNING, "没有成功切换过角色")
        return
    logHandle.custom_print(log_level.LogLevel.INFO, f"共切换过{crsKeyword_count}次角色,信息如下")

    # 解析第一次切换角色的信息
    # 使用正则表达式匹配 oldRole、newRole 和 newRoleLatencyLevel 的值
    check_single_changed_role_info(crsKeyword_lines, 0)
    if crsKeyword_count > 1:
        # 解析最后一次切换角色的信息
        check_single_changed_role_info(crsKeyword_lines, crsKeyword_count - 1)

# 检测单次角色切换的信息
def check_single_changed_role_info(lines, index):
    match = re.search(r'oldRole:(\d+), newRole:(\d+), newRoleLatencyLevel:(\d+)', lines[index])
    if match:
        # 获取匹配到的值
        old_role = match.group(1)
        new_role = match.group(2)
        latency_level = match.group(3)
        logHandle.custom_print(log_level.LogLevel.INFO, f'第{index}次切换用户角色, oldRole: {old_role}, newRole: {new_role}, newRoleLatencyLevel: {latency_level}')
    else:
        logHandle.custom_print(log_level.LogLevel.ERROR, 'No match found.')


# 比较数组中的时间是否相近
def check_engine_intervals(timestamps, action_name):
    for i in range(1, len(timestamps)):
        interval = timestamps[i] - timestamps[i - 1]
        if interval < 0.5:
            logHandle.custom_print(log_level.LogLevel.WARNING, f"存在两次首帧回调间隔小于500ms,请检查下代码逻辑")
            logHandle.custom_print(log_level.LogLevel.WARNING, f"请检查{timestamps[i]}和{timestamps[i - 1]}这两次，这里只列举一次")
            global is_find
            is_find = True
            break