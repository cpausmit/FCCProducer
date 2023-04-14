#!/bin/bash

echo " Job: $0"
echo " Arguments: $@"

echo "START "`date +%s`

CAMPAIGN=$1
GENERATOR=$2
DETECTOR=$3
CARD=$4
JOBID=$5
SEED=$6
NEVTS=$7

ROOT_OUT=${JOBID}_${SEED}_${NEVTS}.root
OUT_DIR=/store/fccee/$CHAMPAIGN/$GENERATOR/$DETECTOR/$CARD
SECONDS=0
unset LD_LIBRARY_PATH
unset PYTHONHOME
unset PYTHONPATH

mkdir $SEED
cd $SEED

source /cvmfs/sw.hsf.org/spackages6/key4hep-stack/2022-12-23/x86_64-centos7-gcc11.2.0-opt/ll3gi/setup.sh
tar fzx ../cards.tgz
cp ./cards/$CAMPAIGN/generator/$GENERATOR/$CARD.sin thecard.sin
cp ./cards/$CAMPAIGN/delphes/card_$DETECTOR.tcl card.tcl
cp ./cards/$CAMPAIGN/delphes/edm4hep_$DETECTOR.tcl edm4hep_output_config.tcl
echo "Run $GENERATOR"
echo "n_events = $NEVTS" > header.sin 
echo "seed = $SEED"  >> header.sin 
cat header.sin thecard.sin > card.sin 
$GENERATOR card.sin 
echo "finished generator"
echo "END - GEN "`date +%s`
pwd; ls -lhrt 

echo "Run DelphesSTDHEP_EDM4HEP"
DelphesSTDHEP_EDM4HEP card.tcl edm4hep_output_config.tcl $ROOT_OUT proc.stdhep 
echo "finished simulation"
echo "END - SIM "`date +%s`
pwd; ls -lhrt 

echo "Copy file ($ROOT_OUT,$OUT_DIR)"
source /cvmfs/grid.cern.ch/centos7-ui-4.0.3-1_umd4v3/etc/profile.d/setup-c7-ui-example.sh
voms-proxy-info -all
echo gfal-copy -p file:///$PWD/$ROOT_OUT root://submit50.mit.edu/$OUT_DIR/$ROOT_OUT
gfal-copy -p file:///$PWD/$ROOT_OUT root://submit50.mit.edu/$OUT_DIR/$ROOT_OUT
echo "RC: $?"
duration=$SECONDS
echo "Duration: $(($duration))"
echo "Events: $NEVTS"

echo "END - JOB "`date +%s`
