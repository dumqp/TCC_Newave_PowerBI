import ree
import dger
import pandas as pd

class Eafb:
    def __init__(self, caminho):
        self.__ree=ree.Ree(caminho)
        self.__ree.le_ree()
        self.__subsistemas = self.__ree.n_subsistemas
        self.__pasta = caminho #pasta principal
        self.__caminho = []
        for i in range(len(self.__subsistemas)):
            self.__caminho.append(caminho + "/saidas/eafbm00"+str(i+1)+".out")
        self.__eafbm = {}
        self.__dger=dger.Dger(caminho)
        self.__dger.leDger()
        self.__nseries = int(self.__dger.n_series_sinteticas)
        self.le_eafbm()
    
    def le_eafbm(self):
        for arquivo in self.__caminho:
            with open(arquivo, "r") as file:
                nsubsistema = self.__caminho.index(arquivo)
                nsubsistema=self.__subsistemas[nsubsistema]
                for i in range (3):  #Pula linhas de cabeçalho
                    linha = file.readline()
                linha = file.readline()  #linha dos anos
                while linha:
                    ano = linha[10:14]
                    linha = file.readline()  # linha dos meses
                    #lê os valores por serie
                    for i in range(self.__nseries):
                        serie = i+1
                        linha = file.readline()
                        for j in range(12):  #percorre os meses apenas para o item TOTAL de cada série
                            mes = j+1
                            valor = linha[8 + (9 * j):16 + (9 * j)].strip()
                            chave = (nsubsistema, ano, mes, serie)
                            self.__eafbm[chave] = valor
                    for i in range(7):
                        linha = file.readline() #lê e pula as linhas de MEDIA, DSVPADRAO, ETC.
                    linha = file.readline()  #linha dos anos
       

    @property
    def eafbm_dataframe(self): #dataframe apenas com cmo
        # Converte o dicionário de cmarg para um DataFrame
        df = pd.DataFrame.from_dict(self.__eafbm, orient='index', columns=['ENA-MWm'])
        df.index = pd.MultiIndex.from_tuples(df.index, names=['Subsistema', 'Ano', 'Mes', 'Serie'])
        df.reset_index(inplace=True)
        df['Subsistema']=pd.to_numeric(df['Subsistema'], downcast='unsigned', errors='coerce')  # Converte para numérico
        df['Ano']=pd.to_numeric(df['Ano'], downcast='unsigned', errors='coerce')  # Converte para numérico
        df['Mes']=pd.to_numeric(df['Mes'], downcast='unsigned', errors='coerce')  # Converte para numérico
        df['Serie']=pd.to_numeric(df['Serie'], downcast='unsigned', errors='coerce')  # Converte para numérico
        df['ENA-MWm']=pd.to_numeric(df['ENA-MWm'], errors='coerce')  # Converte para numérico
        return df

    @property
    def eafbm(self):
        return self.__eafbm
    
    def mlt_historica(self):
        df_mlt = pd.read_excel(self.__pasta + "/ENAs/MLT_subsistema.xlsx")
        df_mlt['Subsistema']=pd.to_numeric(df_mlt['Subsistema'], downcast='unsigned', errors='coerce')  # Converte para numérico
        df_mlt['Mes']=pd.to_numeric(df_mlt['Mes'], downcast='unsigned', errors='coerce')  # Converte para numérico
        df_mlt[['MLT']] = df_mlt[['MLT']].apply(pd.to_numeric, errors='coerce')
        return df_mlt
    
    @property
    def ena_perc_mlt(self):
        df_mlt = self.mlt_historica()
        df_eafbMedia = self.eafbm_dataframe
        df_eafbMedia = df_eafbMedia.groupby(['Subsistema','Ano','Mes']).agg({'ENA-MWm':'mean'}).reset_index()
        df_enaPerc= pd.merge(df_eafbMedia, df_mlt, on=['Subsistema','Mes'], how='left')
        df_enaPerc["%MLT"]=df_enaPerc['ENA-MWm']/df_enaPerc['MLT']
        return df_enaPerc
    
            
eafbm = Eafb("PDE2031-ajustado")
#df=eafbm.eafbm_dataframe
#print(df)
df = eafbm.ena_perc_mlt
print(df)