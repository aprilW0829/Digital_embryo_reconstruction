### 经每个重构胚胎的初步分析，发现那一些胚胎的切片在贴到测序的panel时，方向贴反了，需要人为对这些进行调整


# Need to adjust of E8.5' single slices
import scanpy as sc
import numpy as np
import pandas as pd

# Done:
# E7.0-3:S14
# E7.0-4:S14
# E7.5-1:S21
# E7.5-2:S20
# E8.5:S47, S63, S72, S95, S124, S125
# Undone:

dir = '/data5/wangxin/20250701_digi_embryo/output/spateo/preprocess/Cellseg_QC_h5ad/'
#files = ['A05873A2_E8.5_S47_r1_QC.h5ad','A05875E2_E8.5_S63_r1_QC.h5ad','A05863G5_E8.5_S72_r1_QC.h5ad','A05865A2_E8.5_S124_r1_QC.h5ad','A05865A2_E8.5_S125_r1_QC.h5ad']
#files = ['A05863E5_E8.5_S98_r1_QC.h5ad']
#files = ['A05863E3_E7.5-1_S21_r1_QC.h5ad','A05863E3_E7.5-2_S20_r1_QC.h5ad']
files = ['D05422D1_E7.0-3_S14_r1_QC.h5ad', 'D05422D1_E7.0-4_S14_r1_QC.h5ad']

for i in range(0, len(files)):
    adata = sc.read(dir+files[i])
    print(adata.obsm['spatial'])

    # 仅仅翻转y轴坐标
    coordinates = adata.obsm['spatial']
    #spatial_loc[0] = -spatial_loc[0]
    #spatial_loc[1] = -spatial_loc[1]
    y_min = coordinates[:, 1].min()
    y_max = coordinates[:, 1].max()
    y_median = (y_min + y_max)/2
    coordinates_flipped = np.copy(coordinates)
    coordinates_flipped[:, 1] = 2 * y_median - coordinates[:, 1]

    #print(coordinates_flipped.head())
    adata.obsm['spatial'] = coordinates_flipped
    print(adata.obsm['spatial'])

    adata.write(dir+files[i])
    print('Get '+files[i]+' mirror, done!')
