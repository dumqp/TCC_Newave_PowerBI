import pandas as pd
import dger
import ree
import confhd
import exph
import ghtot
import sistema

class Gsf:
    def __init__(self, caminho):
        self.__caminho= caminho + "/GarantiasFisicas/GarantiasFisicas.xlsx"
        self.__ree=ree.Ree(caminho)
        #self.__ree.le_ree()
        self.__subsistemas = self.__ree.n_subsistemas
        self.__rel_ree_subsitema = self.__ree.rel_ree_subsistema
        self.__dger=dger.Dger(caminho)
        #self.__dger.leDger()
        self.__nseries = int(self.__dger.n_series_sinteticas)
        self.__ghtot = ghtot.Ghtot(caminho)
        self.__ghtot= self.__ghtot.ghtotm_dataframe
        self.__pch = sistema.Sistema(caminho)
        self.__pch = self.__pch.geracaoPQ_dataframe
        self.__pch = self.__pch.loc[self.__pch['Tecnologia'] == 1]
        self.__confhd = confhd.Confhd(caminho)
        self.__confhd = self.__confhd.confhd_dataframe
        self.__exph = exph.Exph(caminho)
        self.__exph = self.__exph.exph_dataframe
    
    def importaDadosGarantiaFisicaUHE(self):
        df = pd.read_excel(self.__caminho, sheet_name="UHE")
        return df
    
    def relacionaExphGF(self):
        df = self.importaDadosGarantiaFisicaUHE()
        df2=self.__exph
        df_merged = pd.merge(df2, df[['CodUsina', 'Garantia Fisica (MWmed)']], on='CodUsina', how='left')
        return df_merged
 
    def gfDadosIniciaisUHE(self):
        #junta dados da planilha de garantia fisica com os dados do confhd
        df = self.__confhd[['CodUsina','UsinaExistente']]
        df2 = self.importaDadosGarantiaFisicaUHE()
        df_merged = pd.merge(df, df2[['CodUsina', 'Garantia Fisica (MWmed)']], on='CodUsina', how='left')
        # Renomear a coluna 'Garantia Fisica (MWmed)' para 'GF'
        df_merged.rename(columns={'Garantia Fisica (MWmed)': 'GF'}, inplace=True)
        df_merged['GF'] = df_merged['GF'].fillna(0)
        df_merged.loc[df_merged['UsinaExistente'] == 'NC', 'GF'] = 0
        df_merged['AnoInicioGF'] = 0  # Inicializa a nova coluna com 0 ou outro valor padrão
        df_merged.loc[df_merged['UsinaExistente'].isin(['EE', 'EX']), 'AnoInicioGF'] = self.__dger.ano_inicio_estudo
        df_merged['MesInicioGF'] = 0  # Inicializa a nova coluna com 0 ou outro valor padrão
        df_merged.loc[df_merged['UsinaExistente'].isin(['EE', 'EX']), 'MesInicioGF'] = self.__dger.mes_inicio_estudo      

        return df_merged
    
    def juntaDadosGeracao(self):
        df = pd.merge(self.__ghtot, self.__pch, on=['Subsistema', 'Ano', 'Mes'], how='left')
        df.rename(columns={'Valor': 'Geracao_PCH'}, inplace=True)
        df.drop(columns=['Tecnologia'])
        df['GeracaoTotal'] = df['Geracao-MWm'] + df['Geracao_PCH']
        df = df.groupby(['Ano', 'Mes', 'Serie'])['GeracaoTotal'].sum().reset_index()
        #retirar meses que não fazem parte da simulacao
        df = df[~((df['Ano'] == int(self.__dger.ano_inicio_estudo)) & (df['Mes'] < int(self.__dger.mes_inicio_estudo)))]
        return df

    def gfPch(self):
        df = self.__pch.groupby(['Subsistema', 'Ano'])['Valor'].mean().reset_index()
        #print(df.loc[df['Ano']==2022])
        df = df.groupby('Ano')['Valor'].sum().reset_index()
        #print(df.loc[df['Ano']==2022])
        df.rename(columns={'Valor': 'GF_PCH'}, inplace=True)
        return df
       
    #Garantia Fisica de UHEs Existentes
    #Retorna apenas um valor referente a GF existente no inicio do caso de simulacao
    def gfUhe_EX(self):
        df = self.gfDadosIniciaisUHE()
        # ordenar o dataframe por CodUsina e DataEntradaAno, 'DataEntradaMes para garantir que a soma seja feita corretamente
        df = df.sort_values(by=['CodUsina', 'AnoInicioGF', 'MesInicioGF'])
        df['GFAcumulada'] = df.groupby(['AnoInicioGF','MesInicioGF'])['GF'].cumsum()
        #print(df)
        #print(df.columns)
        df_filtrado = df[(df['AnoInicioGF'] == self.__dger.ano_inicio_estudo) & (df['MesInicioGF'] == self.__dger.mes_inicio_estudo)]
        GF_UHE_Ex = df_filtrado['GFAcumulada'].max()
        #df_resultado = self.somaAcumuladaUHE_NE(df)
        return GF_UHE_Ex

    #Garantia Fisica de UHEs da Expansão
    def gfUhe_NE(self):
        df = self.relacionaExphGF()
        #garantia física de usinas não existentes será estimada como 90% da potência que entrou
        df['GFIncremental'] = df['Potencia'] * 0.9
        # ordenar o dataframe por CodUsina e DataEntradaAno, 'DataEntradaMes para garantir que a soma seja feita corretamente
        df = df.sort_values(by=['CodUsina', 'DataEntradaAno', 'DataEntradaMes'])
        #print(df[['CodUsina','DataEntradaAno','DataEntradaMes','GFIncremental', 'Garantia Fisica (MWmed)']])
        #Soma a garantia fisica de forma acumulada por código de usina
        df_resultado = self.somaAcumuladaUHE_NE(df)
        df = df_resultado #df completo apenas para verificacao
        # Altera o dataframe para utilizar apenas os dados necessários
        df_resultado = df_resultado[['CodUsina','DataEntradaAno','DataEntradaMes','GF_UHE']]
        # Soma as garantias físicas por data
        df_resultado = df_resultado.groupby(['DataEntradaAno', 'DataEntradaMes'])['GF_UHE'].sum().reset_index()
        df_resultado.rename(columns={'DataEntradaAno': 'Ano','DataEntradaMes': 'Mes', 'GF_UHE' : 'GF_UHE_NE'}, inplace=True)
        #Cria dataframe com todas as datas da simulacao
        df_datas = self.criaDataframeDatas()
        #Junta os dados de garantia física por data com todas as datas da simulação
        df_resultado = pd.merge(df_resultado, df_datas, on=['Ano','Mes'], how='left')
        #muda para zero os valores NaN
        df_resultado['GF_UHE_NE'] = df_resultado['GF_UHE_NE'].fillna(0)
        # calcula a garantia fisica acumulada em cada data
        df_resultado['GF_UHE_NE_Acumulada'] = df_resultado['GF_UHE_NE'].cumsum()
        df_resultado.drop('GF_UHE_NE', axis=1, inplace=True)
        df_resultado.rename(columns={'GF_UHE_NE_Acumulada': 'GF_UHE_NE'}, inplace=True)
        return df_resultado

    def somaAcumuladaUHE_NE(self,df):
        #Faz a soma acumulada e verifica se o valor ultrapassa a GF total da usina
        df['GFAcumulada'] = df.groupby('CodUsina')['GFIncremental'].cumsum()
        df['GF_UHE'] = df[['GFAcumulada', 'Garantia Fisica (MWmed)']].apply(lambda x: min(x['GFAcumulada'], x['Garantia Fisica (MWmed)']), axis=1)
        return df
    
    def criaDataframeDatas(self):
        # Definir os dados iniciais
        inicio_ano = int(self.__dger.ano_inicio_estudo)
        inicio_mes = int(self.__dger.mes_inicio_estudo)
        anos_futuro = int(self.__dger.n_anos_estudo)

        # Criar uma lista de anos e meses
        datas = pd.date_range(start=f'{inicio_ano}-{inicio_mes}-01', periods=anos_futuro*12, freq='MS')

        # Criar o dataframe
        df = pd.DataFrame({'Ano': datas.year, 'Mes': datas.month})
        return df


    def juntaDadosGeracaoGF(self):
        df_geracao = self.juntaDadosGeracao()
        df_gf_pch = self.gfPch()
        gf_uhe_ex = self.gfUhe_EX()
        df_uhe_ne = self.gfUhe_NE()
        #print(df_uhe_ne)
        df = df_geracao
        df['GF_UHE_EX'] = gf_uhe_ex
        #print(df_uhe_ne.columns)
        #print(df.columns)
        df = pd.merge(df, df_uhe_ne, on=['Ano','Mes'], how='left')
        # Substituir NaN com o valor do mês anterior (acumulação)
        df['GF_UHE_NE'] = df['GF_UHE_NE'].fillna(method='ffill')
        # Se ainda restarem NaNs no início (por não haver dados acumulados anteriores), preencher com zero
        df['GF_UHE_NE'] = df['GF_UHE_NE'].fillna(0)
        print(df_gf_pch)
        df = pd.merge(df, df_gf_pch, on=['Ano'], how='left')
        df['GF_Total'] = df['GF_UHE_EX'] + df['GF_UHE_NE'] + df['GF_PCH']

        return df
    
    def calculaGSFMensal(self):
        df = self.juntaDadosGeracaoGF()
        df ['GSF_Mensal'] = df['GeracaoTotal'] / df ['GF_Total']
        #print(df.loc[df['Ano'] == 2024])
        #soma GF de UHE e PCH
        #divide a geração total pela GF total
        #faz o cálculo com as colunas
        return df

    def calculaGSFAnual(self):
        df = self.juntaDadosGeracaoGF()
        df_anual = df.groupby(['Ano','Serie'])['GeracaoTotal'].mean().reset_index()
        df_gf_anual = df.groupby(['Ano','Serie'])['GF_Total'].mean().reset_index()
        #print(df_anual)
        df_final = pd.merge(df_gf_anual, df_anual, on=['Ano','Serie'], how='left')
        #df ['GSF_Mensal'] = df['GeracaoTotal'] / df ['GF_Total']
        df_final ['GSF_Anual'] = df_final['GeracaoTotal'] / df_final ['GF_Total']
        print(df_final.loc[df_final['Ano'] == 2022])
        print(df_final.loc[df_final['Ano'] == 2030])
        #soma GF de UHE e PCH
        #divide a geração total pela GF total
        #faz o cálculo com as colunas
        return df_final


    @property
    def pch(self):
        return self.__pch
    
    @property
    def exph(self):
        return self.__exph

    
gsf = Gsf("PDE2031-ajustado")
#df = gsf.importaDadosGarantiaFisicaUHE()
df = gsf.gfDadosIniciaisUHE()
df2 = gsf.juntaDadosGeracao()
df3 = gsf.gfPch()
df4 = gsf.juntaDadosGeracaoGF()
df5= gsf.gfUhe_EX()
df6 = gsf.calculaGSFMensal()
df7 = gsf.calculaGSFAnual()
#print(df.loc[df['UsinaExistente'] == 'NE'])
#print(df2.loc[df2['Serie']==2])
#print(df3)
#print(df4.loc[df4['Serie']==2])
#print(df)
#print(gsf.exph)
#print(gsf.relacionaExphGF())
#print(gsf.pch)
print(gsf.gfUhe_NE())
#print(df5)

