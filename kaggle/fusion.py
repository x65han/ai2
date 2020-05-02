import json, glob
from trectools import TrecRun, fusion

rs = []
for path in glob.glob('*.txt'):
    run = TrecRun(path)
    rs.append(run)

# Easy way to create new baselines by fusing existing runs:
fused_run = fusion.reciprocal_rank_fusion(rs)


fused_run.print_subset("asymptomatic-shedding.out", topics=fused_run.topics())