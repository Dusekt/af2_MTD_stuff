"""
Script for making my life on metacenter easier.
origin usage for AF2DISTPROB, protein interactions
The starting fire has to have "_number" at the end
can be used to start first mtd simulation with plumed

Parameters
---------
os: Linux/Unix, frontend bash
using python 2.7, library os

pref_a: the prefix of input files, HAS TO END WITH "_" (underscore)
pref_b: the prefix of output files
suf_a: suffix (number)
suf_b: suffix (usually number+1)


"""


import os

pref_a = "mtdt_"
pref_b = pref_a
range = 1
while True:

# cut out number out of dirname, used for as a index

    if str(os.getcwd()[-(range+1)]) == "_":
        break
    else:
        range = range + 1

suf_a = int(os.getcwd()[-range:])
suf_b = suf_a + 1

if suf_a < 10:
    suf_a = "0" + str(suf_a)
if suf_b < 10:
    suf_b = "0" + str(suf_b)

# cant fit this in, left for later improvement
c = "{ trap - TERM EXIT && echo \" crashed at \`hostname\`\" >&2 ; exit 1 ; }"

# filename, dirname
file = pref_a + str(suf_a)
dir = pref_b + str(suf_b)

# copying files, making dir
os.mkdir("../{dir}".format(dir=dir))
os.system('cp {file}.cpt ../{dir}'.format(file=file, dir=dir))
os.system('cp {file}.gro ../{dir}'.format(file=file,dir=dir))
os.system('cp *.top ../{dir}'.format(dir=dir))
os.system('cp *.itp ../{dir}'.format(dir=dir))
os.system('cp *.mdp ../{dir}'.format(dir=dir))
os.system('rm ../{dir}/mdout.mdp'.format(dir=dir))
os.system('cp plumed.dat ../{dir}'.format(dir=dir))
os.system('cp HILLS ../{dir}'.format(dir=dir))


# runit.sh script for plumed Gromacs
with open('../{dir}/runit.sh'.format(dir=dir), 'w') as f:

    f.write('#!/bin/bash\n\
MYDIR=`pwd`\n\
RUN_FILE=`pwd`/mtd.$$\n\
SCRATCH=\'$SCRATCHDIR\'\n\
\
echo "#!/bin/sh" >> $RUN_FILE\n\
echo "#PBS -q gpu" >> $RUN_FILE\n\
echo "#PBS -l walltime=24:00:00" >> $RUN_FILE\n\
echo "#PBS -l select=1:ncpus=9:ngpus=1:mem=64gb:scratch_local=100gb" >> $RUN_FILE\n\
echo "trap \'rm -r \$SCRATCHDIR\' TERM EXIT" >> $RUN_FILE\n\
echo "cp -r $MYDIR/* \$SCRATCHDIR/  || exit 1" >> $RUN_FILE\n\
echo "cd \$SCRATCHDIR || exit 2 " >> $RUN_FILE\n\
echo "export OMP_NUM_THREADS=12" >> $RUN_FILE\n\
\n\
echo "singularity exec -B \$PWD:/scratch --pwd /scratch --nv /storage/brno12-cerit/home/ljocha/singularity/ljocha-gromacs-2021-3_3.sif gmx grompp -f npt.mdp -c {pref_a}{suf_a}.gro -t {pref_a}{suf_a}.cpt -p barnbar.top -o {pref_b}{suf_b}.tpr -maxwarn 666" >> $RUN_FILE\n\
echo "singularity exec -B \$PWD:/scratch --pwd /scratch --nv /storage/brno12-cerit/home/ljocha/singularity/ljocha-gromacs-2021-3_3.sif gmx mdrun -ntomp 12 -deffnm {pref_b}{suf_b} -plumed plumed.dat " >> $RUN_FILE\n\
\n\
echo "cp -r * $MYDIR/ || {c}" >> $RUN_FILE\n\
\n\
qsub $RUN_FILE'.format(c = c, pref_b = pref_b, pref_a = pref_a, suf_a = suf_a, suf_b = suf_b))

os.system('chmod u+x ../{dir}/runit.sh'.format(dir=dir))
#os.system(../{dir}/runit.sh'.format(dir=dir))
os.system('cp runit_casc.py ../{dir}'.format(dir=dir))
