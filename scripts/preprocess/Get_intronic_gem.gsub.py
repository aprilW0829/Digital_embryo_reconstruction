### 给测序下机输出的原始表达矩阵gem.gz文件添加INTRONIC列，方便后续做RNA速率分析

import pandas as pd
import os

# Y01047C2.raw.gem.gz  Y01070C5.raw.gem.gz  Y01070G7.raw.gem.gz
# E7.0-1_D05422D1.raw.gem.gz E7.0-2_D05419F6.raw.gem.gz 
#gem_path = '/data/input/Files/ResultData/Workflow/MouseEmbryo3D_E7.5_E8.5/E7.5-E8.5_gemFile_compressed/E7.5-1_A05875A1.raw.gem.gz'
#output_directory = '/data/work/01.Data/02.intronic_raw_gem'


gem_path = '/data5/wangxin/20250701_digi_embryo/raw_data/01.Data/04.raw_gem/E6.0_D05422C3.raw.gem.gz'
output_directory = '/data5/wangxin/20250701_digi_embryo/raw_data/01.Data/02.intronic_raw_gem'

# 提取文件名并替换后缀
file_name = os.path.basename(gem_path).replace('.raw.gem.gz', '.intronic.raw.gem.gz')
# 构造输出文件路径
output_file = os.path.join(output_directory, file_name)
print(output_file)

df = pd.read_csv(gem_path, sep='\t', comment='#')
df.head()

# caculate column "intronic"
df['INTRONIC'] = df.apply(lambda row: 0 if row['ExonCount']>0 else row['MIDCount'], axis=1)
df.head()

df.columns=['geneID','geneName','x','y','MIDCounts','EXONIC','INTRONIC']
df.head()

df.to_csv(output_file, sep='\t', index=False, compression='gzip')
