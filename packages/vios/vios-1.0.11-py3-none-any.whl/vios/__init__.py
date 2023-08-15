# vios(Virtual Input and Output System)，主要定义设备驱动及执行流程，包含以下功能模块：

# 一、driver：设备驱动
#     1、所有驱动继承自BaseDriver，类名统一为Driver，并要求实现open/close/read/write四个方法。样板见VirtualDevice
#     2、以设备或厂家为名新建文件夹（并于其内新建__init__.py文件）放于driver/common内，将厂家提供的底层库（若有）置于其内

# 二、envelope：执行流程，见各模块说明

# 三、collection：一些工具、函数、类或其他


import json
import sys
from pathlib import Path

try:
    with open(Path.home()/'quark/startup.json', 'r') as f:
        startup = json.loads(f.read())
    sys.path.append(startup['site'])  # for python>=3.11.4
except Exception as e:
    print(e)
    startup = {}
