import pandas as pd
import numpy as np
import pickle
import os
import pkg_resources


def GEMAP(GF=None):
	################ gene name and Ids
	data_path = pkg_resources.resource_filename('GEMAP', 'data/allGenesWithIds.csv')
	allGenes=pd.read_csv(data_path,sep=";")

	print('allGenes.shape ',allGenes.shape)
	ginfo=pd.DataFrame()
	ginfo['id']=allGenes['ensembl_gene_id']
	ginfo['symbol']=allGenes['hgnc_symbol']
	print('ginfo.shape',ginfo.shape)
	geneIds={}
	idGenes={}
	for ii in range(ginfo.shape[0]):
    		idGenes[ginfo.loc[ii,'id']]=ginfo.loc[ii,'symbol']
    		geneIds[ginfo.loc[ii,'symbol']]=ginfo.loc[ii,'id']
	print('geneIds length ',len(geneIds))
	print('idGenes length ',len(idGenes))
	ids=np.unique(list(idGenes.values()))

	############### Input file
	genes=pd.read_excel(GF)
	genes=genes.T
	genes.columns=genes.loc['Unnamed: 0',]
	genes=genes.drop('Unnamed: 0',axis=0)
	genes.index=genes.loc[:,'Genes']
	genes=genes.drop('Genes',axis=1)
	print('genes.shape ',genes.shape)
	
	################# common genes and selected genes
	commonGenes=list(set(genes.columns).intersection(geneIds))
	genes=genes.loc[:,commonGenes]
	genes.columns=[geneIds[i] for i in genes.columns]

	data_path = pkg_resources.resource_filename('GEMAP', 'data/df_3_SS_he_uniform_relu_mae_adam_1_64_1024.pkl')
	file = open(data_path,'rb')
	dd5=pickle.load(file)
	file.close()

	HVG=dd5["fs"]
	genes=genes.loc[:,HVG]
	print('genes.shape ',genes.shape)

	################# DL models
	norm=dd5["norm"]
	model=dd5["model"]
	cellLines=genes.index
	genes=norm.transform(genes)
	metabolites=model.predict(genes)
	metabolites=pd.DataFrame(metabolites)
	metabolites.columns=metabolites.columns+1
	metabolites.index=cellLines
	print(metabolites.head)
	splitStr=GF.split("/")
	root=""
	for i in splitStr[:-1]:
		root=root+i+'/'
	root=root+'metabolites.csv'
	metabolites.to_csv(root)
	print("Metabolomics data saved as: " + root)
	
	################# returning data
	return metabolites