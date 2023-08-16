"""所有指令都会由此模块进行预处理，如采样、失真、串扰等，
并送入设备执行(见device模块)
"""

import numpy as np
# import scipy
from lib.pool import calibrate
from waveforms import Waveform, wave_eval

# from waveforms.math.signal import (correct_reflection, exp_decay_filter,
#                                    predistort)


# def polycaliZ(waveform, sample_rate, paras):
#     if paras == {}:
#         return waveform

#     def fitfunc(t, p):
#         return (t >= 0) * (np.sum(
#             p[1::2, None] * np.exp(-p[2::2, None] * t[None, :]), axis=0))

#     def fitfunc1(t, p, numofExpinosc):
#         p[0] = 0
#         td = t[None, :]
#         pExp_ = p[1:(2 * numofExpinosc + 1)]
#         pOsc_ = p[(2 * numofExpinosc + 1):]

#         A = pExp_[0::2, None]
#         a = -pExp_[1::2, None]
#         b = pOsc_[0::2, None]
#         phi = pOsc_[1::2, None]

#         part = np.sum(A * np.exp(a * td) * np.sin(b * td + phi), axis=0)
#         return (t >= 0) * part

#     waveform = np.real(waveform)

#     length = len(waveform)
#     nrfft = length / 2 + 1
#     nfft = 2 * (nrfft - 1)
#     # freqs = np.linspace(0, nrfft*1.0/nfft*sample_rate,nrfft, endpoint=False)
#     freqs = np.fft.rfftfreq(int(nfft), 1 / sample_rate)
#     i_two_pi_freqs = 2j * np.pi * freqs
#     tlist = np.arange(length, dtype=float) / sample_rate

#     precalc = 1.0
#     for i in paras:
#         timeFunData = 0.0
#         if paras[i] != {}:
#             if 'errFunc' in i:  ##errfunc关键词暂时不用
#                 for idx_err in paras[i]:
#                     func_used = op.func_willBeused[paras[i][idx_err][0]]
#                     errfunc = func_used(
#                         tlist, paras[i][idx_err][1]
#                     )  ###### 某一遍拟合时用的任意函数，把他的参数传给paras={.......,'errFunc':{'1':[func,np.array],'2':[func,np.array],......}}
#                     timeFunData = errfunc
#                     timeFunDataf = np.fft.rfft(timeFunData)
#                     precalc /= (1.0 +
#                                 timeFunDataf * i_two_pi_freqs / sample_rate)
#             else:

#                 if 'pexp' in paras[i]:
#                     pexp = np.array(paras[i]['pexp'])
#                     # print(i,':',paras[i])
#                     if len(pexp) >= 1:
#                         timeFunData += fitfunc(tlist, pexp)

#                 if 'psin' in paras[i]:
#                     psin = np.array(paras[i]['psin'])
#                     numofExpinosc = (len(psin) - 1) // 4
#                     # print(i,':',paras[i])
#                     if len(psin) >= 1:
#                         timeFunData += fitfunc1(tlist, psin, numofExpinosc)

#                 if 'ppoly' in paras[i]:
#                     polyParas, delayParasAND2nd = np.array(
#                         paras[i]['ppoly']), np.array(paras[i]['time'])
#                     pExp1 = polyParas[:2]
#                     pPoly = polyParas[2:]
#                     tCut, tShift, tstart, sigma1 = np.array(
#                         delayParasAND2nd)[:4]
#                     if len(pPoly) >= 1:
#                         timeFunData += pExp1[0]*np.exp(-pExp1[1]*tlist)*np.polyval(pPoly,tlist)*(tlist<=tCut+20)*\
#                         (0.5-0.5*scipy.special.erf(sigma1*(tlist-tCut+tShift)))*(0.5+0.5*scipy.special.erf(4.0*(tlist-tstart+0.5)))

#                 timeFunDataf = np.fft.rfft(timeFunData)
#                 # timeFunDataf *= smoothfilt(freqs,timeFunDataf)
#                 precalc /= (1.0 + timeFunDataf * i_two_pi_freqs / sample_rate
#                             )  ##### 补偿法直接用height而非-height归一化的原因是，此式的加号为负的减号。
#         else:
#             continue

#     f_cali = precalc
#     f_step = np.fft.rfft(waveform)
#     signal = np.fft.irfft(f_step * f_cali)
#     return np.real(signal)


# def fitdistort_func(time_new, tcut, p_0, p_1, p_2, p_3, p_4, p_5, p_6, e1, t1,
#                     e2, t2):
#     return (scipy.special.erf(time_new/tcut)-1)*(p_0+p_1*time_new+p_2*time_new**2+p_3*time_new**3+
#                                                  p_4*time_new**4+p_5*time_new**5+p_6*time_new**6)+\
#     e1*np.exp(-1*(time_new-tcut)/t1)+e2*np.exp(-1*(time_new-tcut)/t2)


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
            return (step, target, cmd)

        cmd[1] = func.sample()

        # 注意！注意！注意！
        # predistort定义移至systemq/lib/pool.py中以便于修改
        try:
            distortion = kwds['calibration'][ch]['distortion']
            cmd[1] = calibrate(cmd[1], distortion, kwds['srate'])
        except:
            distortion = 0
        # if isinstance(distortion, dict):
        #     filters = []
        #     ker = None
        #     if 'decay' in distortion and isinstance(distortion['decay'], list):
        #         for amp, tau in distortion['decay']:
        #             a, b = exp_decay_filter(amp, tau, kwds['srate'])
        #             filters.append((b, a))
        #     if 'IIR' in distortion and isinstance(distortion['IIR'], dict):
        #         filters.append(
        #             [distortion['IIR']['b'], distortion['IIR']['a']])
        #     if 'FIR' in distortion and isinstance(distortion['FIR'],
        #                                           (list, np.ndarray)):
        #         _ker = distortion['FIR']
        #         if isinstance(_ker, list):
        #             ker = np.asarray(distortion['FIR'])
        #     if 'reflection' in distortion and isinstance(
        #             distortion['reflection'], dict):
        #         A = distortion['reflection']['A']
        #         tau = distortion['reflection']['tau']
        #         cmd[1] = correct_reflection(cmd[1], A, tau, kwds['srate'])
        #     length = len(cmd[1])
        #     if length > 0:
        #         points = np.hstack([np.full((length,), cmd[1][0]), cmd[1]])
        #         cmd[1] = predistort(points, filters, ker)[length:]
        #         cmd[1][-1] = cmd[1][0]
        #     if 'polyfit' in distortion:
        #         if isinstance(distortion['polyfit'], list):
        #             if len(distortion['polyfit']) > 0:
        #                 Y_prefactors = []
        #                 for params in distortion['polyfit']:
        #                     sr = kwds['srate']
        #                     points = cmd[1].shape[0]
        #                     f = np.fft.rfftfreq(points, 1 / sr)
        #                     tlist = np.arange(0, 1 / sr * points, 1 / sr)
        #                     distortdata = fitdistort_func(tlist, *params)
        #                     Y_distort = np.fft.rfft(distortdata, points)
        #                     Y_prefactors.append(
        #                         (1 /
        #                          (1 - 1j * 2 * np.pi * f * Y_distort / sr)))
        #                 Y_inputwf = np.fft.rfft(cmd[1], points)
        #                 for idx, each in enumerate(Y_prefactors):
        #                     if idx == 0:
        #                         Y_prefactors_mul = each
        #                     else:
        #                         Y_prefactors_mul = each * Y_prefactors_mul
        #                 Y_pretrans = Y_prefactors_mul * Y_inputwf
        #                 real = np.real(Y_pretrans)
        #                 imag = np.imag(Y_pretrans)
        #                 Y_pretrans_rn = np.append(Y_pretrans, real - 1j * imag)
        #                 pre_trans_pulse = np.fft.irfft(Y_pretrans_rn, points)
        #                 cmd[1] = pre_trans_pulse
        #     if 'polycaliZ' in distortion:
        #         points = cmd[1]
        #         sample_rate = kwds['srate'] / 1e9
        #         paras = distortion['polycaliZ']
        #         cmd[1] = polycaliZ(points, sample_rate, paras)

    else:
        cmd[1] = func

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