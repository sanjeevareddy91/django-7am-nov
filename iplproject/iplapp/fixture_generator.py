import scheduler
import numpy as np
import pandas as pd

nteams = 10
nfields = 3
bestfields = 1

teams = ['Team ' + str(z+1) for z in range(nteams)]
games = scheduler.get_best_schedule(teams,nfields,bestfields)

# Field distribution quality
scheduler.get_aggregate_data(games)

# Schedule quality
np.array(scheduler.get_gap_info(games))   # gaps between games (rows are teams)

# Save the schedule to csv
schedule = scheduler.pivot_schedule(games)
schedule.to_csv('schedule.csv')