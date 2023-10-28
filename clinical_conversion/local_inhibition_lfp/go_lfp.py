import os
from tvb.simulator.lab import *
import numpy as np
import matplotlib.pyplot as plt
LOG = get_logger('demo')
from tvb.simulator.models.stefanescu_jirsa import ReducedSetHindmarshRose
import argparse
from os.path import join as pjoin



parser = argparse.ArgumentParser(description='pass parameters')
parser.add_argument('--Group',type=str, required=True, help='group')
parser.add_argument('--Caseid',type=str, required=True, help='caseid')
parser.add_argument('--Go',type=float, required=True, help='Go')


args = parser.parse_args()

data_dir = '/scratch/yilewang/workspaces/data4project/'
connectome_dir = pjoin(data_dir, 'lateralization/connectome/zip')


file = pjoin(connectome_dir, args.Group, args.Caseid+'.zip')

def tvb_lfp_sj3d(Go, file):
    connectivity.speed = np.array([10.])
    length = 1e3*10
    sim = simulator.Simulator(
        model=ReducedSetHindmarshRose(), 
        connectivity=connectivity.Connectivity.from_file(file),                      
        coupling=coupling.Linear(a=np.array([Go])),
        simulation_length=length,
        integrator=integrators.HeunStochastic(dt=0.01220703125, noise=noise.Additive(nsig=np.array([0.00001]), ntau=0.0,
                                                                                    random_stream=np.random.RandomState(seed=42))),
        monitors=(
        monitors.TemporalAverage(period=1.),
        monitors.Raw(),
        monitors.ProgressLogger(period=1e2)
        )
    ).configure()


    (tavg_time, tavg_data), (raw_time, raw_data),_ = sim.run()
    return raw_data

raw_data = tvb_lfp_sj3d(args.Go, file)
np.save(pjoin('/scratch/yilewang/local_inhibition_lfp_go/',args.Group,args.Caseid+"_"+str(args.Go)+".npy"), raw_data)