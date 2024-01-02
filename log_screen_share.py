import re
import log_level
import log_constants
from datetime import datetime
from log_parse_handle import LogHandle

# if __name__ == "__main__":
logHandle = LogHandle()

# 屏幕共享相关体检
def check_screen_share(t_lines):
    check_request_success(t_lines)

def check_request_success(t_lines):
    ssrsKeyword_lines = [line for line in t_lines if re.search(log_constants.KEY_REQ_SUCCESS, line, re.IGNORECASE)]
    ssrsKeyword_count = len(ssrsKeyword_lines)
    if ssrsKeyword_count <= 1:
        logHandle.custom_print(log_level.LogLevel.INFO, "屏幕分享请求成功")
        return
    logHandle.custom_print(log_level.LogLevel.WARNING, f"屏幕分享请求成功 {ssrsKeyword_count}次")
    if ssrsKeyword_lines:
            if logHandle.print_detail != "all":
                match = re.search(log_constants.TIME_PATTERN, ssrsKeyword_lines[ssrsKeyword_count - 1])
                if match:
                    extracted_time = match.group(1)
                    # 解析字符串为 datetime 对象
                    date_time = datetime.strptime(extracted_time, log_constants.DATA_FORMAT)
                    logHandle.custom_print(log_level.LogLevel.WARNING, f"最后一次屏幕分享请求成功是在:{date_time}")
                return
            logHandle.custom_print(log_level.LogLevel.INFO, "屏幕分享请求成功的详细信息如下")
            for line in ssrsKeyword_lines:
                logHandle.custom_print(log_level.LogLevel.INFO, f"{line}")
