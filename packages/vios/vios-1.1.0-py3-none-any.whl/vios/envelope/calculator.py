"""所有指令都会由此模块进行预处理，如采样、失真、串扰等，
并送入设备执行(见device模块)
"""

import numpy as np
from lib.pool import calibrate
from waveforms import Waveform, wave_eval


def calculate(step: str, target: str, cmd: list):
    """指令的预处理

    Args:
        step (str): 步骤名，如main/step1/...
        target (str): 设备通道，如AWG.CH1.Offset
        cmd (list): 操作指令，格式为(操作类型, 值, 单位, kwds)。其中
            操作类型包括WRITE/READ/WAIT, kwds见assembler.preprocess说明。

    Returns:
        tuple: 预处理结果
    
    >>> calculate('main', 'AWG.CH1.Waveform',('WRITE',square(100e-6),'au',{'calibration':{}}))
    """
    ctype, value, unit, kwds = cmd

    if ctype != 'WRITE':
        return (step, target, cmd)

    if isinstance(value, str):
        try:
            func = wave_eval(value)
        except SyntaxError as e:
            func = value
    else:
        func = value

    if isinstance(func, Waveform):
        try:
            ch = kwds['target'].split('.')[-1]
            delay = kwds['calibration'][ch]['delay']
        except Exception as e:
            print('cali error', e)
            delay = 0
        func = func >> delay
        func.start = 0
        func.stop = kwds['LEN']
        func.sample_rate = kwds['srate']
        func.bounds = tuple(np.round(func.bounds, 18))

        # see etc.filter
        if target.startswith(tuple(kwds.get('filter', ['zzzzz']))):
            cmd[1] = func
            # return (step, target, cmd)
        else:
            cmd[1] = func.sample()

            # 注意！注意！注意！
            # predistort定义移至systemq/lib/pool.py中以便于修改
            try:
                distortion = kwds['calibration'][ch]['distortion']
                cmd[1] = calibrate(cmd[1], distortion, kwds['srate'])
            except:
                distortion = 0
    else:
        # array
        cmd[1] = func

    cmd[-1] = {'sid': kwds['sid'], 'autokeep': kwds['autokeep']}

    return (step, target, cmd)


# def crosstalk(step: str,
#               result: dict,
#               crosstalk: dict = {},
#               stored: dict = {}):
#     """串扰处理

#     Args:
#         step (str): 步数
#         result (dict): 指令预处理后的结果
#         crosstalk (dict, optional): 串扰矩阵等参数. Defaults to {}.
#         stored (dict, optional): 已存储设置. Defaults to {}.

#     Returns:
#         dict: 处理后的指令
#     """
#     # print('ssssssssssssssss', stored)
#     # for ctkey, ctval in crosstalk.items():
#     #     zpulse = []
#     #     zchannel = []
#     #     for ctch in ctval['channels']:
#     #         zpulse.append(result[ctch][2])
#     #         zchannel.append(ctch)
#     #     cres = [1, 2, 3]  # ctval['M']*zpulse
#     #     for idx, ctch in enumerate(zchannel):
#     #         result[ctch][2] = 13414  # cres[idx]
#     #         stored[ctch] = 12341341412
#     return result


# def calibrate(step: str, target: str, cmd: list):
#     return (step, target, cmd)


if __name__ == "__main__":
    import doctest
    doctest.testmod()