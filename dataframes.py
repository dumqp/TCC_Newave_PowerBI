import pandas as pd
import dger
import sistema

class Dataframe:
    #def __init__(self, sistema):
        #sistema.le_sistema()
        #self.__df_intercambio = self.intercambio_dataframe(sistema.intercambio)

    def intercambio_dataframe(self, intercambio):
        # Converte o dicionário de intercâmbio para um DataFrame
        df = pd.DataFrame.from_dict(intercambio, orient='index', columns=['Valor'])
        df.index = pd.MultiIndex.from_tuples(df.index, names=['SubsistemaDE', 'SubsistemaPara', 'Ano', 'Mes'])
        df.reset_index(inplace=True)
        return df

    def df_intercambio(self):
        return self.__df_intercambio
    
# Instancia a classe Sistema
sistema = sistema.Sistema("deck-2408/sistema.dat", "5", "2024")
sistema.le_sistema()

# Instancia a classe Dataframe e chama o método
#df_instance = Dataframe(sistema)
df_instance = Dataframe()
df = df_instance.intercambio_dataframe(sistema.intercambio)
#df = df_instance.df_intercambio

# Exibe o DataFrame
print(df)
print(df.loc[11])
