### 使用测序下机的原始gem进行后期初步分析发现，位置与转录组对不上，后发现可能spateo进行图像的坐标和gem的坐标不是一个方向，故对gem中的xy进行调整使其可以对齐


import math
import pandas as pd
import os


directory = '/data5/wangxin/20250701_digi_embryo/raw_data/01.Data/02.intronic_raw_gem/'
dir = '/data5/wangxin/20250701_digi_embryo/raw_data/01.Data/02.intronic_raw_gem_revise/'
#samples = ['E7.5-2_A05863E3.intronic.raw.gem']
#string = 'E7.5-2_A05863E3.intronic.raw'

def list_files(directory):
    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))  and f.startswith('E6.0')]

files = list_files(directory)
print(files)

#files = ['E7.5-3_A05865C1.intronic.raw.gem','E7.5-4_A05865D4.intronic.raw.gem']
#files = ['Y01047C2.intronic.raw.gem','Y01070C5.intronic.raw.gem','Y01070G7.intronic.raw.gem']

for i in range(0, len(files)):

    gem = pd.read_csv(directory + files[i], header=0, sep='\t')
    print(gem)
    angle = -90
    gem1 = gem
    gem1['coor_x'] = gem1['y']
    gem1['coor_y'] = gem1['x']
    gem1['x'] = gem1['coor_x']
    gem1['y'] = gem1['coor_y']
    #gem1 = gem1[['geneName', 'geneID', 'x', 'y', 'MIDCounts', 'EXONIC', 'INTRONIC', 'coor_x', 'coor_y']]
    #gem1 = gem1[['geneName', 'geneID', 'x', 'y', 'MIDCount', 'ExonCount', 'coor_x', 'coor_y']]
    gem1.columns = ['geneName', 'geneID', 'x', 'y', 'MIDCounts', 'EXONIC', 'INTRONIC', 'coor_x', 'coor_y']
    print(gem1)
    
    gem1.to_csv(dir + files[i].strip('.gem') + '_r1.gem', sep='\t', index=False)
