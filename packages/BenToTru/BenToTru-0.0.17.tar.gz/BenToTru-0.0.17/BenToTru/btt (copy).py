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
    def __init__(self, year: str, level: str, unit: str, gas: str,household=False,exact_estimation=True):
        self.Y = year
        self.L = level
        self.u = unit
        self.gas = gas
        self.household = household
        self.exact_estimation = exact_estimation
        #self.num_sectors = 14
        #self.NUM_PRODUCTS = 17
        self.import_data_ben()
        self.import_data_tru()
        #self.estimation()
        if self.exact_estimation:
          self.exact_estimation_true()
        else:
          self.exact_estimation_false()
        self.verification()
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
      ben = ben.drop(['CONSUMO FINAL NÃO-ENERGÉTICO', 'CONSUMO NÃO-IDENTIFICADO']) #Consider only the sectors that have been identified as generating emissions.
      self.ben = ben
      #In 2005, Ben began reporting the product 'BIODIESEL'. This changed the column order of the products.
      if int(self.Y) >= 2005:
        self.ben_reduced = self.ben.iloc[:,ben_to_tru51_products['produto_BEN_num_after_2004'].astype(float)] #ben products that generate emissions
      else:
        self.ben_reduced = self.ben.iloc[:,ben_to_tru51_products['produto_BEN_num_before_2005'].astype(float)] #ben products that generate emissions
    def import_data_tru(self):
      #import values of intermediate consumption by economic sector (TRU51)
      #tru51 is updated untill 2020 and ben is updated untill 2023
      #if tru51 is not updated, than use the last value available (2020)
      try:
        tru51_CI = tru.read_var(self.Y,self.L,'CI_matrix',self.u).T
      except Exception as e:
        tru51_CI = tru.read_var('2020',self.L,'CI_matrix',self.u).T
      self.tru51_CI_energy = tru51_CI.iloc[:,ben_to_tru51_products['produto_TRU51_num'].values]

    def exact_estimation_false(self):
      num_sectors = 14
      coef1 = pd.DataFrame() #coefficint of distribution (value to tep)
      coef2 = pd.DataFrame() #coefficient of emission (tep to ghg)
      tep = pd.DataFrame()
      emission_tru = pd.DataFrame()

      ben_ = ben_to_tru51_sectors['descricao_atividades_ben2'].unique() #sector ben (j)
      for j in range(num_sectors):
        #corespondent rows of tru matrix to sector (j)
        tru_j_num = ben_to_tru51_sectors[ben_to_tru51_sectors['descricao_atividades_ben2'] == ben_[j]]['setor_tru51']

        #estimate coeficient of distribution
        tru_j = self.tru51_CI_energy.iloc[tru_j_num-1,:]
        X_j = pd.DataFrame(tru_j.sum(axis=0))
        diag_X_j = np.diag(X_j[0].values)
        diag_X_j = diag_X_j.astype(float)
        inv_diag_X_j = np.linalg.pinv(diag_X_j)
        coef1_j = tru_j.values @ inv_diag_X_j
        coef1_j = pd.DataFrame(coef1_j, columns=self.ben_reduced.columns, index= tru_j.index)


        #ajust columns without coeficients of distribution
        total = coef1_j.sum().sum()
        totals = coef1_j.sum(axis=1)
        mean = totals / total
        for col in coef1_j.columns:
          if coef1_j[col].eq(0).all():
            coef1_j[col] = mean

        coef1 = pd.concat([coef1,coef1_j], axis=0)

        #use coef1_j to distribute tep consumption
        tep_j = self.ben_reduced[self.ben_reduced.index.isin(ben_[j].split(' + '))].sum(axis=0).values#.T
        diag_tep_j = np.diag(tep_j.T.flatten())
        tep_j = coef1_j.values @ diag_tep_j

        tep_j_df = pd.DataFrame(tep_j, columns=self.ben_reduced.columns, index= tru_j.index)
        tep = pd.concat([tep,tep_j_df], axis=0)

        #coefficient of emission
        coef2_j = coef_tep_to_ghg[(coef_tep_to_ghg['setor'].isin(ben_[j].split(' + '))) & (coef_tep_to_ghg['gas'].str.contains(self.gas))]
        coef2_j = coef2_j.iloc[:,2:] #exclude rows with unnecessary informations
        coef2_j = pd.DataFrame(coef2_j.mean(axis=0)).T #estimate the mean of coeficients to convert tep to emission

        coef2_j_df = tep_j_df.copy()
        coef2_j_df.loc[:, :] = coef2_j.iloc[0].values
        coef2 = pd.concat([coef2,coef2_j_df], axis=0)

      #tep and coefficients by household
      tep_h = self.ben_reduced[self.ben_reduced.index.str.contains('RESIDENCIAL')]
      coef1_h = tep_h.copy()
      coef1_h = (coef1_h * 0) + 1
      coef2_h = coef_tep_to_ghg[(coef_tep_to_ghg['setor'].str.contains('RESIDENCIAL')) & (coef_tep_to_ghg['gas'].str.contains(self.gas))].iloc[:,2:]
      coef2_h.index = ['RESIDENCIAL']
      coef2_h.columns = coef2.columns #remember that we assume that 'GÁS DE CIDADE E DE COQUERIA' = 'ELETRICIDADE'

      #estimation_emission
      """
      This method makes adjustments to incorporate households into tables.
      Depending on the value of self.household, it aggregates firms and household data
      and calculates emissions.
      """
      # Depending on the value of self.household, reorder DataFrame or not
      if self.household:
          self.tep = pd.concat([reorder_df(tep), tep_h], axis=0)
          self.coef1 = pd.concat([reorder_df(coef1), coef1_h], axis=0)
          self.coef2 = pd.concat([reorder_df(coef2), coef2_h], axis=0)
      else:
          # Aggregate firms and household
          self.tep = reorder_df(tep)
          self.coef1 = reorder_df(coef1)
          self.coef2 = reorder_df(coef2)

      # Calculate emission
      self.emission_tru = self.tep * self.coef2

    def exact_estimation_true(self):
      num_sectors = 14
      coef1 = pd.DataFrame() #coefficint of distribution (value to tep)
      emission_ben = pd.DataFrame() #coefficient of emission (tep to ghg)
      emission_tru = pd.DataFrame()
      tep = pd.DataFrame()
      emission = pd.DataFrame()

      ben_ = ben_to_tru51_sectors['descricao_atividades_ben2'].unique() #sector ben (j)
      for j in range(num_sectors):
        #corespondent rows of tru matrix to sector (j)
        tru_j_num = ben_to_tru51_sectors[ben_to_tru51_sectors['descricao_atividades_ben2'] == ben_[j]]['setor_tru51']


        #tep of sector j
        tep_j = self.ben_reduced[self.ben_reduced.index.isin(ben_[j].split(' + '))]#.sum(axis=0).values#.T


        #emission coeficient of sector j
        coef2_j = coef_tep_to_ghg[(coef_tep_to_ghg['setor'].isin(ben_[j].split(' + '))) & (coef_tep_to_ghg['gas'].str.contains('CO2'))]
        coef2_j = pd.DataFrame(coef2_j.iloc[:,2:]) #exclude rows with unnecessary informations

        #emission of sector j (ben)
        emission_j_ben = tep_j.values * coef2_j.values #(sector1 , sector2, ...)
        emission_j_ben = emission_j_ben.sum(axis=0) #(sector1 + sector2 + ...)
        emission_j_ben = pd.DataFrame(emission_j_ben).T#, columns=sys.ben_reduced.columns)#, index= tep_j.index)
        emission_j_ben.columns = self.ben_reduced.columns
        emission_j_ben.index = [ben_[j]]
        emission_ben = pd.concat([emission_ben,emission_j_ben], axis=0)

        #estimate coeficient of distribution
        tru_j_num = ben_to_tru51_sectors[ben_to_tru51_sectors['descricao_atividades_ben2'] == ben_[j]]['setor_tru51']
        tru_j = self.tru51_CI_energy.iloc[tru_j_num-1,:]
        X_j = pd.DataFrame(tru_j.sum(axis=0))
        diag_X_j = np.diag(X_j[0].values)
        diag_X_j = diag_X_j.astype(float)
        inv_diag_X_j = np.linalg.pinv(diag_X_j)
        coef1_j = tru_j.values @ inv_diag_X_j
        coef1_j = pd.DataFrame(coef1_j, columns=self.ben_reduced.columns, index= tru_j.index)

        #ajust columns without coeficients of distribution
        total = coef1_j.sum().sum()
        totals = coef1_j.sum(axis=1)
        mean = totals / total
        for col in coef1_j.columns:
          if coef1_j[col].eq(0).all():
            coef1_j[col] = mean
        coef1 = pd.concat([coef1,coef1_j], axis=0)

        #emission of sector j (ben)
        emission_j_tru = coef1_j.values * emission_j_ben.values
        emission_j_tru = pd.DataFrame(emission_j_tru, columns=coef1_j.columns, index= coef1_j.index)
        emission_j_tru
        emission_tru = pd.concat([emission_tru,emission_j_tru], axis=0)

      #tep and coefficients by household
      tep_h = self.ben_reduced[self.ben_reduced.index.str.contains('RESIDENCIAL')]
      coef1_h = tep_h.copy()
      coef1_h = (coef1_h * 0) + 1
      coef2_h = coef_tep_to_ghg[(coef_tep_to_ghg['setor'].str.contains('RESIDENCIAL')) & (coef_tep_to_ghg['gas'].str.contains(self.gas))].iloc[:,2:]
      coef2_h.index = ['RESIDENCIAL']
      coef2_h.columns = coef1_j.columns #remember that we assume that 'GÁS DE CIDADE E DE COQUERIA' = 'ELETRICIDADE'
      emission_h_ben = tep_h.values * coef2_h.values
      emission_h_ben = pd.DataFrame(emission_h_ben, columns=coef1_j.columns, index= ['RESIDENCIAL'])

      #estimation_emission
      """
      This method makes adjustments to incorporate households into tables.
      Depending on the value of self.household, it aggregates firms and household data
      and calculates emissions.
      """
      # Depending on the value of self.household, reorder DataFrame or not
      if self.household:
          #self.tep = pd.concat([reorder_df(tep), tep_h], axis=0)
          self.coef1 = pd.concat([reorder_df(coef1), coef1_h], axis=0)
          self.emission_tru = pd.concat([reorder_df(emission_tru), emission_h_ben], axis=0)
          self.emission_ben = pd.concat([emission_ben, emission_h_ben], axis=0)
      else:
          # Aggregate firms and household
          #self.tep = reorder_df(tep)
          self.coef1 = reorder_df(coef1)
          self.emission_tru = reorder_df(emission_tru)
          self.emission_ben = emission_ben
    def verification(self):
      verification = pd.DataFrame(columns=['value', 'sector_ben','product_ben'])
      for i in range(12):
        for ii in range(17):
          map1 = map_ben_to_tru51(self.coef1,i,ii)
          new_row = pd.DataFrame({'value': [map1[0].sum()[0]], 'sector_ben': [map1[1]], 'product_ben':[map1[2]]})
          verification = pd.concat([verification, new_row], ignore_index=True)
          verification_ = verification.pivot(index='product_ben', columns='sector_ben', values='value').T
      self.verification = verification_[self.coef1.columns]






































