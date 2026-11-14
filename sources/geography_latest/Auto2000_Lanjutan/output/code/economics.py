"""Unit-economics algebra; no invented Auto2000 margin, cost or conversion inputs."""
from pathlib import Path
import csv,math

def incremental_contribution(recovered_jobs,baseline_subsidised,displaced_jobs,gross_profit,variable_cost,fixed_cost,displaced_gp=None):
 if displaced_gp is None:displaced_gp=gross_profit
 return recovered_jobs*(gross_profit-variable_cost)-baseline_subsidised*variable_cost-displaced_jobs*displaced_gp-fixed_cost

def minimum_recovered_jobs(baseline_subsidised,displaced_jobs,gross_profit,variable_cost,fixed_cost,displaced_gp=None):
 if displaced_gp is None:displaced_gp=gross_profit
 if gross_profit<=variable_cost:return math.inf
 return (fixed_cost+baseline_subsidised*variable_cost+displaced_jobs*displaced_gp)/(gross_profit-variable_cost)

def maximum_variable_cost(recovered_jobs,baseline_subsidised,displaced_jobs,gross_profit,fixed_cost,displaced_gp=None):
 if displaced_gp is None:displaced_gp=gross_profit
 if recovered_jobs+baseline_subsidised<=0:return None
 return (recovered_jobs*gross_profit-displaced_jobs*displaced_gp-fixed_cost)/(recovered_jobs+baseline_subsidised)

if __name__=='__main__':
 rows=[]
 for ratio in [0,.1,.25,.5,.75,.9,1,1.1]:
  rows.append({'hypothetical_variable_cost_share_of_incremental_GP':ratio,'breakeven_recovered_job_multiple_of_F_div_g_if_no_leakage_or_displacement':1/(1-ratio) if ratio<1 else 'No finite break-even','status':'Algebraic normalised sensitivity, not observed Auto2000 cost/margin'})
 with (Path(__file__).parent/'normalised_economic_sensitivity.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 assert incremental_contribution(10,0,0,1,.5,5)==0
 assert minimum_recovered_jobs(0,0,1,.5,5)==10
 assert maximum_variable_cost(10,0,0,1,5)==.5
 print('Three algebraic identity checks passed; no actual financial parameters assumed.')
