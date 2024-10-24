import ree
import dger
import pandas as pd

class Cmarg:
    def __init__(self, caminho):
        self.__ree=ree.Ree(caminho)
        self.__ree.le_ree()
        self.__subsistemas = self.__ree.n_subsistemas
        self.__caminho = []
        for i in range(len(self.__subsistemas)):
            self.__caminho.append(caminho + "/saidas/cmarg00"+str(i+1)+"-med.out")
        self.__cmarg = {}
        self.__dger=dger.Dger(caminho)
        self.__dger.leDger()
        self.__nseries = int(self.__dger.n_series_sinteticas)
        self.le_cmarg()
    
    def le_cmarg(self):
        for arquivo in self.__caminho:
            with open(arquivo, "r") as file:
                nsubsistema = self.__caminho.index(arquivo)
                nsubsistema=self.__subsistemas[nsubsistema]
                #print(self.__subsistemas[nsubsistema])
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
                        for j in range(12):  #percorre os meses
                            mes = j+1
                            valor = linha[8 + (10 * j):18 + (10 * j)].strip()
                            chave = (nsubsistema, ano, mes, serie)
                            self.__cmarg[chave] = valor
                    for i in range(7):
                        linha = file.readline() #lê e pula as linhas de MEDIA, DSVPADRAO, ETC.
                    linha = file.readline()  #linha dos anos
       

    @property
    def cmarg_dataframe(self): #dataframe apenas com cmo
        # Converte o dicionário de cmarg para um DataFrame
        df = pd.DataFrame.from_dict(self.__cmarg, orient='index', columns=['CMO'])
        df.index = pd.MultiIndex.from_tuples(df.index, names=['Subsistema', 'Ano', 'Mes', 'Serie'])
        df.reset_index(inplace=True)
        df['Subsistema']=pd.to_numeric(df['Subsistema'], downcast='unsigned', errors='coerce')  # Converte para numérico
        df['Ano']=pd.to_numeric(df['Ano'], downcast='unsigned', errors='coerce')  # Converte para numérico
        df['Mes']=pd.to_numeric(df['Mes'], downcast='unsigned', errors='coerce')  # Converte para numérico
        df['Serie']=pd.to_numeric(df['Serie'], downcast='unsigned', errors='coerce')  # Converte para numérico
        df['CMO']=pd.to_numeric(df['CMO'], errors='coerce')  # Converte para numérico
        return df

    @property
    def cmarg(self):
        return self.__cmarg
    
    @property
    def pld_dataframe(self):  # dataframe com cmo e pld
        df=self.cmarg_dataframe
        
        # Define os limites do PLD
        pld_minimo = 61.07 #ref 2024
        pld_maximo = 716.80

        # Aplica os limites e converte de volta para string
        df['PLD'] = df['CMO'].clip(lower=pld_minimo, upper=pld_maximo)  # Aplica os limites
        return df
            
#cmarg = Cmarg("PDE2031-ajustado")
#df=cmarg.pld_dataframe
#print(df)
#df2=cmarg.cmarg_dataframe
#print(df2.loc[2000*12*3+12*9+1])