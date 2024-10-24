import pandas as pd

class Sistema:
    def __init__(self, caminho):
        self.__caminho = caminho + "/sistema.dat"
        self.__n_patamares_deficit = "0"
        self.__custo_deficit = {}
        self.__intercambio = {}
        self.__mercado = {}
        self.__geracaoPQ = {}
        self.le_sistema()

    def le_sistema(self):
        with open(self.__caminho, "r") as file:
            for i in range(4):
                linha = file.readline() # ler e pular as 3 primeiras linhas
            self.__n_patamares_deficit =  linha.strip()

            linha = file.readline()

            # BLOCO CUSTO DO DEFICIT
            if linha.strip() == "CUSTO DO DEFICIT":
                while linha[0:4] != " XXX":
                    linha = file.readline()
                linha = file.readline()
                while linha [0:4] != " 999":
                    self.__custo_deficit.update({linha[1:4].strip():linha[19:26].strip()}) # cod sistema : valor deficit pat1
                    linha = file.readline()
            
            linha = file.readline()  # ir para linha após o 999            

            # BLOCO LIMITES DE INTERCAMBIO
            if linha.strip() == "LIMITES DE INTERCAMBIO":
                while linha[0:4] != " XXX":
                    linha = file.readline()
                linha = file.readline()
                while linha [0:4] != " 999":
                    try:
                        if (int(linha[0:4].strip()) < 900): # No subsistema
                            subsistemaDe = linha.split()[0]
                            subsistemaPara = linha.split()[1]
                        else:
                            for i in range(12):
                                ano = linha[0:4].strip()
                                mes = i+1
                                valor = linha[7 + (8 * i):14 + (8 * i)].strip()
                                chave = (subsistemaDe, subsistemaPara, ano, mes)
                                self.__intercambio[chave] = valor
                    except:
                        aux = subsistemaDe
                        subsistemaDe = subsistemaPara
                        subsistemaPara = aux
                    linha = file.readline()
            linha = file.readline()  # ir para linha após o 999        

            # BLOCO MERCADO DE ENERGIA TOTAL
            if linha.strip() == "MERCADO DE ENERGIA TOTAL":
                linha = file.readline() # Linha XXX
                linha = file.readline() # Linha XXXJAN XXXFEV
                linha = file.readline()
                while linha [0:4] != " 999": # num subsistemas
                    subsistema = linha.strip()
                    linha = file.readline()
                    while linha[0:3]!= "POS":
                        for j in range(12):
                            ano = linha[0:4].strip()
                            mes = j+1
                            valor = linha[7 + (8 * j):14 + (8 * j)].strip()
                            chave = (subsistema, ano, mes)
                            self.__mercado[chave] = valor
                        linha = file.readline()
                    linha = file.readline() # Ler depois do POS

            linha = file.readline()  # ir para linha após o 999

            # BLOCO GERACAO DE USINAS NAO SIMULADAS
            if linha.strip() == "GERACAO DE USINAS NAO SIMULADAS":
                linha = file.readline() # Linha XXX
                linha = file.readline() # Linha XXXJAN XXXFEV
                linha = file.readline()
                while linha [0:4] != " 999": # num subsistemas
                    linhaSplit = linha.split()
                    subsistema = linhaSplit[0]
                    tecnologia = linhaSplit[1]
                    linha = file.readline()
                    while int(linha[0:4].strip()) > 1000: #Verifica se é subsitema ou ano
                        for j in range(12):
                            ano = linha[0:4].strip()
                            mes = j+1
                            valor = linha[7 + (8 * j):14 + (8 * j)].strip()
                            chave = (subsistema, tecnologia, ano, mes)
                            self.__geracaoPQ[chave] = valor
                        linha = file.readline()
               
                        
    @property
    def intercambio(self):
        return self.__intercambio
    
    @property
    def mercado(self):
        return self.__mercado
    
    @property
    def geracaoPQ(self):
        return self.__geracaoPQ
    
    @property
    def n_patamares_deficit(self):
        return self.__n_patamares_deficit
    
    @property
    def custo_deficit(self):
        return self.__custo_deficit
    
    def intercambios(self):
        # Gera o DataFrame e retorna os subsistemas de e para únicos
        df = self.lim_intercambio_dataframe
        intercambios = df[['SubsistemaDE', 'SubsistemaPara']].drop_duplicates().reset_index(drop=True)
        intercambios = intercambios[intercambios['SubsistemaDE'] < intercambios['SubsistemaPara']].reset_index(drop=True)
        return intercambios
    
    @property
    def lim_intercambio_dataframe(self):
        #self.le_sistema()
        # Converte o dicionário de intercâmbio para um DataFrame
        df = pd.DataFrame.from_dict(self.__intercambio, orient='index', columns=['Valor'])
        df.index = pd.MultiIndex.from_tuples(df.index, names=['SubsistemaDE', 'SubsistemaPara', 'Ano', 'Mes'])
        df.reset_index(inplace=True)
        df['SubsistemaDE']=pd.to_numeric(df['SubsistemaDE'], downcast='unsigned', errors='coerce')  # Converte para numérico
        df['SubsistemaPara']=pd.to_numeric(df['SubsistemaPara'], downcast='unsigned', errors='coerce')  # Converte para numérico
        df['Ano']=pd.to_numeric(df['Ano'], downcast='unsigned', errors='coerce')  # Converte para numérico
        df['Mes']=pd.to_numeric(df['Mes'], downcast='unsigned', errors='coerce')  # Converte para numérico
        df['Valor']=pd.to_numeric(df['Valor'], errors='coerce')  # Converte para numérico
        return df
    
    @property
    def mercado_dataframe(self):

        # Converte o dicionário de intercâmbio para um DataFrame
        df = pd.DataFrame.from_dict(self.__mercado, orient='index', columns=['Valor'])
        df.index = pd.MultiIndex.from_tuples(df.index, names=['Subsistema', 'Ano', 'Mes'])
        df.reset_index(inplace=True)
        df['Subsistema']=pd.to_numeric(df['Subsistema'], downcast='unsigned', errors='coerce')  # Converte para numérico
        df['Ano']=pd.to_numeric(df['Ano'], downcast='unsigned', errors='coerce')  # Converte para numérico
        df['Mes']=pd.to_numeric(df['Mes'], downcast='unsigned', errors='coerce')  # Converte para numérico
        df['Valor']=pd.to_numeric(df['Valor'], errors='coerce')  # Converte para numérico
        return df

    @property
    def geracaoPQ_dataframe(self):
        # Converte o dicionário de geracao de pequenas usinas para um DataFrame
        df = pd.DataFrame.from_dict(self.__geracaoPQ, orient='index', columns=['Valor'])
        df.index = pd.MultiIndex.from_tuples(df.index, names=['Subsistema', 'Tecnologia', 'Ano', 'Mes'])
        df.reset_index(inplace=True)
        df['Subsistema']=pd.to_numeric(df['Subsistema'], downcast='unsigned', errors='coerce')  # Converte para numérico
        df['Tecnologia']=pd.to_numeric(df['Tecnologia'], downcast='unsigned', errors='coerce')  # Converte para numérico
        df['Ano']=pd.to_numeric(df['Ano'], downcast='unsigned', errors='coerce')  # Converte para numérico
        df['Mes']=pd.to_numeric(df['Mes'], downcast='unsigned', errors='coerce')  # Converte para numérico
        df['Valor']=pd.to_numeric(df['Valor'], errors='coerce')  # Converte para numérico
        return df
    
    @property
    def geracaoEolica_dataframe(self):
        df = self.geracaoPQ_dataframe
        df = df.loc[df['Tecnologia'] == 3]
        return df
    
    @property
    def geracaoSolar_dataframe(self):
        df = self.geracaoPQ_dataframe
        df = df.loc[df['Tecnologia'] == 4]
        return df
    
    @property
    def geracaoMMGD_dataframe(self):
        df = self.geracaoPQ_dataframe
        df = df.loc[(df['Tecnologia'] == 5) | (df['Tecnologia'] == 6) | (df['Tecnologia'] == 7) | (df['Tecnologia'] == 8)]
        return df
    
#sistema = Sistema("PDE2031-ajustado")
#df1 = sistema.lim_intercambio_dataframe
#print(df1)
#df2 = sistema.mercado_dataframe
#print(df2)
#df3 = sistema.geracaoPQ_dataframe
#print(df3)
#df4 = sistema.geracaoEolica_dataframe
#df5 = sistema.geracaoSolar_dataframe
#df6 = sistema.geracaoMMGD_dataframe

#print(df4)
#print(df5)
#print(df6)

#subsistemas_unicos = sistema.intercambios()
#print(subsistemas_unicos)