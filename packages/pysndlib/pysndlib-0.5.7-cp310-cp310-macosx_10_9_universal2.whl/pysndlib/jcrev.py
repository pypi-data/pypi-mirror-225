from pysndlib.clm import *


def jc_reverb(lowpass=False, volume=1., amp_env = None):
   
    allpass1 = make_all_pass(-.7, .7, 1051)
    allpass2 = make_all_pass(-.7, .7, 337)
    allpass3 = make_all_pass(-.7, .7, 113)
    comb1 = make_comb(.742, 4799)
    comb2 = make_comb(.733, 4999)
    comb3 = make_comb(.715, 5399)
    comb4 = make_comb(.697, 5801)
    chans = clm_channels(CLM.output)
    
    length = clm_length(CLM.reverb)
    filts = [make_delay(seconds2samples(.013))] if chans == 1 else [make_delay(seconds2samples(.013)),make_delay(seconds2samples(.011)) ]
    combs = make_comb_bank([comb1, comb2, comb3, comb4])
    allpasses = make_all_pass_bank([allpass1,allpass2,allpass3])
    
    if lowpass or amp_env:
        flt = make_fir_filter(3, [.25, .5, .25]) if lowpass else None
        envA = make_env(amp_env, scaler=volume, duration = length / CLM.srate)
        
        if lowpass:
            for i in range(length):
                out_bank(filts, i, (env(envA) * fir_filter(flt, comb_bank(combs, all_pass(allpasses, ina(i, CLM.reverb))))))
        else:
            for i in range(length):
                out_bank(filts, i, (env(envA) * comb_bank(combs, all_pass_bank(allpasses, ina(i, CLM.reverb)))))
    else:
        if chans == 1:
            
            gen = filts[0]
            for i in range(length):
                outa(i, delay(gen, volume * comb_bank(combs, all_pass_bank(allpasses, ina(i, CLM.reverb)))))
        else:    
            gen1 = filts[0]
            gen2 = filts[1]
            for i in range(length):
                val = volume * comb_bank(combs, all_pass_bank(allpasses, ina(i, CLM.reverb))) 
                outa(i, delay(gen1, val))
                outb(i, delay(gen2, val))
