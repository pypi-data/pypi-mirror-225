import musx
import functools
from pysndlib.clm import Sound

# musx integration
# TODO move to another file

#returns 
def CLM_Instrument(func):
    @functools.wraps(func)
    def call(time, *args, **kwargs):
        obj = functools.partial(func,time, *args, **kwargs)
        obj.time = time
        return obj
    return call 
    
def render_clm(seq: musx.seq, filename, **kwargs):
    s = seq.events.copy()
    with Sound(filename, **kwargs):
        for event in s:
            event()

# what should the clm score file be? 
# TODO make this something useful that could be read.  i am assuming some type of dictionary
# with header for info and then entries in seq
def print_clm(seq):
    s = seq.events.copy()
    for v in s:
        funcname = v.func.__name__
        args = ("{},"*(len(v.args))).format(*v.args)
        kwargs = ','.join([f'{k}={v}' for k,v in v.keywords.items()])
        #print(args)
        print(f'({funcname} {args}{kwargs})') #TODO: write to actual file
