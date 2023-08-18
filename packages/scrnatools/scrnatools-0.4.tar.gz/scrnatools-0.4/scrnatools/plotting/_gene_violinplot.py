"""
Plots violinplot subplots of expression of genes
From scrnatools package

Created on Wed March 29 17:28:15 2023

@author: joe germino (joe.germino@ucsf.edu), nolan horner (nolan.horner@ucsf.edu)
"""
# external package imports
from anndata import AnnData
from typing import List, Optional, Tuple
import seaborn as sns
import matplotlib.pyplot as plt
import math
import scrnatools

# scrnatools package imports
from .._configs import configs
from .._utils import debug, check_path

logger = configs.create_logger(__name__.split('_', 1)[1])

# -------------------------------------------------------function----------------------------------------------------- #

@debug(logger, configs)
def gene_violinplot(
    adata: AnnData,
    gene_list: List[str],
    x_key: str,
    layer: str = "X",
    x_values: List[str] = ['All'],
    hue_key: Optional[str] = None,
    hue_values: List[str] = ['All'],
    ncols: Optional[int] = None,
    nrows: Optional[int] = None,
    save_path: str = None,
    dpi: int = 300,
    fig_size: Tuple[float] = (0.5, 2.5),
    *args, **kwargs
):
    """
    Plots violinplot subplots of expression of genes
    Parameters
    ----------
    adata
        The AnnData containing the gene expression and cell data.
    gene_list
        A list of genes to plot. Each gene will create a violinplot.
    x_key
        The categorical grouping to display on the x axis of the violinplot.
    layer
        The type of the expression data to use for the violinplot, can be a layer in 'adata.layers' or 'X'
        to use the data stored in adata.X. Default 'X'.
    x_values
        Values from x key group to display on violinplot. Default displays all values in x key.
    hue_key
        The categorical grouping to color the grouped violin plots by. Values will appear in legend. Default None.
    hue_values
        Values from hue_key to display on violinplot. Default displays all values in hue key.
    ncols
        Number of columns to display the violinplots.
    nrows
        Number of rows to display the violinplots.
    save_path
        The path to save the figure. Default None.
    dpi
        The resolution of the saved image. Default 300.
    fig_size
        The scaling factors for the column and row size in the figure. Defaults to (0.5, 2.5)

    Raises
    -------
    ValueError
        If a gene in 'gene_list' provided is not in provided AnnData layer
    ValueError
        If the 'x_values' provided less than 2.
    ValueError
        If the 'hue_values' is provided but hue_key is not provided.
    ValueError
        If the 'hue_values' provided less than 2 if hue_key is also provided.
    ValueError
        If ncols * nrows is less than length of gene list provided.
    ValueError
        If a value in 'x_values' provided is not in AnnData layer x key.
    ValueError
        If a value in 'hue_values' provided is not in AnnData layer hue key given hue key is also provided.
    """
    #check inputs
    invalid_genes = [i for i in gene_list if i not in adata.var_names]
    if len(invalid_genes) > 0:
        raise ValueError(f"Genes not found in data: {invalid_genes}")
    if len(x_values) < 2 and x_values != ['All']:
        raise ValueError(f"Please choose more than one x value. Or use '[All]' to see all {x_key}s")
    if hue_key is None:
        if hue_values != ['All']:
            raise ValueError(f"Please enter a hue_key.")
    else:
        if len(hue_values) < 2 and hue_values != ['All']:
            raise ValueError(f"Please choose more than one hue value. Or use '[All]' to see all {hue_key}s")
    if x_values == ['All']:
        x_values = adata.obs[x_key].unique()
    if hue_values == ['All'] and hue_key != None:
        hue_values = adata.obs[hue_key].unique()

    #format figure
    max_input_len = max(len(x_values), len(hue_values))
    min_input_len = min(len(hue_values), len(x_values))
    if (ncols is None) & (nrows is None):
        if max_input_len > 5:
            ncols = 1
            nrows = len(gene_list)
        elif max_input_len > 2:
            if min_input_len <= 2:
                ncols = 3
            else:
                ncols = 2
        else:
            if min_input_len <= 2:
                ncols = 5
            else:  
                ncols = 3
        nrows = int((len(gene_list) / ncols)) + 1 if (len(gene_list) % ncols) > 0 else int((len(gene_list) / ncols))
    elif (ncols is None) & (nrows is not None):
        ncols = int(len(gene_list) / nrows) + 1 if (len(gene_list) % nrows) > 0 else int((len(gene_list) / nrows))
    elif (nrows is None) & (ncols is not None):
        nrows = int((len(gene_list) / ncols)) + 1 if (len(gene_list) % ncols) > 0 else int((len(gene_list) / ncols))

    if ncols * nrows < len(gene_list):
            raise ValueError("Number of rows and columns must fit number of genes in gene list (nrows * ncols >= length of gene list).")
    
    fig=plt.figure(figsize=(ncols*len(x_values)*max(2, len(hue_values))*fig_size[0], nrows*fig_size[1]))    
    
    #subset data on x values and hue values -> expression matrix
    if hue_key is None:
        subsetAdata = adata[adata.obs[x_key].isin(x_values), gene_list]
    else:
        subsetAdata = adata[adata.obs[x_key].isin(x_values) & adata.obs[hue_key].isin(hue_values), gene_list]
    expression_matrix = scrnatools.tl.get_expression_matrix(subsetAdata, gene_data = layer)
    
    expression_matrix[x_key] = subsetAdata.obs[x_key]
    if hue_key != None:
        expression_matrix[hue_key] = subsetAdata.obs[hue_key]
    
    #check inputted x values and hue values are in subsetted data
    for i in x_values:
        if i not in list(expression_matrix[x_key].unique()):
            raise ValueError(f"{i} is not in adata's x_key {x_key}.\nPossible {x_key}s: {list(adata.obs[x_key].unique())}")
    if hue_key != None:
        for i in hue_values:
            if i not in list(expression_matrix[hue_key].unique()):
                raise ValueError(f"{i} is not in adata's hue_key {hue_key}.\nPossible {hue_key}s: {list(adata.obs[hue_key].unique())}")

    #generate violin plots
    for plt_num, gene in enumerate(gene_list):
        plt.subplot(nrows, ncols, plt_num + 1)
        ax = sns.violinplot(
            expression_matrix,
            x=x_key,
            y=gene,
            hue=hue_key,
            scale='width',
            width = 0.9,
            order=x_values,
            hue_order=hue_values,
            *args, **kwargs
        )
        if hue_key is not None:
            if (plt_num > 0):
                plt.legend([],[], frameon=False)
            else:
                plt.legend(loc='upper right')
        plt.xticks(rotation=90)
        ax.grid(False)
        ax.set(xlabel=None)
        ax.set_title(f"{gene}")
    sns.set_theme(context="paper", style="white")
    fig.tight_layout()
    if save_path is not None:
        if "/" not in save_path:
            save_path = f"./{save_path}"
        check_path(save_path.rsplit("/", 1)[0])
        logger.info(f"Saving figure to {save_path}")
        plt.savefig(save_path, dpi=dpi, facecolor="white",)
    plt.show()
