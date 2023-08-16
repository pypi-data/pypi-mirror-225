import math
from pysndlib.clm import *

# does not include easy case or other optimizations

def fm_violin(beg, dur, frequency, amplitude, fm_index, 
            amp_env = [ 0, 0,  25, 1,  75, 1,  100, 0],
            periodic_vibrato_rate = 5.0,
            random_vibrato_rate = 16.0,
            periodic_vibrato_amplitude = 0.0025,
	        random_vibrato_amplitude = 0.005,
	        fm1_index=None,
	        fm2_index=None,
	        fm3_index=None,
	        fm1_rat = 1.0,
	        fm2_rat = 3.0,
	        fm3_rat = 4.0,
	        fm1_env = [0., 1., 25., .4, 75., .6, 100., 0.],
	        fm2_env = [0., 1., 25., .4, 75., .6, 100., 0.],
	        fm3_env = [0., 1., 25., .4, 75., .6, 100., 0.],
	        gliss_env = [0,0,100,0],
	        glissando_amount = 0.0,
	        noise_amount = 0.0,
	        noise_freq = 1000.,
	        ind_noise_freq = 10.,
	        ind_noise_amount = 0.0,
	        amp_noise_freq = 20.0,
	        amp_noise_amount = 0.0,
	        degree=45,
	        distance=1.0,
	        reverb_amount = .01):
    start = seconds2samples(beg)
    end = start + seconds2samples(dur)
    frq_scl = hz2radians(frequency)
    maxdev = frq_scl * fm_index
    index1 = fm1_index if fm1_index else min(math.pi, maxdev * (5.0 / math.log(frequency)))
    index2 = fm2_index if fm2_index else min(math.pi, maxdev * 3.0 * ((8.5 - math.log(frequency)) / (3.0 + (frequency / 1000.))))
    index3 = fm3_index if fm3_index else min(math.pi, maxdev * (4.0 / math.sqrt(frequency)))
    carrier = make_oscil(frequency)
    fmosc1 = make_oscil(frequency)
    fmosc2 = make_oscil(frequency * fm2_rat)
    fmosc3 = make_oscil(frequency * fm3_rat)
    ampf = make_env(amp_env, scaler = amplitude, duration = dur)
    indf1 = make_env(fm1_env, scaler = index1, duration = dur)
    indf2 = make_env(fm2_env, scaler = index2, duration = dur)
    indf3 = make_env(fm3_env, scaler = index3, duration = dur)
    frqf = make_env(gliss_env, (glissando_amount * frq_scl), duration=dur)
    pervib = make_triangle_wave(periodic_vibrato_rate,periodic_vibrato_amplitude * frq_scl)
    ranvib = make_rand_interp(random_vibrato_rate, random_vibrato_amplitude * frq_scl)
    fm_noi = make_rand(noise_freq, math.pi * noise_amount)
    ind_noi = make_rand_interp(ind_noise_freq, ind_noise_amount)
    amp_noi = make_rand_interp(amp_noise_freq, amp_noise_amount)
    loc = make_locsig(degree, distance, reverb_amount)
    
    for i in range(start, end):
        vib = triangle_wave(pervib) + rand_interp(ranvib) + env(frqf)
        fuzz = rand(fm_noi)
        inoi = 1.0 + rand_interp(ind_noi)
        anoi = env(ampf) * (1.0 + rand_interp(amp_noi))
        locsig(loc, i, anoi * oscil(carrier, 
                        vib + 
                        inoi * 
                        ((env(indf1) * oscil(fmosc1, (vib * fm1_rat) + fuzz)) +
                        (env(indf2) * oscil(fmosc2, ((vib * fm2_rat) + fuzz))) +
                        (env(indf3) * oscil(fmosc3, ((vib * fm3_rat) + fuzz))))))
