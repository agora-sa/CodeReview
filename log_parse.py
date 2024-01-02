#coding=utf-8

"""
日志解析的主入口，这个文件中负责读取文件，进行主文件的相关操作
读取文件后进行分模块进行日志解析,每个模块都是一个独立的python文件

使用方式：
python3 log_parse.py /xxx/xxx.log, 其中 /xxx/xx.log为要解析的log文件的绝对路径

本工程目前是单线程运行模式，后面看具体的运行情况在看是否调整线程模式
"""

import argparse
import log_level
import sys
from ast import arg

import log_parse_basic
import log_parse_engine
import log_parse_channel
import log_parse_av_enable
import log_parse_mute_update
import log_screen_share
import log_call_back

from log_parse_handle import LogHandle

# if __name__ == "__main__":
logHandle = LogHandle()

def analyze_log(log_file_path):
    try:
        # 打开文件，只读
        with open(log_file_path, 'r') as log_file:
            lines = log_file.readlines()
            start_process_log(lines)
    except FileNotFoundError:
        logHandle.print_detail(log_level.LogLevel.ERROR, f"File not found: {log_file_path}")
    except Exception as e:
        logHandle.print_detail(log_level.LogLevel.ERROR, f"An error occurred: {e}")
    # 关闭file
    logHandle.destroy()

def start_process_log(t_lines):
    if not t_lines:
        logHandle.custom_print(log_level.LogLevel.WARNING, "读取文件后解析出错")
        return
    # 基本信息相关体检
    log_parse_basic.check_log_basic_info(t_lines)
    # 声网引擎相关体检
    log_parse_engine.check_engine_creation_and_destruction(t_lines)
    # 声网频道相关体检
    log_parse_channel.check_channel_join_and_leave(t_lines)
    # av_enable相关体检
    log_parse_av_enable.check_av_enable(t_lines)
    # mute & updateChannelMediaOption相关体检
    log_parse_mute_update.check_av_mute_update(t_lines)
    # 屏幕分享相关体检
    log_screen_share.check_screen_share(t_lines)
    # 声网回调相关
    log_call_back.check_agora_call_back(t_lines)

# main
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="log file analyzer")
    # 添加命令行参数
    # python3 log_parse.py -h 查看参数的帮助信息
    # 要解析的日志文件的绝对路径，不传会print提示信息
    parser.add_argument('-f', '--input', help='The input file path.')
    # 体检报告的文件输出路径，有这个路径就输出到文件，没有就直接print的控制台
    parser.add_argument('-o', '--output', help='The output file path.')
    # 输出日志的详细程度，支持三种模式
    # 'all'就是输出全部的体检信息。
    # 'sample'输出叫简洁的体检信息。
    # 'warning'只输出WARNING+的体检信息。
    parser.add_argument('-d', '--detail', help='print detail info or no.')
    args = parser.parse_args()

    input_path = "" if args.input is None else args.input
    if (input_path == ''):
        print('您要解析的文件，给一个？')
        print('您可以类似这样做：python3 log_parse.py -f /xx/xx.log -o /xx/xx.log -d all|sample|warning')
        sys.exit()

    output_path = "" if args.output is None else args.output
    logHandle.create_output_file(output_path)
    detail_info = "" if args.detail is None else args.detail
    logHandle.init_print_detail(detail_info)

    # 开始日志文件全面体检
    analyze_log(args.input)
