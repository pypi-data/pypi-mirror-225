import math
import random
from pysndlib.clm import *
NEARLY_ZERO = 1.0e-10
TWO_PI = math.pi * 2


# --------------- nssb ---------------- #
make_nssb, is_nssb = make_generator('nssb', {'frequency' : 0.0, 'ratio' : 1.0, 'n' : 1, 'angle' : 0.0})

def nssb(gen, fm=0.0):
    cx = gen.angle
    mx = cx * gen.ratio
    den = math.sin(.5 * mx)
    gen.angle += fm + gen.frequency
    if math.fabs(den) <  NEARLY_ZERO:
        return -1.0
    else:
       return ((math.sin(cx) * math.sin(mx * ((gen.n + 1) / 2)) * math.sin((gen.n * mx) / 2)) - (math.cos(cx) * .5 * (den * math.sin(mx * (gen.n + .5))))) /  ((gen.n + 1) * den)

# with Sound(clipped=False, statistics=True, play=True):
#     gen = make_nssb(frequency=1000.0, ratio=.1, n=3)
#     for i in range(44100):
#         outa(i, nssb(gen))

# with Sound(clipped=False, statistics=True, play=True):
#     gen = make_nssb(frequency=1000.0, ratio=.1, n=3)
#     vib = make_oscil(5.0)
#     ampf = make_env([0,0,1,1,2,1,3,0], length=44100, scaler=1.0)
#     for i in range(44100):
#         outa(i, env(ampf)*nssb(gen, hz2radians(100.)*oscil(vib)))

# --------------- nxysin ---------------- #


def nodds(x, n):
    den = math.sin(x)
    num = math.sin(n * x)
    if den == 0.0:
        return 0.0
    else:
        return (num*num) / den
        
def find_nxysin_max(n, ratio):
    def ns(x, n):
        a2 = x / 2
        den = math.sin(a2)
        if den == 0.0:
            return 0.0
        else:
            return (math.sin(n*a2) * math.sin((1 + n) * a2)) / den
            
    def find_mid_max(n, lo, hi):
        mid = (lo + hi) / 2
        ylo = ns(lo, n)
        yhi = ns(hi, n)
        if math.fabs(ylo - yhi) < NEARLY_ZERO:
            return ns(mid,n)
        else:
            if ylo > yhi:
                return find_mid_max(n, lo, mid)   
            else:
                return find_mid_max(n, mid, hi)    
    
    def find_nodds_mid_max(n, lo, hi):
        mid = (lo + hi) / 2
        ylo = nodds(lo, n)
        yhi = nodds(hi, n)
        if math.fabs(ylo - yhi) < NEARLY_ZERO:
            return nodds(mid,n)
        else:
            if ylo > yhi:
                return find_nodds_mid_max(n, lo, mid)   
            else:
                return find_nodds_mid_max(n, mid, hi)    
            
    if ratio == 1:
        return find_mid_max(n, 0.0, math.pi / (n + .5))
    elif ratio == 2:
        return find_nodds_mid_max(n, 0.0, math.pi / ((2 * n) + .5))
    else:
        return n      
        
    

def nxysin_wrapper(g):
    convert_frequency(g)
    g.norm = 1.0 / find_nxysin_max(g.n, g.ratio)
    return g

make_nxysin, is_nxysin = make_generator('nxysin', {'frequency' : 0.0, 'ratio' : 1.0, 'n' : 1, 'angle' : 0.0, 'norm' : 1.0}, wrapper = nxysin_wrapper,
                        docstring="""Creates an nxysin generator.""")
                        
def nxysin(gen, fm=0.0):
    """returns n sines from frequency spaced by frequency * ratio."""
    x = gen.angle
    y = x * gen.ratio
    den = math.sin(y * 0.5)
    gen.angle += fm + gen.frequency
    if math.fabs(den) < NEARLY_ZERO:
        return 0.0
    else:
        return (math.sin(x + (0.5 * (gen.n - 1) * y)) * math.sin(0.5 * gen.n * y) * gen.norm) / den

# with Sound(clipped=False, statistics=True, play=True):
#     gen = make_nxysin(frequency=300, ratio =.3333, n=3)
#     for i in range(44100):
#         outa(i, nxysin(gen))

# --------------- nxycos ---------------- #

make_nxycos, is_nxycos = make_generator('nxycos', {'frequency' : 0.0, 'ratio' : 1.0, 'n' : 1, 'angle' : 0.0}, 
                wrapper=convert_frequency, docstring="""creates an nxycos generator. """)

def nxycos(gen, fm=0.0):
    """Returns n cosines from frequency spaced by frequency * ratio."""
    x = gen.angle
    y = x * gen.ratio
    den = math.sin(y * .5)
    gen.angle += (gen.frequency + fm)
    if math.fabs(den) < NEARLY_ZERO:
        return 1.0
    else:
        return (math.cos(x + (0.5 * (gen.n - 1) * y)) * math.sin(.5 * gen.n * y)) / (gen.n * den)
        

# with Sound(clipped=False, statistics=True, play=True):
#     gen = make_nxycos(frequency=300, ratio=1/3, n=3)
#     for i in range(44100):
#         outa(i, .5 * nxycos(gen))        
        
# --------------- nxy1cos ---------------- #

make_nxy1cos, is_nxy1cos = make_generator('nxy1cos', {'frequency' : 0.0, 'ratio' : 1.0, 'n' : 1, 'angle' : 0.0}, 
                            wrapper=convert_frequency)

def nxy1cos(gen, fm=0.0):
    x = gen.angle
    y = x * gen.ratio
    den = math.cos(y * .5)
    gen.angle += gen.frequency + fm
    if math.fabs(den) < NEARLY_ZERO:
        return -1.0
    else:
        return max(-1., min(1.0, (math.sin(gen.n * y) * math.sin(x + ((gen.n - .5) * y))) / (2 * gen.n * den)))

# with Sound(clipped=False, statistics=True, play=True):
#     gen = make_nxy1cos(frequency=300, ratio=1/3, n=3)
#     for i in range(44100):
#         outa(i, nxy1cos(gen))
#
# with Sound(clipped=False, statistics=True, play=True):
#     gen = make_nxy1cos(frequency=300, ratio=1/3, n=3)
#     gen1 = make_nxycos(frequency=300, ratio=1/3, n=6)
#     for i in range(44100):
#         outa(i, (nxycos(gen1) + nxy1cos(gen)) * .4)
# 
# with Sound(clipped=False, statistics=True, play=True):
#     gen = make_nxy1cos(frequency=radians2hz(.01 * math.pi), ratio=1., n=3)
#     for i in range(44100):
#         outa(i, nxy1cos(gen))
        
# --------------- nxy1sin ---------------- #

make_nxy1sin, is_nxy1sin = make_generator('nxy1sin', {'frequency' : 0.0, 'ratio' : 1.0, 'n' : 1, 'angle' : 0.0},
                            wrapper=convert_frequency)

def nxy1sin(gen, fm=0.0):
    x = gen.angle
    y = x * gen.ratio
    den = math.cos(y * .5)
    gen.angle += gen.frequency + fm
    return (math.sin(x + (.5 * (gen.n - 1) * (y + math.pi))) * math.sin(.5 * gen.n * (y + math.pi))) / (gen.n * den)
    
# with Sound(clipped=False, statistics=True, play=True):
#     gen = make_nxy1sin(frequency=300, ratio=1/3, n=3)
#     for i in range(44100):
#         outa(i, nxy1sin(gen))  


# --------------- noddsin ---------------- #

def find_noddsin_max(n):    
    def find_mid_max(n=n, lo=0.0, hi= math.pi / ((2 * n) + 0.5)):
        mid = (lo + hi) / 2
        ylo = nodds(lo, n)
        yhi = nodds(hi, n)
        if math.fabs(ylo - yhi) < 1.0e-9:
            return nodds(mid,n)
        else:
            if ylo > yhi:
                return find_mid_max(n, lo, mid)   
            else:
                return find_mid_max(n, mid, hi)
    return find_mid_max(n)

NODDSIN_MAXES = np.zeros(100, dtype=np.double)

def noddsin_wrapper(g):
    g.n = max(g.n, 1)
    convert_frequency(g)
    if not (g.n < 100 and NODDSIN_MAXES[g.n] > 0.0) :
        NODDSIN_MAXES[g.n] = find_noddsin_max(g.n)
    else:
        g.norm = 1.0 / NODDSIN_MAXES[g.n]
    return g
        
make_noddsin, is_noddsin = make_generator('noddsin', {'frequency' : 0.0, 'n' : 1, 'angle' : 0.0, 'norm' : 1.0}, wrapper=noddsin_wrapper, docstring="""Creates an noddsin generator.""")

def noddsin(gen, fm=0.0):
    """Returns n odd-numbered sines spaced by frequency."""
    snx = math.sin(gen.n * gen.angle)
    den = math.sin(gen.angle)
    gen.angle += fm + gen.frequency
    if math.fabs(den) < NEARLY_ZERO:
        return 0.0
    else:
        return (gen.norm * snx * snx) / den

# clarinety
# with Sound(clipped=False, statistics=True, play=True):
#     gen = make_noddsin(frequency=300, n=3)
#     ampf = make_env([0,0,1,1,2,1,3,0], length=40000, scaler=.5)
#     for i in range(40000):
#         outa(i, env(ampf) * noddsin(gen))
# --------------- noddcos ---------------- #

make_noddcos, is_noddcos = make_generator('noddcos', {'frequency' : 0.0, 'n' : 1, 'angle' : 0.0}, wrapper = convert_frequency)

def noddcos(gen, fm=0.0):
    cx = gen.angle
    den = 2 * gen.n * math.sin(gen.angle)
    gen.angle += fm + gen.frequency
    
    if math.fabs(den) < NEARLY_ZERO:
        fang = cx % (2 * math.pi)
        if (fang < .001) or (math.fabs(fang - (2 * math.pi)) < .001):
            return 1.0
        else: 
            return -1.0
    else:
        return math.sin(2 * gen.n * cx) / den
        
# with Sound(clipped=False, statistics=True, play=True):
#     gen = make_noddcos(frequency=100, n=10)
#     for i in range(44100):
#         outa(i, noddcos(gen)*.5)
        
# --------------- noddssb ---------------- #

make_noddssb, is_noddssb = make_generator('noddssb', {'frequency' : 0.0, 'ratio' : 1.0, 'n' : 1, 'angle' : 0.0}, 
                wrapper = convert_frequency, docstring="""creates an noddssb generator.""")


def noddssb(gen, fm=0.0):
    """Returns n sinusoids from frequency spaced by 2 * ratio * frequency."""
    cx = gen.angle
    mx = cx * gen.ratio
    x = cx - mx
    sinnx = math.sin(gen.n * mx)
    den = gen.n * math.sin(mx)
    gen.angle += fm + gen.frequency
    
    if math.fabs(den) < NEARLY_ZERO:
        if (mx % (2 * math.pi)) < .1:
            return -1
        else:
            return 1
    else:
        return (math.sin(x) * ((sinnx*sinnx) / den)) - ((math.cos(x) * (math.sin(2 * gen.n * mx) / (2 * den))))

# with Sound(clipped=False, statistics=True, play=True):
#     gen = make_noddssb(frequency=1000.0, ratio=0.1, n=5)
#     for i in range(44100):
#         outa(i, noddssb(gen)*.5)
#
# with Sound(clipped=False, statistics=True, play=True):
#     gen = make_noddssb(frequency=1000.0, ratio=0.1, n=5)
#     vib = make_oscil(5.0)
#     for i in range(44100):
#         outa(i, noddssb(gen, hz2radians(100.0)*oscil(vib))*.5)
# 


# --------------- ncos2 ---------------- #

make_ncos2, is_ncos2 = make_generator('ncos2', {'frequency' : 0.0, 'n' : 1, 'angle' : 0.0}, 
                    docstring="""creates an ncos2 (Fejer kernel) generator""", wrapper = convert_frequency)

def ncos2(gen, fm=0.0):
    """Returns n sinusoids spaced by frequency scaled by (n-k)/(n+1)"""
    x = gen.angle
    den = math.sin(.5 * x)
    gen.angle += fm + gen.frequency
    if math.fabs(den) < NEARLY_ZERO:
        return 1.0
    else:
        val = math.sin(0.5 * (gen.n + 1) * x) / ((gen.n + 1) * den)
        return val * val
        
# with Sound(clipped=False, statistics=True, play=True):
#     gen = make_ncos2(frequency=100.0, n=10)
#     for i in range(44100):
#         outa(i, 0.5 * ncos2(gen))
        
# --------------- ncos4 ---------------- #

make_ncos4, is_ncos4 = make_generator('ncos4', {'frequency' : 0.0, 'n' : 1, 'angle' : 0.0}, 
                    docstring="""creates an ncos4 (Jackson kernel) generator.""", wrapper = convert_frequency)

def ncos4(gen, fm=0.0):
    val = ncos2(gen, fm)
    return val * val
    
# with Sound(clipped=False, statistics=True, play=True):
#     gen = make_ncos4(frequency=100.0, n=10)
#     for i in range(44100):
#         outa(i, 0.5 * ncos4(gen))
  
# --------------- npcos ---------------- #      

make_npcos, is_npcos = make_generator('npcos', {'frequency' : 0.0, 'n' : 1, 'angle' : 0.0},
                        wrapper=convert_frequency, docstring="""creates an npcos (Poussin kernel) generator.""")

def npcos(gen, fm=0.0):
    """returns n*2+1 sinusoids spaced by frequency with amplitudes in a sort of tent shape."""
    result = 0.0
    result1 = 0.0
    result2 = 0.0
    den = math.sin(.5 * gen.angle)
    if math.fabs(den) < NEARLY_ZERO:
        result = 1.0
    else:
        n1 = gen.n + 1
        val = math.sin(.5 * n1 * gen.angle) / (n1 * den)
        result1 = val * val
        p2n2 = (2 * gen.n) + 2
        val = math.sin(.5 * p2n2 * gen.angle) / (p2n2 * den)
        result2 = val * val
        result = (2 * result2) - result1
    gen.angle += fm + gen.frequency
    return result
        
# with Sound(clipped=False, statistics=True, play=True):
#     gen = make_npcos(frequency=100.0, n=10)
#     for i in range(44100):
#         outa(i, 0.5 * npcos(gen))    


# --------------- ncos5 ---------------- #  

make_ncos5, is_ncos5 = make_generator('ncos5', {'frequency' : 0.0, 'n' : 1, 'angle' : 0.0},
                        wrapper=convert_frequency, docstring="""creates an ncos5 generator.""")


def ncos5(gen, fm=0.0):
    """returns n cosines spaced by frequency. All are equal amplitude except the first and last at half amp."""
    
    x = gen.angle
    den = math.tan(.5 * x)
    gen.angle += fm + gen.frequency
    if math.fabs(den) < NEARLY_ZERO:
        return 1.0
    else:
        return ((math.sin(gen.n*x) / (2 * den)) - .5) / (gen.n - .5)
        
# with Sound(clipped=False, statistics=True, play=True):
#     gen = make_ncos5(frequency=100.0, n=10)
#     for i in range(44100):
#         outa(i, 0.5 * ncos5(gen))  
        

# --------------- nsin5 ---------------- #  
def find_nsin5_max(n):
    def ns(x, n):
            den = math.tan(.5 * x)
            if math.fabs(den) < NEARLY_ZERO:
                return 0.0
            else:
                return (1.0 - math.cos(n * x)) / den
                
    def find_mid_max(n, lo, hi):
        mid = (lo + hi) / 2
        ylo = ns(lo, n)
        yhi = ns(hi, n)
        if math.fabs(ylo - yhi) < 1e-9:
            return ns(mid,n)
        else:
            if ylo > yhi:
                return find_mid_max(n, lo, mid)   
            else:
                return find_mid_max(n, mid, hi)
                
    return find_mid_max(n, 0.0, math.pi / (n + .5))
    
def nsin5_wrapper(g):
    convert_frequency(g)
    g.n = max(2, g.n)
    g.norm = find_nsin5_max(g.n)
    return g

make_nsin5, is_nsin5 = make_generator('nsin5', {'frequency' : 0.0, 'n' : 2, 'angle' : 0.0, 'norm' : 1.0},
                        wrapper=nsin5_wrapper, docstring="""creates an nsin5 generator.""")


def nsin5(gen, fm=0.0):
    x = gen.angle
    den = math.tan(.5 * x)
    gen.angle += fm + gen.frequency
    if math.fabs(den) < NEARLY_ZERO:
        return 0.0
    else:
        return (1.0 - math.cos(gen.n*x)) / (den * gen.norm)

# with Sound(clipped=False, statistics=True, play=True):
#     gen = make_nsin5(frequency=100.0, n=10)
#     for i in range(44100):
#         outa(i, nsin5(gen))
    

# --------------- nrsin ---------------- #  

make_nrsin = make_nrxysin
nrsin = nrxysin
is_nrsin = is_nrxysin


# --------------- nrcos ---------------- #  

def nrcos_wrapper(g):
    convert_frequency(g)
    g.n = (1 + g.n)
    g.r = clamp(g.r, -.999999, .999999)
    g.rr = g.r * g.r
    g.r1 = 1.0 + g.rr
    g.e1 = math.pow(g.r, g.n)
    g.e2 = math.pow(g.r, g.n + 1)
    g.norm = ((math.pow(math.fabs(g.r), g.n) - 1.0) / (math.fabs(g.r) - 1.)) - 1.0
    g.trouble = (g.n == 1) or (math.fabs(g.r) < NEARLY_ZERO)
    return g
    
 
def nrcos_set_mus_order(g, val):
    g.n = 1 + val
    g.e1 = math.pow(g.r, g.n)
    g.e2 = math.pow(g.r, (g.n + 1))
    g.norm = ((math.pow(math.fabs(g.r), g.n) - 1.0) / (math.fabs(g.r) - 1.)) - 1.0
    g.trouble = (g.n == 1) or (math.abs(g.r) < NEARLY_ZERO)
    return val
    
def nrcos_set_mus_frequency(g, val):
    g.frequency = hz2radians(val)
    
def nrcos_set_scaler(g, val):
    g.r = min(.999999, max(-.999999, val))
    g.absr = math.fabs(g.r)
    g.rr = g.r * g.r
    g.r1 = 1.0 + g.rr
    g.norm = ((math.pow(g.absr, g.n) - 1) / (g.absr - 1)) - 1.0
    g.trouble = ((g.n == 1) or (g.absr < 1.0e-12))
    return val
    
    
make_nrcos, is_nrcos = make_generator('nrcos', {'frequency' : 0.0, 'n' : 1, 'r' : .5, 'angle' : 0.0, 'rr' : 0., 'r1' : 0., 'e1' : 0., 'e2' : 0.0, 'norm' : 0.0, 'touble' : False},
                        wrapper=nrcos_wrapper, 
                        methods = {'mus_order' : [lambda g : g.n - 1, nrcos_set_mus_order], 'mus_frequency' : [lambda g: radians2hz(g.frequency), nrcos_set_mus_frequency],'mus_scaler' : [lambda g : g.r, nrcos_set_scaler]})  
    

def nrcos(gen, fm=0.0):
    x = gen.angle
    rcos = gen.r * math.cos(gen.angle)
    gen.angle += fm + gen.frequency
    if gen.trouble:
        return 0.0
    else: 
        return ((rcos + (gen.e2 * math.cos((gen.n - 1) * x))) - (gen.e1 * math.cos(gen.n * x)) - gen.rr) / (gen.norm * (gen.r1 + (-2.0 * rcos)))
        

# with Sound(clipped=False, statistics=True, play=True):
#     gen = make_nrcos(frequency=400.0, n=5, r=.5)
#     for i in range(44100):
#         outa(i, .5 * nrcos(gen))
#
# with Sound(clipped=False, statistics=True, play=True):
#     gen = make_nrcos(frequency=1200.0, n=3, r=.99)
#     mod = make_oscil(400)
#     idx = .01
#     for i in range(44100):
#         outa(i, nrcos(gen, (idx * oscil(mod))))
#
# with Sound(clipped=False, statistics=True, play=True):
#     gen = make_nrcos(frequency=2000., n=3, r=.5)
#     mod = make_oscil(400)
#     idx = make_env([0,0,1,.1], length=44100)
#     for i in range(44100):
#         outa(i, .5 * nrcos(gen, (env(idx) * oscil(mod))))
#
#
# def lutish(beg, dur, freq, amp):
#     res1 = max(1, round(1000.0 / max(1.0, min(1000., freq))))
#     maxind = max(.01, min(.3, ((math.log(freq) - 3.5) / 8.0)))
#     gen = make_nrcos(frequency=freq*res1,n=max(1, (res1 - 2)))
#     mod = make_oscil(freq)
#     start = seconds2samples(beg)
#     stop = seconds2samples(beg + dur)
#     indx = make_env([0,maxind, 1, maxind*.25, max(dur, 2.0), 0.0], duration=dur)
#     amplitude = make_env([0,0,.01,1,.2,1,.5,.5,1,.25, max(dur, 2.0), 0.0], duration=dur, scaler =amp)
#     for i in range(start, stop):
#         ind = env(indx)
#         gen.r = ind
#         outa(i, env(amplitude) * nrcos(gen, (ind * oscil(mod))))
# 
# 
# with Sound(clipped=False, statistics=True, play=True):
#     lutish(0,1,440,.1)
# 
# with Sound(clipped=False, statistics=True, play=True):
#     for i in range(10):
#         lutish(i*.1, 2, (100 * (i+1)), .05)


# --------------- nrssb ---------------- #

def nrssb_wrapper(g):
    convert_frequency(g)
    g.r = clamp(g.r, -.999999, .999999)
    g.r = max(g.r, 0.0)
    g.rn = -math.pow(g.r, g.n)
    g.rn1 = math.pow(g.r, (g.n + 1))
    g.norm = (g.rn - 1) / (g.r - 1)
    return g

make_nrssb, is_nrssb = make_generator('nrssb', {'frequency' : 0.0, 'ratio' : 1.0, 'n' : 1, 'r' : .5, 'angle' : 0.0, 'interp' : 0.0, 'rn' : 0.0, 'rn1' : 0.0, 'norm' : 0.0},
                        wrapper=nrssb_wrapper, docstring=""" creates an nrssb generator""")


def nrssb(gen, fm=0.0):
    """returns n sinusoids from frequency spaced by frequency * ratio with amplitudes scaled by r^k."""
    cx = gen.angle
    mx = cx * gen.ratio
    nmx = gen.n * mx
    n1mx = (gen.n - 1) * mx
    den = gen.norm * (1.0 + (-2.0 * gen.r * math.cos(mx)) + (gen.r * gen.r))
    gen.angle += fm + gen.frequency
    return (((math.sin(cx) * ((gen.r * math.sin(mx)) + (gen.rn * math.sin(nmx)) + (gen.rn1 * math.sin(n1mx)))) -
            (math.cos(cx) * (1.0 + (-1. * gen.r * math.cos(mx)) + (gen.rn * math.cos(nmx)) + (gen.rn1 * math.cos(n1mx)))))) / den
            
def nrssb_interp(gen, fm=0.0, interp=0.0):
    """returns n sinusoids from frequency spaced by frequency * ratio with amplitudes scaled by r^k."""
    gen.interp = interp
    cx = gen.angle
    mx = cx * gen.ratio
    nmx = gen.n * mx
    n1mx = (gen.n - 1) * mx
    den = gen.norm * (1.0 + (-2.0 * gen.r * math.cos(mx)) + (gen.r * gen.r))
    gen.angle += fm + gen.frequency
    return (((gen.interp * math.sin(cx) * ((gen.r * math.sin(mx)) + (gen.rn * math.sin(nmx)) + (gen.rn1 * math.sin(n1mx)))) -
            (math.cos(cx) * (1.0 + (-1. * gen.r * math.cos(mx)) + (gen.rn * math.cos(nmx)) + (gen.rn1 * math.cos(n1mx)))))) / den
            
            
# 
# with Sound(clipped=False, statistics=True, play=True):
#     gen = make_nrssb(frequency=1000, ratio=.1, n=5, r=.5)
#     for i in range(44100):
#         outa(i, nrssb(gen))
# 
# with Sound(clipped=False, statistics=True, play=True):
#     gen = make_nrssb(frequency=1000, ratio=.1, n=5, r=.5)
#     vib = make_oscil(5)
#     for i in range(44100):
#         outa(i, nrssb(gen, hz2radians(100) * oscil(vib)))
# !!
# 
# with Sound(clipped=False, statistics=True, play=True):
#     gen = make_nrssb(frequency=100, ratio=.1, n=10, r=.9)
#     gen1 = make_nrssb(frequency=101, ratio=.1, n=10, r=.9)
#     for i in range(44100*10):
#         outa(i, nrssb_interp(gen, 0.0, 1.))
#         outa(i, nrssb_interp(gen1, 0.0, 1.))

# def oboish(beg, dur, freq, amp, aenv):
#     res1 = max(1, round(1400.0 / max(1.0, min(1400.0, freq))))
#     mod1 = make_oscil(5.)
#     res2 = max(1, round(2400.0 / max(1.0, min(2400.0, freq))))
#     gen3 = make_oscil(freq)
#     start = seconds2samples(beg)
#     amplitude = make_env(aenv, duration=dur, base=4, scaler=amp)
#     skenv = make_env([0.0,0.0,1,1,2.0,clm_random(), 3.0, 0.0, max(4.0, dur*20.0), 0.0], duration=dur, scaler=hz2radians(clm_random(freq*.5)))
#     relamp = .85 * clm_random(.1)
#     avib = make_rand_interp(5, .2)
#     hfreq = hz2radians(freq)
#     h3freq = hz2radians(.003 * freq)
#     scl = .05 / amp
#     gen = make_nrssb(frequency=freq*res1, ratio=1/res1, n=res1, r=.75)
#     gen2 = make_oscil(freq*res2)
#     stop = start + seconds2samples(dur)
#     for i in range(start, stop):
#         vol = (.8 + rand_interp(avib)) * env(amplitude)
#         vola = scl * vol
#         vib = (h3freq * oscil(mod1)) + env(skenv)
#         result = vol * (((relamp - vola) * nrssb_interp(gen, (res1*vib), -1.0)) +
#                 (((1 + vola) - relamp)  * oscil(gen2, ((vib*res2)+(hfreq*oscil(gen3, vib))))))
#         outa(i, result)
#         if CLM.reverb :
#             outa(i, (.01*result), CLM.reverb)
#         
# with Sound(clipped=False, statistics=True, play=True):
#     oboish(0,1,300, .1, [0,0,1,1,2,0])
# 
# with Sound(clipped=False, statistics=True, play=True, reverb=jc_reverb):
#     for i in range(10):
#         oboish((i*.3),.4,(100 + (50*i)), .05, [0,0,1,1,2,1,3,0])
# # 
# with Sound(clipped=False, statistics=True, play=True, reverb=jc_reverb):
#     rats = [1,256/243,9/8,32/27,81/64,4/3,1024/729,3/2,128/81,27/16,16/9,243/128,2]
#     mode = [0,0,2,4,11,11,5,6,7,9,2,12,0]
#     for i in range(20):
#         pt1 = clm_random(1.0)
#         pt2 = pt1 + clm_random(1.0)
#         pt3 = pt2 + clm_random(1.0)
#         oboish(clm_random(32) / 8, (3 + clm_random(8) / 8), 16.351 * 16 * rats[mode[clm_random(12)]],
#             .25 + clm_random(.25), [0,0,pt1, 1, pt2, .5, pt3, 0])

# --------------- nkssb ---------------- #  




# TODO: --------------- nsincos ---------------- #  


# TODO: --------------- n1cos ---------------- #  


# TODO: --------------- npos1cos ---------------- #  


# TODO: --------------- npos3cos ---------------- #  

# --------------- rcos ---------------- #

def rcos_wrapper(g):
    g.osc = make_oscil(g.frequency, .5 * math.pi)
    g.r = clamp(g.r, -.999999, .999999)
    g.rr = g.r * g.r
    g.rrp1 = 1.0 + g.rr
    g.rrm1 = 1.0 - g.rr
    g.r2 = 2. * g.r
    absr = math.fabs(g.r)
    g.norm = 0.0 if absr < NEARLY_ZERO else (1.0 - absr) /  ( 2.0 * absr)
    return g
    
def rcos_set_mus_frequency(g,vl):
    g.osc.frequency = val
    
def rcos_set_mus_scaler(g,val):
    g.r = clamp(val, -.999999, .999999)
    g.rr = g.r*g.r
    g.rrp1 = 1.0 + g.rr
    g.rrm1 = 1.0 - g.rr
    g.r2 = 2.0 * g.r
    absr = math.fabs(g.r)
    g.norm = 0.0 if absr < 1.0e-10 else (1.0 - absr) /  ( 2.0 * absr)
    return val
    
make_rcos, is_rcos = make_generator('rcos', {'frequency' : 0.0, 'r' : .5, 'fm' : 0.0, 'osc' : False, 'rr' : 0.0, 'norm' : 0.0, 'rrp1' : 0.0, 'rrm1' : 0.0, 'r1' : 0},
                        wrapper = rcos_wrapper,
                        methods = {'mus_frequency' : [lambda g : g.osc.mus_frequency, rcos_set_mus_frequency], 
                                    'mus_scale' : [lambda g: g.r, rcos_set_mus_scaler]})
    
def rcos(gen, fm=0.):
    return ((gen.rrm1 / (gen.rrp1 - (gen.r2 * oscil(gen.osc, fm)))) - 1.0) * gen.norm


# TODO: --------------- rssb ---------------- #  

# TODO: --------------- rxysin ---------------- #  


# TODO: --------------- rxycos ---------------- #  


# TODO: --------------- safe-rxycos ---------------- #  

# TODO: --------------- ercos ---------------- #  

# TODO: --------------- erssb ---------------- #  

# TODO: --------------- r2sin ---------------- #  

# TODO: --------------- r2cos ---------------- #  

# TODO: --------------- r2ssb ---------------- #  

# TODO: --------------- eoddcos ---------------- #  

# TODO: --------------- rkcos ---------------- #  

# TODO: --------------- rksin ---------------- #  

# TODO: --------------- rkssb ---------------- #  

# TODO: --------------- rk!cos ---------------- #  

# TODO: --------------- rk!ssb ---------------- #  

# TODO: --------------- rxyk!sin ---------------- # 

# TODO: --------------- rxyk!cos ---------------- # 

# TODO: --------------- r2k!cos ---------------- # 

# TODO: --------------- k2sin ---------------- # 

# TODO: --------------- k2cos ---------------- # 

# TODO: --------------- k2ssb ---------------- # 

# TODO: --------------- dblsum ---------------- # 



# --------------- rkoddssb ---------------- #

def rkoddssb_wrapper(g):
    g = convert_frequency(g)
    g.r = clamp(g.r, -.999999, .999999)
    g.rr1 = 1.0 + (g.r * g.r)
    g.norm = 1.0 / (math.log(1.0 + g.r) - math.log(1.0 - g.r))
    return g
    
def rkoddssb_setter(g, val):
    g.r = clamp(val, -.999999, .9999999)
    g.rr1 = 1.0 + (g.r * g.r)
    g.norm = 1.0 / (math.log(1.0 + g.r) - math.log(1.0 - g.r))

make_rkoddssb, is_rkoddssb = make_generator('rkoddssb', {'frequency' : 0.0, 'ratio' : 1.0, 'r' : .5, 'angle' : 0.0, 'fm' : 0.0, 'rr1' : 0.0, 'norm' : 0.0},
                            wrapper=rkoddssb_wrapper, 
                            methods={'mus_scaler' : [lambda gen : gen.r, rkoddssb_setter]})


def rkoddssb(gen, fm=0.):
    cx = gen.angle
    mx = cx * gen.ratio
    cxx = cx - mx
    cmx = 2.0 * gen.r * math.cos(mx)
    gen.angle += fm + gen.frequency
    return (((math.cos(cxx) * .5 * math.log((gen.rr1+cmx) / (gen.rr1-cmx))) - (math.sin(cxx) * (math.atan2((2.0 * gen.r * math.sin(mx)), (1.0 - (gen.r*gen.r)))))) * gen.norm)


# TODO: --------------- krksin ---------------- # 


# TODO: --------------- abcos ---------------- # 

# TODO: --------------- absin ---------------- # 

# TODO: --------------- r2k2cos ---------------- # 

# TODO: --------------- blsaw ---------------- # 

# TODO: --------------- asyfm ---------------- # 

# TODO: --------------- bess ---------------- # 

# TODO: --------------- jjcos ---------------- # 

# TODO: --------------- j0evencos ---------------- # 

# TODO: --------------- j2cos ---------------- # 

# TODO: --------------- jpcos ---------------- # 

# TODO: --------------- jncos ---------------- # 

# TODO: --------------- j0j1cos  ---------------- # 

# TODO: --------------- jycos  ---------------- # 

# TODO: --------------- jcos  ---------------- # 

# TODO: --------------- blackman  ---------------- # 

# --------------- fmssb ---------------- #

make_fmssb, is_fmssb = make_generator('fmssb', {'frequency' : 0.0, 'ratio' : 1.0, 'index' : 1.0, 'angle' : 0.0}, wrapper=convert_frequency)

def fmssb(gen, fm=0.):
    cx = gen.angle
    mx = cx * gen.ratio
    gen.angle += fm + gen.frequency
    
    return (math.cos(cx) * (math.sin(gen.index * math.cos(mx)))) - (math.sin(cx) * (math.sin(gen.index * math.sin(mx))))

# with Sound(play=True,statistics=True):
#     gen = make_fmssb(frequency=1000., ratio=1, index=8.0)
#     for i in range(0, 10000):
#         outa(i, .3 * fmssb(gen))
        
# with Sound(play=True,statistics=True):
#     gen = make_fmssb(frequency=1000., ratio=.1, index=8.0)
#     ampf = make_env([0,0,1,1,100,0], base=32, scaler=.3, length=30000)
#     indf = make_env([0,1,1,0], length=30000, scaler=8)
#     for i in range(0, 30000):
#         gen.index = env(indf)
#         outa(i, env(ampf) * fmssb(gen))


# with Sound(play=True,statistics=True):
#     gen = make_fmssb(frequency=1000., ratio=.05, index=1.0)
#     ampf = make_env([0,0,1,1,100,0], base=32, scaler=.3, length=30000)
#     indf = make_env([0,1,1,0], length=30000, scaler=10)
#     for i in range(0, 30000):
#         gen.index = env(indf)
#         outa(i, env(ampf) * fmssb(gen))

# with Sound(play=True,statistics=True):
#     gen = make_fmssb(frequency=100., ratio=5.4, index=1.0)
#     ampf = make_env([0,0,1,1,100,0], base=32, scaler=.3, length=30000)
#     indf = make_env([0,1,1,0], length=30000, scaler=10)
#     for i in range(0, 30000):
#         gen.index = env(indf)
#         outa(i, env(ampf) * fmssb(gen))

# with Sound(play=True,statistics=True):
#     gen = make_fmssb(frequency=100., ratio=5.4, index=1.0)
#     ampf = make_env([0,0,1,1,100,0], base=32, scaler=.3, length=30000)
#     #ampf = make_env([0,0,1,1,3,1,100,0], base=32, scaler=.3, length=30000)
#     #ampf = make_env([0,0,1,.75,2,1,3,.95,4,.5,10,0], base=32, scaler=.3, length=30000) #bowed
#     #ampf = make_env([0,0,1,.75,2,1,3,.1,4,.7,5,1,6,.8,100,0], base=32, scaler=.3, length=30000) #bowed
# 
#     indf = make_env([0,1,1,0], length=30000, scaler=10)
#     for i in range(0, 30000):
#         gen.index = env(indf)
#         outa(i, env(ampf) * fmssb(gen))

# nice
# with Sound(play=True,statistics=True):
#     gen = make_fmssb(frequency=10., ratio=2.0, index=1.0)
#     ampf = make_env([0,0,1,1,3,1,100,0], base=32, scaler=.3, length=30000)
#     indf = make_env([0,1,1,0], length=30000, scaler=10)
#     for i in range(0, 30000):
#         gen.index = env(indf)
#         outa(i, env(ampf) * fmssb(gen))

# with Sound(play=True,statistics=True):
#     gen1 = make_fmssb(frequency=500, ratio=1)
#     gen2 = make_fmssb(frequency=1000, ratio=.2)
#     ampf = make_env([0,0,1,1,100,0], base=32, scaler=.3, length=30000)
#     indf = make_env([0,1,1,1,10,0], length=30000, scaler=10)
#     for i in range(0, 30000):
#         ind = env(indf)
#         gen1.index = ind
#         gen2.index = ind
#         outa(i, env(ampf) * (fmssb(gen1) + fmssb(gen2)))


# with Sound(play=True,statistics=True):
#     for i in np.arange(0.0, 2.0, .5):        
#         machine1(i, .3, 100, 540, 0.5, 3.0, 0.0)
#         machine1(i,.1,100,1200,.5,10.0,200.0)
#         machine1(i,.3,100,50,.75,10.0,0.0)
#         machine1(i + .1, .1,100,1200,.5,20.0,1200.0)
#         machine1(i + .3, .1,100,1200,.5,20.0,1200.0)
#         machine1(i + .3, .1,100,200,.5,10.0,200.0)
#         machine1(i + .36, .1,100,200,.5,10.0,200.0)
#         machine1(i + .4, .1,400,300,.5,10.0,-900.0)
#         machine1(i + .4, .21,100,50,.75,10.0,1000.0)

# with Sound(play=True,statistics=True):
#     for i in np.arange(0, 2, .2):
#         machine1(i, .3, 100, 540, .5, 4.0, 0.)
#         machine1(i+.1, .3, 200, 540, .5, 3.0, 0.0)
# 
#     for i in np.arange(0., 2., .6):
#         machine1(i, .3, 1000, 540, .5, 6., 0.)
#         machine1(i+.1, .1, 2000, 540, .5, 1.0, 0)

# with Sound(play=True,statistics=True):
#     gen = make_rkoddssb(frequency=1000.0, ratio=2.0, r=.875)
#     noi = make_rand(1500, .04)
#     gen1 = make_rkoddssb(frequency=100.0, ratio=.1, r=.9)
#     ampf = make_env([0, 0, 1, 1, 11, 1, 12, 0],duration=11.0,scaler=.5)
#     frqf = make_env([0, 0, 1, 1, 2, 0, 10, 0, 11, 1, 12, 0, 20, 0], duration=11.0, scaler=hz2radians(1.0))
#     for i in range(0, 12*44100):
#         outa(i, .4 * env(ampf) * (rkoddssb(gen1, env(frqf)) + (2.0 * math.sin(rkoddssb(gen, rand(noi))))))
#         
#     for i in range(0, 10, 6):
#         machine1(i, 3, 1000, 540, .5, 6., 0.)
#         machine1(i+1, 1, 2000, 540, .5, 1., 0.)

# with Sound(play=True,statistics=True):
#     for i in np.arange(0, 2, .2):
#         machine1(i, .3, 1200, 540, .5, 40.0, 0.)
#         machine1(i + .1, .3, 2400, 540, .5, 3.0, 0.0)
# 
#     for i in np.arange(0., 2., .6):
#         machine1(i, .3, 1000, 540, .5, 6., 0.)
#         machine1(i+.1, .1, 2000, 540, .5, 10.0, 100)
# octave higher than above        
# with Sound(play=True,statistics=True):
#     for i in np.arange(0, 2, .2):
#         machine1(i, .3, 2400, 1000, .25, 40.0, 0.)
#         machine1(i + .05, .2, 4800, 1080, .5, 3.0, 0.0)
# 
#     for i in np.arange(0., 2., .6):
#         machine1(i, .3, 2000, 1080, .5, 6., 0.)
#         machine1(i+.05, .1, 4000, 1080, .5, 10.0, 100)     

# --------------- fpmc ---------------- #

    
def fpmc(beg, dur, freq, amp, mc_ratio, fm_index, interp):
    start = seconds2samples(beg)
    end = start + seconds2samples(dur)
    cr = 0.0
    cr_frequency = hz2radians(freq)
    md_frequency = hz2radians(freq*mc_ratio)
    md = 0.0
    
    for i in range(start, end):
        val = complex(math.sin(cr + (fm_index * math.sin(md))), math.sin(cr + (fm_index * math.sin(md))))
        outa(i, amp * (((1.0 - interp) * val.real) + (interp * val.imag)))
        cr += cr_frequency
        md += md_frequency
        
# with Sound(play=True,statistics=True):
#     fpmc(0, 4, 300, .8, 1.2, 1., .1)

        
# --------------- fm_cancellation  ---------------- # 
def fm_cancellation(beg, dur, frequency, ratio, amp, index):
    start = seconds2samples(beg)
    cx = 0.0
    mx = 0.0
    car_frequency = hz2radians(frequency)
    mod_frequency = hz2radians(ratio)
    stop = start + seconds2samples(dur)
    
    for i in range(start, stop):
        outa(i, amp * ((math.cos(cx) * math.sin(index * math.cos(mx))) - (math.sin(cx) * math.sin(index * math.sin(mx)))))
        cx += car_frequency
        mx += mod_frequency
        
# with Sound(play=True,statistics=True):
#     fm_cancellation(0, 1, 1000.0, 100.0, 0.3, 9.0)


        
# TODO: --------------- k3sin  ---------------- # 


def k3sin_wrapper(g):
    convert_frequency(g)
    g.coeffs = np.array([0.0, (np.pi*np.pi) / 6.0, np.pi / -4.0, .08333])
    g.angle = 0.0
    return g
    
def k3sin_reset(g):
    g.frequency = 0.0
    g.amgle = 0.0

make_k3sin, is_k3sin = make_generator('k3sin', {'frequency' : 0.0}, wrapper=k3sin_wrapper,
                        methods={'mus_reset' : [None, k3sin_reset]}, docstring="""creates a k3sin generator.""" )
                        
                        
#returns a sum of sines scaled by k^3                        
def k3sin(gen, fm=0.0):
    x = gen.angle
    if not 0.0 <= x <= np.pi*2:
        x = x % np.pi*2
    gen.angle = x + fm + gen.frequency
    return polynomial(gen.coeffs, x)

# with Sound(play=True,statistics=True):
#     gen = make_k3sin(frequency=340)
#     for i in range(0, 10000):
#         outa(i, .3 * k3sin(gen))


# TODO: --------------- izcos  ---------------- # 

# TODO: --------------- adjustable-square-wave ---------------- # 

# TODO: --------------- adjustable-triangle-wave ---------------- # 

# TODO: --------------- adjustable-sawtooth-wave ---------------- # 

# TODO: --------------- adjustable-oscil-wave ---------------- # 

# TODO: --------------- make-table-lookup-with-env ---------------- # 

# TODO: --------------- make-wave-train-with-env ---------------- # 

# TODO: --------------- round-interp ---------------- # 


# TODO: --------------- env-any functions ---------------- # 

# TODO: --------------- run-with-fm-and-pm ---------------- # 

# TODO: --------------- nchoosekcos ---------------- # 

# TODO: --------------- sinc-train ---------------- # 

# --------------- pink-noise ---------------- # 

def pink_noise_wrapper(g):
    g.data = np.zeros(g.n*2, dtype=np.double)
    amp = 1.0 / (2.5 * math.sqrt(g.n))
    g.data[0] = amp
    for i in range(2,2*g.n,2):
        g.data[i] =  mus_random(amp)
        g.data[i+1] = random.random()
    return g
    
make_pink_noise, is_pink_noise = make_generator('pink_noise', {'n' : 1}, wrapper=pink_noise_wrapper,
    docstring="""Creates a pink-noise generator with n octaves of rand (12 is recommended).""")

def pink_noise(gen):
    """Returns the next random value in the 1/f stream produced by gen."""
    x = 0.5 
    s = 0.0
    amp = gen.data[0]
    size = gen.n*2

    for i in range(2,size,2):
        s += gen.data[i]
        gen.data[i+1] -= x
        
        if gen.data[i+1] < 0.0:
            gen.data[i] = mus_random(amp)
            gen.data[i+1] += 1.0
        x *= .5
    return s + mus_random(amp)

# --------------- brown-noise ---------------- # 

def brown_noise_wrapper(g):
    g.prev = 0.0 
    g.sum = 0.0
    g.gr = make_rand(g.frequency, g.amplitude)
    return g
    
make_brown_noise, is_brown_noise = make_generator('brown_noise', {'frequency' : 0, 'amplitude' : 1.0}, 
                                    wrapper=brown_noise_wrapper,
                                    docstring="""Returns a generator that produces brownian noise.""")

def brown_noise(gen, fm=0.0):
    """returns the next brownian noise sample"""
    val = rand(gen.gr, fm)
    if not val == gen.prev:
        gen.prev = val
        gen.sum += val
    return gen.sum




# --------------- green-noise ---------------- # 

def green_noise_wrapper(g):
    g.gr = make_rand(g.frequency, g.amplitude)
    g.sum = .5 * (g.low + g.high)
    g.prev = 0.0 
    return g
    
make_green_noise, is_green_noise = make_generator('green_noise', {'frequency' : 0.0, 'amplitude' : 1.0, 'low' : -1.0, 'high' : 1.0},    
                                wrapper=green_noise_wrapper, docstring="""returns a new green-noise (bounded brownian noise) generator.""")
                                
                                
def green_noise(gen, fm=0.0):
    """Returns the next sample in a sequence of bounded brownian noise samples."""
    val = rand(gen.gr, fm)
    if not val == gen.prev:
        gen.prev = val
        gen.sum += val
        if not (gen.low <= gen.sum <= gen.high):
            gen.sum -= 2*val
    return gen.sum        
    
    

# --------------- green-noise-interp ---------------- # 

def green_noise_interp_wrapper(g):
    g.sum = .5 * (g.low + g.high)
    g.dv = 1.0 / math.ceil(CLM.srate / max(1.0, g.frequency))
    convert_frequency(g)
    g.incr = mus_random(g.amplitude) * g.dv
    g.angle = 0.0
    return g
    
make_green_noise_interp, is_green_noise_interp = make_generator('green_noise_interp', {'frequency' : 0.0, 'amplitude' : 1.0, 'low' : -1.0, 'high' : 1.0},
                            wrapper = green_noise_interp_wrapper, docstring="""Returns a new interpolating green noise (bounded brownian noise) generator.""")

def green_noise_interp(gen, fm=0.0):
    """Returns the next sample in a sequence of interpolated bounded brownian noise samples."""
    if not (0.0 <= gen.angle and gen.angle <= TWO_PI):
        val = mus_random(gen.amplitude)
        gen.angle %= TWO_PI # in scheme version modulo used which should be same as %
        if gen.angle < 1.0:
            gen.angle += TWO_PI
        if not (gen.low <= (gen.sum+val) <= gen.high):
            val = min(gen.high-gen.sum, max(gen.low-gen.sum, -val))
        gen.incr = gen.dv * val
    gen.angle += fm + gen.frequency
    gen.sum += gen.incr
    return gen.sum
    
        

# TODO: --------------- moving-sum ---------------- # 

def moving_sum_wrapper(g):
    g.gen = make_moving_average(g.n)
    g.gen.mus_increment = 1.0
    return g

make_moving_sum, is_moving_sum = make_generator('moving_sum', {'n' : 128}, wrapper=moving_sum_wrapper,docstring="""Returns a moving-sum generator""")

def moving_sum(gen, inpt):
    """Returns the sum of the absolute values in a moving window over the last n inputs."""
    return moving_average(gen.gen, abs(inpt))

# TODO: --------------- moving-variance ---------------- # 

# TODO: --------------- moving-rms ---------------- # 

# TODO: --------------- moving-length ---------------- # 

# TODO: --------------- weighted-moving-average ---------------- # 

# TODO: --------------- exponentially-weighted-moving-average ---------------- # 

# --------------- polyoid ---------------- # 

def make_polyoid(frequency, partial_amps_and_phases):
    length = len(partial_amps_and_phases)
    n = 0
    for i in range(0, length, 3):
        n = max(n, math.floor(partial_amps_and_phases[i]))   
    topk = n + 1
    sin_amps = np.zeros(topk, dtype=np.double)
    cos_amps = np.zeros(topk, dtype=np.double)
    for j in range(0,length,3):
        n = math.floor((partial_amps_and_phases[j]))
        amp = partial_amps_and_phases[j+1]
        phase = partial_amps_and_phases[j+2]
        if n > 0:
            sin_amps[n] = amp * math.cos(phase)
        cos_amps[n] = amp * math.sin(phase)
    return make_polywave(frequency, xcoeffs=cos_amps, ycoeffs=sin_amps)

def is_polyoid(g):
    return is_polywave(g) and g.mus_channel == Polynomial.BOTH_KINDS
    
polyoid = polywave

#def polyoid_env

# --------------- noid ---------------- # 
# def make_noid(frequency=0.0, n=1, phases=None, choice='all'):  
# the full version of this requires potentially loading a file so
# wondering good way to do this. using maybe binary numpy files
       
    
    
    
#         
        


# TODO: --------------- knoid ---------------- # 

# TODO: --------------- roid ---------------- # 

# --------------- tanhsin ---------------- # 

# is_waveshape = is_polyshape


# TODO: --------------- tanhsin ---------------- # 

def tanhsin_wrapper(g):
    g.osc = make_oscil(g.frequency, g.initial_phase)
    g.frequency = hz2radians(g.frequency)
    return g
    
make_tanhsin, is_tanhsin = make_generator('tanhsin', {'frequency' : 0.0, 'r' : 1.0, 
            'initial_phase' : 0.0}, wrapper=tanhsin_wrapper,
            docstring="""Returns a tanhsin generator.""")
                            

def tanhsin(gen, fm=0.0):
    """Produces tanh(r*sin) which approaches a square wave as r increases."""
    return math.tanh(gen.r * oscil(gen.osc,fm))



# --------------- moving-fft ---------------- # 

def moving_fft_wrapper(g):
    g.rl = np.zeros(g.n)
    g.im = np.zeros(g.n)
    g.data = np.zeros(g.n)
    g.window = make_fft_window(g.window, g.n)
    s = np.sum(g.window)
    g.window = g.window * (2./s)
    g.outctr = g.n+1
    return g
    
moving_fft_methods = {'mus_data' : [lambda g : g.data, None],
                        'mus_xcoeffs' : [lambda g : g.rl, None],
                        'mus_ycoeffs' : [lambda g : g.im, None],
                        'mus_run' : [lambda g,arg1,arg2 : moving_fft(g), None]}

make_moving_fft, is_moving_fft = make_generator('moving_fft', 
                {'input' : False, 
                'n' : 512, 
                'hop' : 128, 
                'window' : Window.HAMMING},
                wrapper=moving_fft_wrapper, 
                methods=moving_fft_methods,
                docstring="""returns a moving-fft generator.""")


def moving_fft(gen):
    new_data = False
    if gen.outctr >= gen.hop:
        if gen.outctr > gen.n:
            for i in range(gen.n):
                gen.data[i] = readin(gen.input)
        else:
            mid = gen.n - gen.hop
            gen.data = np.roll(gen.data, gen.hop)
            for i in range(mid,gen.n):
                gen.data[i] = readin(gen.input)
        
        gen.outctr = 0
        new_data = True
        gen.im.fill(0.0)
        np.copyto(gen.rl, gen.data)        
        gen.rl *= gen.window
        mus_fft(gen.rl,gen.im, gen.n,1)
        gen.rl = rectangular2polar(gen.rl,gen.im)
    gen.outctr += 1
    return new_data


# --------------- moving-spectrum ---------------- # 
# TODO: I am not convinced this is working properly

def phasewrap(x):
    return x - 2.0 * np.pi * np.round(x / (2.0 * np.pi))


def moving_spectrum_wrapper(g):
    g.amps = np.zeros(g.n)
    g.phases = np.zeros(g.n)
    g.amp_incs = np.zeros(g.n)
    g.freqs = np.zeros(g.n)
    g.freq_incs = np.zeros(g.n)
    g.new_freq_incs = np.zeros(g.n)
    g.data = np.zeros(g.n)
    g.dataloc = 0
    g.window = make_fft_window(g.window, g.n)
    s = np.sum(g.window)
    g.window = g.window * (2./s)
    g.outctr = g.n+1
    return g
    
moving_spectrum_methods = {'mus_xcoeffs' : [lambda g : g.phases, None],
                        'mus_ycoeffs' : [lambda g : g.amps, None],
                        'mus_run' : [lambda g,arg1,arg2 : moving_spectrum(g), None]}

make_moving_spectrum, is_moving_spectrum = make_generator('moving_spectrum', 
                {'input' : False, 
                'n' : 512, 
                'hop' : 128, 
                'window' : Window.HAMMING},
                wrapper=moving_spectrum_wrapper, 
                methods=moving_spectrum_methods,
                docstring="""returns a moving-spectrum generator.""")    



def moving_spectrum(gen):
    if gen.outctr >= gen.hop:
        # first time through fill data array with n samples
        if gen.outctr > gen.n:
            for i in range(gen.n):
                gen.data[i] = readin(gen.input)
        #
        else:
            mid = gen.n - gen.hop
            gen.data = np.roll(gen.data, gen.hop)
            for i in range(mid,gen.n):
                gen.data[i] = readin(gen.input)
        
        gen.outctr = 0
        gen.dataloc = gen.dataloc % gen.n

        gen.new_freq_incs.fill(0.0)
       
        data_start = 0
        data_end = gen.n - gen.dataloc
        

        gen.amp_incs[gen.dataloc:gen.n] = gen.window[data_start:data_end] * gen.data[data_start:data_end]

        if gen.dataloc > 0:
            data_start = gen.n - gen.dataloc
            data_end = data_start + gen.dataloc
            gen.amp_incs[0:gen.dataloc] = gen.window[data_start:data_end] * gen.data[data_start:data_end]  
        
        gen.dataloc += gen.hop
        
        mus_fft(gen.amp_incs, gen.new_freq_incs, gen.n, 1)

        gen.amp_incs = rectangular2polar(gen.amp_incs, gen.new_freq_incs)
                
        scl = 1.0 / gen.hop
        kscl = (np.pi*2) / gen.n
        gen.amp_incs -= gen.amps

        gen.amp_incs *= scl

        
        
        n2 = gen.n // 2
        ks = 0.0
        for i in range(n2):
            diff = (gen.new_freq_incs[i] - gen.freq_incs[i]) #% (np.pi*2)
            gen.freq_incs[i] = gen.new_freq_incs[i]
           # diff = phasewrap(diff)
            if diff > np.pi:
                diff = diff - (2*np.pi)
            if diff < -np.pi:
                diff = diff + (2*np.pi)
            gen.new_freq_incs[i] = diff*scl + ks
            ks += kscl
        gen.new_freq_incs -= gen.freqs
        gen.new_freq_incs *= scl

        

    gen.outctr += 1
    
    gen.amps += gen.amp_incs
    gen.freqs += gen.new_freq_incs
    gen.phases += gen.freqs

 

# TODO: --------------- moving-scentroid ---------------- # 

# TODO: --------------- moving-autocorrelation ---------------- # 

# TODO: --------------- moving-pitch ---------------- # 

# TODO: --------------- flocsig ---------------- # 
