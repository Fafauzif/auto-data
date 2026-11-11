from pathlib import Path
import h5py,numpy as np
from scipy.io import loadmat
def load_signals(path):
 if h5py.is_hdf5(path):
  with h5py.File(path) as f:
   g=f['Raw'];return {k:np.array(g[k]).ravel() for k in g},'MATLAB7.3/HDF5'
 m=loadmat(path,squeeze_me=True,struct_as_record=False);o=m['Raw']
 return {k:np.asarray(getattr(o,k)).ravel() for k in o._fieldnames},'MATLAB5-compatible'
