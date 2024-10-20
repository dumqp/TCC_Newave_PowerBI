import pandas as pd

class Exph:
    def __init__(self,caminho):
        self.__caminho = caminho + "/exph.dat"
        self.__exph = {}
        self.le_exph()
    
    def le_exph(self):
        with open(self.__caminho,'r') as file:
            for i in range(3): #linhas de título
                linha = file.readline()
            linha = file.readline()
            while linha:
                codUsina = 0
                dataEntrada = 0
                potencia = 0
                num_maq = 0
                num_conj = 0
                if linha[0:4].strip() != "" and linha[0:4].strip() != "9999":
                    codUsina = linha[0:4].strip()
                    linha=file.readline()
                    while linha[0:4].strip() != "9999":
                        dataEntrada = linha[44:51]
                        potencia = linha[52:58]
                        num_maq = linha[60:62]  
                        num_conj = linha[64:65]
                        chave = (codUsina,dataEntrada,num_maq,num_conj)
                        self.__exph [chave] = potencia
                        linha=file.readline()
                linha = file.readline()

    @property
    def exph_dataframe(self): #dataframe apenas com cmo
        # Converte o dicionário de cmarg para um DataFrame
        df = pd.DataFrame.from_dict(self.__exph, orient='index', columns=['Potencia'])
        df.index = pd.MultiIndex.from_tuples(df.index, names=['CodUsina','DataEntrada', 'NumMaquina', 'NumConjunto'])
        df.reset_index(inplace=True)
        df['CodUsina']=pd.to_numeric(df['CodUsina'], downcast='unsigned', errors='coerce')  # Converte para numérico
        df['DataEntrada']=pd.to_datetime(df['DataEntrada'])  # Converte para data
        df['NumMaquina']=pd.to_numeric(df['NumMaquina'], downcast='unsigned', errors='coerce')  # Converte para numérico
        df['NumConjunto']=pd.to_numeric(df['NumConjunto'], downcast='unsigned', errors='coerce')  # Converte para numérico
        df['Potencia']=pd.to_numeric(df['Potencia'], errors='coerce')  # Converte para numérico
        df['DataEntradaAno']=df['DataEntrada'].dt.year
        df['DataEntradaMes']=df['DataEntrada'].dt.month
        df['DataEntradaAno']=pd.to_numeric(df['DataEntradaAno'], downcast='unsigned', errors='coerce')  # Converte para numérico
        df['DataEntradaMes']=pd.to_numeric(df['DataEntradaMes'], downcast='unsigned', errors='coerce')  # Converte para numérico
        return df

    @property
    def exph(self):
        return self.__exph
    
#exph = Exph("PDE2031-ajustado")
#print(exph.exph_dataframe)