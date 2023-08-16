#+
#   ARES/HADES/BORG Package -- ./scripts/regraft_run.py
#   Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
#   Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>
#
#   Additional contributions from:
#      Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
#   
#+
import warnings

warnings.simplefilter("ignore", FutureWarning)
import h5py as h5
import argparse
import os

class NotCompatible(Exception):
    def __init__(msg_):
        self.msg = msg_

    def __repr__():
        return "NotCompatible: " + self.msg

def restart_name(prefix, cpu):
    return os.path.join(prefix, "restart.h5_%d" % cpu)

def detect_ncpu(prefix):
    ncpu = 0
    while True:
        try:
            os.stat(os.path.join(prefix, "restart.h5_%d" % ncpu))
        except OSError:
            break
        ncpu += 1
    return ncpu

def bias_name(bid):
    return "scalars/galaxy_bias_%d" % bid

def nmean_name(nid):
    return "scalars/galaxy_nmean_%d" % nid

def check_compat(restart_prefix, mcmc):
    print("Checking compatibility of MCMC and restart")
    with h5.File(restart_name(restart_prefix, 0), mode="r") as f_r, \
        h5.File(mcmc, mode="r") as f_m:

        bname = bias_name(0)
        while bname in f_m:
            if not bname in f_r:
                raise NotCompatible("Not enough catalogs")

            if f_m[bname].size != f_r[bname].size:
                raise NotCompatible("Incompatible bias model")

            bias_num += 1
            bname = bias_name(bias_num)

def transfer(src, dest, name, start):
    if (not name in src) or (not name in dest):
        return False

    sz = dest[name].shape[0]
    dest[name][...] = src[name][start:(start+sz),...]
    return True

def checked_transfer(*args):
    if not transfer(*args):
        raise NotCompatible("Problems in grafting")

def graft(restart_prefix, ncpus, mcmc):
    with h5.File(args.mcmc, mode="r") as f_m:
        plane_start = 0
        plane_len = 0

        for cpu in range(ncpus):
            print("Transplanting to restart CPU %d" % cpu)
            with h5.File(restart_name(restart_prefix, cpu), mode="r") as f_r:
                plane_len = f_r['scalars/BORG_final_density'].shape[0]
                checked_transfer(f_m, f_r, 'scalars/BORG_final_density', plane_start)
                checked_transfer(f_m, f_r, 'scalars/s_field', plane_start)
                checked_transfer(f_m, f_r, 'scalars/s_hat_field', plane_start)

                bias_num = 0
                while True:
                    if not transfer(f_m, f_r, bias_name(bias_num), 0):
                        break
                    if not transfer(f_m, f_r, nmean_name(bias_num), 0):
                        break
                    bias_num += 1

                plane_start += plane_len

p = argparse.ArgumentParser(description="Graft the state of a previous run on a given restart.")

p.add_argument('mcmc', type=str, help="MCMC state to import")
p.add_argument('restart', type=str, help="restart prefix directory")
args = p.parse_args()

ncpu = detect_ncpu(args.restart)
print("Found %d CPU restart file")


check_compat(args.restart, args.mcmc)
graft(args.restart, ncpu, args.mcmc)

print("Done")
