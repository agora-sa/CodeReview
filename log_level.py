from enum import Enum, auto

class LogLevel(Enum):
    # 一般信息
    INFO = auto()
    # 警告信息，也是体检结论，重点关注
    WARNING = auto()
    # 错误信息，重点关注
    ERROR = auto()
    # 重要信息，提示作用
    CRITICAL = auto()
    # 模块分割线，无需关注
    PARTING = auto()
