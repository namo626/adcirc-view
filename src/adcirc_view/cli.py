import numpy as np
import os
import matplotlib.pyplot as plt
import argparse

def read_f61(filename):

    with open(filename) as f1:
        l1 = f1.readline()
        l1 = f1.readline()

        # Get timestep info
        info = l1.split()
        num_snaps = int(info[0])
        num_stations = int(info[1])

        if num_snaps < 1:
            raise ValueError("No elevation data present in %s" % filename)
        if num_stations < 1:
            raise ValueError("No stations present in %s" % filename)

        elev = np.zeros((num_snaps, num_stations))
        ts = np.zeros(num_snaps)

        for snap in range(num_snaps):
            timestamp = f1.readline().split()
            ts[snap] = float(timestamp[0]) / 86400.

            for sta in range(num_stations):
                line = f1.readline().split()
                x = line[1]
                if x == "NaN":
                    y = np.nan
                else:
                    y = float(x)
                # If dry, set to zero
                if y < -1000:
                    y = 0.

                elev[snap, sta] = y


        return ts, np.transpose(elev)


def compare_f61(files, folder, shift=0.):
    _, elev = read_f61(files[0])
    num_sta = elev.shape[0]
    data = {}
    
    for f in files:
        ts, elev = read_f61(f)
        data[f] = (ts, elev+shift)

    for sta in range(num_sta):
        plt.figure()
        for f in files:
            ts, elev = data[f]
            try:
                plt.plot(ts, elev[sta,:], label=f)
            except IndexError:
                print("Warning: elevation station %d does not exist in %s. Skipping." % (sta, f))

        plt.xlabel("Time (days)")
        plt.ylabel("Water elevation (m)")
        plt.title("Station %d" % sta)
        plt.legend()
        plt.savefig("%s/sta%04d.jpg" % (folder.strip('/'), sta), bbox_inches="tight", dpi=300)
        plt.close()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('dir', help="Name of output directory. Will be created if does not exist, and overwrites files if it does.")
    parser.add_argument('files', nargs='+', help="One or more fort.61 file names")
    parser.add_argument('--shift', type=float, default=0., help="Offset (m) to apply to all stations")

    args = parser.parse_args()
    files = args.files
    os.makedirs(args.dir, exist_ok=True)

    compare_f61(files, args.dir, args.shift)

if __name__ == "__main__":
    main()
