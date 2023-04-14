! 1) Settings that will be used in a main program.
Main:numberOfEvents = N_EVENTS     ! number of events to generate
Main:timesAllowErrors = 100        ! abort run after this many flawed events
#Random:seed = 1234                ! initialize random generator with a seed

! 2) Settings related to output in init(), next() and stat() functions.
Init:showChangedSettings = on      ! list changed settings
Init:showAllSettings = off         ! list all settings
Init:showChangedParticleData = on  ! list changed particle data
Init:showAllParticleData = off     ! list all particle data
Next:numberCount = 10              ! print message every n events
Next:numberShowLHA = 1             ! print LHA information n times
Next:numberShowInfo = 1            ! print event information n times
Next:numberShowProcess = 1         ! print process record n times
Next:numberShowEvent = 1           ! print event record n times
Stat:showPartonLevel = off         ! additional statistics on MPI

! 3) Tell Pythia that LHEF input is used
Beams:frameType             = 4
Beams:setProductionScalesFromLHEF = off

Beams:allowMomentumSpread  = off

! Vertex smearing :
Beams:allowVertexSpread = on
Beams:sigmaVertexX = 0.0098 
Beams:sigmaVertexY = 2.54e-5 
Beams:sigmaVertexZ = 0.646     
Beams:sigmaTime = 4.227    !  14.1 ps

! 4) Settings for the event generation process in the Pythia8 library.
PartonLevel:ISR = off               ! initial-state radiation
PartonLevel:FSR = off               ! final-state radiation

Check:epTolErr = 1   
Check:mTolErr = 1   ! necessary for xing
LesHouches:matchInOut = off

