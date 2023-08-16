"""指令生成及处理
1、线路编绎，并返回编绎后的结果及相关额外参数
2、将1得到的结果进行硬件解析，并整合所需参数
"""

import os
from copy import deepcopy
from typing import Any

import numpy as np
from lib import stdlib
from waveforms.namespace import DictDriver
from waveforms.qlisp import compile as _compile
from lib.arch.baqis import assembly_code
from lib.arch.baqis_config import QuarkLocalConfig
from qlisp import Signal


#region context
class CompilerContext(QuarkLocalConfig):
    def __init__(self, data) -> None:
        super().__init__(data)
        self.reset(data)
        self.initial = {}
        self.bypass = {}
        self._keys = []

    def reset(self, snapshot):
        if isinstance(snapshot, dict):
            self._QuarkLocalConfig__driver = DictDriver(deepcopy(snapshot))
        else:
            self._QuarkLocalConfig__driver = snapshot

    def snapshot(self):
        return self._QuarkLocalConfig__driver 


cfg = CompilerContext({})  # cfg (CompilerContext): 线路编绎所需配置


def initialize(snapshot, **kwds):
    """初始化编译上下文环境，即每个线路对应的当前的cfg表

    Args:
        snapshot (_type_): 当前的cfg表

    Returns:
        CompilerContext: 用于编译的上下文环境

    # overwrite reset in CompilerContext
    # def reset(self, snapshot):
    #     if isinstance(snapshot, dict):
    #         self.__driver = DictDriver(deepcopy(snapshot))
    #     else:
    #         super().reset(snapshot)

    """
    if isinstance(snapshot, int):
        return os.getpid()
    cfg.reset(snapshot)
    cfg.initial = kwds.get('initial', {'restore': [('WAIT', 'T', 0.01, 's')]})
    cfg.bypass = kwds.get('bypass', {})
    cfg._keys = kwds.get('keys', [])
    return cfg
#endregion context


#region compile
def _form_signal(sig):
    """signal类型
    """
    sig_tab = {
        'trace': Signal.trace,
        'iq': Signal.iq,
        'state': Signal.state,
        'count': Signal.count,
        'diag': Signal.diag,
        'population': Signal.population,
        'trace_avg': Signal.trace_avg,
        'iq_avg': Signal.iq_avg,
        'remote_trace_avg': Signal.remote_trace_avg,
        'remote_iq_avg': Signal.remote_iq_avg,
        'remote_state': Signal.remote_state,
        'remote_population': Signal.remote_population,
        'remote_count': Signal.remote_count,
    }
    if isinstance(sig, str):
        if sig == 'raw':
            sig = 'iq'
        try:
            return sig_tab[sig]
        except KeyError:
            pass
    elif isinstance(sig, Signal):
        return sig
    raise ValueError(f'unknow type of signal "{sig}".'
                     f" optional signal types: {list(sig_tab.keys())}")


def ccompile(sid: int, instruction: dict, circuit: list, **kwds):
    """编绎线路，生成可执行的指令，包括波形生成、采集卡参数、触发设置等

    Args:
        sid (int): 任务步数
        instruction (dict): 默认执行步骤，与编译后的结构(即compiled)相似，但可能更多，便于扩展额外指令
        circuit (list): 用户定义的线路(@HK)

    Returns:
        tuple: 编绎后的线路，数据处理所需参数

    >>> from quark import connect
    >>> s = connect('QuarkServer')
    >>> cfg = initialize(s.snapshot())
    >>> circuit = [(('Measure',0),'Q0503')]
    >>> instruction, datamap =ccompile(0,circuit,signal='iq')
    >>> instruction
    {'main': [('WRITE', 'Q0503.waveform.DDS', <waveforms.waveform.Waveform at 0x291381b6c80>, ''),
              ('WRITE', 'M5.waveform.DDS', <waveforms.waveform.Waveform at 0x291381b7f40>, ''),
              ('WRITE', 'ADx86_159.CH5.Shot', 1024, ''),
              ('WRITE', 'ADx86_159.CH5.Coefficient', {'start': 2.4000000000000003e-08,
                                                      'stop': 4.0299999999999995e-06,
                                                      'wList': [{'Delta': 6932860000.0,
                                                                  'phase': 0,
                                                                  'weight': 'const(1)',
                                                                  'window': (0, 1024),
                                                                  'w': None,
                                                                  't0': 3e-08,
                                                                  'phi': -0.7873217091999384,
                                                                  'threshold': 2334194991.172387}]}, ''),
              ('WRITE', 'ADx86_159.CH5.TriggerDelay', 7e-07, ''),
              ('WRITE', 'ADx86_159.CH5.CaptureMode', 'alg', ''),
              ('WRITE', 'ADx86_159.CH5.StartCapture', 54328, '')],
              'READ': [('READ', 'ADx86_159.CH5.IQ', 'READ', '')]}
     >>> datamap
    {'dataMap': {'cbits': {0: ('READ.ADx86_159.CH5', 0, 6932860000.0, {'duration': 4e-06,
                                                                    'amp': 0.083,
                                                                    'frequency': 6932860000.0,
                                                                    'phase': [[-1, 1], [-1, 1]],
                                                                    'weight': 'const(1)',
                                                                    'phi': -0.7873217091999384,
                                                                    'threshold': 2334194991.172387,
                                                                    'ring_up_amp': 0.083,
                                                                    'ring_up_waist': 0.083,
                                                                    'ring_up_time': 5e-07,
                                                                    'w': None},
                            3e-08,
                            2.4000000000000003e-08,
                            4.0299999999999995e-06)},
                'signal': 2,
                'arch': 'baqis'}}

    """
    kwds['signal'] = _form_signal(kwds.get('signal'))
    kwds['lib'] = kwds.get('lib', stdlib)

    ctx = kwds.get('ctx', cfg)
    ctx.snapshot().cache = kwds.get('cache', {})

    # print('Compiling', circuit)
    code = _compile(circuit, cfg=ctx, **kwds)
    cmds, datamap = assembly_code(code)
    # print('Compiled', cmds)
    compiled = {}
    for cmd in cmds:
        ctype = type(cmd).__name__  # WRITE,TRIG,READ
        if ctype == 'WRITE':
            step = 'main'
        else:
            step = ctype
        op = (ctype, cmd.address, cmd.value, 'au')
        if step in compiled:
            compiled[step].append(op)
        else:
            compiled[step] = [op]

    # merge loop body with compiled result
    for step, _cmds in compiled.items():
        if step in instruction:
            instruction[step].extend(_cmds)
        else:
            instruction[step] = _cmds

    return instruction, {'dataMap': datamap} | kwds

#endregion compile


#region assemble
def assemble(sid: int, instruction: dict[str, list[str, str, Any, str]]):
    """重组编译(ccompile)生成的指令集合(见cccompile), 并生成相应的硬件操作指令

    Args:
        sid (int): 任务步数
        instruction (dict[str, list[str, str, Any, str]]): 编译生成的指令集合(见ccompile)，可能包括额外的操作

    Raises:
        TypeError: srate应为浮点数，否则设置为-1.0
    """
    for step, operations in instruction.items():
        ccmd = {}  # cached cmds not in the mapping
        scmd = {}  # effective cmds in the mapping
        for ctype, target, value, unit in operations:
            kwds = {'target': target, 'filter': cfg.query('etc.filter')}
            if 'CH' in target or ctype == 'WAIT':
                _target = target
            else:
                try:
                    context = cfg.query(target.split('.', 1)[0])
                    mapping = cfg.query('etc.mapping')
                    _target = decode(target, context, mapping)
                    kwds.update({"context": context})  # , 'cached': ccmd})
                except (ValueError, KeyError) as e:
                    ccmd[target] = value
                    continue

                if sid == 0:
                    init = cfg.query(target.removesuffix('.Q').removesuffix('.Q'))
                    cfg.initial['restore'].append((ctype, target, init, unit))

            if ctype != 'WAIT':
                dev = _target.split('.', 1)[0]
                kwds['srate'] = cfg.query(f'dev.{dev}.srate')
            _wrval = [ctype, value, unit, kwds]

            try:
                if sid == 0:
                    cfg.bypass.clear()
                preprocess(_target, _wrval, scmd, cfg.bypass)
            except Exception as e:
                print(f'Failed to preprocess {target}!')
                scmd[_target] = _wrval
        instruction[step] = scmd


# 设备通道与config表中字段的映射关系
MAPPING = {
    "setting_LO": "LO.Frequency",
    "setting_POW": "LO.Power",
    "setting_OFFSET": "ZBIAS.Offset",
    "waveform_RF_I": "I.Waveform",
    "waveform_RF_Q": "Q.Waveform",
    "waveform_TRIG": "TRIG.Marker1",
    "waveform_DDS": "DDS.Waveform",
    "waveform_SW": "SW.Marker1",
    "waveform_Z": "Z.Waveform",
    "setting_PNT": "ADC.PointNumber",
    "setting_SHOT": "ADC.Shot",
    "setting_TRIGD": "ADC.TriggerDelay"
}


# 指令过滤
SUFFIX = ('Waveform', 'Shot', 'Coefficient', 'TriggerDelay')


def decode(target: str, context: dict, mapping: dict = MAPPING):
    """Qubit等属性与硬件通道之间的映射转换

    Args:
        target (str): 待解析对象，如Q0.setting.LO
        context (dict): 对象所在cfg的字段
        mapping (dict, optional): 通道和硬件属性的映射关系. Defaults to MAPPING.

    Raises:
        KeyError: 通道映射不存在
        ValueError: 通道不存在

    Returns:
        str: 通道，如AD.CH1.TraceIQ
    """
    try:
        mkey = target.split('.', 1)[-1].replace('.', '_')
        chkey, quantity = mapping[mkey].split('.', 1)
    except KeyError as e:
        raise KeyError(f'{e} not found in mapping!')

    try:
        channel = context.get('channel', {})[chkey]
    except KeyError as e:
        raise KeyError(f'{chkey} not found!')

    if channel is None:
        raise ValueError('ChannelNotFound')
    elif not isinstance(channel, str):
        raise TypeError(f'Wrong type of channel of {target}, string needed got {channel}')
    elif 'Marker' not in channel:
        channel = '.'.join((channel, quantity))

    return channel


def merge(context: dict, cached: dict = {'Q0101.calibration.Z.delay': 12345}):
    """合并指令执行上下文环境，如将{'Q0101.calibration.z.delay':12345}合并至Q0101
    context['target']: 如Q010.waveform.Z，根据Q0101来判断合并cached中的哪个字段

    Args:
        context (dict): 从cfg表中获取，即Qubit、Coupler等字段
        cached (dict): 无实际通道的指令缓存，形如{'Q0101.calibration.z.delay':12345}
    """
    for ck, cv in cached.items():
        node, path = ck.split('.', 1)
        if context['target'].startswith(node):
            for k in path.split('.'):
                dk = context.get(k, {})
                if isinstance(dk, dict):
                    context = dk
                    continue
                context[k] = cv


def preprocess(target: str, cmd: list, cache: dict, bypass: dict = {}):
    """设备逻辑预处理（如相同通道写多个波形等），处理完毕送往calculator进行采样等计算。

    Args:
        target (str): 设备通道，如AWG.CH1.Waveform
        cmd (list): 待执行指令，格式为(READ|WRITE,value,unit,kwds)。其中kwds为
                    {'target':'原始指令如Q0101.waveform.Z', 
                     'filter':calculator中波形是否采样列表,
                     'srate':'对应设备采样率',
                     'context':'cfg表中字段，如Q0101', 
                     'cached':'无实际通道指令，详见merge函数'}
        cache (dict): 已缓存指令，格式为{target: cmd}
        bypass (dict): 缓存重复指令以避免重复设置
    """
    kwds = cmd[-1]

    # 重复指令缓存
    if target in bypass and target.endswith(SUFFIX) and bypass[target][0] == cmd[1]:
        return cache
    bypass[target] = (cmd[1], kwds['target'])

    # context设置，用于calculator.calculate
    context = kwds.pop('context', {})  # 即Qubit、Coupler等
    if context:
        kwds['LEN'] = context['waveform']['LEN']
        kwds['calibration'] = context['calibration']
        # merge(context=kwds, cached=kwds.pop('cached', {}))

    # 波形采样率设置
    if target.endswith('Waveform') and type(cmd[1]).__name__ == 'Waveform':
        cmd[1].sample_rate = kwds['srate']

    # 处理多通道共用逻辑
    if target in cache and target.endswith('Waveform'):
        cache[target][1] += cmd[1]
    else:
        cache[target] = cmd


#endregion assemble

# %%
if __name__ == "__main__":
    import doctest
    doctest.testmod()
