import temp

from line_profiler import LineProfiler

lp = LineProfiler()
lp_wrapper = lp(temp.run)
lp_wrapper()

lp.print_stats()
print("done")
