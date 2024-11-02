import ree
import dger
import pandas as pd

class Ghtot:
    def __init__(self, caminho):
        self.__ree=ree.Ree(caminho)
        self.__subsistemas = self.__ree.n_subsistemas
        self.__caminho = []
        for i in range(len(self.__subsistemas)):
            self.__caminho.append(caminho + "/saidas/ghtotm00"+str(i+1)+".out")
        self.__ghtotm = {}
        self.__dger=dger.Dger(caminho)
        self.__nseries = int(self.__dger.n_series_sinteticas)
        with open(caminho + "/patamar.dat", "r") as file:
            for _ in range(2):  # Pula as duas primeiras linhas
                file.readline()
            self.__nPatamares = int(file.readline().strip())  # Lê a terceira linha e pega o numero de patamares do caso
        self.le_ghtotm()
    
    def le_ghtotm(self):
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
                        for k in range(self.__nPatamares):  
                            linha = file.readline()    #pula as linhas de patamares
                        linha = file.readline()
                        for j in range(12):  #percorre os meses apenas para o item TOTAL de cada série
                            mes = j+1
                            valor = linha[12 + (9 * j):21 + (9 * j)].strip()
                            chave = (nsubsistema, ano, mes, serie)
                            self.__ghtotm[chave] = valor
                    for i in range(7):
                        linha = file.readline() #lê e pula as linhas de MEDIA, DSVPADRAO, ETC.
                    linha = file.readline()  #linha dos anos
       

    @property
    def ghtotm_dataframe(self): #dataframe apenas com cmo
        # Converte o dicionário de cmarg para um DataFrame
        df = pd.DataFrame.from_dict(self.__ghtotm, orient='index', columns=['Geracao-MWm'])
        df.index = pd.MultiIndex.from_tuples(df.index, names=['Subsistema', 'Ano', 'Mes', 'Serie'])
        df.reset_index(inplace=True)
        df['Subsistema']=pd.to_numeric(df['Subsistema'], downcast='unsigned', errors='coerce')  # Converte para numérico
        df['Ano']=pd.to_numeric(df['Ano'], downcast='unsigned', errors='coerce')  # Converte para numérico
        df['Mes']=pd.to_numeric(df['Mes'], downcast='unsigned', errors='coerce')  # Converte para numérico
        df['Serie']=pd.to_numeric(df['Serie'], downcast='unsigned', errors='coerce')  # Converte para numérico
        df['Geracao-MWm']=pd.to_numeric(df['Geracao-MWm'], errors='coerce')  # Converte para numérico
        return df

    @property
    def ghtotm(self):
        return self.__ghtotm
