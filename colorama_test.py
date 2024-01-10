# is_find = False

# def abc():
#     if is_find:
#         print('123')

# def bcd():
#     global is_find
#     is_find = True


# import re

# log_line = "[01/08/24 15:38:29:270][14963][A]:(00000176): ChannelProxy::emitConnStateChanged->onConnectionStateChanged(this:0x759c1e6500, state:2, reason:0)"

# # 使用正则表达式解析日志行
# pattern = r"\[(.*?)\]\[(.*?)\]\[(.*?)\]:(.*?): (.*)"
# match = re.match(pattern, log_line)

# if match:
#     date_time, process_id, log_level, log_identifier, details = match.groups()
#     print(details)

#     # 进一步解析括号中的信息
#     details_pattern = r"ChannelProxy::emitConnStateChanged->onConnectionStateChanged\(this:(.*?), state:(.*?), reason:(.*?)\)"
#     details_match = re.match(details_pattern, details)

#     if details_match:
#         this_value, state_value, reason_value = details_match.groups()

#         # 将信息存储到集合中，可以选择使用字典形式存储更有结构化
#         log_data = {
#             "日期时间": date_time,
#             "进程ID": process_id,
#             "日志级别": log_level,
#             "日志标识": log_identifier,
#             "详细信息": {
#                 "this": this_value,
#                 "state": state_value,
#                 "reason": reason_value
#             }
#         }

#         # 输出结果或进行其他操作
#         print(log_data)
#     else:
#         print("无法解析详细信息")
# else:
#     print("无法解析日志行")