import re
import log_level
from datetime import datetime

from log_parse_handle import LogHandle

date_format = "%m/%d/%y %H:%M:%S:%f"
TIME_PATTERN = r'\[(\d{2}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}:\d{3})\]'

# 定义匹配的正则表达式
pattern = r'"rtc\.channel_profile":(\d+)'
# 定义匹配的正则表达式
kfi_pattern = r'"che\.video\.keyFrameInterval":(\d+)'

# if __name__ == "__main__":
logHandle = LogHandle()

# 设置了通信模式
channel_profile_key = "rtc.channel_profile"
# 设置硬编 - 待确认
enable_hw_encoder_key = "engine.video.enable_hw_encoder"
# 关键帧间隔
keyFrameInterval_key = "che.video.keyFrameInterval"


# 检查日志中带有[rp]相关的关键日志信息
# 其中t_lines 里面包含的都是带有关键字[rp]信息的所有行
def check_rp_info(t_lines):
    check_channel_profile(t_lines)
    check_key_frame_interval(t_lines)

# 对[rp]中的channel_profile进行体检
def check_channel_profile(t_lines):
    cpKeyword_lines = [line for line in t_lines if re.search(channel_profile_key, line, re.IGNORECASE)]
    cpKeyword_count = len(cpKeyword_lines)
    logHandle.custom_print(log_level.LogLevel.INFO, f"共设置通信模式:{cpKeyword_count}次")

    channel_profile = set()
    if cpKeyword_count > 0:
        for line in cpKeyword_lines:
            # 使用正则表达式进行匹配
            match = re.search(pattern, line)
            # 如果匹配成功，则打印匹配结果
            if match:
                channel_profile.add(match.group(1))
            else:
                logHandle.custom_print(log_level.LogLevel.WARNING, "没有设置过通信模式")

        match = re.search(TIME_PATTERN, cpKeyword_lines[cpKeyword_count - 1])
        if match:
            extracted_time = match.group(1)
            # 解析字符串为 datetime 对象
            date_time = datetime.strptime(extracted_time, date_format)
    if (len(channel_profile) == 1):
        logHandle.custom_print(log_level.LogLevel.WARNING, f"用户只设置过直播模式，最后一次设置是在{date_time}")
    else:
        logHandle.custom_print(log_level.LogLevel.WARNING, "用户设置过多种通信模式即,分别是:channel_profile.")
        for value in channel_profile:
            logHandle.custom_print(log_level.LogLevel.WARNING, f"{value}")

# 对[rp]中的keyFrameInterval进行体检
def check_key_frame_interval(t_lines):
    kiKeyword_lines = [line for line in t_lines if re.search(keyFrameInterval_key, line, re.IGNORECASE)]
    kiKeyword_count = len(kiKeyword_lines)

    if kiKeyword_count == 0:
        logHandle.custom_print(log_level.LogLevel.INFO, f"没有设置过关键帧间隔")
        return

    keyFrameInterval = set()
    if kiKeyword_count > 0:
        for line in kiKeyword_lines:
            # 使用正则表达式进行匹配
            match = re.search(kfi_pattern, line)
            # 如果匹配成功，则打印匹配结果
            if match:
                keyFrameInterval.add(match.group(1))
            else:
                logHandle.custom_print(log_level.LogLevel.ERROR, "未找到 che.video.keyFrameInterval 的值")

        match = re.search(TIME_PATTERN, kiKeyword_lines[kiKeyword_count - 1])
        if match:
            extracted_time = match.group(1)
            # 解析字符串为 datetime 对象
            date_time = datetime.strptime(extracted_time, date_format)

    if (len(keyFrameInterval) == 1):
        list_data = list(keyFrameInterval)
        logHandle.custom_print(log_level.LogLevel.WARNING, f"用户只设置过关键帧间隔是{list_data[0]},最后一次设置是在{date_time}")
    else:
        logHandle.custom_print(log_level.LogLevel.WARNING, "用户设置过多个关键帧间隔，分别是：")
        for value in keyFrameInterval:
            logHandle.custom_print(log_level.LogLevel.WARNING, f"{value}")