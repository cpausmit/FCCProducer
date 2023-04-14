#!/usr/bin/env python
import sys
import os
import subprocess
import random
import config
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--campaign", type=str, help="Campaign", default='spring2023')
parser.add_argument("--detector", type=str, help="Detector", default='IDEA')
parser.add_argument("--generator", type=str, help="Generator", default='whizard')
parser.add_argument("--card", type=str, help="Card", default='wzp6_ee_qq_ecm91p2')
parser.add_argument("--nevents", type=int, help="Nevents", default=10)
args = parser.parse_args()

n_per_job = 50000

nevents = int(args.nevents)
njobs = int(nevents/n_per_job)
n_missing = int(args.nevents) - njobs*n_per_job

######################################################
cwd = os.getcwd()
stack = config.stacks[args.campaign]
priority = 'group_u_FCC.local_gen'
queue = "workday" # espresso microcentury longlunch workday tomorrow testmatch nextweek

script = "run_job.sh"
submit_dir = f"{cwd}/submit/{args.campaign}/{args.detector}/{args.generator}/{args.card}"
out_base = f"/store/fccee"

local_dir = f"{cwd}/local/{args.campaign}/{args.detector}/{args.generator}/{args.card}"

def find_running(args):
    file_ids = []
    (rc,string) = subprocess.getstatusoutput('condor_q -format "%d " ClusterId -format "%s\n" Args | grep -v cmsRun')
    for line in string.split('\n'):
        f = line.split(" ")
        if len(f)>5 and args.campaign in line and args.detector in line and args.generator in line and args.card in line: 
            file_ids.append(line.split(" ")[5])
    return file_ids

def find_existing(dir):
    file_ids = []
    (rc,flist) = subprocess.getstatusoutput(f'gfal-ls root://submit50.mit.edu/{dir}')
    for filename in flist.split('\n'):
        if '.root' in filename:
            file_ids.append(filename[0:6])
    return file_ids
    
    
def make(dir,script):
    # make a job file that when executed generates the events
    
    #    with open(f"{dir}/{script}",'w') as fOut:
    #    
    #        fOut.write('#!/bin/bash\n')
    #        fOut.write('echo " Job: $0"\n')
    #        fOut.write('echo " Arguments: $@"\n')
    #        fOut.write('CAMPAIGN=$1\n')
    #        fOut.write('GENERATOR=$2\n')
    #        fOut.write('DETECTOR=$3\n')
    #        fOut.write('CARD=$4\n')
    #        fOut.write('JOBID=$5\n')
    #        fOut.write('SEED=$6\n')
    #        fOut.write('NEVTS=$7\n')
    #        fOut.write('ROOT_OUT=${JOBID}_${SEED}_${NEVTS}.root\n')
    #        fOut.write(f'OUT_DIR={out_base}/$CAMPAIGN/$GENERATOR/$DETECTOR/$CARD')
    #        fOut.write('SECONDS=0\n')
    #        fOut.write('unset LD_LIBRARY_PATH\n')
    #        fOut.write('unset PYTHONHOME\n')
    #        fOut.write('unset PYTHONPATH\n')
    #        fOut.write('mkdir $SEED\n')
    #        fOut.write('cd $SEED\n')
    #        fOut.write(f'source {stack}\n')
    #    
    #        fOut.write('tar fzx ../cards.tgz\n')
    #        fOut.write('cp ./cards/$CAMPAIGN/generator/$GENERATOR/$CARD.sin thecard.sin\n')
    #        fOut.write('cp ./cards/$CAMPAIGN/delphes/card_$DETECTOR.tcl card.tcl\n')
    #        fOut.write('cp ./cards/$CAMPAIGN/delphes/edm4hep_$DETECTOR.tcl edm4hep_output_config.tcl\n')
    #    
    #        fOut.write('echo "Run $GENERATOR"\n')
    #        fOut.write('echo "n_events = $NEVTS" > header.sin \n')
    #        fOut.write('echo "seed = $SEED"  >> header.sin \n')
    #        fOut.write('cat header.sin thecard.sin > card.sin \n') 
    #        fOut.write('$GENERATOR card.sin \n')
    #        fOut.write('pwd; ls -lhrt \n')
    #        fOut.write('echo "finished run"\n')
    #        
    #        fOut.write('echo "Run DelphesSTDHEP_EDM4HEP"\n')
    #        fOut.write('DelphesSTDHEP_EDM4HEP card.tcl edm4hep_output_config.tcl $ROOT_OUT proc.stdhep \n')
    #        fOut.write('pwd; ls -lhrt \n')
    #        fOut.write('echo "DONE"\n')
    #        
    #        fOut.write('echo "Copy file ($ROOT_OUT,$OUT_DIR)"\n')
    #        fOut.write('#cp $ROOT_OUT $OUT_DIR\n')
    #        fOut.write('source /cvmfs/grid.cern.ch/centos7-ui-4.0.3-1_umd4v3/etc/profile.d/setup-c7-ui-example.sh\n')
    #        fOut.write('voms-proxy-info -all\n')
    #        fOut.write('echo gfal-copy -p file:///$PWD/$ROOT_OUT root://submit50.mit.edu/$OUT_DIR/$ROOT_OUT\n')
    #        fOut.write('gfal-copy -p file:///$PWD/$ROOT_OUT root://submit50.mit.edu/$OUT_DIR/$ROOT_OUT\n')
    #        fOut.write('echo "RC: $?"\n')
    #        fOut.write('duration=$SECONDS\n')
    #        fOut.write('echo "Duration: $(($duration))"\n')
    #        fOut.write('echo "Events: $NEVTS"\n')
    #                
    if not os.path.exists(f"{dir}/{script}"):
        subprocess.getstatusoutput(f'chmod 750 {script}')
        subprocess.getstatusoutput(f'cp ./bin/{script} {dir}')
    if not os.path.exists(f"{dir}/cards.tgz"):
        subprocess.getstatusoutput(f'cp ./cards.tgz {dir}')
        
    return

if __name__=="__main__":

    # Just a trial run
    if njobs > 0:

        if not os.path.exists(f"./cards.tgz"):
            subprocess.getstatusoutput(f'tar fzc .cards.tgz cards/')
        if not os.path.exists(submit_dir):
            os.makedirs(submit_dir)
    
        print(f"{out_base}/{args.campaign}/{args.generator}/{args.detector}/{args.card}")

        existing_ids = find_existing(f"{out_base}/{args.campaign}/{args.generator}/{args.detector}/{args.card}")
        print(" Done: ")
        print(existing_ids)

        running_ids = find_running(args)
        print(" Running: ")
        print(running_ids)

        njob = 0
        make(submit_dir,script)
        fOutName = f'condor.cfg'

        with open(fOutName,'w') as fOut:
            fOut.write(f'executable           = {script}\n')
            fOut.write(f'transfer_input_files = {submit_dir}/cards.tgz\n')
            fOut.write(f'Log                  = {submit_dir}/$(ClusterId).log\n')
            fOut.write(f'getenv               = True\n')
            fOut.write(f'use_x509userproxy    = True\n')
            fOut.write(f'environment          = "LS_SUBCWD={submit_dir}"\n')
            fOut.write(f'requirements         = ( BOSCOCluster =!= "t3serv008.mit.edu" && BOSCOCluster =!= "ce03.cmsaf.mit.edu" && BOSCOCluster =!= "eofe8.mit.edu" )\n')
            fOut.write(f'+DESIRED_Sites       = "mit_tier3"\n')
            fOut.write(f'+SingularityImage    = "/cvmfs/singularity.opensciencegrid.org/opensciencegrid/osgvo-el7:latest"\n')
            fOut.write(f'on_exit_remove       = (ExitBySignal == False) && (ExitCode == 0)\n')
            fOut.write(f'max_retries          = 3\n')
            fOut.write(f'+JobFlavour          = "{queue}"\n')
            fOut.write(f'+AccountingGroup     = "{priority}"\n')

            empty = True
            while njob <= njobs:
                nevt = n_per_job
                if njob==njobs:
                    nevt = n_missing
                seed = f"{random.randint(1000000000,9999999999)}"
                njob += 1
                cjob = "%06d"%njob
                if   cjob in existing_ids:
                    print(f"Existing - job {njob} with seed {seed} and {nevt} events -- SKIP")
                elif cjob in running_ids:
                    print(f"Running -- job {njob} with seed {seed} and {nevt} events -- SKIP")
                else:
                    empty = False
                    print(f"Prepare job {njob} with seed {seed} and {nevt} events")
                    fOut.write(f'Args                 = {args.campaign} {args.generator} {args.detector} {args.card} {cjob} {seed} {nevt}\n')
                    fOut.write(f'Output               = {submit_dir}/{cjob}_{seed}_{nevt}.$(ClusterId).$(ProcId).out\n')
                    fOut.write(f'Error                = {submit_dir}/{cjob}_{seed}_{nevt}.$(ClusterId).$(ProcId).error\n')
                    fOut.write(f'Queue\n')
        
        if not empty:
            subprocess.getstatusoutput(f'chmod 750 {fOutName}')
            os.system(f"cp {fOutName} {submit_dir}; cd {submit_dir}; condor_submit {fOutName}")
        else:
            subprocess.getstatusoutput(f'rm {fOutName}')

    else:
        if os.path.exists(local_dir):
            print(f"Please remove test dir {local_dir}")
            quit()
        os.makedirs(local_dir)
        out_dir = local_dir
        submit_script = make(1111111111, local_dir)
        os.system('cd %s && %s'%(local_dir, submit_script))
        
        # extract cross-section
        os.system(f'cat {local_dir}/job_1111111111/{args.generator}.log | grep "| Time estimate for generating" -B 3')
