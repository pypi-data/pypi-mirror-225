import math
import numpy as np
from pysndlib import *
from .env import scale_envelope
# 
# 
# def src_duration(e):
#     length = e.mus_length - 2
NEARLY_ZERO = 1.0e-10

def binomial(n, k):
    if 0 <= k <= n:
        a= 1
        b=1
        for t in range(1, min(k, n - k) + 1):
            a *= n
            b *= t
            n -= 1
        return a // b
    else:
        return 0

# --------------- src_duration ---------------- #

def src_duration(e):
    length = len(e) - 2
    dur = 0.0
    all_x = e[length] - e[0]
    area = 0
    for i in range(0,length, 2):
        x0 = e[i]
        x1 = e[i+2]
        y0 = e[i+1]
        y1 = e[i+3]
        if abs(y0-y1) < .0001:
            area = (x1 - x0) / (y0 * all_x)
        else:
            if y0 == 0:
                raise ValueError("src can't use an evelope that has 0 as a y value")
            area = (math.log(y1 / y0) * (x1 - x0)) / ((y1-y0)*all_x)
        dur += abs(area)
    return dur
    
# --------------- src_fit_envelope ---------------- #

def src_fit_envelope(e, target_dur):
    return scale_envelope(e, src_duration(e) / target_dur)
    
    
    
# --------------- Dolph-Chebyshev window ---------------- #
# TODO: already in sndlib but will port over later

    
    
# --------------- down_oct ---------------- #
    
# def down_oct(n, snd, chn):
#     length = clm_length(snd)
#     fftlen = math.floor(2**math.ceil(math.log(length, 2)))
#     fftlen2 = fftlen / 2
#     fft_1 = (n * fftlen) - 1
#     fftscale = (1.0 / fftlen)
#     rl = 
#     

# --------------- highpass ---------------- #
# freq in radians
def make_lowpass(fc, length=30):
    """makes an FIR highpass filter"""
    arrlen = 1 + (2 * length)
    arr = np.zeros(arrlen)
    for i in range(-length,length):
        k = i + length
        denom = math.pi * i
        num = -math.sin(fc * i)
        if i == 0:
            arr[k] = fc / math.pi
        else:
            arr[k] = (num / denom) * (.54 + (.46 * math.cos((i * math.pi) / length)))
    print(arr)   
    return make_fir_filter(arrlen, arr)
    
highpass = fir_filter

# --------------- lowpass ---------------- #
# freq in radians
def make_lowpass(fc, length=30):
    """makes an FIR lowpass filter"""
    arrlen = 1 + (2 * length)
    arr = np.zeros(arrlen)
    for i in range(-length,length):
        k = i + length
        denom = math.pi * i
        num = math.sin(fc * i)
        if i == 0:
            arr[k] = fc / math.pi
        else:
            arr[k] = (num / denom) * (.54 + (.46 * math.cos((i * math.pi) / length)))
    print(arr)   
    return make_fir_filter(arrlen, arr)
    
lowpass = fir_filter


# --------------- bandpass ---------------- #
# freq in radians
def make_bandpass(flo, fhi, length=30):
    """makes an FIR bandpass filter"""
    arrlen = 1 + (2 * length)
    arr = np.zeros(arrlen)
    for i in range(-length,length):
        k = i + length
        denom = math.pi * i
        num = math.sin(fhi * i) - math.sin(flo * i)
        if i == 0:
            arr[k] = (fhi - flo) / math.pi
        else:
            arr[k] = (num / denom) * (.54 + (.46 * math.cos((i * math.pi) / length)))
    print(arr)   
    return make_fir_filter(arrlen, arr)
    
bandpass = fir_filter

# --------------- bandstop ---------------- #
# freq in radians

def make_bandstop(flo, fhi, length=30):
    """makes an FIR bandstop filter"""
    arrlen = 1 + (2 * length)
    arr = np.zeros(arrlen)
    for i in range(-length,length):
        k = i + length
        denom = math.pi * i
        num = math.sin(flo * i) - math.sin(fhi * i)
        if i == 0:
            arr[k] = (1.0 - (fhi - flo) / math.pi)
        else:
            arr[k] = (num / denom) * (.54 + (.46 * math.cos((i * math.pi) / length)))
    print(arr)   
    return make_fir_filter(arrlen, arr)
    
bandstop = fir_filter


# --------------- TODO: differentiator ---------------- #

# --------------- IIR filters ---------------- #

# --------------- Butterworth filters ---------------- #

butter = clm_filter

def make_butter_high_pass(fq):
    """makes a Butterworth filter with high pass cutoff at 'freq'"""
    r = math.tan((math.pi * fq) / get_srate())
    r2 = r * r
    c1 = 1.0 / (1.0 + (r * math.sqrt(2.0)) + r2)
    return make_filter(3, [c1, (-2.0 * c1), c1], [0.0, 2.0*(r2-1.0)*c1, ((1.0 + r2 ) - (r * math.sqrt(2.0))) * c1])
    

def make_butter_low_pass(fq):
    """makes a Butterworth filter with low pass cutoff at 'freq'"""
    r = 1.0 / math.tan((math.pi * fq) / get_srate())
    r2 = r * r
    c1 = 1.0 / (1.0 + (r * math.sqrt(2.0)) + r2)
    return make_filter(3, [c1, (2.0 * c1), c1], [0.0, 2.0*(1.0-r2)*c1, ((1.0 + r2 ) - (r * math.sqrt(2.0))) * c1])
    

def make_butter_band_pass(fq, bw):
    """makes a bandpass Butterworth filter with low edge at 'freq' and width 'band'"""
    c = 1.0 / math.tan((math.pi*bw) / get_srate())
    d = 2.0 * math.cos((2.0 * math.pi * fq) / get_srate())
    c1 = 1.0 / (1.0 + c)
    return make_filter(3, [c1,0.0,-c1], [0., -c * d * c1, (c - 1.0) * c1])
    

def make_butter_band_reject(fq, bw):
    """makes a band-reject Butterworth filter with low edge at 'freq' and width 'band'"""
    c = 1.0 / math.tan((math.pi*bw) / get_srate())
    c1 = 1.0 / (1.0 + c)
    c2 = c1 * -2.0 * math.cos((2.0*math.pi*fq) / get_srate())
    return make_filter(3, [c1,c2,c1], [0.0, c2, ((1.0 - c) * c1)])
    

# --------------- Biquads ---------------- #

biquad = clm_filter

def make_biquad(a0,a1,a2,b1,b2):
    """returns a biquad filter (use with the CLM filter gen)"""
    return make_filter(3, [a0,a1,a2], [0.0,b1,b2])
    
def make_local_biquad(a0, a1, a2, gamma, beta):
    return make_biquad(a0, a1, a2, (-2.0 * gamma), (2.0 * beta))

def make_iir_low_pass_2(fc, din):
    theta = (2 * math.pi * fc) / get_srate()
    d = math.sin(theta) * ( (din or math.sqrt(2.0)) / 2.0)
    beta = .5 * ((1.0 - d) / (1.0 + d))
    gamma = (.5 + beta) * math.cos(theta)
    alpha = (.5 * ((.5 + beta) - gamma))
    return make_local_biquad(alpha, 2.0*alpha, alpha, gamma, beta)
    
def make_iir_band_pass_2(f1, f2):
    theta = (2 * math.pi * math.sqrt(f1*f2)) / get_srate()
    t2 = math.tan(theta / (2 * (math.sqrt(f1*f2) / (f2-f1))))
    beta = .5 * ((1.0-t2)/(1.0+t2))
    gamma = (.5 * beta) * math.cos(theta)
    alpha = .5 - beta
    return make_local_biquad(alpha, 0.0, -alpha, gamma, beta)
    
def make_iir_band_stop_2(f1, f2):
    theta = (2 * math.pi * math.sqrt(f1*f2)) / get_srate()
    t2 = math.tan(theta / (2 * (math.sqrt(f1*f2) / (f2-f1))))
    beta = .5 * ((1.0-t2)/(1.0+t2))
    gamma = (.5 * beta) * math.cos(theta)
    alpha = .5 + beta
    return make_local_biquad(alpha, -2.0*gamma, alpha, gamma, beta)



