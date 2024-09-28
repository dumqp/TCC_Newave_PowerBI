import ree
import dger
import pandas as pd

class Gtert:
    def __init__(self, caminho):
        self.__ree=ree.Ree(caminho)
        self.__ree.le_ree()
        self.__subsistemas = self.__ree.n_subsistemas
        self.__caminho = []
        for i in range(len(self.__subsistemas)):
            self.__caminho.append(caminho + "/saidas/gtert00"+str(i+1)+".out")
        self.__gtert = {}
        self.__dger=dger.Dger(caminho)
        self.__dger.leDger()
        self.__nseries = int(self.__dger.n_series_sinteticas)
        with open(caminho + "/patamar.dat", "r") as file:
            for _ in range(2):  # Pula as duas primeiras linhas
                file.readline()
            self.__nPatamares = int(file.readline().strip())  # Lê a terceira linha e pega o numero de patamares do caso
        self.le_gtert()
    
    def le_gtert(self):
        for arquivo in self.__caminho:
            with open(arquivo, "r") as file:
                nsubsistema = self.__caminho.index(arquivo)
                nsubsistema=self.__subsistemas[nsubsistema]
                valor = []
                for k in range(self.__nPatamares):  #valores por patamar
                    valor.append([])
                for i in range (3):  #Pula linhas de cabeçalho
                    linha = file.readline()
                while linha:
                    linha = file.readline()  #linha dos anos
                    ano = linha[10:14]
                    linha = file.readline()  # linha dos meses
                    linha = file.readline()
                    while linha[2:7]!="TOTAL":
                        print(linha)
                        if linha[2:5] !="": classeTermica = linha[2:5].strip()
                        #lê os valores por serie
                        for i in range(self.__nseries):
                            serie = i+1
                            for k in range(self.__nPatamares):  #valores por patamar
                                linha = file.readline()    
                                for j in range(12):  #percorre os meses apenas para o item TOTAL de cada série
                                    valor[k].append(linha[17 + (9 * j):26 + (9 * j)].strip())
                            #soma valores dos patamares
                            valortotal=[0]*12
                            for k in range(self.__nPatamares):  #valores por patamar
                                for j in range(12):  #percorre os meses apenas para o item TOTAL de cada série
                                    valortotal[j]+=float(valor[k][j])
                            for j in range(12):
                                mes = j+1
                                chave = (classeTermica,nsubsistema, ano, mes, serie)
                                self.__gtert[chave] = valortotal[j]
                            #resetar valor
                            del valortotal
                            del valor
                            valor = []
                            for k in range(self.__nPatamares):  #valores por patamar
                                valor.append([])
                            print(str(serie) + " - " + str(classeTermica))
                        for i in range(5):
                            linha = file.readline() #lê e pula as linhas de MEDIA, DSVPADRAO, ETC. DA CLASSE TERMICA
                        linha = file.readline()
                    for i in range(self.__nseries-1): #O primeiro TOTAL é lido no loop anterior
                        linha = file.readline() #lê e pula as linhas de TOTAL do ANO
                    print(linha + "TOTAL")
                    for i in range(6):
                        linha = file.readline() #lê e pula as linhas de MEDIA, DSVPADRAO, ETC. DO ANO
                    linha = file.readline()  #linha em branco antes dos anos
                del valor
       

    @property
    def gtert_dataframe(self): #dataframe apenas com cmo
        # Converte o dicionário de cmarg para um DataFrame
        df = pd.DataFrame.from_dict(self.__gtert, orient='index', columns=['Geracao-MWm'])
        df.index = pd.MultiIndex.from_tuples(df.index, names=['ClasseTermica','Subsistema', 'Ano', 'Mes', 'Serie'])
        df.reset_index(inplace=True)
        df['ClasseTermica']=pd.to_numeric(df['ClasseTermica'], downcast='unsigned', errors='coerce')  # Converte para numérico
        df['Subsistema']=pd.to_numeric(df['Subsistema'], downcast='unsigned', errors='coerce')  # Converte para numérico
        df['Ano']=pd.to_numeric(df['Ano'], downcast='unsigned', errors='coerce')  # Converte para numérico
        df['Mes']=pd.to_numeric(df['Mes'], downcast='unsigned', errors='coerce')  # Converte para numérico
        df['Serie']=pd.to_numeric(df['Serie'], downcast='unsigned', errors='coerce')  # Converte para numérico
        df['Geracao-MWm']=pd.to_numeric(df['Geracao-MWm'], errors='coerce')  # Converte para numérico
        return df

    @property
    def gtert(self):
        return self.__gtert
    
            
gtert = Gtert("PDE2031-ajustado")
df=gtert.gtert_dataframe
#print(df)
#print(df.loc[(df['Subsistema'] == 1) & (df['Ano'] == 2023) & (df['Mes'] == 8) & (df['Serie'] == 100)])
#print(df.loc[(df['Subsistema'] == 2) & (df['Ano'] == 2023) & (df['Mes'] == 8) & (df['Serie'] == 100)])
#print(df.loc[(df['Subsistema'] == 3) & (df['Ano'] == 2023) & (df['Mes'] == 8) & (df['Serie'] == 100)])
#print(df.loc[(df['Subsistema'] == 4) & (df['Ano'] == 2023) & (df['Mes'] == 8) & (df['Serie'] == 100)])
