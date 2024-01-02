import log_level

from colorama import init, Fore, Back, Style

"""
单例，这个类主要是操作体检报告的输出文件
"""
class LogHandle:
    _instance = None
    output_file = None
    print_detail = ''

    init()

    def __new__(cls) -> 'LogHandle':
        if not cls._instance:
            cls._instance = super(LogHandle, cls).__new__(cls)
        return cls._instance

    # 创建体检报告的文件
    def create_output_file(self, output_path):
        if output_path != "":
            self.output_file = open(output_path, 'w')
    
    # 初始化是否输出详细信息的开关参数
    # 使用的时候判断 detail="all"输出全部，detail="sample"输出简易信息，不加这个参数，默认输出sample
    def init_print_detail(self, detail):
        self.print_detail = detail

    # 执行销毁操作，这里主要是关闭文件
    def destroy(self):
        if self.output_file is not None:
            self._instance.output_file.close()

    """
    自定义体检报告输出
    设置文本颜色为红色
    red_text = "\033[91mHello, World!\033[0m
    设置文本颜色为绿色
    green_text = "\033[92mHello, World!\033[0m"
    设置文本颜色为黄色
    yellow_text = "\033[93mHello, World!\033[0m"
    设置文本颜色为蓝色
    blue_text = "\033[94mHello, World!\033[0m"
    """
    def custom_print(self, level, info):
        if level == log_level.LogLevel.INFO:
            if (self.print_detail != 'warning'):
                if self.output_file is None:
                    print(Fore.BLUE + info)
                else:
                    self.output_file.write(info + "\n")
        elif level == log_level.LogLevel.WARNING:
            if self.output_file is None:
                print("【WARNING】" + Fore.YELLOW + info)
            else:                
                self.output_file.write("【WARNING】" + info+ "\n")
        elif level == log_level.LogLevel.PARTING:
            if (self.print_detail != 'warning'):
                if self.output_file is None:
                    print(Fore.BLACK + info)
                else:
                    self.output_file.write(info+ "\n")
        elif level == log_level.LogLevel.ERROR:
            if self.output_file is None:
                print(Fore.RED + info)
            else:
                self.output_file.write(info+ "\n")
