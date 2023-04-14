#!/usr/bin/env python

import sys
import os
import subprocess
import random
import config
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--champaign", type=str, help="Champaign", default='spring2023')
parser.add_argument("--detector", type=str, help="Detector", default='IDEA')
parser.add_argument("--generator", type=str, help="Generator", default='whizard')
parser.add_argument("--card", type=str, help="Card", default='wzp6_ee_qq_ecm91p2')
parser.add_argument("--nevents", type=int, help="Nevents", default=10)
args = parser.parse_args()

######################################################
### CONFIG
######################################################
#tag = "winter2023" # corresponds to detector configuration

nevents = args.nevents
njobs = 1         # -1 means to run locally (dry run)

######################################################
cwd = os.getcwd()
stack = config.stacks[args.champaign]
priority = 'group_u_FCC.local_gen'
queue = "workday" # espresso microcentury longlunch workday tomorrow testmatch nextweek


whizard_card_def = f"./cards/{args.champaign}/generator/whizard/{args.card}.sin"
delphes_card = f"./cards/{args.champaign}/delphes/card_{args.detector}.tcl"
delphes_cfg_card = f"./cards/{args.champaign}/delphes/edm4hep_{args.detector}.tcl"

name = f"{args.card}"
submit_dir = f"{cwd}/submit/{args.champaign}/{args.card}/"
#out_dir = f"/eos/experiment/fcc/users/j/jaeyserm/sampleProduction/{args.champaign}/{args.card}/"
out_dir = f"/data/submit/cms/store/fccee/{args.champaign}/{args.detector}/{args.card}/"
local_dir = f"{cwd}/local/{args.champaign}/{args.detector}/{args.card}/"

def make(seed, savedir):
    # make a job file that when executed generates the events
    
    fOutName = f"{savedir}/submit_{seed}.sh"
    if os.path.exists(fOutName):
        return -1
    rootOutName = f"events_{seed}.root"
    if os.path.exists(f"{out_dir}/{rootOutName}"):
        return -1
    
    fOut = open(fOutName, 'w')

    fOut.write('#!/bin/bash\n')
    fOut.write('SECONDS=0\n')
    fOut.write('unset LD_LIBRARY_PATH\n')
    fOut.write('unset PYTHONHOME\n')
    fOut.write('unset PYTHONPATH\n')
    fOut.write('mkdir job_%s\n'%seed)
    fOut.write('cd job_%s\n'%seed)
    fOut.write('source %s\n'%stack)

    fOut.write('tar fzx ../cards.tgz\n')
    fOut.write('cp %s thecard.sin\n'%(whizard_card_def))
    fOut.write('cp %s card.tcl\n'%delphes_card)
    fOut.write('cp %s edm4hep_output_config.tcl\n'%delphes_cfg_card)

    fOut.write('echo "Run Whizard"\n')
    fOut.write('echo "n_events = %i" > header.sin \n'%nevents)
    fOut.write('echo "seed = %s"  >> header.sin \n'%seed)
    fOut.write('cat header.sin thecard.sin > card.sin \n') 
    fOut.write('whizard card.sin \n')
    fOut.write('pwd; ls -lhrt \n')
    fOut.write('echo "finished run"\n')
    
    fOut.write('echo "Run DelphesSTDHEP_EDM4HEP"\n')
    fOut.write('DelphesSTDHEP_EDM4HEP card.tcl edm4hep_output_config.tcl %s proc.stdhep \n'%rootOutName)
    fOut.write('pwd; ls -lhrt \n')
    fOut.write('echo "DONE"\n')
    
    fOut.write('echo "Copy file (%s,%s)"\n'%(rootOutName,out_dir))
    fOut.write('#cp %s %s/\n'%(rootOutName,out_dir))
    fOut.write('source /cvmfs/grid.cern.ch/centos7-ui-4.0.3-1_umd4v3/etc/profile.d/setup-c7-ui-example.sh\n')
    fOut.write(f'echo gfal-copy -p file:///$PWD/{rootOutName} root://submit50.mit.edu//store/user/paus{out_dir.replace("/data/submit/cms/store","")}{rootOutName}\n')
    fOut.write(f'gfal-copy -p file:///$PWD/{rootOutName} root://submit50.mit.edu//store/user/paus{out_dir.replace("/data/submit/cms/store","")}{rootOutName}\n')
    fOut.write('duration=$SECONDS\n')
    fOut.write('echo "Duration: $(($duration))"\n')
    fOut.write('echo "Events: %d"\n'%nevents)
            
    subprocess.getstatusoutput('chmod 777 %s'%fOutName)
    subprocess.getstatusoutput('cp ./cards.tgz %s'%(savedir))

    return fOutName

if __name__=="__main__":

    if njobs == -1:
        if os.path.exists(local_dir):
            print(f"Please remove test dir {local_dir}")
            quit()
        os.makedirs(local_dir)
        out_dir = local_dir
        sh = make(1111111111, local_dir)
        os.system('cd %s && %s'%(local_dir, sh))
        
        # extract cross-section
        os.system('cat %s/job_1111111111/whizard.log | grep "| Time estimate for generating" -B 3'%local_dir)
    else:
        if not os.path.exists(submit_dir):
            os.makedirs(submit_dir)
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
    
        execs = []
        njob = 0
        while njob < njobs:
            seed = f"{random.randint(1000000000,9999999999)}"
            sh = make(seed, submit_dir)
            if sh == -1:
                continue
            njob += 1
            print(f"Prepare job {njob} with seed {seed}")
            execs.append(sh)
            
        fOutName = f'{submit_dir}/condor.cfg'
        fOut = open(fOutName, 'w')

        fOut.write(f'executable           = $(filename)\n')
        fOut.write(f'transfer_input_files = {submit_dir}/cards.tgz\n')
        fOut.write(f'Log                  = {submit_dir}/condor_job.$(ClusterId).$(ProcId).log\n')
        fOut.write(f'Output               = {submit_dir}/condor_job.$(ClusterId).$(ProcId).out\n')
        fOut.write(f'Error                = {submit_dir}/condor_job.$(ClusterId).$(ProcId).error\n')
        fOut.write(f'getenv               = True\n')
        fOut.write(f'use_x509userproxy    = True\n')
        fOut.write(f'environment          = "LS_SUBCWD={submit_dir}"\n')
        #fOut.write(f'requirements         = ( (OpSysAndVer =?= "CentOS7") && (Machine =!= LastRemoteHost) && (TARGET.has_avx2 =?= True) )\n')
        fOut.write(f'requirements         = ( BOSCOCluster =!= "t3serv008.mit.edu" && BOSCOCluster =!= "ce03.cmsaf.mit.edu" && BOSCOCluster =!= "eofe8.mit.edu" )\n')
        fOut.write(f'+DESIRED_Sites       = "mit_tier3"\n')
        fOut.write(f'+SingularityImage    = "/cvmfs/singularity.opensciencegrid.org/opensciencegrid/osgvo-el7:latest"\n')
                                          
        fOut.write(f'on_exit_remove       = (ExitBySignal == False) && (ExitCode == 0)\n')
        fOut.write(f'max_retries          = 3\n')
        fOut.write(f'+JobFlavour          = "{queue}"\n')
        fOut.write(f'+AccountingGroup     = "{priority}"\n')
        
        execsStr = ' '.join(execs) 
        fOut.write(f'queue filename matching files {execsStr}\n')
        fOut.close()
        
        subprocess.getstatusoutput(f'chmod 777 {fOutName}')
        os.system(f"condor_submit {fOutName}")
