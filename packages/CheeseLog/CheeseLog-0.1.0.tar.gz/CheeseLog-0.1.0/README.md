# **CheeseLog**

## **介绍**

一款完全动态的日志系统，它有以下特点：

1. 多种的消息等级，可自定义添加新的等级。在打印与日志写入可以使用权重、指定消息或指定模块内的消息进行过滤，实现个性化的消息输出。

2. 支持控制台样式打印，有完善的样式体系可以直接使用，自定义的消息模版可以实现个性化的消息输出，在未有打印环境的情况下停止打印节省资源。

3. 支持日志文件记录，支持动态修改输出文件，可自由开启关闭。该方法不会阻塞进程，对你的程序影响微乎其微。

4. 可以输出自定义格式的进度条，这对于一些下载或加载的控制台显示非常有帮助。

## **安装**

目前仅支持python3.11，这里也推荐将python升级到3.11。

```bash
pip install CheeseLog
```

## **示例**

### **基本用法**

打印各种类型的Hello World，更多的内置方法请查看[Logger](https://github.com/CheeseUnknown/CheeseLog/blob/master/documents/Logger.md)。

```python
from CheeseLog import logger

logger.debug('Hello World')
logger.info('Hello World')
logger.warning('Hello World')
logger.danger('Hello World')
logger.error('Hello World')

logger.destory()
```

### **样式打印**

更多样式请查看[Style](https://github.com/CheeseUnknown/CheeseLog/blob/master/documents/Style.md)。

```python
from CheeseLog import logger

# 如果没有日志文件输出，可以在message直接使用样式
logger.debug('<green>Hello World</green>')

# 因为message会被记录到日志文件中
logger.debug('Hello World', '<green>Hello World</green>')

logger.destory()
```

### **日志输出**

```python
from CheeseLog import logger

logger.filePath = './myLog.log'
logger.debug('Hello World')
# 中途修改输出日志是可以的
logger.filePath = './yourLog.log'
logger.debug('Hello World')

logger.destory()
```

### **消息过滤**

更多消息过滤信息请看[Logger](https://github.com/CheeseUnknown/CheeseLog/blob/master/documents/Logger.md)。

更多消息等级信息请看[Level](https://github.com/CheeseUnknown/CheeseLog/blob/master/documents/Level.md)。

```python
from CheeseLog import logger

logger.filePath = './myLog.log'
logger.weightFilter = 20 # 权重过滤，优先级最高
logger.levelFilter.add('DANGER') # 指定消息等级过滤，优先级其次
logger.moduleFilter['Xxx'] = 100 # 指定模块过滤，优先级最后
...
```

## **更多...**

### 1. [**Style**](https://github.com/CheeseUnknown/CheeseLog/blob/master/documents/Style.md)

### 2. [**Level**](https://github.com/CheeseUnknown/CheeseLog/blob/master/documents/Level.md)

### 3. [**Logger**](https://github.com/CheeseUnknown/CheeseLog/blob/master/documents/Logger.md)

### 4. [**Progress Bar**](https://github.com/CheeseUnknown/CheeseLog/blob/master/documents/ProgressBar.md)
