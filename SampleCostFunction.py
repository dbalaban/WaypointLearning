import DataHandler as dh
import numpy as np

def getSampleValues(n, value_range, isLogScale=False) :
  if isLogScale :
    value_range = np.log(np.array(value_range)).tolist()
  values = (value_range[1] - value_range[0])*(np.arange(0,n))/(n-1) + value_range[0]
  if isLogScale :
    values = np.exp(np.array(values))
  return values.tolist()

def sample_spherical(npoints, ndim=4):
    vec = np.random.randn(ndim, npoints)
    vec /= np.linalg.norm(vec, axis=0)
    return vec
 
def getCostsAtRadius(nsample, radius, dx, v0x, vf, obs_t, obs_offset, optimal):
    sample = radius*sample_spherical(nsample)
    optimal = np.array([0.38167919,  0.39101533, -0.44043292,  0.05524485]).reshape([4,1])
    sample += optimal
    
    T_opt, _, _, x = data_handler.getOptimalSolution(
                        dx, v0x, vf, obs_t, obs_offset)
    
    costs = np.zeros(nsample)
    for i in range(nsample):
        T, T_col = data_handler.Evaluate(dx, v0x, vf, sample[:,i], obs_t, obs_offset)
        costs[i] = data_handler.GetCost(T_opt, T_col, T)
    
    return costs
       
if __name__ == "__main__":
    data_handler = dh.DataHandler(10, "optimal_nn.csv", "eval_nn.csv", True, 1)
    
    nsample = 100
    optimal = np.array([0.38167919,  0.39101533,
                        -0.44043292,  0.05524485]).reshape([4,1])
    
    dx = np.array([0, 1])
    v0x = 1
    vf = np.array([0, 1])
    obs_t=0.5
    obs_offset=0.0
    
    nradii = 10
    radii = getSampleValues(nradii, [0.0001, 10], isLogScale=True)
    data = np.zeros([nradii*nsample, 2])
    
    for ri in range(nradii):
        radius = radii[ri]
        costs = getCostsAtRadius(nsample, radius, dx, v0x, vf,
                                 obs_t, obs_offset, optimal)
        data[ri*nsample:(ri+1)*nsample,0] = radius
        data[ri*nsample:(ri+1)*nsample,1] = costs
    np.savetxt("costs_at_radius.csv", data, delimiter=',')
    