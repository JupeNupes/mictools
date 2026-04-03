import h5py
import numpy as np
import matplotlib.pyplot as plt
import os

#Define my plotting function
def plot_spectra(filename):
    with h5py.File(filename,'r') as f:
        data = f['data']

# Execute the function when running the file
if __name__ == '__main__':
    x = 2 #x (horizontal) position of pixel
    y = 3 #y (vertical) position of pixel

    # Define the scan number and create the scan string
    ScanNum = 239
    scan_str = f"Scan_{ScanNum:04d}"
    path2Data = ( '/Volumes/data1/isn/2026-1/2026-1-Harder/RAW/' + scan_str +
                 '/ME7/' + f{'scan_'})
    # filename = scan_str + '/ME7/' + '.h5'
    print(path2Data)

    # path2Data = '/Volumes/data1/isn/2026-1/2026-1-Harder/RAW/'
    # filename = 'test.h5'
    # plot_spectra(filename)