# encoding: utf-8
"""
Higher-level abstraction for the underlying profile module
"""

try:
    import cProfile as profile
except:
    import profile

class Profiler(object):
    def __init__(self):
        self._profiler = profile.Profile()
        
    def profile(self, f, args=[], kwargs={}):
        return self._profiler.runcall(f, *args, **kwargs)

    def stats(self):
        """
        Due to the way profile is designed we cannot return more than one
        level of the callgraph since there is no way to reliably determine the
        call stack for anything with multiple callers
        """

        stats = self._profiler.getstats()
        stats.sort()
        
        simple_stats = []
        
        for s in stats:
            simple_stats.extend(self.process_profiler_entry(s))

        return simple_stats

    def process_profiler_entry(self, entry):
        label = self.label_for_code(entry.code)
        if "_lsprof" in label:
            return []
        
        d = {
            "label": label,
            "call_count": entry.callcount,
            "internal_time": entry.inlinetime,
            "recursive_call_count": entry.reccallcount,
            "total_time": entry.totaltime,
        }

        if getattr(entry, "calls", None):
            d['calls'] = [ self.process_profiler_entry(i) for i in entry.calls ] 
        
        return [d]

    def label_for_code(self, code):
        """Generate a friendlier version of the code function called"""
        if isinstance(code, str):
            return code
        else:
            return '%s <%s:%d>' % (code.co_name,
                                 code.co_filename,
                                 code.co_firstlineno)
