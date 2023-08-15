# -*- coding:UTF-8 -*-
"""
@author: dyy
@contact: douyaoyuan@126.com
@time: 2023/8/8 9:57
@file: blackboard.py
@desc: 提供字符打印相关的操作方法，例如彩色文字，字符对齐，表格整理和输出，光标控制，语义日期 等
"""

# -----------------colorama模块的一些常量---------------------------
# Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
# Back: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
# Style: DIM, NORMAL, BRIGHT, RESET_ALL
#

# region 导入依赖项
import os
import re
from datetime import datetime, timedelta
from enum import Enum, unique

try:
    from wcwidth import wcwidth  # 需要安装 wcwidth 模块
except ImportError as impErr:
    print("尝试导入 wcwidth 依赖时检测到异常：", impErr)
    print("尝试安装 wcwidth 模块：")
    try:
        os.system("pip install wcwidth")
    except OSError as osErr:
        print("尝试安装模块 wcwidth 时检测到异常：", osErr)
        exit(0)
    else:
        try:
            # 如果模块安装成功，则再次尝试导入依赖
            from wcwidth import wcwidth
        except Exception as expErr:
            wcwidth = None
            print("再次尝试导入 wcwidth 依赖时检测到异常：", expErr)
            exit(0)

try:
    from colorama import init, Fore, Back, Style  # 需要安装 colorama 模块

    init(autoreset=True)
except ImportError as impErr:
    print("尝试导入 colorama 依赖时检测到异常：", impErr)
    print("尝试安装 colorama 模块：")
    try:
        os.system("pip install colorama")
    except OSError as osErr:
        print("尝试安装模块 colorama 时检测到异常：", osErr)
        exit(0)
    else:
        try:
            # 如果模块安装成功，则再次尝试导入依赖
            from colorama import init, Fore, Back, Style

            init(autoreset=True)
        except Exception as expErr:
            print("再次尝试导入 colorama 依赖时检测到异常：", expErr)
            exit(0)


# endregion


@unique
class 对齐方式(Enum):
    左对齐: int = -1
    居中对齐: int = 0
    右对齐: int = 1


# region 公共方法
def 打印(*values: object, sep: str or None = None, end: str or None = None, flush: bool = ...) -> None:
    print(*values,
          sep=sep,
          end=end,
          flush=flush)


def 显示宽度(内容: str) -> int:
    if not 内容:
        return 0
    颜色控制字匹配模式: str = r'\033\[\d+m'
    内容整理: str = re.sub(颜色控制字匹配模式, '', str(内容))
    if 内容整理:
        return sum([wcwidth(字符) for 字符 in 内容整理])
    else:
        return 0


def 镜像字符(字符: str) -> str:
    镜像字典: dict = {None: None,
                  '<': '>',
                  '>': '<',
                  '/': '\\',
                  '\\': '/',
                  '[': ']',
                  ']': '[',
                  '(': ')',
                  ')': '(',
                  '《': '》',
                  '》': '《',
                  '〈': '〉',
                  '«': '»',
                  '‹': '›',
                  '⟨': '⟩',
                  '〉': '〈',
                  '»': '«',
                  '›': '‹',
                  '⟩': '⟨',
                  '（': '）',
                  '）': '（',
                  '↗': '↖',
                  '↖': '↗',
                  '↙': '↘',
                  '↘': '↙',
                  'd': 'b',
                  'b': 'd',
                  '⇐': '⇒',
                  '⇒': '⇐'}

    if 字符 and 字符 in 镜像字典:
        return 镜像字典[字符]
    else:
        return 字符


# region terminal 文本色彩控制
def 字体上色(字体颜色, *values) -> str:
    合成临时字符串: str = (' '.join(str(itm) for itm in values)).strip()

    def 检查字符串首是否有字体控制字(字符串: str) -> bool:
        检查结果: bool = False

        # 匹配字符串首部的连续的所有字符控制字
        颜色控制字匹配模式: str = r'^(?:\033\[\d+m)+'
        匹配字符串 = re.match(颜色控制字匹配模式, 字符串)
        if 匹配字符串:
            if r'[3' in 匹配字符串.string:
                检查结果 = True

        return 检查结果

    if 合成临时字符串:
        # 如果字符串首部尚不存在字体颜色控制字,则在字符串首部补充一个字体颜色控制字
        if not 检查字符串首是否有字体控制字(合成临时字符串):
            合成临时字符串 = '{}{}'.format(字体颜色, 合成临时字符串)

        # 检查原字符串尾部结束符
        if 合成临时字符串.endswith(Fore.RESET + Back.RESET):
            合成临时字符串 = 合成临时字符串[:-len(Back.RESET + Fore.RESET)] + Back.RESET
        elif 合成临时字符串.endswith(Fore.RESET):
            合成临时字符串 = 合成临时字符串[:-len(Fore.RESET)]

        # 将 Fore.RESET 部位替换成要求的字体颜色, 并在末尾补充一个Fore.RESET
        合成临时字符串 = 合成临时字符串.replace(Fore.RESET, 字体颜色) + Fore.RESET
    else:
        合成临时字符串 = ''
    return 合成临时字符串


def 背景上色(背景颜色, *values) -> str:
    合成临时字符串: str = (' '.join(str(itm) for itm in values)).strip()

    def 检查字符串首是否有背景控制字(字符串: str) -> bool:
        检查结果: bool = False

        # 匹配字符串首部的连续的所有字符控制字
        颜色控制字匹配模式: str = r'^(?:\033\[\d+m)+'
        匹配字符串 = re.match(颜色控制字匹配模式, 字符串)
        if 匹配字符串:
            if r'[4' in 匹配字符串.string:
                检查结果 = True

        return 检查结果

    if 合成临时字符串:
        # 如果字符串首部尚不存在背景颜色控制字,则在字符串首部补充一个背景颜色控制字
        if not 检查字符串首是否有背景控制字(合成临时字符串):
            合成临时字符串 = '{}{}'.format(背景颜色, 合成临时字符串)

        # 检查原字符串尾部结束符
        if 合成临时字符串.endswith(Back.RESET + Fore.RESET):
            合成临时字符串 = 合成临时字符串[:-len(Back.RESET + Fore.RESET)] + Fore.RESET
        elif 合成临时字符串.endswith(Back.RESET):
            合成临时字符串 = 合成临时字符串[:-len(Back.RESET)]

        # 将 Back.RESET 部位替换成要求的背景颜色, 并在末尾补充一个Back.RESET
        合成临时字符串 = 合成临时字符串.replace(Back.RESET, 背景颜色) + Back.RESET
    else:
        合成临时字符串 = ''

    return 合成临时字符串


def 红字(*values) -> str:
    return 字体上色(Fore.RED, *values)


def 红底(*values) -> str:
    return 背景上色(Back.RED, *values)


def 红底白字(*values) -> str:
    return 字体上色(Fore.WHITE, 背景上色(Back.RED, *values))


def 红底黑字(*values) -> str:
    return 字体上色(Fore.BLACK, 背景上色(Back.RED, *values))


def 红底黄字(*values) -> str:
    return 字体上色(Fore.YELLOW, 背景上色(Back.RED, *values))


def 绿字(*values) -> str:
    return 字体上色(Fore.GREEN, *values)


def 绿底(*values) -> str:
    return 背景上色(Back.GREEN, *values)


def 黄字(*values) -> str:
    return 字体上色(Fore.YELLOW, *values)


def 黄底(*values) -> str:
    return 背景上色(Back.YELLOW, *values)


def 蓝字(*values) -> str:
    return 字体上色(Fore.BLUE, *values)


def 蓝底(*values) -> str:
    return 背景上色(Back.BLUE, *values)


def 洋红字(*values) -> str:
    return 字体上色(Fore.MAGENTA, *values)


def 洋红底(*values) -> str:
    return 背景上色(Back.MAGENTA, *values)


def 青字(*values) -> str:
    return 字体上色(Fore.CYAN, *values)


def 青底(*values) -> str:
    return 背景上色(Back.CYAN, *values)


def 白字(*values) -> str:
    return 字体上色(Fore.WHITE, *values)


def 黑字白底(*values) -> str:
    return 字体上色(Fore.BLACK, 背景上色(Back.WHITE, *values))


def 黑字(*values) -> str:
    return 字体上色(Fore.BLACK, *values)


def 黑底(*values) -> str:
    return 背景上色(Back.BLACK, *values)


def 白字绿底(*values) -> str:
    return 字体上色(Fore.WHITE, 背景上色(Back.GREEN, *values))


# endregion


# region terminal 光标控制
def 光标上移(行数: int = 0) -> None:
    if 行数 > 0:
        print('\033[{}A'.format(行数 + 1))


def 光标下移(行数: int = 0) -> None:
    if 行数 > 0:
        print('\033[{}B'.format(行数))


def 光标右移(列数: int = 0) -> None:
    if 列数 > 0:
        print('\033[{}C'.format(列数))


def 清屏() -> None:
    print('\033[{}J'.format(2))


def 设置光标位置(行号: int, 列号: int) -> None:
    if 行号 >= 0 and 列号 >= 0:
        print('\033[{};{}H'.format(行号, 列号))


def 保存光标位置() -> None:
    print('\033[s')


def 恢复光标位置() -> None:
    print('\033[u')


def 隐藏光标() -> None:
    print('\033[?25l')


def 显示光标() -> None:
    print('\033[?25h')


# endregion
# endregion


class 分隔线模板:
    __符号: str = '-'
    __提示内容: str = None
    __总长度: int = 50
    __提示对齐: 对齐方式 = 对齐方式.居中对齐
    __修饰方法: callable = None
    __打印方法: callable = None

    def __init__(self,
                 符号: str = '-',
                 提示内容: str = None,
                 总长度: int = 50,
                 提示对齐: 对齐方式 = 对齐方式.居中对齐,
                 修饰方法: callable = None,
                 打印方法: callable = print):
        if 符号 is not None:
            self.__符号 = str(符号)
        if 提示内容 is not None:
            self.__提示内容 = 提示内容
        if str(总长度).isdigit():
            总长度 = int(总长度)
            if 总长度 > 0:
                self.__总长度 = 总长度
        if isinstance(提示对齐, 对齐方式):
            self.__提示对齐 = 提示对齐
        if callable(修饰方法):
            self.__修饰方法 = 修饰方法
        if callable(打印方法):
            self.__打印方法 = 打印方法

    # region 访问器
    def 副本(self):
        副本: 分隔线模板 = 分隔线模板()

        副本._分隔线模板__符号 = self.__符号
        副本._分隔线模板__提示内容 = self.__提示内容
        副本._分隔线模板__总长度 = self.__总长度
        副本._分隔线模板__提示对齐 = self.__提示对齐
        副本._分隔线模板__修饰方法 = self.__修饰方法
        副本._分隔线模板__打印方法 = self.__打印方法

        return 副本

    # endregion

    def 符号(self, 符号: str = None):
        if 符号 is None:
            self.__符号 = '-'
        else:
            self.__符号 = str(符号)
        return self

    def 提示内容(self, 提示: str = None):
        if 提示 is None:
            self.__提示内容 = ''
        else:
            self.__提示内容 = str(提示)
        return self

    def 总长度(self, 长度: int = 50):
        if not str(长度).isdigit():
            self.__总长度 = 50
        else:
            长度 = int(长度)
            if 长度 > 0:
                self.__总长度 = 长度
            else:
                self.__总长度 = 50
        return self

    def 文本对齐(self, 方式: 对齐方式 = 对齐方式.居中对齐):
        if isinstance(方式, 对齐方式):
            self.__提示对齐 = 方式
        return self

    def 修饰方法(self, 修饰方法: callable):
        if callable(修饰方法):
            self.__修饰方法 = 修饰方法
        return self

    def 展示(self, 打印方法: callable = None):
        if callable(打印方法):
            self.__打印方法 = 打印方法
        if callable(self.__打印方法):
            self.__打印方法(self.__str__())
        else:
            print(self.__str__())

    def __str__(self) -> str:
        分隔线字符串: str = ''
        if not self.__符号 or 显示宽度(self.__符号) < 1:
            self.__修饰符 = '-'

        提示文本: str = ''
        if self.__提示内容:
            提示文本 = str(self.__提示内容).strip()

        修饰符重复次数: int = ((self.__总长度 - 显示宽度(提示文本)) / 显示宽度(self.__修饰符)).__floor__()
        if self.__提示对齐 == 对齐方式.左对齐:
            if 修饰符重复次数 > 0:
                分隔线字符串 = '{}{}'.format(提示文本, self.__修饰符 * 修饰符重复次数)
        elif self.__提示对齐 == 对齐方式.右对齐:
            if 修饰符重复次数 > 0:
                分隔线字符串 = '{}{}'.format(self.__修饰符 * 修饰符重复次数, 提示文本)
        else:
            修饰符重复次数: int = (((self.__总长度 - 显示宽度(提示文本)) * 0.5) / 显示宽度(self.__修饰符)).__floor__()
            if 修饰符重复次数 > 0:
                左边修饰符: str = self.__修饰符 * 修饰符重复次数
                右边修饰符: str = self.__修饰符 * 修饰符重复次数

                右边修饰符修正: list[str] = []
                if 右边修饰符:
                    # 右边修饰符需要做方向转换, 例如 > 转为 <
                    右边修饰符 = ''.join(reversed(右边修饰符))
                    for 字符 in 右边修饰符:
                        右边修饰符修正.append(镜像字符(字符))

                if 左边修饰符 and 右边修饰符修正:
                    分隔线字符串 = '{}{}{}'.format(左边修饰符, 提示文本, ''.join(右边修饰符修正))

        if not 分隔线字符串:
            分隔线字符串 = 提示文本

        if callable(self.__修饰方法):
            分隔线字符串 = self.__修饰方法(分隔线字符串)

        return 分隔线字符串


class 语义日期模板:
    __目标日期: datetime = None
    __打印方法: callable = None

    def __init__(self,
                 目标日期: datetime = datetime.now(),
                 打印方法: callable = print):
        if 目标日期:
            self.__目标日期 = 目标日期
        else:
            self.__目标日期 = datetime.now()
        if callable(打印方法):
            self.__打印方法 = 打印方法
        else:
            self.__打印方法 = print

    def 目标日期(self, 日期: datetime = datetime.now()):
        if 日期:
            self.__目标日期 = 日期
        else:
            self.__目标日期 = datetime.now()
        return self

    def 展示(self, 打印方法: callable = None):
        if callable(打印方法):
            打印方法(self.__str__())
        elif callable(self.__打印方法):
            self.__打印方法(self.__str__())
        else:
            print(self.__str__())

    # region 访问器
    @property
    def 偏离天数(self) -> int:
        return (self.__目标日期.date() - datetime.now().date()).days

    @property
    def 偏离周数(self) -> int:
        目标日期对齐到周一: datetime = self.__目标日期 + timedelta(days=1 - self.__目标日期.isoweekday())
        基准日期对齐到周一: datetime = datetime.now() + timedelta(days=1 - datetime.now().isoweekday())
        对齐到周一的日期偏离天数: int = (目标日期对齐到周一.date() - 基准日期对齐到周一.date()).days
        return (对齐到周一的日期偏离天数 / 7).__floor__()

    @property
    def 偏离月数(self) -> int:
        return (self.__目标日期.year - datetime.now().year) * 12 + self.__目标日期.month - datetime.now().month

    @property
    def 偏离年数(self) -> int:
        return self.__目标日期.year - datetime.now().year

    @property
    def 语义(self) -> str:
        return self.__str__()

    @property
    def 副本(self):
        副本: 语义日期模板 = 语义日期模板()

        副本._语义日期模板__目标日期 = self.__目标日期
        副本._语义日期模板__打印方法 = self.__打印方法

        return 副本

    # endregion

    def __str__(self) -> str:
        语义: str = ''

        天数 = self.偏离天数
        周数 = self.偏离周数
        月数 = self.偏离月数
        年数 = self.偏离年数

        if 天数 == -3:
            语义 = '大前天'
        elif 天数 == -2:
            语义 = '前天'
        elif 天数 == 0:
            语义 = '今天'
        elif 天数 == -1:
            语义 = '昨天'
        elif 天数 == 1:
            语义 = '明天'
        elif 天数 == 2:
            语义 = '后天'
        elif 天数 == 3:
            语义 = '大后天'
        elif 周数 == -2:
            语义 = '上上周'
        elif 周数 == -1:
            语义 = '上周'
        elif 周数 == 1:
            语义 = '下周'
        elif 周数 == 2:
            语义 = '下下周'
        elif 月数 == -2:
            语义 = '上上月'
        elif 月数 == -1:
            语义 = '上月'
        elif 月数 == 1:
            语义 = '下月'
        elif 月数 == 2:
            语义 = '下下月'
        elif 年数 == -3:
            语义 = '大前年'
        elif 年数 == -2:
            语义 = '前年'
        elif 年数 == -1:
            语义 = '去年'
        elif 年数 == 1:
            语义 = '明年'
        elif 年数 == 2:
            语义 = '后年'
        elif 年数 == 3:
            语义 = '大后年'
        elif 年数 != 0:
            语义 = '{}年{}'.format(年数.__abs__(), '前' if 年数 < 0 else '后')
        elif 月数 != 0:
            语义 = '{}个月{}'.format(月数.__abs__(), '前' if 月数 < 0 else '后')
        elif 周数 != 0:
            语义 = '{}周{}'.format(周数.__abs__(), '前' if 周数 < 0 else '后')
        elif 天数 != 0:
            语义 = '{}天{}'.format(天数.__abs__(), '前' if 天数 < 0 else '后')

        return 语义


class 调试模板:
    # 默认 debug 状态为 False
    __调试状态: bool = False
    # 缩进量， 默认无缩进
    __缩进字符: str = ''
    # 默认的打印前缀为 '|-'
    __打印头: str = '|-'
    # 默认的位置提示标记为 '->'
    __位置提示符: str = '->'
    # 定义一个 table 的 buffer，用来临时存储需要打印的table内容
    __表格: list = None

    def __init__(self,
                 调试状态: bool = False,
                 缩进字符: str = None,
                 打印头: str = None,
                 位置提示符: str = None):
        if 调试状态:
            self.__调试状态 = True
        else:
            self.__调试状态 = False

        if 缩进字符 is not None:
            self.__缩进字符 = 缩进字符

        if 打印头 is not None:
            self.__打印头 = 打印头

        if 位置提示符 is not None:
            self.__位置提示符 = 位置提示符

        self.__表格 = []

    # region 访问器
    @property
    def 调试状态(self) -> bool:
        return self.__调试状态

    @property
    def 缩进字符(self) -> str:
        return self.__缩进字符

    @缩进字符.setter
    def 缩进字符(self, 符号: str = None) -> None:
        if 符号 is None:
            self.__缩进字符 = ''
        else:
            self.__缩进字符 = str(符号)

    @property
    def 打印头(self) -> str:
        return self.__打印头

    @打印头.setter
    def 打印头(self, 符号: str = None) -> None:
        if 符号 is None:
            self.__打印头 = ''
        else:
            self.__打印头 = str(符号)

    @property
    def 位置提示符(self) -> str:
        return self.__位置提示符

    @位置提示符.setter
    def 位置提示符(self, 符号: str = None) -> None:
        if 符号 is None:
            self.__位置提示符 = '->'
        else:
            self.__位置提示符 = str(符号)

    @property
    def 表格行数(self) -> int:
        if not self.__表格:
            return 0
        else:
            return len(self.__表格)

    @property
    def 表格列表(self) -> list[list[str]]:
        if not self.__表格:
            return [[]]
        else:
            临时表: list[list[str]] = []
            for 行元素 in self.__表格:
                这一行: list[str] = []
                for 元素 in 行元素:
                    这一行.append(元素)
                临时表.append(这一行)
            return 临时表

    @property
    def 分隔线(self, 仅调试: bool = False) -> 分隔线模板:
        新建分隔线: 分隔线模板
        if 仅调试:
            新建分隔线 = 分隔线模板(打印方法=self.调试消息)
        else:
            新建分隔线 = 分隔线模板(打印方法=self.消息)
        return 新建分隔线

    @property
    def 语义日期(self, 目标日期: datetime = datetime.now(), 仅调试: bool = False) -> 语义日期模板:
        语义日期: 语义日期模板
        if 仅调试:
            语义日期 = 语义日期模板(目标日期=目标日期, 打印方法=self.调试消息)
        else:
            语义日期 = 语义日期模板(目标日期=目标日期, 打印方法=self.消息)
        return 语义日期

    @property
    def 副本(self):
        副本: 调试模板 = 调试模板()

        副本._调试模板__调试状态 = self.__调试状态
        副本._调试模板__打印头 = self.__打印头
        副本._调试模板__缩进字符 = self.__缩进字符
        副本._调试模板__位置提示符 = self.__位置提示符

        副本.添加多行(self.表格列表)

        return 副本

    # endregion

    # region 表格操作
    def 准备表格(self):
        self.__表格 = []

        class 方法集合:
            添加一行: callable = None
            添加一调试行: callable = None

        返回方法: 方法集合 = 方法集合()
        返回方法.添加一行 = self.添加一行
        返回方法.添加一调试行 = self.添加一调试行

        return 返回方法

    def 添加一行(self, *元素列表):
        if len(元素列表) == 1 and type(元素列表[0]) in [list, tuple]:
            self.__添加一行(元素列表[0])
        elif len(元素列表) > 0:
            self.__添加一行(元素列表)

        class 方法集合:
            修饰方法: callable = None
            展示表格: callable = None

        返回方法: 方法集合 = 方法集合()
        返回方法.修饰方法 = self.__修饰最后一行
        返回方法.展示表格 = self.展示表格

        return 返回方法

    def 添加空行(self, 空行数量: int = 1) -> None:
        if 空行数量 < 1:
            return None
        for 次数 in range(空行数量):
            self.__添加一行([''])

    def 添加多行(self, 行列表: list or tuple, 拆分列数: int = -1, 拆分行数: int = -1):
        if type(行列表) in [list, tuple]:
            if 拆分列数 < 0 and 拆分行数 < 0:
                for 行元素 in 行列表:
                    if type(行元素) in [list, tuple]:
                        self.__添加一行(行元素)
                    else:
                        self.__添加一行([str(行元素)])
            elif 拆分列数 > 0:
                拆分行列表: list[list] = [行列表[截断位置: 截断位置 + 拆分列数] for 截断位置 in range(0, len(行列表), 拆分列数)]
                self.添加多行(拆分行列表)
            else:
                计算拆分列数: int = (len(行列表) / 拆分行数).__ceil__()
                self.添加多行(行列表=行列表, 拆分列数=计算拆分列数)
        else:
            self.__添加一行([str(行列表)])

        class 方法集合:
            展示表格: callable = None

        返回方法: 方法集合 = 方法集合()
        返回方法.展示表格 = self.展示表格

        return 返回方法

    def 添加一调试行(self, *元素列表):
        if self.__调试状态:
            self.添加一行(*元素列表)

        class 方法集合:
            修饰方法: callable = None
            展示表格: callable = None

        返回方法: 方法集合 = 方法集合()
        if self.__调试状态:
            返回方法.修饰方法 = self.__修饰最后一行
            返回方法.展示表格 = self.展示表格
        else:
            返回方法.修饰方法 = self.__空方法
            返回方法.展示表格 = self.__空方法

        return 返回方法

    def 添加多调试行(self, 元素列表: list[list]):
        if self.__调试状态:
            self.添加多行(元素列表)

        class 方法集合:
            展示表格: callable = None

        返回方法: 方法集合 = 方法集合()
        返回方法.展示表格 = self.展示表格

        return 返回方法

    def 上下颠倒表格(self):
        if self.__表格:
            self.__表格.reverse()

        class 方法集合:
            左右颠倒表格: callable = None
            展示表格: callable = None

        返回方法: 方法集合 = 方法集合()
        返回方法.左右颠倒表格 = self.左右颠倒表格
        返回方法.展示表格 = self.展示表格

        return 返回方法

    def 左右颠倒表格(self):
        if self.__表格:
            表格最大行数: int = max([len(表格行) for 表格行 in self.__表格])

            临时表格: list = []
            for 表格行 in self.__表格:
                这一行: list[str] = []
                for 列号 in range(表格最大行数):
                    if 列号 < len(表格行):
                        这一行.append(表格行[列号])
                    else:
                        这一行.append("")
                这一行.reverse()
                临时表格.append(这一行)
            self.__表格 = 临时表格

        class 方法集合:
            上下颠倒表格: callable = None
            展示表格: callable = None

        返回方法: 方法集合 = 方法集合()
        返回方法.上下颠倒表格 = self.上下颠倒表格
        返回方法.展示表格 = self.展示表格

        return 返回方法

    # 将tableBuf中的内容，对齐每一列后进行输出
    def 展示表格(self, 列间距: int = 2) -> None:
        # 如果 __表格 无内容，则直接返回
        if not self.__表格:
            return None

        # 把 self.__表格展开，主要是展开单元格中的子行
        展开的表格: list[list[str]] = self.__表格展开()

        # 计算 展开的表格 中每一行中列数的最大值
        总列数: int = max([len(row) for row in 展开的表格])
        if 总列数 < 1:
            return None

        # 计算每一列中各行内容的最大显示长度值
        各列最长字符串显示长度: list = [idx * 0 for idx in range(总列数)]
        for 行元素 in 展开的表格:
            列数 = len(行元素)
            for 列号 in range(总列数):
                if 列号 < 列数:
                    各列最长字符串显示长度[列号] = max(显示宽度(行元素[列号]), 各列最长字符串显示长度[列号])

        # 消除 各列最长字符串显示长度 尾部的零，即如果最后 N 列的内容长度都是 0，则可以不再处理最后的 N 列
        临时序列: list = []
        for 列号 in range(总列数):
            if sum(各列最长字符串显示长度[列号:]) > 0:
                临时序列.append(各列最长字符串显示长度[列号])
        各列最长字符串显示长度 = 临时序列

        # 更新 总列数 为实际的 各列最长字符串显示长度 的长度
        总列数 = len(各列最长字符串显示长度)

        # 计算每一列的起始位置
        列前空格数量: int = 2
        if 列间距 >= 0:
            列前空格数量 = 列间距
        列起位置: list = []
        for 列号 in range(len(各列最长字符串显示长度)):
            if 列号 == 0:
                # 第一列的列起始位置为 0
                列起位置.append(0)
            else:
                # 每列的起始位置计算, 前一列起始位置 + 前一列最大长度 + 指定数量的个空格
                列起位置.append(列起位置[列号 - 1] + 各列最长字符串显示长度[列号 - 1] + 列前空格数量)

        # 根据每一列的起始位置，将第一行的内容合成一个字符串
        行字符串列表: list[str] = []
        for 行元素 in 展开的表格:
            列数 = len(行元素)
            行字符串: str = ''
            for 列号 in range(总列数):
                if 列号 < 列数:
                    # 补齐 行字符串 尾部的空格，以使其长度与该列的起始位置对齐
                    行字符串 += ' ' * max(0, (列起位置[列号] - 显示宽度(行字符串)))
                    # 在补齐的基础上, 添加该列的内容
                    行字符串 += 行元素[列号]
            行字符串列表.append(行字符串.rstrip())

        # 打印输出每一行的内容
        for 行字符串 in 行字符串列表:
            print('{}{}{}'.format(self.__缩进字符, self.__打印头, 行字符串))
        return None

    def __添加一行(self, 行表: list or tuple = None) -> None:
        if 行表 is None:
            return None

        if type(行表) not in [list, tuple]:
            return None

        这一行: list[str] = []

        # 将每一行中的元素转为字符串，存于list中
        for 元素 in 行表:
            这一行.append(str(元素).strip())

        if 这一行:
            self.__表格.append(这一行)
        return None

    def __表格展开(self) -> list[list[str]]:
        # 这个函数将 self.__表格 进行展开操作，主要是展开表格内容中的换行符
        展开的表格: list[list[str]] = []
        if self.__表格:
            for 行元素 in self.__表格:
                # 对表格中的每一行元素，做如下处理
                这一行: list[str]

                换行符: str = '\n'
                换行符的个数: int = sum([1 if str(元素).__contains__(换行符) else 0 for 元素 in 行元素])
                if 换行符的个数 == 0:
                    换行符 = '\r'
                    换行符的个数 = sum([1 if str(元素).__contains__(换行符) else 0 for 元素 in 行元素])

                if 换行符的个数 == 0:
                    # 列表中的元素字符串中不包括换行符
                    这一行 = []
                    for 元素 in 行元素:
                        这一行.append(元素)
                    if 这一行:
                        展开的表格.append(这一行)
                else:
                    # 列表中的元素包括了换行符,则需要处理换行符,处理的方案是换行后的内容放到新的表格行中
                    行列表: list[list[str]] = [str(元素).split(换行符) for 元素 in 行元素]
                    最大行数: int = max([len(列表) for 列表 in 行列表])
                    列数: int = len(行列表)
                    for 行号 in range(最大行数):
                        这一行 = []
                        for 列号 in range(列数):
                            列表: list[str] = 行列表[列号]
                            if 行号 < len(列表):
                                这一行.append(列表[行号].strip())
                            else:
                                这一行.append('')
                        if 这一行:
                            展开的表格.append(这一行)
        return 展开的表格

    def __修饰最后一行(self, 方法: callable = None):
        if callable(方法):
            if self.__表格:
                最后一行的索引: int = len(self.__表格) - 1
                for 序号 in range(len(self.__表格[最后一行的索引])):
                    元素: str = str(self.__表格[最后一行的索引][序号]).strip()

                    换行符: str = '\n'
                    换行符的个数: int = 1 if 元素.__contains__(换行符) else 0
                    if 换行符的个数 == 0:
                        换行符 = '\r'
                        换行符的个数 = 1 if 元素.__contains__(换行符) else 0

                    if 换行符的个数 == 0:
                        self.__表格[最后一行的索引][序号] = 方法(元素)
                    else:
                        self.__表格[最后一行的索引][序号] = 换行符.join([方法(段) for 段 in 元素.split(换行符)])

        class 方法集合:
            展示表格: callable = None
            上下颠倒表格: callable = None
            左右颠倒表格: callable = None

        返回方法: 方法集合 = 方法集合()
        返回方法.展示表格 = self.展示表格
        返回方法.上下颠倒表格 = self.上下颠倒表格
        返回方法.左右颠倒表格 = self.左右颠倒表格

        return 返回方法

    def __空方法(self, *参数表) -> None:
        pass

    # endregion

    def 缩进(self, 缩进字符: str = None):
        if 缩进字符 is None:
            self.__缩进字符 = ' ' + self.__缩进字符
        else:
            self.__缩进字符 = 缩进字符 + self.__缩进字符
        return self

    def 打开调试(self):
        self.__调试状态 = True
        return self

    def 关闭调试(self):
        self.__调试状态 = False
        return self

    def 设置打印头(self, 符号: str = None):
        self.打印头 = 符号
        return self

    def 设置位置提示符(self, 符号: str = None):
        self.位置提示符 = 符号
        return self

    def 消息(self, *参数表) -> None:
        print('{}{}{}'.format(self.__缩进字符, self.__打印头, ' '.join((str(参数).strip() for 参数 in 参数表))))

    def 提示错误(self, *参数表) -> None:
        print('{}{}{}'.format(self.__缩进字符, self.__打印头, 红底黄字(' '.join((str(参数).strip() for 参数 in 参数表)))))

    def 调试消息(self, *参数表) -> None:
        if self.__调试状态:
            self.消息(*参数表)

    def 提示调试错误(self, *参数表) -> None:
        if self.__调试状态:
            self.提示错误(*参数表)

    def 执行位置(self, 参数) -> None:
        if self.__调试状态:
            提示文本: str
            if not callable(参数):
                提示文本 = str(参数)
            else:
                提示文本 = str(参数.__name__)

            提示文本 = 提示文本.strip()
            if 提示文本:
                print('{}{}{}'.format(self.__缩进字符, self.__位置提示符, 黄字(提示文本) + ' 开始执行'))
