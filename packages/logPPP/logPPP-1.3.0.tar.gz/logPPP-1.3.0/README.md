# 日志记录

## 简介
日志记录模块是一个简单的日志输出工具，它可以将不同等级（INFO、WARNING、ERROR、DEBUG、CRITICAL）的日志输出到控制台。

## 使用方法
要使用日志记录模块，请在您的Python脚本或模块中导入它，如下所示：

```
pip install logPPP
```

## 示例

```python
from logPPP import *

logger = get_logger(logging_level=INFO,
                    logging_is_output_sys_stdout=True,
                    logging_file="log.log",
                    logger_name=None,
                    logging_fmt=None,
                    logging_date_fmt=None)

logger.info("info")
logger.debug("debug")
logger.warning("warning")
logger.error("error")
logger.critical("critical")
```
