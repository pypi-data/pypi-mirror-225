# GEMAP Package

The rapid evolution of technology has equipped researchers with the means to estimate metabolite abundance, thereby unlocking potential paths to understand their critical roles in cellular processes, including intercellular communication. Despite this progress, a need remains for enhanced methodologies capable of accurately quantifying all metabolites within a single cell due to the vast metabolomic diversity present. The dataset provided by Sarah et al., which encompasses 180 pan-cancer cell lines, each with six replicates, offers information on the abundance of a limited set of 1809 metabolites. Simultaneously, RNA-based Next-generation sequencing (NGS) techniques enable the profiling of hundreds of thousands of cells in one run. This juxtaposition raises a crucial question: Can gene expressions serve as reliable predictors for metabolite abundance? Given the limited metabolite data available for the 180 cell lines and our understanding of metabolic reactions, this study proposes a regression-based analysis with the objective of formulating a regression model predicated on gene expression data to predict metabolite abundance. This study scrutinizes the correlation between gene expressions and the roles of enzymes in substrate and product formation, aspiring to reveal the predictive capability of gene expressions in determining metabolite abundance. Collectively, this research aims to bridge the gap between gene expressions and metabolite abundance, highlighting the potential of gene expression data in predicting metabolite levels.

# Instructions

## How to install?
1. These are are required packages: 
   
	numpy, pandas, pickle, os, pkg_resources

2. To install these packages use below command
   	
	!pip install numpy, pandas, pickle, os, pkg_resources

3. Updates for GEMAP can be checked at the provided link:
   	
	https://pypi.org/project/TAMAP

4. Or install it using below command.
   	
	pip install GEMAP

## How to use?
1. Please ensure that the gene expression file is in the following format: 
  
  - Rows represent gene symbols.
  
  - Columns represent cell names.
  
  - The file is saved with a .xlsx extension.

2. from GEMAP import GEMAP
   
  - GEMAP("gene expression file name with absolute address") 
   
  - For example: 

    - from GEMAP import GEMAP
   
    - metaboplites=GEMAP("/Users/kris/Desktop/NIHMS1530136Simple.xlsx")
   
    - print(metaboplites.head)
   
  - For testing purposes, the GEMAP package includes a gene expression file. To use this file, follow the steps below:
   
    - Refernce for the file: https://doi.org/10.1158/0008-5472.CAN-18-2047
    
    - import pkg_resources
  
    - data_path = pkg_resources.resource_filename('GEMAP', 'data/NIHMS1530136Simple.xlsx')
    
    - from GEMAP import GEMAP

    - metaboplites=GEMAP(data_path)

3. The output data will represent metabolite abundance, where columns contain peak IDs and row names contain cell names.

  - Peak IDs refer to untargeted metabolites. Further information about each peak ID, including associated HMDB IDs, is provided below:
  
    - Refernce for the file: https://doi.org/10.15252/msb.202211033
  
    - import pkg_resources
  
    - data_path = pkg_resources.resource_filename('GEMAP', 'data/peakID_info.csv')
    
    - import pandas as pd
    
    - pd.read_csv(data_path)
    
    - In the peakID_info.csv file, the column 'ionIdx' corresponds to peak IDs.

