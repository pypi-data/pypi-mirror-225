# 日志记录

## 简介
日志记录模块是一个简单的日志输出工具，它可以将不同等级（INFO、WARNING、ERROR、DEBUG、CRITICAL）的日志输出到控制台。

## 使用方法
要使用日志记录模块，请在您的Python脚本或模块中导入它，如下所示：

```
pip install logPPP
```

```python
import logPPP/from logPPP import *
```

## 示例

```python
from logPPP import *

Config(logging_is_output_sys_stdout=True, logging_is_output_file=False, logging_level=DEBUG)
logger.info("info")
logger.debug("debug")
logger.warning("warning")
logger.error("error")
logger.critical("critical")

import logPPP

logPPP.Config(logging_is_output_sys_stdout=True, logging_is_output_file=False, logging_level=logPPP.DEBUG)
logPPP.logger.info("info")
logPPP.logger.debug("debug")
logPPP.logger.warning("warning")
logPPP.logger.error("error")
logPPP.logger.critical("critical")
```
