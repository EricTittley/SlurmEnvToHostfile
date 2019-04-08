# Read the Slurm environment variables and produce a hostfile suitable for mpirun -h hostfile
#
# Based on Christopher Hoffman's code (https://github.com/pftool/pftool/blob/master/scripts/pfscripts.py)
# but extended to parse SLURM_JOB_CPUS_PER_NODE correctly, not just as a single integer.
#
#
# EXAMPLE USAGE
#
# jobsubmission.sbatch:
#  ...
#  python3 SlurmEnvToHostfile.py
#  mpirun --hostfile hostfile MyMPIExecutable

# Eric Tittley 2019-02-33

import os
import sys
import re
import parse

def get_nodeallocation():
  """
  This function reads the SLURM environment to see if any variables
  are set that give an indication of what nodes/processes are
  currently allocated for the code running. The 2-tuple (nodelist,numprocs)
  is returned. If no allocation is set, then ([],0) is
  returned
  This function parses SLURM_JOB_NODELIST values such as:
    worker[005,007,009-012,036-055,060]
  and SLURM_JOB_CPUS_PER_NODE values such as
    2,4,2(x2),7,1,2(x4),1,2(x10),7,1,2(x3),3
  """

  nodelist = []                                                         # the list of nodes in the allocation
  numprocs = []                                                         # total number of processors/processes for the job

        # check Environment for Job control variables
  try:                                                                  # check for SLURM
    slurm_nodes = os.environ['SLURM_JOB_NODELIST']
    slurm_ppn = os.environ['SLURM_JOB_CPUS_PER_NODE']
                # parse the node list variable
    if re.match("[a-zA-Z-]+[0-9]*[a-zA-Z-]*$",slurm_nodes) is not None: # examples of cases matched: fta04, r-fta05, r-b-node, fta, fta003sb
      nodelist.append(slurm_nodes)                                      # just one node in list
    else:                                                               # examples of cases matched: fta[03-06], fta[05,07,09], fta[01-04,07,09,10-12]
      mobj = re.match("([a-zA-Z-]+)\[((([0-9]+(\-[0-9]+)*)\,*)+)\]([a-zA-Z-]*)$",slurm_nodes)

      if mobj is None:                                                  # not a valid SLURM_JOB_NODELIST value -> get out of here!
        raise KeyError                                  

      npre = mobj.group(1)                                              # Group 1 is the node name prefix (i.e. fta)
      nnum = mobj.group(2).split(',')                                   # Group 2 is a list of the node numbers (i.e. 01-04,07)
      nsuf = mobj.group(6)                                              # Group 6 is the node name suffix after any numbers (i.e. s)
      for n in nnum:
          nums = n.split('-')
          if len(nums) < 2:                                             # not a range of numbers
            if len(nsuf):                                               # see if we have a node name suffix
              nodelist.append(npre + nums[0] + nsuf)
            else:
              nodelist.append(npre + nums[0])
          else:                                                         # a range is specified
            low = int(nums[0])
            high = int(nums[1])+1
            maxdigits = len(nums[1])

            if high < low:                                              # paranoid check. If true -> something is terribly wrong!
              raise KeyError
            for i in range(low,high):                                   # iterate through range, adding nodes to list
              if len(nsuf):
                nodelist.append("%s%0*d%s" % (npre,maxdigits,i,nsuf))
              else:
                nodelist.append("%s%0*d" % (npre,maxdigits,i))

    numprocs_unparsed = slurm_ppn.split(",")
    for n in numprocs_unparsed:
          if "x" not in n:
              numprocs.append(int(n))
          else: # parse elements of the form 3(x2) meaning two consecutive nodes have three slots each
              L=parse.parse("{}(x{})",n)
              num        = int(L[0])
              numrepeats = int(L[1])
              for j in range(0,numrepeats):
                  numprocs.append(num)
     
  except KeyError:
    nodelist = []
    numprocs = 0

  return(nodelist,numprocs)


####### START OF MAIN #######

# Parse the environment
nodelist,numprocs=get_nodeallocation()

# Write the hostfile
f=open("hostfile","w")
for i in range(0,len(nodelist)):
    f.writelines([nodelist[i],' slots=',str(numprocs[i]),'\n'])
f.close()
