import pandas as pd

class Confhd:
    def __init__ (self, caminho):
        self.__confhd= {}
        self.__caminho = caminho + "/confhd.dat"
        self.leConfhd()
    
    def leConfhd(self):
        with open(self.__caminho, "r") as file:
            for i in range(2): #linhas de cabeçalho
                linha = file.readline()
            linha = file.readline()
            while linha:
                #NUM  NOME         POSTO JUS  SSIS V.INIC U.EXIS MODIF INIC.HIST FIM HIS DESVIOS
                codUsina = linha[1:5].strip()
                nomeUsina = linha[6:18].strip()
                posto = linha[19:23].strip()
                usinaJus = linha[25:29].strip()
                subsistema = linha[30:34].strip()
                volInicial=linha[35:41].strip()
                usinaExistente = linha[42:46].strip()
                modif = linha[49:53].strip()
                inicioHist = linha[58:62].strip()
                fimHist = linha[67:71].strip()
                self.__confhd [codUsina] = [nomeUsina,posto,usinaJus,subsistema,volInicial,usinaExistente,modif,inicioHist,fimHist]
                linha = file.readline()
            
    @property
    def confhd(self):
        return self.__confhd
    
    @property
    def confhd_dataframe(self): #dataframe apenas com cmo
        # Converte o dicionário de cmarg para um DataFrame
        df = pd.DataFrame.from_dict(self.__confhd, orient='index', columns=['NomeUsina','Posto','UsinaJusante','Subsistema','VolumeInicial',
                                                                            'UsinaExistente','Modificacao','InicioHistorico','FimHistorico'])
        df.index.name = 'CodUsina'
        df.reset_index(inplace=True)
        df['CodUsina']=pd.to_numeric(df['CodUsina'], downcast='unsigned', errors='coerce')  # Converte para numérico
        df['Subsistema']=pd.to_numeric(df['Subsistema'], downcast='unsigned', errors='coerce')  # Converte para numérico
        df['VolumeInicial']=pd.to_numeric(df['VolumeInicial'], errors='coerce')  # Converte para numérico
        df['Modificacao']=pd.to_numeric(df['Modificacao'], downcast='unsigned', errors='coerce')  # Converte para numérico
        df['InicioHistorico']=pd.to_numeric(df['InicioHistorico'], downcast='unsigned', errors='coerce')  # Converte para numérico
        df['FimHistorico']=pd.to_numeric(df['FimHistorico'], downcast='unsigned', errors='coerce')  # Converte para numérico
        return df
    




