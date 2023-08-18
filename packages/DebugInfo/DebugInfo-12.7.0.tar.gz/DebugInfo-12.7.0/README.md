# 调试模块

#### 介绍

一个用于消息整理和打印输出的模块，主要功能包括 文本对齐，表格整理对方，文本修饰等。

#### 软件架构

调试模块.py # 主功能代码
效果测试.py # 用于测试主功能代码的使用效果

#### 安装教程

安装 DebugInfo 模块
```bash
pip install DebugInfo
```

在脚本中使用 DebugInfo 模块
```python
# region 引入 调试模块
from DebugInfo.DebugInfo import *
# endregion
```

#### 使用说明

测试代码可以见 **效果测试.py** 文档内的代码

文本处理效果的演示代码如下：

```python
from DebugInfo.DebugInfo import *

if __name__ == '__main__':
    # 对象实例化时,可以指定调试模式,也可以指定其它参数
    白板 = 调试模板(True)

    # 如果调试模式打开, 这里可以打印执行位置消息
    白板.执行位置(os.path.basename(__file__) + '[这个信息应该被显示]')

    # 可以关闭调试模式
    白板.关闭调试()
    # 关闭调试模式后,执行位置信息不再打印
    白板.执行位置(os.path.basename(__file__) + '[这个提示不应该被显示]')

    # 调试信息只有在调试状态才会打印输出
    白板.关闭调试()
    白板.调试消息('这是一个调试状态才会输出的消息, 这是1号消息')
    白板.打开调试()
    白板.调试消息('这是一个调试状态才会输出的消息, 这是2号消息, 你应该看不到1号消息的')

    # 可以进行缩进处理, 默认缩进一个空格符
    白板.消息('这是缩进前')
    白板.缩进()
    白板.消息('这是缩进后')
    # 你也可以指定缩进的字符,例如可以指定缩进两个空格
    白板.缩进('  ')
    白板.消息('注意,这一行相对上一行,缩进了两个空格')

    # 注意,缩进功能没有提供回退方法,推荐的方法是如果你需要临时缩进,你可以通过创建副本的方法来进行,对副本的操作不会影响原对象
    小白板: 调试模板 = 白板.副本.缩进()
    小白板.消息('这是新对象的打印,应该有一个缩进效果')
    白板.消息('这还是原对象的打印')

    # 你可以级联进行多个操作,例如 创建副本, 缩进, 打开调试
    虫卵: 调试模板 = 白板.副本.关闭调试().设置打印头('@')
    虫卵.消息('这是一个卵宝宝,请注意打印头符号')

    # 你可以打印一个错误消息,错误消息将标记为红色背景
    白板.提示错误('天啊,这里有一个致命错误')

    # 可以生成并打印一个分隔线
    白板.分隔线.符号('~').提示内容('这是一个黄色背景的分隔线').修饰方法(黄底).总长度(50).展示()
    白板.分隔线.符号('*').提示内容('这是一个黄色字体的分隔线').修饰方法(黄字).总长度(60).展示()
    白板.消息('下面是一个不加修饰的分隔线')
    白板.分隔线.展示()

    # 可以很方便的整理并打印一个表格
    白板.准备表格()  # 每次使用表格功能前,你需要手动准备一下表格
    白板.添加一行('列1', '列2', '列3')  # 你可以把第一行的内容视做表头
    白板.添加一行('行1', '天下', '太平')
    白板.添加一行('行2', '和', '谐', '社', '会')
    白板.添加一行('', '', '', '这一行前面的列没有内容', '这一列没有表头哈')

    # 你可以添加一行只有在调试模式才显示的内容
    白板.添加一调试行('行5', '这一行只有调试状态下才显示')

    # 也可以通过list添加一行
    白板.添加一行(['行6', '', '', '行6列4'])

    # 也可以添加多行
    白板.添加多行([['行7', '行7列2'], ['行8', '', '行8列3']])
    白板.展示表格()

    白板.分隔线.提示内容('这是一个绿色的分隔线').修饰方法(绿字).展示()

    # 你可以在表格,或者其它需要的地方,使用颜色修饰你的字符
    白板.准备表格()
    白板.添加一行('彩字效果', '编码展示')
    彩字 = 蓝字('蓝字')
    白板.添加一行(彩字, 彩字.encode())
    彩字 = 红底(彩字 + '红底')
    白板.添加一行(彩字, 彩字.encode())
    彩字 = 黄底(彩字 + '黄底')
    白板.添加一行(彩字, 彩字.encode())
    彩字 = 绿字(彩字 + '绿字')
    白板.添加一行(彩字, 彩字.encode())
    白板.展示表格()
```

以上代码的运行效果如下：  
![文本处理效果演示](image0.png)

语义日期效果的演示代码如下：

```python
from DebugInfo.DebugInfo import *

if __name__ == '__main__':
    白板: 调试模板 = 调试模板()
    白板.消息(分隔线模板().提示内容('语义日期演示').修饰方法(红字))
    白板.准备表格()
    白板.添加一行('日期', '日期语义')
    白板.添加一行(datetime.now().date() + timedelta(days=-365 * 5), 语义日期模板(datetime.now() + timedelta(days=-365 * 5)))
    白板.添加一行(datetime.now().date() + timedelta(days=-365), 语义日期模板(datetime.now() + timedelta(days=-365)))
    白板.添加一行(datetime.now().date() + timedelta(days=-180), 语义日期模板(datetime.now() + timedelta(days=-180)))
    白板.添加一行(datetime.now().date() + timedelta(days=-40), 语义日期模板(datetime.now() + timedelta(days=-40)))
    白板.添加一行(datetime.now().date() + timedelta(days=-20), 语义日期模板(datetime.now() + timedelta(days=-20)))
    白板.添加一行(datetime.now().date() + timedelta(days=-8), 语义日期模板(datetime.now() + timedelta(days=-8)))
    白板.添加一行(datetime.now().date() + timedelta(days=-2), 语义日期模板(datetime.now() + timedelta(days=-2)))
    白板.添加一行(datetime.now().date() + timedelta(days=-1), 语义日期模板(datetime.now() + timedelta(days=-1)))
    白板.添加一行(datetime.now().date() + timedelta(days=-0), 语义日期模板(datetime.now() + timedelta(days=-0)))
    白板.添加一行(datetime.now().date() + timedelta(days=1), 语义日期模板(datetime.now() + timedelta(days=1)))
    白板.添加一行(datetime.now().date() + timedelta(days=2), 语义日期模板(datetime.now() + timedelta(days=2)))
    白板.添加一行(datetime.now().date() + timedelta(days=3), 语义日期模板(datetime.now() + timedelta(days=3)))
    白板.添加一行(datetime.now().date() + timedelta(days=9), 语义日期模板(datetime.now() + timedelta(days=9)))
    白板.添加一行(datetime.now().date() + timedelta(days=18), 语义日期模板(datetime.now() + timedelta(days=18)))
    白板.添加一行(datetime.now().date() + timedelta(days=40), 语义日期模板(datetime.now() + timedelta(days=40)))
    白板.添加一行(datetime.now().date() + timedelta(days=180), 语义日期模板(datetime.now() + timedelta(days=180)))
    白板.添加一行(datetime.now().date() + timedelta(days=365), 语义日期模板(datetime.now() + timedelta(days=365)))
    白板.添加一行(datetime.now().date() + timedelta(days=365 * 4), 语义日期模板(datetime.now() + timedelta(days=365 * 4)))

    白板.展示表格()
```

以上代码的运行效果如下：  
![语义日期效果演示](image.png)

使用乘法表演示表格对齐打印效果的代码如下：

```python
from DebugInfo.DebugInfo import *

if __name__ == '__main__':
    # 对象实例化时,可以指定调试模式,也可以指定其它参数
    白板 = 调试模板(True)

    # 打印乘法表
    白板.准备表格()
    白板.添加多行([[f'{被乘数}・{乘数} = {被乘数 * 乘数}' for 被乘数 in range(1, 乘数 + 1)] for 乘数 in range(1, 15)])

    白板.分隔线.提示内容('展示乘法表').修饰方法(红字).展示()
    白板.展示表格()

    白板.分隔线.提示内容('左右颠倒乘法表').修饰方法(红字).展示()
    白板.副本.左右颠倒表格().展示表格()

    白板.分隔线.提示内容('上下颠倒乘法表').修饰方法(红字).展示()
    白板.副本.上下颠倒表格().展示表格()

    白板.分隔线.提示内容('上下左右颠倒乘法表').修饰方法(红字).展示()
    白板.副本.上下颠倒表格().左右颠倒表格().展示表格()
```
以上代码的运行效果如下：  
![乘法表打印效果](image3.png)

以下演示表格的列对齐控制功能，代码如下：

```python
from DebugInfo.DebugInfo import *

if __name__ == '__main__':
    # 对象实例化时,可以指定调试模式,也可以指定其它参数
    白板 = 调试模板(True)

    白板.分隔线.提示内容('表格对齐效果演示').修饰方法(绿字).展示()
    白板.准备表格('lcr').添加一行('左对齐', '居中对齐', '右对齐').修饰方法(青字)
    白板.添加一行('左对齐一', '居中', '12')
    白板.添加一行('左对齐一二', '居-中', '123')
    白板.添加一行('左对齐一二三', '居--中', '1234')
    白板.添加一行('左对齐一二三四', '居-------中', '12345')
    白板.展示表格()

    # 表格列对齐可以独立设置
    # 虫子.设置列对齐('lrr')
```
以上代码的运行效果如下：  
![表格控制列对齐效果](image10.png)


以下演示秒表装饰器功能，代码如下：

```python
from DebugInfo.DebugInfo import *
# 一个方法,用来测试秒表装饰器效果
@秒表
def 秒表测试方法(白板: 调试模板 = 调试模板()):
    白板.执行位置(秒表测试方法)

    白板.准备表格()
    填充次数 = 5000
    白板.消息(f'填充表格 {填充次数} 次')
    for 序号 in range(填充次数):
        白板.添加一行(序号, '秒表演示')

    休眠时间 = 1
    白板.消息(f'休眠 {休眠时间}s')
    time.sleep(休眠时间)

if __name__ == '__main__':
    # 对象实例化时,可以指定调试模式,也可以指定其它参数
    白板 = 调试模板(True)

    # 调用秒表测试方法
    秒表测试方法(白板.副本.缩进())
```
以上代码先定义了一个方法，这个方法中循环填充表格，然后进行休眠。使用秒表来装饰这个方法。
在主程序中，执行 秒表测试方法，观察 秒表装饰器的效果，如下：  
![秒表装饰器效果演示](image4.png)




#### 参与贡献

1. Fork 本仓库
2. 新建 Feat_xxx 分支
3. 提交代码
4. 新建 Pull Request

#### 特技

1. 使用 Readme\_XXX.md 来支持不同的语言，例如 Readme\_en.md, Readme\_zh.md
2. Gitee 官方博客 [blog.gitee.com](https://blog.gitee.com)
3. 你可以 [https://gitee.com/explore](https://gitee.com/explore) 这个地址来了解 Gitee 上的优秀开源项目
4. [GVP](https://gitee.com/gvp) 全称是 Gitee 最有价值开源项目，是综合评定出的优秀开源项目
5. Gitee 官方提供的使用手册 [https://gitee.com/help](https://gitee.com/help)
6. Gitee 封面人物是一档用来展示 Gitee 会员风采的栏目 [https://gitee.com/gitee-stars/](https://gitee.com/gitee-stars/)
