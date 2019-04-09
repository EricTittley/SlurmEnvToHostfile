#!/bin/tcsh

# SLURM provides the following two environment variables from which a hostfile
# can be generated.

setenv SLURM_JOB_NODELIST "worker[005,007,009-012,036-055,060]"
setenv SLURM_JOB_CPUS_PER_NODE "2,4,2(x2),7,1,2(x4),1,2(x10),7,1,2(x3),3"

python3 SlurmEnvToHostfile.py

python3 SlurmEnvToHostfile.py --no-file

python3 SlurmEnvToHostfile.py --hostfile=machinefile --style=mpich

