import DataHandler as dh
import CoordinateDescent as cd
import numpy as np

def getSampleValues(n, value_range, isLogScale=False) :
  if isLogScale :
    value_range = np.log(np.array(value_range)).tolist()
  values = (value_range[1] - value_range[0])*(np.arange(0,n))/(n-1) + value_range[0]
  if isLogScale :
    values = np.exp(np.array(values))
  return values.tolist()

def collectProblemData(dx, v0x, vf, obs_t, obs_offset):
    data_handler = dh.DataHandler(500, "optimal.csv", "eval.csv", False, 2)
    step_range = [.1,10]
    lr_range = [.1,.99]
    nstep = 10 # number of sampled step sizes
    nlr = 100 # number of sampled learning rates per initial step sizes
    
    step_values = getSampleValues(nstep, step_range)
    lr_values = getSampleValues(nlr, lr_range)
    
    data = np.zeros([nstep*nlr, 4])
    iter_count = -1
    for step in step_values:
        for lr in lr_values:
            iter_count += 1
            solver = cd.CoordinateDecent(data_handler, 0.001, 0.001, step, lr)
            C,_,count,_,_ = solver.solve(dx, v0x, vf, obs_t, obs_offset)
            data[iter_count, 0] = step
            data[iter_count, 1] = lr
            data[iter_count, 2] = C
            data[iter_count, 3] = count
    return data

if __name__ == "__main__":
    dx = np.array([0, 1])
    v0x = 1
    vf = np.array([0, 1])
    obs_t=0.5
    obs_offset=0.0
    data = collectProblemData(dx, v0x, vf, obs_t, obs_offset)        
    np.savetxt("CoordinateDescentData.csv", data, delimiter=',')
    