import math
import numpy as np
from pysndlib.clm import *
from .env import stretch_envelope, interleave, max_envelope, min_envelope



# from pysndlib.env import stretch_envelope
# --------------- pluck ---------------- #

# could just use multiple value return
def tuneIt(f, s1):
    def getOptimumC(S,o,p):
        pa = (1.0 / o) * math.atan2((S * math.sin(o)), (1.0 + (S * math.cos(o))) - S)
        tmpInt = math.floor(p - pa)
        pc = p - pa - tmpInt
        
        if pc < .1:
            while pc >= .1:
                tmpInt = tmpInt - 1
                pc += 1.0
        return [tmpInt, (math.sin(o) - math.sin(o * pc)) / math.sin(o + (o * pc))]
        
    p = get_srate() / f
    s = .5 if s1 == 0.0 else s1
    o = hz2radians(f)
    vals = getOptimumC(s,o,p)
    vals1 = getOptimumC((1.0 - s), o, p)
    
    if s != 1/2 and math.fabs(vals[1]) < math.fabs(vals1[1]):
        return [(1.0 - s), vals[1], vals[0]]
    else:
        return [s, vals1[1], vals1[0]]



def pluck(start, dur, freq, amp, weighting=.5, lossfact=.9):
    vals = tuneIt(freq, weighting)
    wt0 = vals[0]
    c = vals[1]
    dlen = vals[2]
    beg = seconds2samples(start)
    end = seconds2samples(start + dur)
    lf = 1.0 if (lossfact == 0.0) else min(1.0, lossfact)
    wt = .5 if (wt0 == 0.0) else min(1.0, wt0)
    tab = np.zeros(dlen, dtype=np.double)
    allp = make_one_zero(lf * (1.0 - wt), (lf * wt))
    feedb = make_one_zero(c, 1.0)
    c1 = 1.0 - c
    
    for i in range(0,dlen):
        tab[i] = mus_random(1.0) # could replace with python random
        
    ctr = 0
    for i in range(beg, end):
        ctr = (ctr + 1) % dlen
        val = (c1 * (one_zero(feedb, one_zero(allp, tab[ctr]))))
        tab[ctr] = val
        outa(i, amp * val)


# TODO: --------------- mlbvoi ---------------- #




vox_formants = {
    'I' : ( 390, 1990, 2550),
    'E' : ( 530, 1840, 2480),
    'AE' : ( 660, 1720, 2410),
    'UH' : ( 520, 1190, 2390),
    'A' : ( 730, 1090, 2440),
    'OW' : ( 570, 840, 2410),
    'U' : ( 440, 1020, 2240),
    'OO' : ( 300, 870, 2240),
    'ER' : ( 490, 1350, 1690),
    'W' : ( 300, 610, 2200),
    'LL' : ( 380, 880, 2575),
    'R' : ( 420, 1300, 1600),
    'Y' : ( 300, 2200, 3065),
    'EE' : ( 260, 3500, 3800),
    'LH' : ( 280, 1450, 1600),
    'L' : ( 300, 1300, 3000),
    'I2' : ( 350, 2300, 3340),
    'B' : ( 200, 800, 1750),
    'D' : ( 300, 1700, 2600),
    'G' : ( 250, 1350, 2000),
    'M' : ( 280, 900, 2200),
    'N' : ( 280, 1700, 2600),
    'NG' : ( 280, 2300, 2750),
    'P' : ( 300, 800, 1750),
    'T' : ( 200, 1700, 2600),
    'K' : ( 350, 1350, 2000),
    'F' : ( 175, 900, 4400),
    'TH' : ( 200, 1400, 2200),
    'S' : ( 200, 1300, 2500),
    'SH' : ( 200, 1800, 2000),
    'V' : ( 175, 1100, 2400),
    'THE' : ( 200, 1600, 2200),
    'Z' : ( 200, 1300, 2500),
    'ZH' : ( 175, 1800, 2000),
    'ZZ' : ( 900, 2400, 3800),
    'VV' : ( 565, 1045, 2400)
}

# caar (car (car x))  [0][0]
# cdar (cdr (car x)) [1:][0]
# cadr (car (cdr x)) [1]
# caddr (car (cdr (cdr x))) [2]


# 
# def vox_fun(phons, which):
#     
#     def find_phoneme(phoneme, forms):
#                 
#     
#     pass
# 
# 
# 
# def vox(beg, dur, freq, amp, ampfun, freqfun, freqscl, phonemes, formant_amps, formant_indices,vibscl=.1, deg=0, pcrev=0):
#     start = seconds2samples(beg)
#     end = seconds2samples(beg + dur)
#     car_os = make_oscil(0)
#     fs = len(formant_amps)
#     per_vib = make_triangle_wave(6, amplitude=hz2radians(freq * vibscl))
#     ran_vib = make_rand(20, amplitude=hz2radians(freq * .5 * vibscl))
#     freqf = make_env(freqfun, duration=dur, scaler=hz2radians(freqscl * freq), offset=hz2radians(freq))
#     
#     # simple case
#     a0 = make_env(ampfun, scaler=amp*formant_amps[0], duration=dur)
#     a1 = make_env(ampfun, scaler=amp*formant_amps[1], duration=dur)
#     a2 = make_env(ampfun, scaler=amp*formant_amps[2], duration=dur)
#     o0 = make_oscil(0.0)
#     o1 = make_oscil(0.0)
#     o2 = make_oscil(0.0)
#     e0 = make_oscil(0.0)
#     e1 = make_oscil(0.0)
#     e2 = make_oscil(0.0)
#     ind0 = formant_indices[0]
#     ind1 = formant_indices[1]
#     ind2 = formant_indices[2]
#     f0 = make_env
    


# TODO: --------------- pqwvox ---------------- #

# --------------- fof ---------------- #


def fofins(beg, dur, frq, amp, vib, f0, a0, f1, a1, f2, a2, ae=[0, 0, 25, 1, 75, 1, 100,0], ve=[0,1,100,1]):
    foflen = math.floor(get_srate() / 220.5)
    start = seconds2samples(beg)
    end = seconds2samples(beg + dur)
    ampf = make_env(ae, scaler=amp, duration=dur)
    vibf = make_env(ve, scaler=vib, duration=dur)
    frq0 = hz2radians(f0)
    frq1 = hz2radians(f1)
    frq2 = hz2radians(f2)
    vibr = make_oscil(0)
    foftab = np.zeros(foflen)
    win_freq = ((2.0 * math.pi) / foflen)
    for i in range(foflen):
        v = (a0 * math.sin(i * frq0)) + (a1 * math.sin(i * frq1)) + (a2 * math.sin(i * frq2))
        foftab[i] = v * .5 * (1.0 - math.cos(i * win_freq))
    wt0 = make_wave_train(frq, foftab)
    
    for i in range(start, end):
        outa(i, env(ampf) * wave_train(wt0, (env(vibf) * oscil(vibr))))



# with Sound(play=True):
#     fofins(0, 1, 270, .2, .001, 730, .6, 1090, .3, 2440, .1) # "Ahh"
#
# 
# with Sound( play = True ): #one of JC's favorite demos
#     fofins(0,4,270,.2,0.005,730,.6,1090,.3,2440,.1,[0,0,40,0,75,.2,100,1],
#             [0,0,.5,1,3,.5,10,.2,20,.1,50,.1,60,.2,85,1,100,0])
#     fofins(0,4,(6/5 * 540),.2,0.005,730,.6,1090,.3,2440,.1,[0,0,40,0,75,.2,100,1],
#             [0,0,.5,.5,3,.25,6,.1,10,.1,50,.1,60,.2,85,1,100,0])
#     fofins(0,4,135,.2,0.005,730,.6,1090,.3,2440,.1,[0,0,40,0,75,.2,100,1],
#             [0,0,1,3,3,1,6,.2,10,.1,50,.1,60,.2,85,1,100,0])
        #    

# --------------- fm_trumpet ---------------- #

def fm_trumpet(startime, dur, frq1=250, frq2=1500, amp1=.5, amp2=.1, 
    ampatt1=.03, ampdec1=.35,
    ampatt2=.03, ampdec2=.3,
    modfrq1=250,
    modind11=0.0,
    modind12=2.66,
    modfrq2=250.,
    modind21=0.0,
    modind22=1.8,
    rvibamp=.007,
    rvibfrq=125.0,
    vibamp=.007,
    vibfrq=7.0,
    vibatt=.6,
    vibdec=.2,
    frqskw=.03,
    frqatt=.06,
    ampenv1=[0,0,25,1,75,.9,100,0],
    ampenv2=[0,0,25,1,75,.9,100,0],
    indenv1=[0,0,25,1,75,.9,100,0],
    indenv2=[0,0,25,1,75,.9,100,0],
    degree=0.0,
    distance=1.0,
    reverb_amount=.005):
    
    dec_01 = max(75, (100 * (1.0 - (.01 / dur))))
    beg = seconds2samples(startime)
    end = seconds2samples(startime + dur)
    loc = make_locsig(degree, distance, reverb_amount)
    vibe = stretch_envelope([0,1,25,.1, 75, 0, 100, 0], 25, min((100 * (vibatt / dur)), 45), 75, max((100 * (1.0 - (vibdec / dur)), 55)))

    per_vib_f = make_env(vibe, scaler=vibamp, duration=dur)
    ran_vib = make_rand_interp(rvibfrq, rvibamp)
    per_vib = make_oscil(vibfrq)
    frqe = stretch_envelope([0,0,25,1,75,1,100,0], 25, min(25, (100 * (frqatt / dur))), 75, dec_01)
    frq_f = make_env(frqe, scaler=frqskw, offset=1.0, duration=dur)
    ampattpt1 = min(25, (100 * (ampatt1 / dur)))
    ampdecpt1 = max(75, (100 * (1.0 - (ampdec1 / dur))))
    ampattpt2 = min(25, (100 * (ampatt2 / dur)))
    ampdecpt2 = max(75, (100 * (1.0 - (ampdec2 / dur))))
    
    mod1_f = make_env(stretch_envelope(indenv1, 25, ampattpt1, 75, dec_01), scaler=(modfrq1 * (modind12 - modind11)), duration=dur)
    mod1 = make_oscil(0.0)
    car1 = make_oscil(0.0)
    car1_f = make_env(stretch_envelope(ampenv1, 25, ampattpt1, 75, ampdecpt1), scaler=amp1, duration=dur)
    
    mod2_f = make_env(stretch_envelope(indenv2, 25, ampattpt2, 75, dec_01), scaler=(modfrq2 * (modind22 - modind21)), duration=dur)

    mod2 = make_oscil(0.0)
    car2 = make_oscil(0.0)
    car2_f = make_env(stretch_envelope(ampenv2, 25, ampattpt2, 75, ampdecpt2), scaler=amp2, duration=dur)
    
    for i in range(beg, end):
        frq_change = hz2radians((1.0 + rand_interp(ran_vib)) * 
                            (1.0 + (env(per_vib_f) * oscil(per_vib))) *
                            env(frq_f))
                            
                            
        locsig(loc, i, env(car1_f) * oscil(car1, frq_change * (frq1 + env(mod1_f) * oscil(mod1, modfrq1 * frq_change))) +
                        env(car2_f) * oscil(car2, frq_change * (frq2 + env(mod2_f) * oscil(mod2, modfrq2 * frq_change))))
# 
# with Sound(play=True, statistics=True, reverb=nrev, channels=2):
#     fm_trumpet(0, 3, 250, 1500, .5, .1, degree=45)
#     fm_trumpet(2.9, 3, 350, 1500, .5, .1, degree=45)    

# --------------- stereo_flute ---------------- #

def stereo_flute(start,dur,freq,flow,
                flow_envelope = [0,1,100,1], 
                decay=.01, 
                noise=0.0356, 
                embouchure_size=0.5,
                fbk_scl1=.5, 
                fbk_scl2=.55, 
                offset_pos=0.764264,
                out_scl=1.0, 
                a0=.7, 
                b1=-.3, 
                vib_rate=5, 
                vib_amount=.03, 
                ran_rate=5, 
                ran_amount=0.03):
                    
    period_samples = math.floor(CLM.srate / freq)
    embouchure_samples = math.floor(embouchure_size * period_samples)
    current_excitation = 0.0
    current_difference = 0.0
    current_flow = 0.0
    out_sig = 0.0
    tap_sig = 0.0
    previous_out_sig = 0.0
    previous_tap_sig = 0.0
    dc_blocked_a = 0.0
    dc_blocked_b = 0.0
    previous_dc_blocked_a = 0.0
    previous_dc_blocked_b = 0.0
    delay_sig = 0.0
    emb_sig = 0.0
    beg = seconds2samples(start)
    end = seconds2samples(start + dur)
    flowf = make_env(flow_envelope, scaler=flow, duration=dur - decay)
    periodic_vibrato = make_oscil(vib_rate)
    random_vibrato = make_rand_interp(ran_rate, ran_amount)
    breath = make_rand(CLM.srate/2, amplitude=noise)
    embouchure = make_delay(embouchure_samples, initial_element=0.0)
    bore = make_delay(period_samples)
    offset = math.floor(period_samples * offset_pos)
    reflection_lowpass_filter = make_one_pole(a0, b1)

    for i in range(beg, end):
        
        delay_sig = delay(bore, out_sig)
        emb_sig = delay(embouchure, current_difference)
        current_flow = (vib_amount * oscil(periodic_vibrato)) + rand_interp(random_vibrato) + env(flowf)
        current_difference = current_flow + (current_flow * rand(breath) + (fbk_scl1 * delay_sig))
        current_excitation = emb_sig - (emb_sig*emb_sig*emb_sig)
        out_sig = one_pole(reflection_lowpass_filter, (current_excitation + (fbk_scl2 * delay_sig)))
        tap_sig = tap(bore, offset)
        dc_blocked_a = (out_sig + (.995 * previous_dc_blocked_a)) - previous_out_sig
        dc_blocked_b = (tap_sig + (.995 * previous_dc_blocked_b)) - previous_tap_sig
        outa(i, (out_scl * dc_blocked_a))          
        outb(i, (out_scl * dc_blocked_b)) 
        previous_out_sig = out_sig
        previous_dc_blocked_a = dc_blocked_a
        previous_tap_sig = tap_sig
        previous_dc_blocked_b = dc_blocked_b       
                    
                    
   
# with Sound( play = True, statistics=True, channels=2 ):
#     stereo_flute(0,3,220,.55, flow_envelope=[0,0,25,1,75,1,100,0], ran_amount=.03)
# 
# with Sound( play = True, statistics=True, channels=2 ):
#     stereo_flute(0,3,220,.55, flow_envelope=[0,0,25,1,75,1,100,0], offset_pos=.5)                 


# --------------- fm_bell ---------------- #

def fm_bell(startime, dur, frequency, amplitude, 
        amp_env=[0, 0, .1, 1, 10, .6, 25, .3, 50, .15, 90, .1, 100, 0], 
        index_env=[0, 1, 2, 1.1, 25, .75, 75, .5, 100, .2], index=1.):
    fmInd2 = hz2radians( (8.0 - (frequency / 50.)) * 4)
    beg = seconds2samples(startime)
    end = seconds2samples(startime + dur)
    fmInd1 = hz2radians(32.0 * frequency)
    fmInd3 = fmInd2 * .705 * (1.4 - (frequency / 250.))
    fmInd4 = hz2radians(32.0 * (20  - (frequency / 20)))
    mod1 = make_oscil(frequency * 2)
    mod2 = make_oscil(frequency * 1.41)
    mod3 = make_oscil(frequency * 2.82)
    mod4 = make_oscil(frequency * 2.4)
    car1 = make_oscil(frequency)
    car2 = make_oscil(frequency)
    car3 = make_oscil(frequency * 2.4)
    indf = make_env(index_env, scaler=index, duration=dur)
    ampf = make_env(amp_env, scaler=amplitude, duration=dur)
    
    for i in range(beg, end):
        fmenv = env(indf)
        outa(i, env(ampf) * (oscil(car1, fm=(fmenv * fmInd1 * oscil(mod1))) +
                             (.15 * oscil(car2, fm=(fmenv * ( (fmInd2 * oscil(mod2)) + (fmInd3 * oscil(mod3)) )))) +
                             (.15 * oscil(car3, fm=(fmenv * fmInd4 * oscil(mod4)))) ))
                             
# with Sound( play = True, statistics=True, channels=1 ):
#     fbell = [0,1,2,1.1,25,.75,75,.5,100,.2]
#     abell = [0,0,.1,1,10,.6,25,.3,50,.15,90,.1,100,0]
#     fm_bell( 0,5.000,233.046,.028,abell,fbell,.750)
#     fm_bell( 5.912,2.000,205.641,.019,abell,fbell,.650)
#     fm_bell( 6.085,5.000,207.152,.017,abell,fbell,.750)
#     fm_bell( 6.785,7.000,205.641,.010,abell,fbell,.650)
#     fm_bell( 15.000,.500,880,.060,abell,fbell,.500)
#     fm_bell( 15.006,6.500,293.66,.1,abell,fbell,0.500)
#     fm_bell( 15.007,7.000,146.5,.1,abell,fbell,1.000)
#     fm_bell( 15.008,6.000,110,.1,abell,fbell,1.000)
#     fm_bell( 15.010,10.00,73.415,.028,abell,fbell,0.500)
#     fm_bell( 15.014,4.000,698.46,.068,abell,fbell,0.500)
        
        
# --------------- fm_insect ---------------- #

def fm_insect(startime, dur, frequency, 
                amplitude, 
                amp_env, 
                mod_freq, 
                mod_skew, 
                mod_freq_env, 
                mod_index, 
                mod_index_env, 
                fm_index, 
                fm_ratio, 
                degree=0.0, 
                distance=1.0,
                reverb_amount=.005):
                
    beg = seconds2samples(startime)
    end = seconds2samples(startime + dur)
    loc = make_locsig(degree, distance, reverb_amount)
    carrier = make_oscil(frequency)
    fm1_osc = make_oscil(mod_freq)
    fm2_osc = make_oscil((fm_ratio * frequency))
    ampf = make_env(amp_env, scaler=amplitude, duration=dur)
    indf = make_env(mod_index_env, scaler=hz2radians(mod_index), duration=dur)
    modfrqf = make_env(mod_freq_env, scaler=hz2radians(mod_skew), duration=dur)
    fm2_amp = hz2radians(fm_index * fm_ratio * frequency)
    
    for i in range(beg, end):
        garble_in = (env(modfrqf) * oscil(fm1_osc, env(modfrqf)))
        locsig(loc, i, (env(ampf) * oscil(carrier, (fm2_amp * oscil(fm2_osc, garble_in)) + garble_in)))
        
# LOCUST = [0,0,40,1,95,1,100,.5]
# BUG_HI = [0,1,25,.7,75,.78,100,1]
# AMP = [0,0,25,1,75,.7,100,0]
# 
# with Sound(play=True, statistics=True, channels=1):
#     fm_insect(0,1.699,4142.627,.015,AMP,60,-16.707,LOCUST,500.866,BUG_HI,.346,.500)
#     fm_insect(0.195,.233,4126.284,.030,AMP,60,-12.142,LOCUST,649.490,BUG_HI,.407,.500)
#     fm_insect(0.217,2.057,3930.258,.045,AMP,60,-3.011,LOCUST,562.087,BUG_HI,.591,.500)
#     fm_insect(2.100,1.500,900.627,.06,AMP,40,-16.707,LOCUST,300.866,BUG_HI,.346,.500)
#     fm_insect(3.000,1.500,900.627,.06,AMP,40,-16.707,LOCUST,300.866,BUG_HI,.046,.500)
#     fm_insect(3.450,1.500,900.627,.09,AMP,40,-16.707,LOCUST,300.866,BUG_HI,.006,.500)
#     fm_insect(3.950,1.500,900.627,.12,AMP,40,-10.707,LOCUST,300.866,BUG_HI,.346,.500)
#     fm_insect(4.300,1.500,900.627,.09,AMP,40,-20.707,LOCUST,300.866,BUG_HI,.246,.500)
        
# --------------- fm_drum ---------------- #

def fm_drum(start_time, duration, frequency, amplitude, index, high=True, degree=0.0, distance=1.0, reverb_amount=.01):
    indxfun = [0,0,5,.014,10,.033,15,.061,20,.099,
            	25,.153,30,.228,35,.332,40,.477,
		        45,.681,50,.964,55,.681,60,.478,65,.332,
		        70,.228,75,.153,80,.099,85,.061,
		        90,.033,95,.0141,100,0]

    indxpt = 100 - (100 * ((duration - .1) / duration))
    atdrpt = 100 * ((.01 if high else .015) / duration)
    divindxf = stretch_envelope(indxfun, 50, atdrpt, 65, indxpt)
    ampfun = [0,0,3,.05,5,.2,7,.8,8,.95,10,1.0,12,.95,20,.3,30,.1,100,0]
    casrat = 8.525 if high else 3.515    
    fmrat = 3.414 if high else 1.414
    glsfun = [0,0,25,0,75,1,100,1]
    beg = seconds2samples(start_time)
    end = seconds2samples(start_time + duration)
    glsf = make_env(glsfun, scaler=(hz2radians(66) if high else 0.0), duration=duration)
    ampe = stretch_envelope(ampfun, 10, atdrpt, 15, max((atdrpt + 1), 100 - (100 * ((duration - .05) / duration))))
    ampf = make_env(ampe, scaler=amplitude, duration=duration)
    indxf = make_env(divindxf, scaler=min(hz2radians(index * fmrat * frequency), math.pi), duration=duration)
    mindxf = make_env(divindxf, scaler=min(hz2radians(index * casrat * frequency), math.pi), duration=duration)
    deve = stretch_envelope(ampfun, 10, atdrpt, 90, max((atdrpt + 1), (100 - (100 * ((duration - .05) / duration)))))
    devf = make_env(deve, scaler=min(math.pi, hz2radians(7000)), duration=duration)
    loc = make_locsig(degree, distance, reverb_amount)
    rn = make_rand(7000., 1.0)
    carrier = make_oscil(frequency)
    fmosc = make_oscil(frequency*fmrat)
    cascade = make_oscil(frequency*casrat)
    
    for i in range(beg, end):
        gls = env(glsf)
        locsig(loc, i, (env(ampf) * oscil(carrier, (gls + (env(indxf) * 
                                        oscil(fmosc, ((gls*fmrat)+(env(mindxf)*
                                            oscil(cascade, ((gls*casrat)+(env(devf)*rand(rn))))))))))))
 # 
# with Sound(play=True, statistics=True):
#     fm_drum(0, 1.5, 55, .3, 5, False)
#     fm_drum(2, 1.5, 66, .3, 5, True)

# --------------- gong ---------------- #

def gong(start_time, duration, frequency, amplitude, degree=0.0, distance=1.0, reverb_amount=.005):
    mfq1 = frequency * 1.16
    mfq2 = frequency * 3.14
    mfq3 = frequency * 1.005    
    indx01 = hz2radians(.01 * mfq1)
    indx11 = hz2radians(.30 * mfq1)
    indx02 = hz2radians(.01 * mfq2)
    indx12 = hz2radians(.38 * mfq2)
    indx03 = hz2radians(.01 * mfq3)
    indx13 = hz2radians(.50 * mfq3)
    atpt = 5
    atdur = 100 * (.002 / duration)
    expf = [0,0,3,1,15,.5,27,.25,50,.1,100,0]
    rise = [0,0,15,.3,30,1.0,75,.5,100,0]
    fmup = [0,0,75,1.0,98,1.0,100,0]
    fmdwn = [0,0,2,1.0,100,0]
    ampfun = make_env(stretch_envelope(expf, atpt, atdur, None, None), scaler=amplitude, duration=duration)
    indxfun1 = make_env(fmup, duration=duration, scaler=indx11-indx01, offset=indx01)
    indxfun2 = make_env(fmup, duration=duration, scaler=indx12-indx02, offset=indx02)
    indxfun3 = make_env(fmup, duration=duration, scaler=indx13-indx03, offset=indx03)
    loc = make_locsig(degree, distance, reverb_amount)
    carrier = make_oscil(frequency)
    mod1 = make_oscil(mfq1)
    mod2 = make_oscil(mfq2)
    mod3 = make_oscil(mfq3)
    beg = seconds2samples(start_time)
    end = seconds2samples(start_time + duration)
    
    for i in range(beg, end):
        locsig(loc, i, env(ampfun) * oscil(carrier, (env(indxfun1) * oscil(mod1)) + (env(indxfun2) * oscil(mod2)) + (env(indxfun3) * oscil(mod3))))
        
# with Sound(play=True, statistics=True):
#     gong(0, 3, 261.61, .6)
    
# --------------- attract ---------------- #


def attract(beg, dur, amp, c):
    st = seconds2samples(beg)
    nd = seconds2samples(beg + dur)
    a = .2
    b = .2
    dt = .04
    scale = (.5 * amp) / c
    x = -1.0
    y = 0.0
    z = 0.0
    x1 = 0.0
    
    for i in range(st,nd):
        x1 = x - (dt * (y + z))
        y  += (dt * (x + (a * y)))
        z  += (dt * ((b + (x * z)) - (c * z)))
        x = x1
        outa(i, scale * x)

# with Sound(play=True, statistics=True):
#     attract(0, 2, .5, 4)
    
# --------------- pqw ---------------- #


    
def clip_env(e):
    xs = e[0::2]
    ys = [min(x,1.0) for x in e[1::2]]
    return interleave(xs, ys)
    
    

def pqw(start, dur, spacing_freq, carrier_freq, amplitude, 
        ampfun, indexfun, partials, degree=0.0, distance=1.0, reverb_amount=.005):
    normalized_partials = normalize_partials(partials)
    spacing_cos = make_oscil(spacing_freq, initial_phase=math.pi/2.0)
    spacing_sin = make_oscil(spacing_freq)
    carrier_cos = make_oscil(carrier_freq, initial_phase=math.pi/2.0)
    carrier_sin = make_oscil(carrier_freq)
    sin_coeffs = partials2polynomial(normalized_partials, Polynomial.SECOND_KIND)
    cos_coeffs = partials2polynomial(normalized_partials, Polynomial.FIRST_KIND)
    amp_env = make_env(ampfun, scaler=amplitude, duration=dur)
    ind_env = make_env(clip_env(indexfun), duration=dur)
    loc = make_locsig(degree, distance, reverb_amount)
    r = carrier_freq / spacing_freq
    tr = make_triangle_wave(5, hz2radians(.005 * spacing_freq))
    rn = make_rand_interp(12, hz2radians(.005 * spacing_freq))
    beg = seconds2samples(start)
    end = seconds2samples(start + dur)
    
    for i in range(beg, end):
        vib = triangle_wave(tr) + rand_interp(rn)
        ax = env(ind_env) * oscil(spacing_cos, vib)
        locsig(loc, i, env(amp_env) * 
            ((oscil(carrier_sin, (vib * r)) * oscil(spacing_sin, vib) * polynomial(sin_coeffs, ax)) -
                (oscil(carrier_cos, (vib * r)) * polynomial(cos_coeffs, ax))))

# with Sound( play = True, statistics=True):
#     pqw(0, .5, 200, 1000, .2, [0,0,25,1,100,0], [0, 1, 100, 0], [2, .1, 3, .3, 6, .5])



# --------------- tubebell ---------------- #


def tubebell(beg, dur, freq, amp, base=32.0):
    osc0 = make_oscil(freq * .995)
    osc1 = make_oscil(freq * 1.414 * 0.995)
    osc2 = make_oscil(freq * 1.005)
    osc3 = make_oscil(freq * 1.414)
    ampenv1 = make_env([0,0,.005, 1, dur, 0], base=base, duration=dur, scaler=(amp * .5 * .707))
    ampenv2 = make_env([0,0,.001, 1, dur, 0], base=(2 * base), duration=dur, scaler=(amp * .5))
    ampmod = make_oscil(2.0)
    st = seconds2samples(beg)
    nd = seconds2samples(beg + dur)
    
    for i in range(st, nd):
        outa(i, ((.007 * oscil(ampmod)) + .993) *
                ((env(ampenv1) * oscil(osc0, (.203 * oscil(osc1)))) +
                 (env(ampenv2) * oscil(osc2, (.144 * oscil(osc3))))))
    
# import random
# with Sound( play = True, statistics=True):
#     freqs = [1174.659, 1318.510, 1396.913, 1567.982, 2093.005]
#     for t in np.arange(0, 10, .4):
#         tubebell(t, 1, random.choice(freqs), .5)    

# --------------- wurley ---------------- #

def wurley(beg, dur, freq, amp):
    osc0 = make_oscil(freq)
    osc1 = make_oscil(freq * 4.0)
    osc2 = make_oscil(510.0)
    osc3 = make_oscil(510.0)
    ampmod = make_oscil(8.0)
    g0 = .5 * amp
    ampenv = make_env([0,0,1,1,9,1,10,0], duration=dur)
    indenv = make_env([0,0,.001,1,.15,0,max(dur, .16),0], duration=dur, scaler=.117)
    resenv = make_env([0,0,.001,1,.25,0,max(dur, .26),0], duration=dur, scaler=(.5 * .307 * amp))
    st = seconds2samples(beg)
    nd = seconds2samples(beg + dur)
    for i in range(st, nd):
        outa(i, env(ampenv) * 
            (1.0 + (.007 * oscil(ampmod))) * 
            ((g0 * oscil(osc0, (.307 * oscil(osc1)))) + (env(resenv) * oscil(osc2, (env(indenv) * oscil(osc3))))))
            


# --------------- rhodey ---------------- #

def rhodey(beg, dur, freq, amp, base=.5):
    osc0 = make_oscil(freq)
    osc1 = make_oscil(freq * .5)
    osc2 = make_oscil(freq)
    osc3 = make_oscil(freq * 15.0)
    ampenv1 = make_env([0,0,.005, 1, dur, 0], base=base, duration=dur, scaler=(amp * .5))
    ampenv2 = make_env([0,0,.001, 1, dur, 0], base=(1.5 * base), duration=dur, scaler=(amp * .5))
    ampenv3 = make_env([0,0,.001, 1, .25, 0, max(dur, .26), 0], base=(4. * base), duration=dur, scaler= .109)
    st = seconds2samples(beg)
    nd = seconds2samples(beg + dur)
    for i in range(st, nd):
        outa(i, ( env(ampenv1)*oscil(osc0, (.535 * oscil(osc1)))) + (env (ampenv2) * oscil(osc2, env(ampenv3) * oscil(osc3))))

# --------------- hammondoid ---------------- #

def hammondoid(beg, dur, freq, amp):
    osc0 = make_oscil(freq * .999)
    osc1 = make_oscil(freq * 1.997)
    osc2 = make_oscil(freq * 3.006)
    osc3 = make_oscil(freq * 6.009)
    ampenv1 = make_env([0,0,.005, 1, dur-.008, 1, dur, 0], duration=dur)
    ampenv2 = make_env([0,0,.005, 1, dur, 0], duration=dur, scaler=(.5 * .75 * amp))
    g0 = .25 * .75 * amp
    g1 = .25 * .75 * amp
    g2 = .5 * amp
    st = seconds2samples(beg)
    nd = seconds2samples(beg + dur)
    
    for i in range(st, nd):
        outa(i, (env(ampenv1) * ((g0 * oscil(osc0)) + (g1 * oscil(osc1)) + (g2 * oscil(osc2)))) +
                    (env(ampenv2)*oscil(osc3)))

# --------------- metal ---------------- #

def metal(beg, dur, freq, amp):
    osc0 = make_oscil(freq)
    osc1 = make_oscil(freq * 4.0 * 0.999)
    osc2 = make_oscil(freq * 3.0 * 1.001)
    osc3 = make_oscil(freq * 0.50 * 1.002)
    ampenv0 = make_env([0,0,.001,1, (dur-.002),1,dur,0], duration=dur, scaler=(amp * .615))
    ampenv1 = make_env([0,0,.001,1,(dur-.011),1,dur,0], duration=dur, scaler=.202)
    ampenv2 = make_env([0,0,.01,1,(dur-.015),1,dur,0], duration=dur, scaler=.574)
    ampenv3 = make_env([0,0,.03,1,(dur-.040),1,dur,0], duration=dur, scaler=.116)
    st = seconds2samples(beg)
    nd = seconds2samples(beg + dur)
    
    for i in range(st, nd):
        outa(i, (env(ampenv0) * (oscil(osc0, ((env(ampenv1) * oscil(osc1, env(ampenv2) * oscil(osc2))))) +
                    (env(ampenv3) * oscil(osc3)))))
                    
                    
# --------------- drone ---------------- #

def drone(startime, dur, frequency, amp, ampfun, synth, ampat, ampdc, amtrev, deg, dis, rvibamt, rvibfreq):
    beg = seconds2samples(startime)
    end = seconds2samples(startime + dur)
    waveform = partials2wave(synth)
    amplitude = amp * .25
    freq = hz2radians(frequency)
    s = make_table_lookup(frequency, wave=waveform)
    ampe = stretch_envelope(ampfun, 25, (100 * (ampat / dur)), 75, (100 - (100 * (ampdc / dur))))
    amp_env = make_env(ampe, scaler=amplitude, duration=dur)
    ran_vib = make_rand(rvibfreq, rvibamt*freq)
    loc = make_locsig(deg, dis, amtrev)
    
    for i in range(beg, end):
        locsig(loc, i, env(amp_env) * table_lookup(s, rand(ran_vib)))


# --------------- canter ---------------- #

def canter(beg, dur, pitch, amp_1, deg, dis, pcrev, ampfun, ranfun, skewfun, skewpc, ranpc, ranfreq, indexfun, atdr, dcdr, 
            ampfun1, indfun1, fmtfun1, 
            ampfun2, indfun2, fmtfun2, 
            ampfun3, indfun3, fmtfun3, 
            ampfun4, indfun4, fmtfun4):

    amp = amp_1 * .25
    rangetop = 910.0
    rangebot = 400.0
    k = math.floor(100 * math.log(pitch / rangebot, rangetop / rangebot))
    atpt = 100 * (atdr / dur)
    dcpt = 100 - ( 100 * (dcdr / dur))
    lfmt1 = env_interp(k, fmtfun1)
    lfmt2 = env_interp(k, fmtfun2)
    lfmt3 = env_interp(k, fmtfun3)
    lfmt4 = env_interp(k, fmtfun4)
    
    dev11 = hz2radians(envelope_interp(k, indfun1) * pitch)
    dev12 = hz2radians(envelope_interp(k, indfun2) * pitch)
    dev13 = hz2radians(envelope_interp(k, indfun3) * pitch)
    dev14 = hz2radians(envelope_interp(k, indfun4) * pitch)
    start = seconds2samples(beg)
    end = seconds2samples(beg + dur)
    dev01 = dev11 * .5
    dev02 = dev12 * .5
    dev03 = dev13 * .5
    dev04 = dev14 * .5
    
    harm1 = math.floor(.5 + (lfmt1 / pitch))
    harm2 = math.floor(.5 + (lfmt2 / pitch))
    harm3 = math.floor(.5 + (lfmt3 / pitch))
    harm4 = math.floor(.5 + (lfmt4 / pitch))

    lamp1 = envelope_interp(k, ampfun1) * amp * (1 - math.fabs(harm1 - (lfmt1 / pitch)))
    lamp2 = envelope_interp(k, ampfun2) * amp * (1 - math.fabs(harm2 - (lfmt2 / pitch)))
    lamp3 = envelope_interp(k, ampfun3) * amp * (1 - math.fabs(harm3 - (lfmt3 / pitch)))
    lamp4 = envelope_interp(k, ampfun4) * amp * (1 - math.fabs(harm4 - (lfmt4 / pitch)))
    
    tidx_stretched = stretch_envelope(indexfun, 25, atpt, 75, dcpt)
    tampfun = make_env(stretch_envelope(ampfun, 25, atpt, 75, dcpt), duration=dur)
    tskwfun = make_env(stretch_envelope(skewfun, 25, atpt, 75, dcpt), scaler=hz2radians(pitch * skewpc), duration=dur)
    tranfun = make_env(stretch_envelope(ranfun, 25, atpt, 75, dcpt), duration=dur)    
    d1env = make_env(tidx_stretched, offset=dev01, scaler=dev11, duration=dur)
    d2env = make_env(tidx_stretched, offset=dev02, scaler=dev12, duration=dur)
    d3env = make_env(tidx_stretched, offset=dev03, scaler=dev13, duration=dur)
    d4env = make_env(tidx_stretched, offset=dev04, scaler=dev14, duration=dur)
    modgen = make_oscil(pitch)
    ranvib = make_rand(ranfreq, hz2radians(ranpc * pitch))
    loc = make_locsig(deg, dis, pcrev)
    gen1 = make_oscil(pitch * harm1)
    gen2 = make_oscil(pitch * harm2)
    gen3 = make_oscil(pitch * harm3)
    gen4 = make_oscil(pitch * harm4)
    
    for i in range(start, end):
        frqval = env(tskwfun) + (env(tranfun) * rand(ranvib))
        modval = oscil(modgen, frqval)
        
        locsig(loc, i, env(tampfun) * 
                (lamp1 * oscil(gen1, (((env(d1env)*modval) + frqval) * harm1))) +
                (lamp2 * oscil(gen2, (((env(d2env)*modval) + frqval) * harm2))) +
                (lamp3 * oscil(gen3, (((env(d3env)*modval) + frqval) * harm3))) +
                (lamp4 * oscil(gen4, (((env(d4env)*modval) + frqval) * harm4))))
    

# --------------- nrev ---------------- #

def is_even(n):
    return bool(n%2==0)
    
def next_prime(n):
    np=[]
    isprime=[]
    for i in range (n+1,n+200):
        np.append(i)
    for j in np:
        val_is_prime = True
        for x in range(2,j-1):
            if j % x == 0:
                val_is_prime = False
                break
        if val_is_prime:
            isprime.append(j)
    return min(isprime)
    
def nrev(reverb_factor=1.09, lp_coeff=.7, volume=1.0):
    srscale = get_srate() / 25641
    dly_len = [1433,1601,1867,2053,2251,2399,347,113,37,59,53,43,37,29,19]
    chans = CLM.output.mus_channels
    chan2 = chans > 1
    chan4 = chans == 4
    
    for i in range(0,15):
        val = math.floor(srscale * dly_len[i])
        if is_even(val):
            val += 1
        dly_len[i] = next_prime(val)
        
    length = math.floor(get_srate()) + CLM.reverb.mus_length
    comb1 = make_comb(.822 * reverb_factor, dly_len[0])
    comb2 = make_comb(.802 * reverb_factor, dly_len[1])
    comb3 = make_comb(.733 * reverb_factor, dly_len[2])
    comb4 = make_comb(.753 * reverb_factor, dly_len[3])
    comb5 = make_comb(.753 * reverb_factor, dly_len[4])
    comb6 = make_comb(.733 * reverb_factor, dly_len[5])
    low = make_one_pole(lp_coeff, lp_coeff - 1.0)
    allpass1 = make_all_pass(-.7000, .700, dly_len[6])
    allpass2 = make_all_pass(-.7000, .700, dly_len[7])
    allpass3 = make_all_pass(-.7000, .700, dly_len[8])
    allpass4 = make_all_pass(-.7000, .700, dly_len[9])
    allpass5 = make_all_pass(-.7000, .700, dly_len[11])
    allpass6 = make_all_pass(-.7000, .700, dly_len[12]) if chan2 else None
    allpass7 = make_all_pass(-.7000, .700, dly_len[13]) if chan4 else None
    allpass8 = make_all_pass(-.7000, .700, dly_len[14]) if chan4 else None
    
    filts = []
    
    if not chan2:
        filts.append(allpass5)
        if not chan4:
            filts.extend([allpass5, allpass6])
        else:
            filts.extend([allpass5, allpass6, allpass7, allpass8])
    
    combs = make_comb_bank([comb1, comb2, comb3, comb4, comb5, comb6])
    allpasses = make_all_pass_bank([allpass1, allpass2, allpass3])
    for i in range(length):
        out_bank(filts, i, all_pass(allpass4, one_pole(low, all_pass_bank(allpasses, comb_bank(combs, volume * ina(i, CLM.reverb))))))
    
    

# --------------- reson ---------------- #

def reson(startime, dur, pitch, amp, numformants, indxfun, skewfun, pcskew, skewat, skewdc,
		      vibfreq, vibpc, ranvibfreq, ranvibpc, degree, distance, reverb_amount, data):
		      
    beg = seconds2samples(startime)
    end = seconds2samples(startime + dur)
    carriers = [None] * numformants
    modulator = make_oscil(pitch)
    ampfs = [None] * numformants
    indfs = [None] * numformants
    c_rats = [None] * numformants
    totalamp = 0.0
    loc = make_locsig(degree, distance, reverb_amount)
    pervib = make_triangle_wave(vibfreq, hz2radians(vibpc * pitch))
    ranvib = make_rand_interp(ranvibfreq, hz2radians(ranvibpc * pitch))
    frqe = stretch_envelope(skewfun, 25, 100 * (skewat / dur), 75, 100 - (100 * (skewdc / dur)))
    frqf = make_env(frqe, scaler=hz2radians(pcskew * pitch), duration=dur)
    
    for i in range(0,numformants):
        totalamp += data[i][2]
        
    for i in range(0, numformants):
        frmdat = data[i]
        freq = frmdat[1]
        harm = round(freq / pitch)
        rfamp = frmdat[2]
        ampat = 100 * (frmdat[3] / dur)
        ampdc = 100 - (100 * (frmdat[4] / dur))
        dev0 = hz2radians(frmdat[5] * freq)
        dev1 = hz2radians(frmdat[6] * freq)
        indxat = 100 * (frmdat[7] / dur)
        indxdc = 100 - (100 * (frmdat[8] / dur))
        ampf = frmdat[0]
        rsamp = 1.0 - math.fabs(harm - (freq / pitch))
        cfq = pitch * harm
        if ampat == 0:
            ampat = 25
        if ampdc == 0:
            ampdc = 75
        if indxat == 0:
            indxat = 25
        if indxdc == 0:
            indxdc = 75
        indfs[i] = make_env(stretch_envelope(indxfun, 25, indxat, 75, indxdc), duration=dur, scaler=(dev1 - dev0), offset=dev0)
        ampfs[i] = make_env(stretch_envelope(ampf, 25, ampat, 75, ampdc), duration=dur, scaler=(rsamp * amp * rfamp) / totalamp)
        c_rats[i] = harm
        carriers[i] = make_oscil(cfq)
        
    if numformants == 2:
        e1 = ampfs[0]
        e2 = ampfs[1]
        c1 = carriers[0]
        c2 = carriers[1]
        i1 = indfs[0]
        i2 = indfs[1]
        r1 = c_rats[0]
        r2 = c_rats[1]
        
        for i in range(beg, end):
            vib = env(frqf) + triangle_wave(pervib) + rand_interp(ranvib)
            modsig = oscil(modulator, vib)
            locsig(loc, i, (env(e1) * oscil(c1, (vib * r1) + (env(i1) * modsig))) + (env(e2) * oscil(c2, (vib * r2) + (env(i2) * modsig))))
        
    else:
        for i in range(beg, end):
            outsum = 0.0
            vib = env(frqf) + triangle_wave(pervib) + rand_interp(ranvib)
            modsig = oscil(modulator, vib)
            
            for k in range(0,numformants):
                outsum += env(ampfs[k]) * oscil(carriers[k], (vib * c_rats[k]) + (env(indfs[k]) * modsig))
            
            locsig(loc, i, outsum)       
        

# --------------- cellon ---------------- #


def cellon(beg, dur, pitch0, amp, ampfun, betafun, beta0, beta1, betaat, betadc, ampat, ampdc, dis, pcrev, deg,
            pitch1, glissfun, glissat, glissdc, pvibfreq, pvibpc, pvibfun=[0,1,100,1], pvibat=0, pvibdc=0, rvibfreq=0, rvibpc=0, rvibfun=[0,1,100,1]):
	
    st = seconds2samples(beg)
    nd = seconds2samples(beg + dur)
    pit1 = pitch0 if pitch1 == 0.0 else pitch1
    loc = make_locsig(deg, dis, pcrev)
    carrier = make_oscil(pitch0)
    low = make_one_zero(.5, -.5)
    fm = 0.0
    fmosc = make_oscil(pitch0)
    pvib = make_triangle_wave(pvibfreq, 1.0)
    rvib = make_rand_interp(rvibfreq, 1.0)
    ampap = (100 * (ampat / dur)) if ampat > 0.0 else 25
    ampdp = (100 * (1.0 - (ampdc / dur))) if ampdc > 0.0 else 75
    glsap = (100 * (glissat / dur)) if glissat > 0.0 else 25
    glsdp = (100 * (1.0 - (glissdc / dur))) if glissdc > 0.0 else 75
    betap = (100 * (betaat / dur)) if betaat > 0.0 else 25
    betdp = (100 * (1.0 - (betadc / dur))) if betadc > 0.0 else 75
    pvbap = (100 * (pvbap / dur)) if pvibat > 0.0 else 25
    pvbdp = (100 * (1.0 - (pvibdc / dur))) if pvibdc > 0.0 else 75
    
    pvibenv = make_env(stretch_envelope(pvibfun, 25, pvbap, 75, pvbdp), duration=dur, scaler=hz2radians(pvibpc * pitch0))
    rvibenv = make_env(rvibfun, duration=dur, scaler=hz2radians(rvibpc * pitch0))
    glisenv = make_env(stretch_envelope(pvibfun, 25, pvbap, 75, pvbdp), duration=dur, scaler=hz2radians(pvibpc * pitch0))
    amplenv = make_env(stretch_envelope(ampfun, 25, ampap, 75, ampdp), scaler=amp, duration=dur)
    betaenv = make_env(stretch_envelope(betafun, 25, betap, 75, betdp), duration=dur, scaler=(beta1 - beta0), offset=beta0)
    
    if (pitch0 == pitch1) and (is_zero(pvibfreq) or is_zero(pvibpc)) and (is_zero(rvibfreq) or is_zero(rvibpc)):
        for i in range(st, nd):
            fm = one_zero(low, env(betaenv) * oscil(fmosc, fm))
            locsig(loc, i, env(amplenv)*oscil(carrier,fm))
    else:
        for i in range(st, nd):
            vib = (env(pvibenv)*triangle_wave(pvib)) + (env(rvibenv)*rand_interp(rvib)) + env(glisenv)
            fm = one_zero(low, env(betaenv) * oscil(fmosc, (fm+vib)))
            locsig(loc, i, env(amplenv)*oscil(carrier,fm+vib))

# with Sound( play = True, statistics=True):
#     cellon(0,1,220,.1,[0,0,25,1,75,1,100,0],[0,0,25,1,75,1,100,0],.75,1.0,0,0,0,0,1,0,0,220,[0,0,25,1,75,1,100,0],0,0,0,0,[0,0,100,0],0,0,0,0,[0,0,100,0])  
    
# --------------- jl_reverb ---------------- #

def jl_reverb(decay=3.0, volume=1.0):
    allpass1 = make_all_pass(-.700, .700, 2111)
    allpass2 = make_all_pass(-.700, .700, 673)
    allpass3 = make_all_pass(-.700, .700, 223)
    comb1 = make_comb(.742, 9601)
    comb2 = make_comb(.733, 10007)
    comb3 = make_comb(.715, 10799)
    comb4 = make_comb(.697, 11597)
    outdel1 = make_delay(seconds2samples(.013))
    outdel2 = make_delay(seconds2samples(.011))
    length = math.floor((decay * get_srate()) + Sound.reverb.mus_length)
    filts = [outdel1, outdel2]
    combs = make_comb_bank([comb1, comb2, comb3, comb4])
    allpasses = make_all_pass_bank([allpass1, allpass2, allpass3])
    for i in range(0, length):
        out_bank(filts, i, volume * comb_bank(combs, all_pass_bank(allpasses, ina(i, Sound.reverb))))

# --------------- gran_synth ---------------- #

def gran_synth(startime, duration, audio_freq, grain_dur, grain_interval, amp):
    grain_size = math.ceil(max(grain_dur, grain_interval) * get_srate())
    beg = seconds2samples(startime)
    end = seconds2samples(startime + duration)
    grain_env = make_env([0,0,25,1,75,1,100,0], duration=grain_dur)
    carrier = make_oscil(audio_freq)
    grain = [(env(grain_env) * oscil(carrier)) for i in range(grain_size)]
    grains = make_wave_train(1.0 / grain_interval, grain)
    
    for i in range(beg, end):
        outa(i, amp * wave_train(grains))

# with Sound( play = True, statistics=True):
#     gran_synth(0, 2, 100, .0189, .02, .4)

# --------------- touch_tone ---------------- #

def touch_tone(start, telephone_number):
    touch_tab_1 = [0,697,697,697,770,770,770,852,852,852,941,941,941]
    touch_tab_2 = [0,1209,1336,1477,1209,1336,1477,1209,1336,1477,1209,1336,1477]
    
    for i in range(len(telephone_number)):
        k = telephone_number[i]
        beg = seconds2samples(start + (i * .4))
        end = beg + seconds2samples(.3)
        if is_number(k):
            i = k if not (0 == k) else 11
        else:
            i = 10 if k == '*' else 12
        
        frq1 = make_oscil(touch_tab_1[i])
        frq2 = make_oscil(touch_tab_2[i])
        
        for j in range(beg, end):
            outa(j, (.1 * (oscil(frq1) + oscil(frq2))))
            
# with Sound( play = True, statistics=True):
#     touch_tone(0, [7,2,3,4,9,7,1])
        
# --------------- spectra ---------------- #

def spectra(startime, duration, frequency, amplitude, partials=[1,1,2,0.5], amp_envelope=[0,0,50,1,100,0], 
                vibrato_amplitude=0.005, vibrato_speed=5.0,degree=0.0, distance=1.0, reverb_amount=0.005):

    beg = seconds2samples(startime)
    end = seconds2samples(startime + duration)
    waveform = partials2wave(partials)
    freq = hz2radians(frequency)
    s = make_table_lookup(frequency=frequency, wave=waveform)
    amp_env = make_env(amp_envelope, scaler=amplitude, duration=duration)
    per_vib = make_triangle_wave(vibrato_speed, vibrato_amplitude * freq)
    loc = make_locsig(degree, distance, reverb_amount)
    ran_vib = make_rand_interp(vibrato_speed + 1.0, vibrato_amplitude * freq)
    for i in range(beg, end):
        locsig(loc, i, env(amp_env) * table_lookup(s, triangle_wave(per_vib) + rand_interp(ran_vib)))

# with Sound( play = True, statistics=True):
#     spectra(0, 4, 440.0, .1, [1.0,.4,2.0,.2,3.0,.2,4.0,.1,6.0,.1], [0.0,0.0,1.0,1.0,5.0,0.9,12.0,0.5,25.0,0.25,100.0,0.0])

# --------------- two_tab ---------------- #

def two_tab(startime, duration, frequency, amplitude, partial_1=[1.0,1.0,2.0,0.5], partial_2=[1.0,0.0,3.0,1.0], 
                    amp_envelope=[0,0,50,1,100,0], interp_func=[0,1,100,0], 
                    vibrato_amplitude=.005, vibrato_speed=5.0, 
                    degree=0.0, distance=1.0, reverb_amount=.005):

    beg = seconds2samples(startime)
    end = seconds2samples(startime + duration)
    waveform_1 = partials2wave(partial_1)
    waveform_2 = partials2wave(partial_2)
    freq = hz2radians(frequency)
    s_1 = make_table_lookup(frequency, wave=waveform_1)
    s_2 = make_table_lookup(frequency, wave=waveform_2)
    amp_env = make_env(amp_envelope, scaler=amplitude, duration=duration)
    interp_env = make_env(interp_func, duration=duration)
    interp_env_1 = make_env(interp_func, duration=duration, offset=1.0, scaler=-1.0)
    loc = make_locsig(degree, distance, reverb_amount)
    per_vib = make_triangle_wave(vibrato_speed, vibrato_amplitude * freq)
    ran_vib = make_rand_interp(vibrato_speed+1.0, vibrato_amplitude * freq)
    for i in range(beg, end):
        vib = triangle_wave(per_vib) + rand_interp(ran_vib)
        locsig(loc, i, env(amp_env) * ((env(interp_env)*table_lookup(s_1, vib)) + (env(interp_env_1)*table_lookup(s_2, vib))))
    


# TODO: --------------- lbj_piano ---------------- #


# moved this outside function definition
PIANO_SPECTRA = [[1.97,.0326,2.99,.0086,3.95,.0163,4.97,.0178,5.98,.0177,6.95,.0315,8.02,.0001 ,8.94,.0076,9.96,.0134,10.99,.0284,11.98,.0229,13.02,.0229,13.89,.0010,15.06,.0090,16.00,.0003 ,17.08,.0078,18.16,.0064,19.18,.0129,20.21,.0085,21.27,.0225,22.32,.0061,23.41,.0102,24.48,.0005 ,25.56,.0016,26.64,.0018,27.70,.0113,28.80,.0111,29.91,.0158,31.06,.0093,32.17,.0017,33.32,.0002 ,34.42,.0018,35.59,.0027,36.74,.0055,37.90,.0037,39.06,.0064,40.25,.0033,41.47,.0014,42.53,.0004 ,43.89,.0010,45.12,.0039,46.33,.0039,47.64,.0009,48.88,.0016,50.13,.0006,51.37,.0010,52.70,.0002 ,54.00,.0004,55.30,.0008,56.60,.0025,57.96,.0010,59.30,.0012,60.67,.0011,61.99,.0003,62.86,.0001 ,64.36,.0005,64.86,.0001,66.26,.0004,67.70,.0006,68.94,.0002,70.10,.0001,70.58,.0002,72.01,.0007 ,73.53,.0006,75.00,.0002,77.03,.0005,78.00,.0002,79.57,.0006,81.16,.0005,82.70,.0005,84.22,.0003 ,85.41,.0002,87.46,.0001,90.30,.0001,94.02,.0001,95.26,.0002,109.39,.0003],
			        [1.98,.0194,2.99,.0210,3.97,.0276,4.96,.0297,5.96,.0158,6.99,.0207,8.01,.0009 ,9.00,.0101,10.00,.0297,11.01,.0289,12.02,.0211,13.04,.0127,14.07,.0061,15.08,.0174,16.13,.0009 ,17.12,.0093,18.16,.0117,19.21,.0122,20.29,.0108,21.30,.0077,22.38,.0132,23.46,.0073,24.14,.0002 ,25.58,.0026,26.69,.0035,27.77,.0053,28.88,.0024,30.08,.0027,31.13,.0075,32.24,.0027,33.36,.0004 ,34.42,.0004,35.64,.0019,36.78,.0037,38.10,.0009,39.11,.0027,40.32,.0010,41.51,.0013,42.66,.0019 ,43.87,.0007,45.13,.0017,46.35,.0019,47.65,.0021,48.89,.0014,50.18,.0023,51.42,.0015,52.73,.0002 ,54.00,.0005,55.34,.0006,56.60,.0010,57.96,.0016,58.86,.0005,59.30,.0004,60.75,.0005,62.22,.0003 ,63.55,.0005,64.82,.0003,66.24,.0003,67.63,.0011,69.09,.0007,70.52,.0004,72.00,.0005,73.50,.0008 ,74.95,.0003,77.13,.0013,78.02,.0002,79.48,.0004,82.59,.0004,84.10,.0003],
			        [2.00,.0313,2.99,.0109,4.00,.0215,5.00,.0242,5.98,.0355,7.01,.0132,8.01,.0009 ,9.01,.0071,10.00,.0258,11.03,.0221,12.02,.0056,13.06,.0196,14.05,.0160,15.11,.0107,16.11,.0003 ,17.14,.0111,18.21,.0085,19.23,.0010,20.28,.0048,21.31,.0128,22.36,.0051,23.41,.0041,24.05,.0006 ,25.54,.0019,26.62,.0028,27.72,.0034,28.82,.0062,29.89,.0039,30.98,.0058,32.08,.0011,33.21,.0002 ,34.37,.0008,35.46,.0018,36.62,.0036,37.77,.0018,38.92,.0042,40.07,.0037,41.23,.0011,42.67,.0003 ,43.65,.0018,44.68,.0025,45.99,.0044,47.21,.0051,48.40,.0044,49.67,.0005,50.88,.0019,52.15,.0003 ,53.42,.0008,54.69,.0010,55.98,.0005,57.26,.0013,58.53,.0027,59.83,.0011,61.21,.0027,62.54,.0003 ,63.78,.0003,65.20,.0001,66.60,.0006,67.98,.0008,69.37,.0019,70.73,.0007,72.14,.0004,73.62,.0002 ,74.40,.0003,76.52,.0006,77.97,.0002,79.49,.0004,80.77,.0003,81.00,.0001,82.47,.0005,83.97,.0001 ,87.27,.0002],
			        [2.00,.0257,2.99,.0142,3.97,.0202,4.95,.0148,5.95,.0420,6.95,.0037,7.94,.0004 ,8.94,.0172,9.95,.0191,10.96,.0115,11.97,.0059,12.98,.0140,14.00,.0178,15.03,.0121,16.09,.0002 ,17.07,.0066,18.08,.0033,19.15,.0022,20.18,.0057,21.22,.0077,22.29,.0037,23.33,.0066,24.97,.0002 ,25.49,.0019,26.55,.0042,27.61,.0043,28.73,.0038,29.81,.0084,30.91,.0040,32.03,.0025,33.14,.0005 ,34.26,.0003,35.38,.0019,36.56,.0037,37.68,.0049,38.86,.0036,40.11,.0011,41.28,.0008,42.50,.0004 ,43.60,.0002,44.74,.0022,45.99,.0050,47.20,.0009,48.40,.0036,49.68,.0004,50.92,.0009,52.17,.0005 ,53.46,.0007,54.76,.0006,56.06,.0005,57.34,.0011,58.67,.0005,59.95,.0015,61.37,.0008,62.72,.0004 ,65.42,.0009,66.96,.0003,68.18,.0003,69.78,.0003,71.21,.0004,72.45,.0002,74.22,.0003,75.44,.0001 ,76.53,.0003,78.31,.0004,79.83,.0003,80.16,.0001,81.33,.0003,82.44,.0001,83.17,.0002,84.81,.0003 ,85.97,.0003,89.08,.0001,90.70,.0002,92.30,.0002,95.59,.0002,97.22,.0003,98.86,.0001,108.37,.0001 ,125.54,.0001],
			        [1.99,.0650,3.03,.0040,4.03,.0059,5.02,.0090,5.97,.0227,6.98,.0050,8.04,.0020 ,9.00,.0082,9.96,.0078,11.01,.0056,12.01,.0095,13.02,.0050,14.04,.0093,15.08,.0064,16.14,.0017 ,17.06,.0020,18.10,.0025,19.14,.0023,20.18,.0015,21.24,.0032,22.29,.0029,23.32,.0014,24.37,.0005 ,25.43,.0030,26.50,.0022,27.60,.0027,28.64,.0024,29.76,.0035,30.81,.0136,31.96,.0025,33.02,.0003 ,34.13,.0005,35.25,.0007,36.40,.0014,37.51,.0020,38.64,.0012,39.80,.0019,40.97,.0004,42.09,.0003 ,43.24,.0003,44.48,.0002,45.65,.0024,46.86,.0005,48.07,.0013,49.27,.0008,50.49,.0006,52.95,.0001 ,54.23,.0005,55.45,.0004,56.73,.0001,58.03,.0003,59.29,.0002,60.59,.0003,62.04,.0002,65.89,.0002 ,67.23,.0002,68.61,.0002,69.97,.0004,71.36,.0005,85.42,.0001],
			        [1.98,.0256,2.96,.0158,3.95,.0310,4.94,.0411,5.95,.0238,6.94,.0152,7.93,.0011 ,8.95,.0185,9.92,.0166,10.93,.0306,11.94,.0258,12.96,.0202,13.97,.0403,14.95,.0228,15.93,.0005 ,17.01,.0072,18.02,.0034,19.06,.0028,20.08,.0124,21.13,.0137,22.16,.0102,23.19,.0058,23.90,.0013 ,25.30,.0039,26.36,.0039,27.41,.0025,28.47,.0071,29.64,.0031,30.60,.0027,31.71,.0021,32.84,.0003 ,33.82,.0002,35.07,.0019,36.09,.0054,37.20,.0038,38.33,.0024,39.47,.0055,40.55,.0016,41.77,.0006 ,42.95,.0002,43.27,.0018,44.03,.0006,45.25,.0019,46.36,.0033,47.50,.0024,48.87,.0012,50.03,.0016 ,51.09,.0004,53.52,.0017,54.74,.0012,56.17,.0003,57.40,.0011,58.42,.0020,59.70,.0007,61.29,.0008 ,62.56,.0003,63.48,.0002,64.83,.0002,66.12,.0012,67.46,.0017,68.81,.0003,69.13,.0003,70.53,.0002 ,71.84,.0001,73.28,.0002,75.52,.0010,76.96,.0005,77.93,.0003,78.32,.0003,79.73,.0003,81.69,.0002 ,82.52,.0001,84.01,.0001,84.61,.0002,86.88,.0001,88.36,.0002,89.85,.0002,91.35,.0003,92.86,.0002 ,93.40,.0001,105.28,.0002,106.22,.0002,107.45,.0001,108.70,.0003,122.08,.0002],
			        [1.97,.0264,2.97,.0211,3.98,.0234,4.98,.0307,5.96,.0085,6.94,.0140,7.93,.0005 ,8.96,.0112,9.96,.0209,10.98,.0194,11.98,.0154,12.99,.0274,13.99,.0127,15.01,.0101,15.99,.0002 ,17.04,.0011,18.08,.0032,19.14,.0028,20.12,.0054,21.20,.0053,22.13,.0028,23.22,.0030,24.32,.0006 ,25.24,.0004,26.43,.0028,27.53,.0048,28.52,.0039,29.54,.0047,30.73,.0044,31.82,.0007,32.94,.0008 ,34.04,.0012,35.13,.0018,36.29,.0007,37.35,.0075,38.51,.0045,39.66,.0014,40.90,.0004,41.90,.0002 ,43.08,.0002,44.24,.0017,45.36,.0013,46.68,.0020,47.79,.0015,48.98,.0010,50.21,.0012,51.34,.0001 ,53.82,.0003,55.09,.0004,56.23,.0005,57.53,.0004,58.79,.0005,59.30,.0002,60.03,.0002,61.40,.0003 ,62.84,.0001,66.64,.0001,67.97,.0001,69.33,.0001,70.68,.0001,73.57,.0002,75.76,.0002,76.45,.0001 ,79.27,.0001,80.44,.0002,81.87,.0002],
			        [2.00,.0311,2.99,.0086,3.99,.0266,4.97,.0123,5.98,.0235,6.97,.0161,7.97,.0008 ,8.96,.0088,9.96,.0621,10.99,.0080,11.99,.0034,12.99,.0300,14.03,.0228,15.04,.0105,16.03,.0004 ,17.06,.0036,18.09,.0094,18.95,.0009,20.17,.0071,21.21,.0161,22.25,.0106,23.28,.0104,24.33,.0008 ,25.38,.0030,26.46,.0035,27.50,.0026,28.59,.0028,29.66,.0128,30.75,.0139,31.81,.0038,32.93,.0006 ,34.04,.0004,35.16,.0005,36.25,.0023,37.35,.0012,38.46,.0021,39.59,.0035,40.71,.0006,41.86,.0007 ,42.42,.0001,43.46,.0003,44.17,.0032,45.29,.0013,46.57,.0004,47.72,.0011,48.79,.0005,50.11,.0005 ,51.29,.0003,52.47,.0002,53.68,.0004,55.02,.0005,56.18,.0003,57.41,.0003,58.75,.0007,59.33,.0009 ,60.00,.0004,61.34,.0001,64.97,.0003,65.20,.0002,66.48,.0002,67.83,.0002,68.90,.0003,70.25,.0003 ,71.59,.0002,73.68,.0001,75.92,.0001,77.08,.0002,78.45,.0002,81.56,.0002,82.99,.0001,88.39,.0001],
			        [0.97,.0059,1.98,.0212,2.99,.0153,3.99,.0227,4.96,.0215,5.97,.0153,6.98,.0085 ,7.98,.0007,8.97,.0179,9.98,.0512,10.98,.0322,12.00,.0098,13.02,.0186,14.00,.0099,15.05,.0109 ,15.88,.0011,17.07,.0076,18.11,.0071,19.12,.0045,20.16,.0038,21.23,.0213,22.27,.0332,23.34,.0082 ,24.34,.0014,25.42,.0024,26.47,.0012,27.54,.0014,28.60,.0024,29.72,.0026,30.10,.0008,31.91,.0021 ,32.13,.0011,33.02,.0007,34.09,.0014,35.17,.0007,36.27,.0024,37.39,.0029,38.58,.0014,39.65,.0017 ,40.95,.0012,41.97,.0004,42.43,.0002,43.49,.0001,44.31,.0012,45.42,.0031,46.62,.0017,47.82,.0013 ,49.14,.0013,50.18,.0010,51.54,.0003,53.90,.0006,55.06,.0010,56.31,.0003,57.63,.0001,59.02,.0003 ,60.09,.0004,60.35,.0004,61.62,.0009,63.97,.0001,65.19,.0001,65.54,.0002,66.92,.0002,67.94,.0002 ,69.17,.0003,69.60,.0004,70.88,.0002,72.24,.0002,76.12,.0001,78.94,.0001,81.75,.0001,82.06,.0001 ,83.53,.0001,90.29,.0002,91.75,.0001,92.09,.0002,93.28,.0001,97.07,.0001],
			        [1.98,.0159,2.98,.1008,3.98,.0365,4.98,.0133,5.97,.0101,6.97,.0115,7.97,.0007 ,8.99,.0349,10.01,.0342,11.01,.0236,12.00,.0041,13.02,.0114,14.05,.0137,15.06,.0100,16.05,.0007 ,17.04,.0009,18.12,.0077,19.15,.0023,20.12,.0017,21.24,.0113,22.26,.0126,23.30,.0093,24.36,.0007 ,25.43,.0007,26.47,.0009,27.55,.0013,28.59,.0025,29.61,.0010,30.77,.0021,31.86,.0023,32.96,.0003 ,34.03,.0007,35.06,.0005,36.20,.0006,37.34,.0006,38.36,.0009,39.60,.0016,40.69,.0005,41.77,.0002 ,42.92,.0002,44.02,.0003,45.24,.0006,46.33,.0004,47.50,.0007,48.71,.0007,49.87,.0002,51.27,.0002 ,53.42,.0003,55.88,.0003,57.10,.0004,58.34,.0002,59.86,.0003,61.13,.0003,67.18,.0001,68.50,.0001 ,71.17,.0001,83.91,.0001,90.55,.0001],
			        [0.98,.0099,2.00,.0181,2.99,.0353,3.98,.0285,4.97,.0514,5.96,.0402,6.96,.0015 ,7.98,.0012,8.98,.0175,9.98,.0264,10.98,.0392,11.98,.0236,13.00,.0153,14.04,.0049,15.00,.0089 ,16.01,.0001,17.03,.0106,18.03,.0028,19.05,.0024,20.08,.0040,21.11,.0103,22.12,.0104,23.20,.0017 ,24.19,.0008,25.20,.0007,26.24,.0011,27.36,.0009,27.97,.0030,29.40,.0044,30.37,.0019,31.59,.0017 ,32.65,.0008,33.59,.0005,34.79,.0009,35.75,.0027,36.88,.0035,37.93,.0039,39.00,.0031,40.08,.0025 ,41.16,.0010,43.25,.0004,44.52,.0012,45.62,.0023,45.85,.0012,47.00,.0006,47.87,.0008,48.99,.0003 ,50.48,.0003,51.62,.0001,52.43,.0001,53.56,.0002,54.76,.0002,56.04,.0002,56.68,.0006,57.10,.0003 ,58.28,.0005,59.47,.0003,59.96,.0002,60.67,.0001,63.08,.0002,64.29,.0002,66.72,.0001,67.97,.0001 ,68.65,.0001,70.43,.0001,79.38,.0001,80.39,.0001,82.39,.0001],
			        [1.00,.0765,1.99,.0151,2.99,.0500,3.99,.0197,5.00,.0260,6.00,.0145,6.98,.0128 ,7.97,.0004,8.98,.0158,9.99,.0265,11.02,.0290,12.02,.0053,13.03,.0242,14.03,.0103,15.06,.0054 ,16.04,.0006,17.08,.0008,18.10,.0058,19.16,.0011,20.16,.0055,21.18,.0040,22.20,.0019,23.22,.0014 ,24.05,.0005,25.31,.0019,26.38,.0018,27.44,.0022,28.45,.0024,29.57,.0073,30.58,.0032,31.66,.0071 ,32.73,.0015,33.85,.0005,34.96,.0003,36.00,.0020,37.11,.0018,38.18,.0055,39.23,.0006,40.33,.0004 ,41.52,.0003,43.41,.0028,45.05,.0003,45.99,.0002,47.07,.0003,48.52,.0002,49.48,.0003,50.63,.0003 ,51.81,.0002,54.05,.0002,55.24,.0001,56.62,.0001,57.81,.0004,59.16,.0013,60.23,.0003,66.44,.0001 ,68.99,.0004,75.49,.0001,87.56,.0004],
			        [0.98,.0629,1.99,.0232,2.98,.0217,4.00,.0396,4.98,.0171,5.97,.0098,6.99,.0167 ,7.99,.0003,8.98,.0192,9.98,.0266,10.99,.0256,12.01,.0061,13.02,.0135,14.02,.0062,15.05,.0158 ,16.06,.0018,17.08,.0101,18.09,.0053,19.11,.0074,20.13,.0020,21.17,.0052,22.22,.0077,23.24,.0035 ,24.00,.0009,25.32,.0016,26.40,.0022,27.43,.0005,28.55,.0026,29.60,.0026,30.65,.0010,31.67,.0019 ,32.77,.0008,33.81,.0003,34.91,.0003,36.01,.0005,37.11,.0010,38.20,.0014,39.29,.0039,40.43,.0012 ,41.50,.0006,43.38,.0017,43.75,.0002,44.94,.0005,46.13,.0002,47.11,.0003,48.28,.0005,48.42,.0005 ,49.44,.0003,50.76,.0004,51.93,.0002,54.15,.0003,55.31,.0005,55.50,.0003,56.98,.0003,57.90,.0004 ,60.33,.0002,61.39,.0001,61.59,.0001,65.09,.0002,66.34,.0001,68.85,.0001,70.42,.0002,71.72,.0001 ,73.05,.0003,79.65,.0001,85.28,.0002,93.52,.0001],
			        [1.02,.0185,1.99,.0525,2.98,.0613,3.99,.0415,4.98,.0109,5.97,.0248,6.99,.0102 ,7.98,.0005,8.98,.0124,9.99,.0103,10.99,.0124,12.00,.0016,13.01,.0029,14.03,.0211,15.04,.0128 ,16.07,.0021,17.09,.0009,18.09,.0043,19.14,.0022,20.13,.0016,21.20,.0045,22.21,.0088,23.26,.0046 ,24.29,.0013,25.35,.0009,26.39,.0028,27.49,.0009,28.51,.0006,29.58,.0012,30.70,.0010,31.74,.0019 ,32.75,.0002,33.85,.0001,34.95,.0005,36.02,.0003,37.16,.0009,38.25,.0018,39.35,.0008,40.54,.0004 ,41.61,.0002,43.40,.0004,43.74,.0003,45.05,.0001,46.11,.0003,47.40,.0002,48.36,.0004,49.55,.0004 ,50.72,.0002,52.00,.0001,55.58,.0002,57.02,.0001,57.98,.0002,59.13,.0003,61.56,.0001,66.56,.0001 ,87.65,.0002],
			        [1.00,.0473,1.99,.0506,2.99,.0982,3.99,.0654,5.00,.0196,5.99,.0094,6.99,.0118 ,7.93,.0001,8.99,.0057,10.01,.0285,11.01,.0142,12.03,.0032,13.03,.0056,14.06,.0064,15.06,.0059 ,16.11,.0005,17.09,.0033,18.14,.0027,19.15,.0014,20.17,.0010,21.21,.0059,22.26,.0043,23.31,.0031 ,24.31,.0018,25.33,.0009,26.41,.0005,27.47,.0015,28.53,.0015,29.58,.0041,30.65,.0025,31.73,.0011 ,32.83,.0010,34.98,.0003,36.07,.0009,37.23,.0001,38.26,.0020,39.41,.0014,40.53,.0005,41.40,.0003 ,42.80,.0002,43.48,.0028,43.93,.0001,45.03,.0003,46.18,.0007,47.41,.0001,48.57,.0002,49.67,.0001 ,50.83,.0002,54.39,.0001,55.58,.0002,57.97,.0005,58.11,.0002,59.21,.0001,60.42,.0002,61.66,.0001],
			        [1.00,.0503,2.00,.0963,2.99,.1304,3.99,.0218,4.98,.0041,5.98,.0292,6.98,.0482 ,7.99,.0005,8.99,.0280,10.00,.0237,11.00,.0152,12.02,.0036,12.95,.0022,14.06,.0111,15.07,.0196 ,16.08,.0016,17.11,.0044,18.13,.0073,19.17,.0055,20.19,.0028,21.20,.0012,22.27,.0068,23.30,.0036 ,24.35,.0012,25.35,.0002,26.46,.0005,27.47,.0005,28.59,.0009,29.65,.0021,30.70,.0020,31.78,.0012 ,32.89,.0010,35.06,.0005,36.16,.0008,37.27,.0010,38.36,.0010,39.47,.0014,40.58,.0004,41.43,.0007 ,41.82,.0003,43.48,.0008,44.53,.0001,45.25,.0003,46.43,.0002,47.46,.0002,48.76,.0005,49.95,.0004 ,50.96,.0002,51.12,.0002,52.33,.0001,54.75,.0001,55.75,.0002,56.90,.0002,58.17,.0002,59.40,.0004 ,60.62,.0002,65.65,.0001,66.91,.0002,69.91,.0001,71.25,.0002],
			        [1.00,.1243,1.98,.1611,3.00,.0698,3.98,.0390,5.00,.0138,5.99,.0154,7.01,.0287 ,8.01,.0014,9.01,.0049,10.00,.0144,11.01,.0055,12.05,.0052,13.01,.0011,14.05,.0118,15.07,.0154 ,16.12,.0028,17.14,.0061,18.25,.0007,19.22,.0020,20.24,.0011,21.27,.0029,22.30,.0046,23.34,.0049 ,24.35,.0004,25.45,.0003,26.47,.0007,27.59,.0008,28.16,.0009,29.12,.0002,29.81,.0006,30.81,.0009 ,31.95,.0004,33.00,.0011,34.12,.0005,35.18,.0003,36.30,.0008,37.38,.0003,38.55,.0003,39.64,.0006 ,40.77,.0007,41.52,.0006,41.89,.0006,43.04,.0011,43.60,.0009,44.31,.0002,45.68,.0002,46.56,.0003 ,47.60,.0001,48.83,.0006,50.01,.0003,51.27,.0003,56.04,.0005,57.21,.0003,58.56,.0004,59.83,.0003 ,61.05,.0001,62.20,.0001,67.37,.0002,76.53,.0001],
			        [0.99,.0222,1.99,.0678,2.99,.0683,4.00,.0191,5.00,.0119,6.01,.0232,6.98,.0336 ,7.99,.0082,9.01,.0201,10.01,.0189,11.01,.0041,12.01,.0053,13.05,.0154,14.04,.0159,15.06,.0092 ,16.11,.0038,17.12,.0014,18.15,.0091,19.16,.0006,20.30,.0012,21.25,.0061,22.28,.0099,23.34,.0028 ,24.38,.0012,25.43,.0016,26.49,.0048,27.55,.0025,28.62,.0015,29.71,.0032,30.78,.0077,31.88,.0011 ,32.97,.0007,34.08,.0006,35.16,.0008,36.28,.0004,37.41,.0006,38.54,.0005,39.62,.0002,40.80,.0003 ,41.93,.0001,43.06,.0002,44.21,.0003,45.38,.0002,46.54,.0007,47.78,.0003,48.95,.0004,50.10,.0003 ,51.37,.0002,53.79,.0003,56.20,.0001,58.71,.0002,66.47,.0003],
			        [1.01,.0241,1.99,.1011,2.98,.0938,3.98,.0081,4.99,.0062,5.99,.0291,6.99,.0676 ,7.59,.0004,8.98,.0127,9.99,.0112,10.99,.0142,12.00,.0029,13.02,.0071,14.02,.0184,15.03,.0064 ,16.07,.0010,17.09,.0011,18.11,.0010,19.15,.0060,20.19,.0019,21.24,.0025,22.29,.0013,23.31,.0050 ,25.41,.0030,26.50,.0018,27.53,.0006,28.63,.0012,29.66,.0013,30.77,.0020,31.84,.0006,34.04,.0001 ,35.14,.0001,36.32,.0004,37.41,.0007,38.53,.0007,39.67,.0009,40.85,.0003,45.49,.0002,46.65,.0001 ,47.81,.0004,49.01,.0002,53.91,.0002,55.14,.0002,57.69,.0002],
			        [1.00,.0326,2.00,.1066,2.99,.1015,4.00,.0210,4.97,.0170,5.99,.0813,6.98,.0820 ,7.96,.0011,8.99,.0248,10.03,.0107,11.01,.0126,12.01,.0027,13.01,.0233,14.04,.0151,15.05,.0071 ,16.04,.0002,17.10,.0061,18.12,.0059,19.15,.0087,20.23,.0005,21.25,.0040,22.30,.0032,23.35,.0004 ,24.40,.0001,25.45,.0030,26.54,.0022,27.60,.0003,28.70,.0009,29.80,.0029,30.85,.0006,31.97,.0006 ,34.19,.0004,35.30,.0003,36.43,.0007,37.56,.0005,38.68,.0019,39.88,.0013,41.00,.0003,43.35,.0003 ,44.51,.0002,45.68,.0006,46.93,.0010,48.11,.0006,49.29,.0003,55.58,.0002],
			        [0.98,.0113,1.99,.0967,3.00,.0719,3.98,.0345,4.98,.0121,6.00,.0621,7.00,.0137 ,7.98,.0006,9.01,.0314,10.01,.0171,11.02,.0060,12.03,.0024,13.05,.0077,14.07,.0040,15.12,.0032 ,16.13,.0004,17.15,.0011,18.20,.0028,19.18,.0003,20.26,.0003,21.31,.0025,22.35,.0021,23.39,.0005 ,25.55,.0002,26.62,.0014,27.70,.0003,28.78,.0005,29.90,.0030,31.01,.0011,32.12,.0005,34.31,.0001 ,35.50,.0002,36.62,.0002,37.76,.0005,38.85,.0002,40.09,.0004,43.60,.0001,44.73,.0002,46.02,.0002 ,47.25,.0004,48.44,.0004],
			        [0.99,.0156,1.98,.0846,2.98,.0178,3.98,.0367,4.98,.0448,5.98,.0113,6.99,.0189 ,8.00,.0011,9.01,.0247,10.02,.0089,11.01,.0184,12.03,.0105,13.00,.0039,14.07,.0116,15.09,.0078 ,16.13,.0008,17.14,.0064,18.19,.0029,19.22,.0028,20.25,.0017,21.32,.0043,22.37,.0055,23.42,.0034 ,24.48,.0004,25.54,.0002,26.61,.0017,27.70,.0011,28.80,.0002,29.89,.0019,30.97,.0028,32.09,.0007 ,34.30,.0002,35.44,.0003,36.55,.0001,37.69,.0004,38.93,.0002,40.05,.0005,41.20,.0005,42.37,.0002 ,43.54,.0003,44.73,.0001,45.95,.0002,47.16,.0001,48.43,.0005,49.65,.0004,55.90,.0002,59.81,.0004],
			        [1.01,.0280,2.00,.0708,2.99,.0182,3.99,.0248,4.98,.0245,5.98,.0279,6.98,.0437 ,7.99,.0065,8.99,.0299,10.00,.0073,10.99,.0011,12.03,.0122,13.03,.0028,14.08,.0044,15.11,.0097 ,16.15,.0010,17.17,.0025,18.19,.0017,19.24,.0008,20.28,.0040,21.32,.0024,22.38,.0008,23.46,.0032 ,24.52,.0010,25.59,.0008,26.68,.0009,27.76,.0012,28.88,.0003,29.95,.0005,31.05,.0017,32.14,.0002 ,33.29,.0003,37.88,.0002,39.03,.0002,40.19,.0004,41.37,.0003,43.74,.0002,46.20,.0001,48.68,.0001 ,49.93,.0001,51.19,.0002],
			        [1.00,.0225,1.99,.0921,2.98,.0933,3.99,.0365,4.99,.0100,5.98,.0213,6.98,.0049 ,7.98,.0041,8.98,.0090,9.99,.0068,11.01,.0040,12.03,.0086,13.02,.0015,14.04,.0071,15.09,.0082 ,16.14,.0011,17.15,.0014,18.18,.0010,19.26,.0013,20.26,.0005,21.33,.0006,22.36,.0011,23.46,.0016 ,24.52,.0004,25.59,.0002,26.70,.0006,27.78,.0007,28.87,.0002,30.03,.0008,31.14,.0010,32.24,.0006 ,33.37,.0002,35.67,.0003,37.99,.0004,39.17,.0004,40.35,.0005,41.53,.0001,46.42,.0001],
			        [1.00,.0465,1.99,.0976,2.98,.0678,4.00,.0727,4.99,.0305,5.98,.0210,6.98,.0227 ,8.00,.0085,9.01,.0183,10.02,.0258,11.05,.0003,12.06,.0061,13.05,.0021,14.10,.0089,15.12,.0077 ,16.16,.0016,17.21,.0061,18.23,.0011,19.29,.0031,20.36,.0031,21.41,.0007,22.48,.0013,23.55,.0020 ,24.64,.0004,25.74,.0005,26.81,.0006,27.95,.0006,29.03,.0001,30.22,.0010,31.30,.0004,32.48,.0001 ,33.60,.0002,38.30,.0003],
			        [1.00,.0674,1.99,.0841,2.98,.0920,3.99,.0328,4.99,.0368,5.98,.0206,6.99,.0246 ,8.01,.0048,9.01,.0218,10.03,.0155,11.05,.0048,12.06,.0077,13.00,.0020,14.10,.0083,15.15,.0084 ,16.18,.0015,17.22,.0039,18.27,.0032,19.34,.0026,20.40,.0012,21.47,.0009,22.54,.0008,23.62,.0016 ,24.71,.0005,25.82,.0004,26.91,.0002,28.03,.0008,29.17,.0002,30.32,.0028,31.45,.0004,32.61,.0005 ,33.77,.0001,36.14,.0003,37.32,.0002,38.54,.0005,39.75,.0002,42.23,.0002,48.65,.0001],
			        [1.01,.0423,1.99,.0240,2.98,.0517,4.00,.0493,5.00,.0324,6.00,.0094,6.99,.0449 ,7.99,.0050,9.00,.0197,10.03,.0132,11.03,.0009,12.07,.0017,13.08,.0023,14.12,.0094,15.16,.0071 ,16.21,.0020,17.25,.0005,18.30,.0027,19.04,.0004,20.43,.0022,21.51,.0002,22.59,.0006,23.72,.0018 ,24.80,.0002,25.88,.0002,27.03,.0002,28.09,.0006,29.31,.0002,30.46,.0004,31.61,.0007,32.78,.0005 ,33.95,.0001,36.34,.0002,37.56,.0001,38.80,.0001,40.02,.0001,44.14,.0001],
			        [1.00,.0669,1.99,.0909,2.99,.0410,3.98,.0292,4.98,.0259,5.98,.0148,6.98,.0319 ,7.99,.0076,9.01,.0056,10.02,.0206,11.04,.0032,12.05,.0085,13.08,.0040,14.12,.0037,15.16,.0030 ,16.20,.0013,17.24,.0021,18.30,.0010,19.36,.0015,20.44,.0013,21.50,.0009,22.60,.0015,23.69,.0014 ,24.80,.0006,25.87,.0002,27.02,.0006,28.12,.0002,29.28,.0003,30.43,.0002,31.59,.0007,32.79,.0001 ,35.14,.0001,37.57,.0001,40.03,.0002,41.28,.0004,44.10,.0001],
			        [0.99,.0421,1.99,.1541,2.98,.0596,3.98,.0309,4.98,.0301,5.99,.0103,7.00,.0240 ,8.01,.0073,9.01,.0222,10.04,.0140,11.05,.0033,12.08,.0045,13.13,.0009,14.13,.0015,15.21,.0026 ,16.24,.0003,17.30,.0004,18.35,.0010,19.39,.0003,20.50,.0015,21.57,.0003,22.68,.0011,23.80,.0005 ,24.90,.0008,26.02,.0002,27.16,.0001,28.30,.0006,29.48,.0002,31.81,.0005,33.00,.0003,34.21,.0001 ,37.89,.0001],
			        [0.99,.0389,2.00,.2095,3.00,.0835,3.99,.0289,5.00,.0578,5.99,.0363,7.01,.0387 ,8.01,.0056,9.04,.0173,10.05,.0175,11.08,.0053,12.10,.0056,13.15,.0064,14.19,.0036,15.22,.0019 ,16.29,.0010,17.36,.0017,18.43,.0018,19.51,.0004,20.60,.0011,21.70,.0003,22.82,.0003,23.95,.0001 ,25.05,.0004,26.17,.0001,28.50,.0003,29.68,.0001,32.07,.0003,33.28,.0004,34.52,.0001],
			        [1.00,.1238,1.99,.2270,3.00,.0102,3.99,.0181,4.98,.0415,6.00,.0165,7.01,.0314 ,8.02,.0148,9.04,.0203,10.05,.0088,11.07,.0062,12.11,.0070,13.14,.0054,14.19,.0028,15.24,.0044 ,16.30,.0029,17.38,.0009,18.45,.0026,19.56,.0003,20.65,.0025,21.74,.0014,22.87,.0013,23.99,.0007 ,25.15,.0002,27.46,.0004,28.39,.0006,28.65,.0004,29.85,.0001,31.05,.0002,32.27,.0003,33.52,.0002 ,34.76,.0003],
			        [1.00,.1054,2.00,.2598,2.99,.0369,3.98,.0523,4.99,.0020,5.99,.0051,7.00,.0268 ,8.01,.0027,9.04,.0029,10.05,.0081,11.08,.0047,12.12,.0051,13.16,.0091,14.19,.0015,15.27,.0030 ,16.34,.0017,17.42,.0006,18.51,.0003,19.61,.0007,20.72,.0003,21.84,.0001,22.99,.0010,24.13,.0001 ,28.44,.0001,30.09,.0001],
			        [0.99,.0919,2.00,.0418,2.99,.0498,3.99,.0135,4.99,.0026,6.00,.0155,7.01,.0340 ,8.02,.0033,9.04,.0218,10.08,.0084,11.11,.0057,12.15,.0051,13.21,.0043,14.25,.0015,15.31,.0023 ,16.40,.0008,17.48,.0004,18.59,.0016,19.71,.0010,20.84,.0018,21.98,.0002,23.11,.0013,24.26,.0003 ,26.67,.0002,29.12,.0002,30.37,.0002,31.62,.0003,32.92,.0001],
			        [0.99,.1174,1.99,.1126,2.99,.0370,3.99,.0159,5.01,.0472,6.01,.0091,7.03,.0211 ,8.05,.0015,9.07,.0098,10.11,.0038,11.15,.0042,12.20,.0018,13.24,.0041,14.32,.0033,15.41,.0052 ,16.49,.0001,17.61,.0004,18.71,.0004,19.84,.0004,20.99,.0002,22.14,.0006,23.31,.0006,24.50,.0004 ,25.70,.0002,28.09,.0002,28.66,.0002,32.00,.0001],
			        [1.00,.1085,2.00,.1400,2.99,.0173,3.99,.0229,5.00,.0272,6.02,.0077,7.03,.0069 ,8.04,.0017,9.08,.0045,10.10,.0030,11.15,.0040,12.20,.0007,13.25,.0019,14.32,.0008,15.42,.0024 ,16.50,.0002,17.59,.0005,18.71,.0003,19.83,.0002,20.98,.0005,23.29,.0008],
			        [1.00,.0985,2.00,.1440,2.99,.0364,3.99,.0425,5.00,.0190,6.01,.0089,7.03,.0278 ,8.04,.0006,9.07,.0083,10.10,.0021,11.14,.0050,12.18,.0005,13.26,.0036,14.33,.0005,15.41,.0026 ,17.62,.0004,18.75,.0004,19.89,.0003,21.04,.0012,22.21,.0002,23.38,.0004,27.04,.0001],
		            [0.99,.1273,2.00,.1311,2.99,.0120,4.00,.0099,5.00,.0235,6.02,.0068,7.03,.0162 ,8.06,.0009,9.08,.0083,10.12,.0014,11.17,.0050,12.24,.0010,13.29,.0013,14.39,.0022,15.48,.0011 ,16.59,.0002,17.70,.0003,18.84,.0010,20.00,.0003,21.17,.0003,23.56,.0004,28.79,.0003],
		            [1.00,.1018,2.00,.1486,3.00,.0165,4.00,.0186,5.01,.0194,6.02,.0045,7.04,.0083 ,8.06,.0012,9.10,.0066,10.15,.0009,11.19,.0008,12.26,.0011,13.34,.0028,14.45,.0006,15.53,.0009 ,16.66,.0002,17.79,.0006,18.94,.0005,20.11,.0003,21.29,.0005,22.49,.0003,23.73,.0005,26.22,.0001 ,27.52,.0001,28.88,.0002],
			        [1.00,.1889,1.99,.1822,3.00,.0363,4.00,.0047,5.01,.0202,6.03,.0053,7.05,.0114 ,8.01,.0002,9.13,.0048,10.17,.0010,11.23,.0033,12.30,.0010,13.38,.0006,14.50,.0002,15.62,.0010 ,20.27,.0001,21.47,.0001],
			        [1.00,.0522,1.99,.0763,2.99,.0404,4.00,.0139,5.01,.0185,6.01,.0021,7.06,.0045 ,8.09,.0002,9.11,.0003,10.17,.0006,11.25,.0004,12.32,.0005,13.40,.0003,14.53,.0003,15.65,.0007 ,16.80,.0001,17.95,.0002,19.14,.0006,20.34,.0002,21.56,.0003],
			        [0.99,.1821,1.99,.0773,3.00,.0125,4.01,.0065,5.01,.0202,6.03,.0071,7.05,.0090 ,8.08,.0006,9.13,.0008,10.18,.0013,11.25,.0010,12.33,.0012,13.42,.0006,14.54,.0005,15.65,.0004 ,17.97,.0002,19.15,.0001],
			        [1.00,.1868,2.00,.0951,3.00,.0147,4.01,.0134,5.02,.0184,6.04,.0132,7.06,.0011 ,8.11,.0008,9.15,.0010,10.22,.0012,11.30,.0011,12.40,.0003,13.11,.0004,13.49,.0002,14.62,.0003 ,15.77,.0001],
			        [1.00,.1933,2.00,.0714,3.00,.0373,4.00,.0108,5.02,.0094,6.02,.0010,7.07,.0022 ,8.11,.0002,9.16,.0065,10.23,.0015,11.31,.0023,12.40,.0003,13.53,.0014,14.66,.0002,15.81,.0011 ,18.20,.0002,19.41,.0001],
			        [0.99,.2113,1.99,.0877,3.00,.0492,4.01,.0094,5.02,.0144,6.04,.0103,7.07,.0117 ,8.12,.0006,9.19,.0019,10.25,.0007,11.35,.0017,12.45,.0010,13.58,.0003,14.74,.0003,15.91,.0003 ,19.57,.0002],
			        [0.99,.2455,1.99,.0161,3.00,.0215,4.01,.0036,5.03,.0049,6.04,.0012,7.09,.0036 ,8.14,.0011,9.21,.0009,10.30,.0001,11.40,.0012,12.50,.0001,13.66,.0005,14.84,.0001],
			        [1.00,.1132,2.00,.0252,3.00,.0292,4.01,.0136,5.03,.0045,6.06,.0022,7.11,.0101 ,8.17,.0004,9.23,.0010,10.33,.0012,11.44,.0013,12.58,.0011,13.75,.0002,14.93,.0005,16.14,.0002],
			        [1.00,.1655,2.00,.0445,3.00,.0120,4.00,.0038,5.02,.0015,6.07,.0038,7.11,.0003 ,8.19,.0002,9.25,.0010,10.36,.0011,11.48,.0005,12.63,.0002,13.79,.0003,16.24,.0002],
			        [0.99,.3637,1.99,.0259,3.01,.0038,4.01,.0057,5.03,.0040,6.07,.0067,7.12,.0014 ,8.19,.0004,9.27,.0003,10.38,.0002,12.67,.0001],
			        [1.00,.1193,2.00,.0230,3.00,.0104,4.01,.0084,5.04,.0047,6.08,.0035,7.13,.0041 ,8.20,.0002,9.29,.0005,10.40,.0005,11.53,.0003,12.70,.0002,13.91,.0002],
			        [1.00,.0752,2.00,.0497,3.00,.0074,4.02,.0076,5.05,.0053,6.09,.0043,7.15,.0024 ,8.22,.0001,9.32,.0006,10.45,.0002,11.58,.0001,12.78,.0001,15.22,.0001],
			        [1.00,.2388,2.00,.0629,3.01,.0159,4.04,.0063,5.07,.0051,6.12,.0045,7.19,.0026 ,8.29,.0015,9.43,.0001,11.75,.0002],
			        [1.00,.1919,2.01,.0116,3.01,.0031,4.03,.0090,5.07,.0061,6.13,.0036,7.19,.0013 ,8.30,.0016,9.13,.0001,10.59,.0002,11.78,.0002],
			        [1.00,.1296,2.00,.0135,3.01,.0041,4.04,.0045,5.09,.0028,6.14,.0046,7.23,.0007 ,8.32,.0007,9.50,.0001],
			        [1.00,.0692,2.00,.0209,3.02,.0025,4.05,.0030,5.09,.0047,6.17,.0022,7.25,.0015 ,8.36,.0015,9.53,.0010,10.69,.0001,13.40,.0001],
			        [1.00,.1715,2.00,.0142,3.01,.0024,4.03,.0015,5.07,.0017,6.13,.0018,7.22,.0009 ,8.33,.0014,9.51,.0007,10.69,.0002],
			        [1.00,.1555,2.01,.0148,3.02,.0007,4.06,.0006,5.10,.0005,6.16,.0008,7.26,.0009 ,8.39,.0008,9.58,.0002],
			        [1.00,.1357,2.00,.0116,3.02,.0026,4.04,.0009,5.09,.0004,6.17,.0005,7.27,.0002 ,8.40,.0001],
			        [1.00,.2185,2.01,.0087,3.03,.0018,4.06,.0025,5.11,.0020,6.20,.0012,7.32,.0005 ,8.46,.0001,9.66,.0003],
			        [1.00,.2735,2.00,.0038,3.02,.0008,4.06,.0012,5.12,.0008,6.22,.0011,7.35,.0003 ,8.50,.0002],
			        [1.00,.1441,1.99,.0062,3.01,.0023,4.05,.0011,5.11,.0012,6.20,.0003,7.33,.0004 ,8.50,.0001],
			        [1.00,.0726,2.01,.0293,3.03,.0022,5.14,.0005,6.26,.0011,7.41,.0002,8.63,.0002],
			        [1.00,.0516,2.00,.0104,3.02,.0029,5.15,.0002,6.27,.0001],
			        [1.00,.0329,2.00,.0033,3.03,.0013,4.10,.0005,5.19,.0004,6.32,.0002],
			        [1.00,.0179,1.99,.0012,3.04,.0005,4.10,.0017,5.20,.0005,6.35,.0001],
			        [1.00,.0334,2.01,.0033,3.04,.0011,4.13,.0003,5.22,.0003],
			        [0.99,.0161,2.01,.0100,3.04,.0020,4.13,.0003],
			        [1.00,.0475,1.99,.0045,3.03,.0035,4.12,.0011],
			        [1.00,.0593,2.00,.0014,4.17,.0002],
			        [1.00,.0249,2.01,.0016],
			        [1.00,.0242,2.00,.0038,4.19,.0002],
			        [1.00,.0170,2.02,.0030],
			        [1.00,.0381,2.00,.0017,3.09,.0002],
			        [1.00,.0141,2.03,.0005,3.11,.0003,4.26,.0001],
		            [1.00,.0122,2.03,.0024],
			        [1.00,.0107,2.07,.0007,3.12,.0004],
		            [1.00,.0250,2.02,.0026,3.15,.0002],
			        [1.01,.0092],
			        [1.01,.0102,2.09,.0005],
			        [1.00,.0080,2.00,.0005,3.19,.0001],
			        [1.01,.0298,2.01,.0005]]
			        
def get_piano_partials(freq):
    return PIANO_SPECTRA[round(12 * math.log(freq / 32.703, 2))]  

def lbj_piano(startime, duration, frequency, amplitude, pfreq=None, degree=45, reverb_amount=0, distance=1):
    piano_attack_duration = .04
    piano_release_duration = .2
    
    def make_piano_ampfun(dur):
        db_drop_per_second = -10.0
        releaseAmp = db2linear(db_drop_per_second * dur)
        attackTime = (piano_attack_duration*100) / dur
        return [0,0,(attackTime/4), 1.0, attackTime, 1.0, 100, releaseAmp]
        
    if not is_number(pfreq):
        pfreq = frequency
        
    partials = normalize_partials(get_piano_partials(pfreq))
    beg = seconds2samples(startime)
    newdur = duration + piano_attack_duration + piano_release_duration
    end = beg + seconds2samples(newdur)
    env1dur = newdur - piano_release_duration
    siz = len(partials) // 2
    env1samples = beg + seconds2samples(env1dur)
    freqs = np.zeros(siz, dtype=np.double)
    phases = np.zeros(siz, dtype=np.double)
    alist = np.zeros(siz, dtype=np.double)
    locs = make_locsig(degree, distance, reverb_amount)
    ampfun1 = make_piano_ampfun(env1dur)
    ampenv1 = make_env(ampfun1, scaler=amplitude, duration=env1dur, base=10000.0)
    ampenv2 = make_env([0,1,100,0], scaler=amplitude * ampfun1[len(ampfun1)-1], duration=env1dur, base=1.0)
    
    for i in range(siz):
        freqs[i] =  hz2radians(partials[::2][i]*frequency)
        alist[i] =  partials[1::2][i]
        
    obank = make_oscil_bank(freqs, phases, alist, stable=True)
    
    for i in range(beg,env1samples):
        locsig(locs, i, env(ampenv1) * oscil_bank(obank))
    for i in range(env1samples, end):
        locsig(locs, i, env(ampenv2) * oscil_bank(obank))
    



# --------------- resflt ---------------- #

def resflt(start, dur, driver, ranfreq, noiamp, noifun, cosamp, cosfreq1, cosfreq0, cosnum, 
                ampcosfun, freqcosfun, frq1, r1, g1, frq2, r2, g2, frq3, r3, g3, 
                degree=0.0,distance=1.0,reverb_amount=0.005):
   
    with_noise = driver == 1
    beg = seconds2samples(start)
    end = seconds2samples(start + dur)
    f1 = make_two_pole(frq1, r1) # fix when these have kw args
    f2 = make_two_pole(frq2, r2)
    f3 = make_two_pole(frq3, r3)
    loc = make_locsig(degree, distance, reverb_amount)

    if with_noise:
        ampf = make_env(noifun, scaler=noiamp, duration=dur)
        rn = make_rand(frequency=ranfreq)
    else:
        frqf = make_env(freqcosfun, duration=dur, scaler=hz2radians(cosfreq1 - cosfreq0))             
        cn = make_ncos(cosfreq0, cosnum)
        ampf = make_env(ampcosfun, scaler=cosamp, duration=dur)
        
    f1.mus_xcoeffs[0] = g1
    f2.mus_xcoeffs[0] = g2
    f3.mus_xcoeffs[0] = g3
    
    if with_noise:
        for i in range(beg, end):   
            input1 = env(ampf) * rand(rn)
            locsig(loc, i, two_pole(f1, input1) + two_pole(f2, input1) + two_pole(f3, input1))
    else:
        for i in range(beg, end):   
            input1 = env(ampf) * ncos(cn, env(frqf))
            locsig(loc, i, two_pole(f1, input1) + two_pole(f2, input1) + two_pole(f3, input1))
         
# with Sound( play = True, statistics=True):
#     resflt(0,1.0,0,0,0,False,.1,200,230,10,[0,0,50,1,100,0],[0,0,100,1],500,.995,.1,1000,.995,.1,2000,.995,.1)  

# --------------- scratch ---------------- #

# Made changes based on callback functions and such in python


def scratch(start, file, src_ratio, turnaroundlist):
    f = make_file2frample(file)
    beg = seconds2samples(start)
    turntable = turnaroundlist
    turn_i = 1
    turns = len(turnaroundlist)
    cur_sample = seconds2samples(turntable[0])
    
    turn_sample = seconds2samples(turntable[1])
    def func(direction):
        nonlocal cur_sample
        inval = file2sample(f, cur_sample)
        cur_sample = cur_sample + direction
        return inval
   
    turning = 0
    last_val = 0.0
    last_val2 = 0.0
    rd = make_src(func, srate=src_ratio)
    forwards = src_ratio > 0.0
    
    if forwards and turn_sample < cur_sample:
        rd.mus_increment = -src_ratio
    
    i = beg
    
    while turn_i < turns:

        val = src(rd, 0.0)

        if turning == 0:
            if forwards and (cur_sample >= turn_sample):
                turning = 1
            else:
                if (not forwards) and (cur_sample <= turn_sample):
                    turning = -1
        else:                
            if ((last_val2 <= last_val) and (last_val >= val)) or ((last_val2 >= last_val) and (last_val <= val)):
                turn_i += 1
                if turn_i < turns:
                    turn_sample = seconds2samples(turntable[turn_i])
                    forwards = not forwards
                    rd.mus_increment = -rd.mus_increment
                turning = 0
        last_val2 = last_val
        last_val = val
        outa(i, val)
        i += 1
        
# with Sound( play = True, statistics=True):
#     scratch(0.0, 'yeah.aiff', 1., [0.0, .5, .25, 1.0, .5, 5.0])    

# TODO: --------------- pins ---------------- #

# def pins(beg, dur, file, amp, transposition=1.0, time_scaler=1.0, fftsize=256, highest_bin=128, max_peaks=16, attack=False):
#     fdr = np.zeros(fftsize-1)   
#     fdi = np.zeros(fftsize-1) 
#     start = seconds2samples(beg)
                   
                    

# --------------- zc ---------------- #

def zc(time, dur, freq, amp, length1, length2, feedback):
    beg = seconds2samples(time)
    end = seconds2samples(time + dur)
    s = make_pulse_train(freq, amplitude=amp)
    d0 = make_comb(feedback, size=length1, max_size=(1 + max(length1, length2)))
    zenv = make_env([0,0,1,1], scaler=(length2-length1), duration=dur)
    for i in range(beg, end):
        outa(i, comb(d0, pulse_train(s), env(zenv)))

# with Sound( play = True, statistics=True):
#     zc(0,3,100,.5,20,100,.95) 
#     zc(3., 3, 100, .5, 100, 20, .95)
#     
# --------------- zn ---------------- #

def zn(time, dur, freq, amp, length1, length2, feedforward):
    beg = seconds2samples(time)
    end = seconds2samples(time + dur)
    s = make_pulse_train(freq, amplitude=amp)
    d0 = make_notch(feedforward, size=length1, max_size=(1 + max(length1, length2)))
    zenv = make_env([0,0,1,1], scaler=(length2-length1), duration=dur)
    for i in range(beg, end):
        outa(i, notch(d0, pulse_train(s), env(zenv)))

# with Sound(play=True,statistics=True):
#     zn(0,1,100,.5,20,100,.995) 
#     zn(1.5, 1, 100, .5, 100, 20, .995)
    
# TODO: --------------- za ---------------- #

def za(time, dur, freq, amp, length1, length2, feedback, feedforward):
    beg = seconds2samples(time)
    end = seconds2samples(time + dur)
    s = make_pulse_train(freq, amplitude=amp)
    d0 = make_all_pass(feedback, feedforward, size=length1, max_size=(1 + max(length1, length2)))
    zenv = make_env([0,0,1,1], scaler=(length2-length1), duration=dur)
    for i in range(beg, end):
        outa(i, all_pass(d0, pulse_train(s), env(zenv)))

# with Sound(play=True,statistics=True):
#     za(0,1,100,.5, 20, 100, .95, .95)
#     za(1.5, 1, 100, .5, 100, 20, .95, .95)

# --------------- clm_expsrc ---------------- #

def clm_expsrc(beg, dur, input_file, exp_ratio, src_ratio, amp, rev=False, start_in_file=False):
    stf = math.floor((start_in_file or 0)*clm_srate(input_file))
    two_chans = clm_channels(input_file) == 2 and clm_channels(CLM.output) == 2
    revit = CLM.reverb and rev
    st = seconds2samples(beg)
    exA = make_granulate(make_readin(input_file, chan=0, start=stf), expansion=exp_ratio)
    if two_chans:
        exB = make_granulate(make_readin(input_file, chan=1, start=stf), expansion=exp_ratio)
    srcA = make_src(lambda d : granulate(exA), srate=src_ratio)
    if two_chans:
        srcB = make_src(lambda d : granulate(exB),srate=src_ratio)
    if revit:
        if two_chans:
            rev_amp = rev * .5
        else:
            rev_amp = rev 
    else:
        rev_amp = 0.0
        
    nd = seconds2samples(beg + dur)
    
    if revit:
        valA = 0.0
        valB = 0.0
        
        if two_chans:
            for i in range(st, nd):
                valA = amp * src(srcA)
                valB = amp * src(srcB)
                outa(i, valA)
                outb(i, valB)
                outa(i, rev_amp * (valA + valB), CLM.reverb)
        else:
            
            for i in range(st, nd):
                valA = amp * src(srcA)
                outa(i, valA)
                outb(i, rev_amp * valA, CLM.reverb)
    else:
        if two_chans:
            for i in range(st, nd):
                outa(i, amp*src(srcA))
                outb(i, amp*src(srcB))
        else:
            for i in range(st, nd):
                outa(i, amp * src(srcA))

# with Sound(play=True,statistics=True):
#     clm_expsrc(0, 2.5, 'oboe.snd', 2.0, 1.0, 1.0)

# --------------- exp_snd ---------------- #
# moved file arg from 1st arg

def exp_snd(beg, dur, file, amp, exp_amt=1.0, ramp=.4, seglen=.15, sr=1.0, hop=.05, ampenv=[0,0,.5,1,1,0]):
    def is_pair(x): #seems only useful in this instrument
        return isinstance(x, list)
    max_seg_len = max_envelope(seglin) if is_pair(seglen) else seglen
    initial_seg_len = seglin[1] if is_pair(seglen) else seglen
    rampdata = ramp if is_pair(ramp) else [0, ramp, 1, ramp]
    max_out_hop = max_envelope(hop) if is_pair(hop) else hop
    initial_out_hop = hop[1] if is_pair(hop) else hop
    min_exp_amt = min_envelope(exp_amt) if is_pair(exp_amt) else exp_amt
    initial_exp_amt = exp_amt[1] if is_pair(exp_amt) else exp_amt

    if (min_envelope(rampdata) <= 0.0) or (max_envelope(rampdata) >= .5):
        raise RuntimeError(f'ramp argument to exp_snd must always be between 0.0 and .5: {ramp}.')

    st = seconds2samples(beg)
    nd = seconds2samples(beg + dur)
    f0 = make_readin(file)

    expenv = make_env( exp_amt if is_pair(exp_amt) else [0, exp_amt, 1, exp_amt], duration=dur)
    lenenv = make_env( seglen if is_pair(seglen) else [0, seglen, 1, seglen], scaler=CLM.srate, duration=dur)
    scaler_amp = ((.6 * .15) / max_seg_len) if max_seg_len > .15 else .6
    srenv = make_env(sr if is_pair(sr) else [0, sr, 1, sr], duration=dur)
    rampenv = make_env(rampdata, duration=dur)
    initial_ramp_time = ramp[1] if is_pair(ramp) else ramp
    max_in_hop = max_out_hop / min_exp_amt
    max_len = seconds2samples(max(max_out_hop, max_in_hop) + max_seg_len)
    hopenv = make_env( hop if is_pair(hop) else [0, hop, 1, hop], duration=dur)
    ampe = make_env(ampenv, scaler= amp, duration=dur)
    exA = make_granulate(f0, expansion=initial_exp_amt, max_size=max_len, ramp=initial_ramp_time, hop=initial_out_hop, length=initial_seg_len, scaler=scaler_amp)
    vol = env(ampe)
    
    valA0 = vol * granulate(exA)
    valA1 = vol * granulate(exA)
    ex_samp = 0.0
    next_samp = 0.0
    
    for i in range(st, nd):
        sl = env(lenenv)
        vol = env(ampe)
        exA.mus_length = round(sl)
        exA.mus_ramp = math.floor(sl * env(rampenv))
        exA.mus_frequency = env(hopenv)
        exA.mus_increment = env(expenv)
        next_samp += env(srenv)
        
        if next_samp > (ex_samp + 1):
            samps = math.floor(next_samp - ex_samp)
            if samps > 2:
                for k in range(samps-2):
                    granulate(exA)
            valA0 = (vol * granulate(exA)) if samps >= 2 else valA1
            valA1 = vol * granulate(exA)
            ex_samp += samps
            
            outa(i, valA0 if next_samp == ex_samp else (valA0 + ((next_samp - ex_samp) * (valA1 - valA0)))) 

# with Sound(play=True,statistics=True):
#     exp_snd(0, 3, 'fyow.snd', 1, [0,1,1,3],   .4, .15, [0,2,1,.5], .05)
# 
# with Sound(play=True,statistics=True):
#     exp_snd(0, 3, 'oboe.snd', 1, [0,1,1,3],   .4, .15, [0,2,1,.5], .2)    

# TODO: --------------- grm ---------------- #

# TODO: --------------- expfil ---------------- #

# TODO: --------------- graphEq ---------------- #

# TODO: --------------- anoi ---------------- #

# TODO: --------------- bes_fm ---------------- #

# TODO: --------------- sbfm ---------------- #

# TODO: --------------- fm2 ---------------- #

# TODO: --------------- rmsg ---------------- #

# TODO: --------------- rms ---------------- #

# TODO: --------------- cnvrev ---------------- #



        
        
        
    
    
