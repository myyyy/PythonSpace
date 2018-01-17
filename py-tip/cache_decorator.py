import time
import hashlib
import pickle
 
cache = {}
 
def is_obsolete(entry,duration):
    d = time.time()-entry['time']
    return d>duration
   
def compute_key(function,args,kwargs):
    key = pickle.dumps((function.func_name,args,kwargs))
    return hashlib.sha1(key).hexdigest()
 
def memoize(duration=10):
    def _memorize(function):
        def __memorize(*args):
            import pdb;pdb.set_trace()
            key = compute_key(function,args,{})
           
            if key in cache and not is_obsolete(cache[key],duration):
                print 'we got a winner'
                return cache[key][ 'value']
           
            result = function(*args)
            cache[key] = { 'value':result, 'time':time.time()}
            return result
        return __memorize
    return _memorize

@memoize()
def complex(a,b):
    time.sleep(2)
    print a+b 

if __name__ == '__main__':
    complex(1,2)
    complex(1,2)
