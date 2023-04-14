#---------------------------------------------------------------------------------------------------
# Python Module File to describe a dataset
#
# Author: C.Paus                                                                      (Apr 16, 2023)
#---------------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------------
"""
Class:  Dataset(campaign,detector,generator,card,txs,nevents)

    Each dataset is describe by the above parameters.
    
    As an example:
     - campaign - spring2023
     - detector - IDEA
     - generator - whizard
     - card - wzp6_ee_qq_ecm91p2
     - txs [nb] - total cross section
     - eff_lumi [/nb] - effective luminosity
     - nevents - number of events to produce
"""
#---------------------------------------------------------------------------------------------------
class Dataset:
    "Description of a dataset"

    #-----------------------------------------------------------------------------------------------
    # constructor for new dataset
    #-----------------------------------------------------------------------------------------------
    def __init__(self,campaign,detector,generator,card,txs,eff_lumi):
        self.campaign = campaign
        self.detector = detector
        self.generator = generator
        self.card = card
        self.txs = txs
        self.eff_lumi = eff_lumi
        self.nevents = int(self.eff_lumi*self.txs)

    def show(self):
        print(f" Campaign: {self.campaign}, Detector: {self.detector}, Generator: {self.generator}, Card: {self.card}, Txs [nb]: {self.txs}, eLumi [/nb]: {self.eff_lumi}, Nevts: {self.nevents}")
