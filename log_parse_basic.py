"""
该文件主要是为了统计日志文件的基本信息，包括如下：
1、done:日志文件的总行数
2、done:sdk的版本号以及版本号打印的次数
3、done:音视频的编码解码信息
4、todo:appid
5、todo:3A是否开启?软3a还是硬件3a
6、todo:channel_profile
7、todo:audio profile + audio scenatio
8、done:日志文件的时间区间
9、done:输出版本号及build号相关信息
"""

import re
import log_level
import log_parse_rp
from datetime import datetime
import log_constants

from log_parse_handle import LogHandle

# 定义版本号和 build 号的正则表达式
version_build_pattern = r"ver\s+(\S+)\s+build\s+(\S+)"
# 定义匹配的正则表达式，同时匹配rp和rtc\.channel_profile
cp_pattern = r'\[rp\].*?"rtc\.channel_profile":\d+|.*?\[rtc\.channel_profile\].*?"rtc\.channel_profile":\d+'


# if __name__ == "__main__":
logHandle = LogHandle()

def check_log_basic_info(t_lines):
    if not check_log_integrality(t_lines):
        logHandle.custom_print(log_level.LogLevel.WARNING, "日志文件不完整，没有加入过声网的房间")
    check_log_lines(t_lines)
    bewteen_start_end_time(t_lines)
    check_sdk_version(t_lines)
    check_channel_profile(t_lines)
    check_encode_mode(t_lines)
    check_decode_mode(t_lines)
    logHandle.custom_print(log_level.LogLevel.PARTING, "---- 以上是sdk基本信息的体检报告 ----\n")
    return True;

# 检测日志的完整性
def check_log_integrality(t_lines):
    iKeyword_lines = [line for line in t_lines if re.search(log_constants.KEY_INTEGRALITY, line, re.IGNORECASE)]
    iKeyword_count = len(iKeyword_lines)
    return True if iKeyword_count > 0 else False

# 统计日志文件的总行数
def check_log_lines(t_lines):
    total_lines = len(t_lines)
    if total_lines <= 0:
        logHandle.custom_print(log_level.LogLevel.WARNING, "日志文件是空的！")
    logHandle.custom_print(log_level.LogLevel.INFO, f"日志共: {total_lines} 行")

# 检查编码器是否重启过
def check_r下周eset_codec(t_lines):
    rcKeyword_lines = [line for line in t_lines if re.search(log_constants.KEY_RESET_CODEC, line, re.IGNORECASE)]
    rcKeyword_count = len(rcKeyword_lines)
    if rcKeyword_count <= 1:
        logHandle.custom_print(log_level.LogLevel.INFO, "编码器没有重启过")
        return
    logHandle.custom_print(log_level.LogLevel.WARNING, f"编码器重启了{rcKeyword_count}次")
    if rcKeyword_lines:
            if logHandle.print_detail != "all":
                match = re.search(log_constants.TIME_PATTERN, rcKeyword_lines[rcKeyword_count - 1])
                if match:
                    extracted_time = match.group(1)
                    # 解析字符串为 datetime 对象
                    date_time = datetime.strptime(extracted_time, log_constants.DATA_FORMAT)
                    logHandle.custom_print(log_level.LogLevel.WARNING, f"最后一次重启编码器是在:{date_time}")
                return
            logHandle.custom_print(log_level.LogLevel.INFO, "编码器重启的详细信息如下")
            for line in rcKeyword_lines:
                logHandle.custom_print(log_level.LogLevel.INFO, f"{line}")

# 检查编码方式
# hw_encoder_accelerating 0-软编、1-硬编
def check_encode_mode(t_lines):
    # 使用正则表达式匹配日志中的数字
    match = re.search(r'hw_encoder_accelerating: (\d+)', log_constants.KEY_ENCODE_MODE)
    if match:
        # 获取匹配到的数字
        value = match.group(1)
        # rint(f'hw_encoder_accelerating value: {value}')
        if value == "0":
            logHandle.custom_print(log_level.LogLevel.INFO, "编码方式:软编")
        elif value == "1":
            logHandle.custom_print(log_level.LogLevel.INFO, "编码方式:硬编")
    else:
        logHandle.custom_print(log_level.LogLevel.INFO, "没有找到使用的编码方式")

# 检查解码方式
# hw_encoder_accelerating 0-软解、1-硬解
def check_decode_mode(t_lines):
    decode_mode = "Init Succeeds, hw_decoder_accelerating: 1"
    # 使用正则表达式匹配日志中的数字
    match = re.search(r'hw_decoder_accelerating: (\d+)', log_constants.KEY_DECODE_MODE)
    if match:
        # 获取匹配到的数字
        value = match.group(1)
        # print(f'hw_decoder_accelerating value: {value}')
        if int(value) == 0:
            logHandle.custom_print(log_level.LogLevel.INFO, "解码方式:软解")
        elif int(value) == 1:
            logHandle.custom_print(log_level.LogLevel.INFO, "解码方式:硬解")
    else:
        logHandle.custom_print(log_level.LogLevel.INFO, "没有找到使用的解码方式")


# 日志文件的时间区间
def bewteen_start_end_time(t_lines):
    start_match = re.search(log_constants.TIME_PATTERN, t_lines[0])
    start_time = ''
    end_time = ''
    if start_match:
        extracted_time = start_match.group(1)
        # 解析字符串为 datetime 对象
        start_time = datetime.strptime(extracted_time, log_constants.DATA_FORMAT)
    else:
        logHandle.custom_print(log_level.LogLevel.WARNING, "没有找到开始时间")

    end_match = re.search(log_constants.TIME_PATTERN, t_lines[len(t_lines)-1])
    if end_match:
        extracted_time = end_match.group(1)
        # 解析字符串为 datetime 对象
        end_time = datetime.strptime(extracted_time, log_constants.DATA_FORMAT)
    else:
        logHandle.custom_print(log_level.LogLevel.WARNING, "没有找到结束时间")

    logHandle.custom_print(log_level.LogLevel.INFO, f"日志 从: {start_time} 到 {end_time}")

# 统计客户使用的版本号和build号相关信息
def check_sdk_version(t_lines):
    versionKeyword_lines = [line for line in t_lines if re.search(log_constants.KEY_VERSION, line, re.IGNORECASE)]
    verKeyword_count = len(versionKeyword_lines)

    # 使用正则表达式进行匹配
    match = re.search(version_build_pattern, versionKeyword_lines[0])
    # 如果匹配成功，则提取版本号和构建号
    if match:
        version = match.group(1)
        build_number = match.group(2)
        logHandle.custom_print(log_level.LogLevel.INFO, f"用户使用sdk版本号: {version}, 构建号: {build_number}")
    else:
        logHandle.custom_print(log_level.LogLevel.WARNING, "未找到版本号的build号信息")

    logHandle.custom_print(log_level.LogLevel.WARNING, f"出现版本号信息共: {verKeyword_count} 次,说明执行引擎create{int(verKeyword_count/2)}次左右")

    logHandle.custom_print(log_level.LogLevel.INFO, f"版本号和build信息如下")
    if verKeyword_count > 0:
        for line in versionKeyword_lines:
            if logHandle.print_detail == "all":
                logHandle.custom_print(log_level.LogLevel.INFO, f"  {line.strip()}")

# 检查通信模式，包括
# 一共设置多少次
# 如果都是一样的，直接将设置的通信模式输出
# 如果有不一样的，将不一样的那一次或多次的时间和设置的值输出
def check_channel_profile(t_lines):
    rpKeyword_lines = [line for line in t_lines if re.search(log_constants.KEY_RP, line, re.IGNORECASE)]
    rpKeyword_count = len(rpKeyword_lines)
    logHandle.custom_print(log_level.LogLevel.INFO, f"发现[rp]相关日志{rpKeyword_count}次")

    log_parse_rp.check_rp_info(rpKeyword_lines)