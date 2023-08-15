import pandas as pd
import numpy as np

from iotbr import tru as tru

from importlib import resources
import io

#ben_to_tru51_products
#ben_to_tru51_products = pd.read_csv('https://raw.githubusercontent.com/fms-1988/datas/main/correspondencia_produtos_TRU51_BEN.csv',sep=';')
with resources.open_binary('BenToTru.data', 'correspondencia_produtos_TRU51_BEN.csv') as f:
  data_ = f.read()
  bytes_io = io.BytesIO(data_)
ben_to_tru51_products = pd.read_csv(bytes_io, sep=';')
ben_to_tru51_products = ben_to_tru51_products[ben_to_tru51_products['produto_TRU51'] != 'nc'].reset_index(drop=True)

#ben_to_tru51_sectors
#ben_to_tru51_sectors = pd.read_csv('https://raw.githubusercontent.com/fms-1988/datas/main/correspondencia_MIP56_TRU51_BEN.csv')
with resources.open_binary('BenToTru.data', 'correspondencia_MIP56_TRU51_BEN.csv') as f:
  data_ = f.read()
  bytes_io = io.BytesIO(data_)
ben_to_tru51_sectors = pd.read_csv(bytes_io)

#coef_tep_to_ghg
#coef_tep_to_ghg = pd.read_csv('https://raw.githubusercontent.com/fms-1988/datas/main/coeficientes_emissoes_gee_ajustado.csv')
with resources.open_binary('BenToTru.data', 'coeficientes_emissoes_gee_ajustado.csv') as f:
  data_ = f.read()
  bytes_io = io.BytesIO(data_)
coef_tep_to_ghg = pd.read_csv(bytes_io)
#não existe coeficiente de emissões para o produto "ELETRICIDADE". Então eu considerei os mesmos coeficientes do produto "GÁS DE CIDADE E DE COQUERIA". O ideal é excluir esse bem da análise
coef_tep_to_ghg = coef_tep_to_ghg.iloc[:,[0]+[1]+[2]+[3]+[5]+[6]+[7]+[8]+[9]+[10]+[11]+[12]+[13]+[14]+[13]+[15]+[16]+[17]+[18]]


def reorder_df(df_):
  #correct order of rows on tru51
  ar1 = [ 0,  1,  2,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15,  3,  4, 16, 17,\
         18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34,\
          5, 35, 36, 47, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 48, 49, 50]
  return df_.iloc[ar1,:]

def map_ben_to_tru51(matrix,sector_ben_index,product_ben_index):
  sector_ben = ben_to_tru51_sectors['descricao_atividades_ben2'].unique()[sector_ben_index]
  sectors_tru51 = ben_to_tru51_sectors[ben_to_tru51_sectors['descricao_atividades_ben2'] == sector_ben]['setor_tru51']
  product_ben = matrix.columns[product_ben_index]
  return pd.DataFrame(matrix.iloc[sectors_tru51-1,product_ben_index]), sector_ben, product_ben

class system:
    def __init__(self, year: str, level: str, unit: str, gas: str,household=False):
        self.Y = year
        self.L = level
        self.u = unit
        self.gas = gas
        self.household = household
        #self.num_sectors = 14
        #self.NUM_PRODUCTS = 17
        self.import_data_ben()
        self.import_data_tru()
        self.estimation()
    def import_data_ben(self):
      #import and adjust matrix ben to 22 sectors
      #ben = pd.read_excel('https://github.com/fms-1988/datas/raw/main/Matrizes%20Consolidadas%20(em%20tep)%201970%20-%202022.xls', sheet_name=self.Y)
      with resources.open_binary('BenToTru.data','Matrizes Consolidadas (em tep) 1970 - 2022.xls') as f:
        data = f.read()
        bytes_io = io.BytesIO(data)
      ben = pd.read_excel(bytes_io, sheet_name=self.Y)        
      ben = ben.iloc[:, 1:]
      ben = ben.iloc[[11] + [33] + list(range(35, 40)) + list(range(41, 45)) + list(range(46, 58))]
      ben = ben.set_axis(ben.iloc[0], axis=1)
      ben = ben[1:].reset_index(drop=True)
      ben = ben.set_axis(ben.iloc[:,0], axis=0)
      ben = ben.iloc[:,1:-1]
      ben.rename_axis(index='setor', columns='produto', inplace=True)
      ben.columns = ben.columns.str.strip()
      ben.index = ben.index.str.strip()
      ben.columns = ben.columns.str.replace('ÓLEO COMBUSTIVEL', 'ÓLEO COMBUSTÍVEL') #before 2004 this name was writteng wrong
      ben.columns = ben.columns.str.replace('GÁS DE COQUERIA','GÁS DE CIDADE E DE COQUERIA') #this name was written wrong in 2004
      ben = ben.drop(['CONSUMO FINAL NÃO-ENERGÉTICO', 'CONSUMO NÃO-IDENTIFICADO'])
      ben_emission = ben.iloc[:,ben_to_tru51_products['produto_BEN_num'].astype(float)] #ben products that generate emissions
    def import_data_tru(self):
      tru51_CI = tru.read_var(self.Y,self.L,'CI_matrix',self.u).T
      tru51_CI_energy = tru51_CI.iloc[:,ben_to_tru51_products['produto_TRU51_num'].values]
    def estimation(self):
      num_sectors = 14
      coef1 = pd.DataFrame() #coefficint of distribution (value to tep)
      coef2 = pd.DataFrame() #coefficient of emission (tep to ghg)
      tep = pd.DataFrame()
      emission = pd.DataFrame()

      ben_ = ben_to_tru51_sectors['descricao_atividades_ben2'].unique() #sector ben (j)
      for j in range(num_sectors):
        #corespondent rows of tru matrix to sector (j)
        tru_j_num = ben_to_tru51_sectors[ben_to_tru51_sectors['descricao_atividades_ben2'] == ben_[j]]['setor_tru51']

        #estimate coeficient of distribution
        tru_j = tru51_CI_energy.iloc[tru_j_num-1,:]
        X_j = pd.DataFrame(tru_j.sum(axis=0))
        diag_X_j = np.diag(X_j[0].values)
        diag_X_j = diag_X_j.astype(float)
        inv_diag_X_j = np.linalg.pinv(diag_X_j)
        coef1_j = tru_j.values @ inv_diag_X_j
        coef1_j = pd.DataFrame(coef1_j, columns=ben_emission.columns, index= tru_j.index)


        #ajust columns without coeficients of distribution 
        total = coef1_j.sum().sum()
        totals = coef1_j.sum(axis=1)
        mean = totals / total
        for col in coef1_j.columns:
          if coef1_j[col].eq(0).all():
            coef1_j[col] = mean 

        coef1 = pd.concat([coef1,coef1_j], axis=0)

        #use coef1_j to distribute tep consumption
        tep_j = ben_emission[ben_emission.index.str.contains(ben_[j].replace(' + ', '|'))].sum(axis=0).values#.T
        diag_tep_j = np.diag(tep_j.T.flatten())
        tep_j = coef1_j.values @ diag_tep_j

        tep_j_df = pd.DataFrame(tep_j, columns=ben_emission.columns, index= tru_j.index)
        tep = pd.concat([tep,tep_j_df], axis=0)

        #coefficient of emission
        coef2_j = coef_tep_to_ghg[(coef_tep_to_ghg['setor'].str.contains(ben_[j].replace(' + ', '|'))) & (coef_tep_to_ghg['gas'].str.contains(self.gas))]
        coef2_j = pd.DataFrame(coef2_j.iloc[:,2:]) #exclude rows with unnecessary informations
        coef2_j_df = tep_j_df.copy()
        coef2_j_df.loc[:, :] = coef2_j.iloc[0].values
        coef2 = pd.concat([coef2,coef2_j_df], axis=0)

      #tep and coefficients by household
      tep_h = ben_emission[ben_emission.index.str.contains('RESIDENCIAL')]
      coef1_h = tep_h.copy()
      coef1_h = (coef1_h * 0) + 1
      coef2_h = coef_tep_to_ghg[(coef_tep_to_ghg['setor'].str.contains('RESIDENCIAL')) & (coef_tep_to_ghg['gas'].str.contains(self.gas))].iloc[:,2:]
      coef2_h.index = ['RESIDENCIAL']
      coef2_h.columns = coef2.columns #remembet that we assume that 'GÁS DE CIDADE E DE COQUERIA' = 'ELETRICIDADE'

      #agregate firms + household
      self.tep = reorder_df(pd.concat([tep,tep_h], axis=0))
      self.coef1 = reorder_df(pd.concat([coef1,coef1_h], axis=0))
      self.coef2 = reorder_df(pd.concat([coef2,coef2_h], axis=0))

      #emission
      self.emission =  self.tep * self.coef2









































