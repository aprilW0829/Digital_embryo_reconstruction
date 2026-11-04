### 基于Spateo进行细胞核分割，扩展细胞质，计算每个胚胎切片的表达矩阵到h5ad


import spateo as st
import matplotlib.pyplot as plt
import skimage
import os
import anndata as ad
import time
import itertools
import sys



def cellbin_spateo(gem_path, ssDNA_path, save_cellseg_pdf_path, save_cellseg_h5ad_path, name):

    adata = st.io.read_bgi_agg(
        gem_path, ssDNA_path,
    )
    #name = ssDNA_path.split('/')[-1].split('_ssDNA_regist_gray.tif')[0]  # SN_slice

    ## 01 stain mask
    st.cs.mask_nuclei_from_stain(adata)
    st.pl.imshow(adata, 'stain_mask', save_show_or_return = 'save', save_kwargs={'path':save_cellseg_pdf_path + '01.stain_mask_' + name})
    
    ## 02 watershed_labels
    st.cs.find_peaks_from_mask(adata, 'stain', 7)
    st.cs.watershed(adata, 'stain', 5, out_layer='watershed_labels')
    fig, ax = st.pl.imshow(adata, 'stain', save_show_or_return='return')
    st.pl.imshow(adata, 'watershed_labels', labels=True, alpha=0.5, ax=ax, save_show_or_return='save', save_kwargs={'path':save_cellseg_pdf_path + '02.watershed_labels_' + name})
    #adata.write(save_path + '02.watershed_labeled_adata_' + name + '.h5ad')
     
    ## 03 expand_labels to mitigate the effects of RNA diffusion
    st.cs.expand_labels(adata, 'watershed_labels', distance=7, out_layer='cell_labels_expanded')
    #st.cs.expand_labels(adata, 'cell_labels', distance=2, out_layer='cell_labels_expanded')
    fig, ax = st.pl.imshow(adata, 'stain', save_show_or_return='return')
    st.pl.imshow(adata, 'cell_labels_expanded', labels=True, alpha=0.5, ax=ax, save_show_or_return='save', save_kwargs={'path':save_cellseg_pdf_path + '06.expanded_labels_' + name})
    print('06 exxpand labels to mitigate the effectes of RNA diffusion, done!')
    
    #print(adata.uns['__type'])
    #adata.uns['__type']='UMI'
    print(adata.uns['__type'])
    ## labels data
    #adata.write(save_cellseg_h5ad_path + '06.final_labeled_adata_' + name + '.h5ad')
    print('Get 06.final_labels_adata,done!')


    ## final adata
    cell_adata = st.io.read_bgi(
        gem_path,
        segmentation_adata=adata,
        labels_layer='cell_labels_expanded',
    )
    #data.uns['__type']='UMI'
    cell_adata.write(save_cellseg_h5ad_path + 'final_adata_' + name + '.h5ad')
    
    '''
    fig, ax=plt.subplots(figsize=[4,4])
    st.pl.space(adata, color='area',show_legend='upper left')
    plt.savefig(save_cellseg_pdf_path + name + '_Spateo_cellseg_result.png', dpi=200, bbox_inches='tight')
    '''
    print('successfully for spateo cell segmentation analysis of '+name+' ,done!')
    return 0


#ssDNA_path='/disk1/ioz10/digi_embryo/test_data/spateo/SS200000135IL-D1.ssDNA.tif'
#gem_path='/disk1/ioz10/digi_embryo/test_data/spateo/SS200000135TL_D1_all_bin1.txt.gz'
#save_path='/disk1/ioz10/digi_embryo/test_data/spateo/output/'
gem_path = sys.argv[1]
ssDNA_path = sys.argv[2]
save_cellseg_pdf_path = sys.argv[3]
save_cellseg_h5ad_path = sys.argv[4]
name = sys.argv[5]

cellbin_spateo(gem_path, ssDNA_path, save_cellseg_pdf_path, save_cellseg_h5ad_path, name)
