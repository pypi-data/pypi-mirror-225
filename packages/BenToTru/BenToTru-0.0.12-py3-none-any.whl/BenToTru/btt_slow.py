import pandas as pd
import numpy as np

from iotbr import tru as tru


from importlib import resources
import io

with resources.open_binary('BenToTru.data', 'coeficientes_emissoes_gee_ajustado.csv') as f:
  data_ = f.read()
  bytes_io = io.BytesIO(data_)
coef_tep_to_ghg = pd.read_csv(bytes_io)

with resources.open_binary('BenToTru.data', 'correspondencia_MIP56_TRU51_BEN.csv') as f:
  data_ = f.read()
  bytes_io = io.BytesIO(data_)
ben_to_tru51_sectors = pd.read_csv(bytes_io)

with resources.open_binary('BenToTru.data', 'correspondencia_produtos_TRU51_BEN.csv') as f:
  data_ = f.read()
  bytes_io = io.BytesIO(data_)
ben_to_tru51_products = pd.read_csv(bytes_io, sep=';')

#ben_to_tru51_products = pd.read_csv('https://raw.githubusercontent.com/fms-1988/datas/main/correspondencia_produtos_TRU51_BEN.csv',sep=';')
#ben_to_tru51_sectors = pd.read_csv('https://raw.githubusercontent.com/fms-1988/datas/main/correspondencia_MIP56_TRU51_BEN.csv')
#coef_tep_to_ghg = pd.read_csv('https://raw.githubusercontent.com/fms-1988/datas/main/coeficientes_emissoes_gee_ajustado.csv')


def reorder_df(df_):
  #correct order of rows on tru51
  ar1 = [ 0,  1,  2,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15,  3,  4, 16, 17,\
         18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34,\
          5, 35, 36, 47, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 48, 49, 50]
  return df_.iloc[ar1,:]

def map_ben_to_tru51(self, matrix,sector_ben_index,product_ben_index):
  sector_ben = self.ben_to_tru51_sectors['descricao_atividades_ben2'].unique()[sector_ben_index]
  sectors_tru51 = self.ben_to_tru51_sectors[self.ben_to_tru51_sectors['descricao_atividades_ben2'] == sector_ben]['setor_tru51']
  product_ben = matrix.columns[product_ben_index]
  return pd.DataFrame(matrix.iloc[sectors_tru51-1,product_ben_index]), sector_ben, product_ben

class system:
    def __init__(self, year: str, level: str, unit: str, gas: str,household=False):
        self.Y = year
        self.L = level
        self.u = unit
        self.gas = gas
        self.household = household
        self.NUM_SECTORS = 12
        self.NUM_PRODUCTS = 14
        self.import_data()
        self.household_estimation()
        self.estimations_firms()
        self.verification()
        self.ajust_coefficients_value_to_tep()
        self.ajust_tep()
        self.estimation_firms_plus_household()
        #self.ajust_tep()
    def import_data(self):
        #import and adjust matrix ben to 22 sectors
        with resources.open_binary('BenToTru.data','Matrizes Consolidadas (em tep) 1970 - 2022.xls') as f:
          data = f.read()
          bytes_io = io.BytesIO(data)
        ben = pd.read_excel(bytes_io, sheet_name=self.Y)        
        #ben = pd.read_excel('https://github.com/fms-1988/datas/raw/main/Matrizes%20Consolidadas%20(em%20tep)%201970%20-%202022.xls', sheet_name=self.Y)
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
        self.ben = ben

        #import relation between products of BEN and TRU51
        #self.ben_to_tru51_products = pd.read_csv('https://raw.githubusercontent.com/fms-1988/datas/main/correspondencia_produtos_TRU51_BEN.csv',sep=';')
        self.ben_to_tru51_products = ben_to_tru51_products[ben_to_tru51_products['produto_TRU51'] != 'nc'].reset_index(drop=True)

        #import relation between sectors of BEN and TRU51
        #self.ben_to_tru51_sectors = pd.read_csv('https://raw.githubusercontent.com/fms-1988/datas/main/correspondencia_MIP56_TRU51_BEN.csv')
        self.ben_to_tru51_sectors = ben_to_tru51_sectors

        #import coeficients to convert tep to emission
        #self.coef_tep_to_ghg = pd.read_csv('https://raw.githubusercontent.com/fms-1988/datas/main/coeficientes_emissoes_gee_ajustado.csv')
        self.coef_tep_to_ghg = coef_tep_to_ghg

        #import values of intermediate consumption by economic sector (TRU51)
        #tru51 is updated untill 2020 and ben is updated untill 2023
        #if tru51 is not updated, than use the last value available (2020)
        try:
          self.tru51_CI = tru.read_var(self.Y,self.L,'CI_matrix',self.u).T
        except Exception as e:
          self.tru51_CI = tru.read_var('2020',self.L,'CI_matrix',self.u).T
    def household_estimation(self):
        products_ben_ghg = ['GÁS NATURAL', 'CARVÃO VAPOR', 'LENHA', 'PRODUTOS DA CANA',\
                            'OUTRAS FONTES PRIMÁRIAS', 'ÓLEO DIESEL', 'ÓLEO COMBUSTÍVEL',\
                            'GASOLINA', 'GLP', 'QUEROSENE', 'GÁS DE CIDADE E DE COQUERIA',\
                            'COQUE DE CARVÃO MINERAL']
        tep_household = pd.DataFrame(self.ben.loc['RESIDENCIAL',:]).T#.sum(axis=0)
        tep_household = tep_household[products_ben_ghg]
        self.tep_household = tep_household

        #household emission
        coef_tep_to_ghg_h = self.coef_tep_to_ghg[(self.coef_tep_to_ghg['setor'].str.contains('RESIDENCIAL')) & (self.coef_tep_to_ghg['gas'].str.contains(self.gas))][products_ben_ghg].astype(float)
        coef_tep_to_ghg_h.index = ['RESIDENCIAL']
        emission_housegold = self.tep_household.multiply(coef_tep_to_ghg_h.iloc[0], axis=1)
        self.emission_housegold = emission_housegold
        self.coef_tep_to_ghg_h = coef_tep_to_ghg_h

    def estimations_firms(self):
        #create a loop to all sectors and than a loop to all products.
        #this loop create:
        #1) coeficients to convert values (BRL) to tep.
        #2) coeficients to convert tep to GHG.
        #3) emission of GHG by sector and year.
        #4) consue of energy (tep) by sector and year.
        coefficients_value_to_tep = pd.DataFrame()
        coefficients_tep_to_emission = pd.DataFrame()
        tep = pd.DataFrame()
        emission = pd.DataFrame()

        for i in range(0,self.NUM_SECTORS):
          df0 = pd.DataFrame()
          product_ben = self.ben_to_tru51_products['produto_BEN'][i] # e.g:'CARVÃO VAPOR'
          product_tru51 = self.ben_to_tru51_products['produto_TRU51_num'][i] #e.g: 'Carvão mineral'
          for ii in range(0,self.NUM_PRODUCTS):
            #'ÓLEO COMBUSTÍVEL' ins't in the ben before 2004
            sector_ben = self.ben_to_tru51_sectors['descricao_atividades_ben2'].unique()[ii] #e.g: 'AGROPECUÁRIO'
            #the TRU51 of 2006 have a problem. the name of two sectors are wrong: 'Eletrodomésticos e material eletronico' and 'Máquinas para escritório aparelhos e e material eletronico'
            #because of this problem, we must use the number of the sector, not its name.
            sectors_tru51_int = self.ben_to_tru51_sectors[self.ben_to_tru51_sectors['descricao_atividades_ben2'] == sector_ben]['setor_tru51']
            #the TRU51 of 2019 have a problem. the name of the product 'Produção e distribuição de eletricidade gás água esgoto e limpeza urbana' is wrong.
            #because of this problem, we must use the number of the product, not its name. It is the row that the product is alocated on TRU51.
            products_tru51_int = self.ben_to_tru51_products[self.ben_to_tru51_products['produto_BEN'] == product_ben]['produto_TRU51_num']

            #sector (x) and product (y) of the TRU51
            tru51_CI_reduced = self.tru51_CI.iloc[sectors_tru51_int -1,products_tru51_int].copy()

            #create coeficient of distribution (values to tep)
            ##coef1 = coeficient Montoya (2013) adapted to convert ben22_tep to tru51_tep
            total = tru51_CI_reduced.iloc[:, 0].sum()#[0]

            if total != 0:
              tru51_CI_reduced['coef1'] = tru51_CI_reduced.iloc[:, 0]/total
            else:
              tru51_CI_reduced['coef1'] = tru51_CI_reduced.iloc[:, 0] #* 0

            #estimate tep by sector
            tru51_CI_reduced['tep'] = tru51_CI_reduced['coef1'] * self.ben.loc[sector_ben.split(' + '),[product_ben]].sum()[0]

            ##criate coeficient to convert tep to emission
            ##coef2 = coeficient estimated by E&E to convert tep to emission (CO2, NH4, …)
            coef_tep_to_ghg_x = self.coef_tep_to_ghg[(self.coef_tep_to_ghg['setor'].str.contains(sector_ben.replace(' + ', '|'))) & (self.coef_tep_to_ghg['gas'].str.contains(self.gas))][product_ben].astype(float).mean()
            tru51_CI_reduced['coef2'] = coef_tep_to_ghg_x

            ##estimate emission of ghg of sectors tru51 by consuming diesel (1000 tep)
            tru51_CI_reduced['emission'] = tru51_CI_reduced['tep'] * tru51_CI_reduced['coef2']

            ##concatenate information
            df0 = pd.concat([df0,tru51_CI_reduced], axis=0)

          #coefficients_value_to_tep
          coefficients_value_to_tep = pd.concat([coefficients_value_to_tep,df0['coef1']], axis=1)
          coefficients_value_to_tep = coefficients_value_to_tep.rename(columns={coefficients_value_to_tep.columns[i]: product_ben})
          self.coefficients_value_to_tep = reorder_df(coefficients_value_to_tep)

          #coefficients_tep_to_emission
          coefficients_tep_to_emission = pd.concat([coefficients_tep_to_emission,df0['coef2']], axis=1)
          coefficients_tep_to_emission = coefficients_tep_to_emission.rename(columns={coefficients_tep_to_emission.columns[i]: product_ben})
          self.coefficients_tep_to_emission = reorder_df(coefficients_tep_to_emission)

          #tep
          tep = pd.concat([tep,df0['tep']], axis=1)
          tep = tep.rename(columns={tep.columns[i]: product_ben})
          self.tep = reorder_df(tep)

          #emission
          emission = pd.concat([emission,df0['emission']], axis=1)
          emission = emission.rename(columns={emission.columns[i]: product_ben})
          self.emission = reorder_df(emission)

    def verification(self):
      verification = pd.DataFrame(columns=['value', 'sector_ben','product_ben'])
      for i in range(self.NUM_PRODUCTS):
        for ii in range(self.NUM_SECTORS):
          map1 = map_ben_to_tru51(self,self.coefficients_value_to_tep,i,ii)
          new_row = pd.DataFrame({'value': [map1[0].sum()[0]], 'sector_ben': [map1[1]], 'product_ben':[map1[2]]})
          verification = pd.concat([verification, new_row], ignore_index=True)
      self.verification = verification.pivot(index='product_ben', columns='sector_ben', values='value').T
    def ajust_coefficients_value_to_tep(self):
      coefficients_value_to_tep_ajusted = pd.DataFrame()
      for i in range(self.NUM_PRODUCTS):
        map1 = map_ben_to_tru51(self, self.coefficients_value_to_tep,i,range(self.NUM_SECTORS))[0]
        total = map1.sum().sum()
        totals = map1.sum(axis=1)
        mean = totals / total
        for col in map1.columns:
          if map1[col].eq(0).all():
            map1[col] = mean
        coefficients_value_to_tep_ajusted = pd.concat([coefficients_value_to_tep_ajusted,map1], axis=0)
      self.coefficients_value_to_tep_ajusted = reorder_df(coefficients_value_to_tep_ajusted)
    def ajust_tep(self):
      tep_ajusted = pd.DataFrame()
      for i in range(self.NUM_PRODUCTS):
        map1 = map_ben_to_tru51(self, self.coefficients_value_to_tep_ajusted,i,range(self.NUM_SECTORS))
        sector_ben = map1[1]
        map2 = self.ben.loc[sector_ben.split(' + ')].sum()
        map2 = pd.DataFrame(map2).T
        common_columns = map1[0].columns#just producs that cause emission
        map2_filtered = map2[common_columns]#just producs that cause emission
        map3 = map1[0].multiply(map2_filtered.iloc[0], axis=1)
        tep_ajusted = pd.concat([tep_ajusted,map3], axis=0)
      self.tep_ajusted = reorder_df(tep_ajusted)

    def estimation_firms_plus_household(self): #some ajusts must be done to incert households on tables
      if self.household ==True:
        self.coefficients_tep_to_emission = pd.concat([self.coefficients_tep_to_emission, self.coef_tep_to_ghg_h], axis=0)
        self.coefficients_value_to_tep = pd.concat([self.coefficients_value_to_tep, self.tep_household*0 +1], axis=0)
        self.coefficients_value_to_tep_ajusted = pd.concat([self.coefficients_value_to_tep_ajusted, self.tep_household*0 +1], axis=0)
        self.tep = pd.concat([self.tep,self.tep_household], axis=0)
        self.tep_ajusted = pd.concat([self.tep_ajusted,self.tep_household], axis=0)
        self.emission = pd.concat([self.emission,self.emission_housegold], axis=0)










































