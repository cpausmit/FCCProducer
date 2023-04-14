import os
import dataset

#datasets = [ 'wzp6_ee_qq_ecm91p2',
#             'wzp6_ee_mumu_ecm91p2',
#             'wzp6_ee_tautau_ecm91p',
#             'wzp6_ee_ee_Mee_5_150_ecm91p2',
#             'wzp6_gaga_mumu_5_ecm91p',
#             'wzp6_gaga_ee_5_ecm91p',
#         ]

#   7 TXS HADRON    ( 91.20000)=  30.4571012817   0.0000000000   2.6888061763
#   8 TXS MUON      ( 91.20000)=   1.4812689317   0.0000000000   0.1292285884
#   9 TXS TAU       ( 91.20000)=   1.4770162084   0.0000000000   0.1293724672

qq = dataset.Dataset('spring2023','IDEA','whizard','wzp6_ee_qq_ecm91p2',30.51,1.1e5)
mm = dataset.Dataset('spring2023','IDEA','whizard','wzp6_ee_mumu_ecm91p2',1.50,1.1e5)
tt = dataset.Dataset('spring2023','IDEA','whizard','wzp6_ee_tautau_ecm91p2',1.50,1.1e5)

datasets = [ qq, mm, tt ]

def submit(dataset):
    cmd = f"./python/run.py --campaign {dataset.campaign} --detector {dataset.detector} --generator {dataset.generator} --card {dataset.card} --nevents {dataset.nevents}"
    print(f" CMD: {cmd}")
    os.system(cmd)        
    return

for dataset in datasets:
    submit(dataset)
