import sistema
import dger
import pandas as pd

class Intxx:
    def __init__(self, caminho):
        self.__intercambios=sistema.Sistema(caminho)
        self.__intercambios=self.__intercambios.intercambios()
        self.__caminho = []
        for index, row in self.__intercambios.iterrows():
            subsistemaDe = row['SubsistemaDE']
            subsistemaPara = row['SubsistemaPara']
            if subsistemaDe < 10 and subsistemaPara < 10:
                self.__caminho.append(caminho + "/saidas/int00"+str(subsistemaDe)+"00"+str(subsistemaPara)+".out")
            elif subsistemaDe < 10 and subsistemaPara >= 10:
                self.__caminho.append(caminho + "/saidas/int00"+str(subsistemaDe)+"0"+str(subsistemaPara)+".out")
            elif subsistemaDe >= 10 and subsistemaPara < 10:
                self.__caminho.append(caminho + "/saidas/int0"+str(subsistemaDe)+"00"+str(subsistemaPara)+".out")
            else:
                self.__caminho.append(caminho + "/saidas/int0"+str(subsistemaDe)+"0"+str(subsistemaPara)+".out")
        self.__int = {}
        self.__dger=dger.Dger(caminho)
        self.__dger.leDger()
        self.__nseries = int(self.__dger.n_series_sinteticas)
        with open(caminho + "/patamar.dat", "r") as file:
            for _ in range(2):  # Pula as duas primeiras linhas
                file.readline()
            self.__nPatamares = int(file.readline().strip())  # Lê a terceira linha e pega o numero de patamares do caso
        self.le_int()
    
    def le_int(self):
        for arquivo in self.__caminho:
            with open(arquivo, "r") as file:
                index = self.__caminho.index(arquivo)
                subsistemaDE=self.__intercambios.loc[index,'SubsistemaDE']
                subsistemaPara=self.__intercambios.loc[index,'SubsistemaPara']
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
                            chave = (subsistemaDE, subsistemaPara, ano, mes, serie)
                            self.__int[chave] = valor
                    for i in range(7):
                        linha = file.readline() #lê e pula as linhas de MEDIA, DSVPADRAO, ETC.
                    linha = file.readline()  #linha dos anos
       

    @property
    def int_dataframe(self): #dataframe apenas com cmo
        # Converte o dicionário de cmarg para um DataFrame
        df = pd.DataFrame.from_dict(self.__int, orient='index', columns=['MWm'])
        df.index = pd.MultiIndex.from_tuples(df.index, names=['SubsistemaDE', 'SubsistemaPara', 'Ano', 'Mes', 'Serie'])
        df.reset_index(inplace=True)
        df['SubsistemaDE']=pd.to_numeric(df['SubsistemaDE'], downcast='unsigned', errors='coerce')  # Converte para numérico
        df['SubsistemaPara']=pd.to_numeric(df['SubsistemaPara'], downcast='unsigned', errors='coerce')  # Converte para numérico
        df['Ano']=pd.to_numeric(df['Ano'], downcast='unsigned', errors='coerce')  # Converte para numérico
        df['Mes']=pd.to_numeric(df['Mes'], downcast='unsigned', errors='coerce')  # Converte para numérico
        df['Serie']=pd.to_numeric(df['Serie'], downcast='unsigned', errors='coerce')  # Converte para numérico
        df['MWm']=pd.to_numeric(df['MWm'], errors='coerce')  # Converte para numérico
        return df

    @property
    def int(self):
        return self.__int
    
            
#intercambio = Intxx("PDE2031-ajustado")
#df=intercambio.int_dataframe
#print(df)
#print(df.loc[2001*13])
#print(df.loc[(df['SubsistemaDE'] == 1) & (df['SubsistemaPara'] == 11) & (df['Ano'] == 2023) & (df['Mes'] == 8) & (df['Serie'] == 100)])