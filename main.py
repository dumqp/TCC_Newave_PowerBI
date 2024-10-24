import cmarg
import ghtot
import gtert
import sistema
import eafb
import intXX
import exportaDados as ed

caminho_caso = "PDE2031-ajustado"

#Dados de CMO e PLD
print("Lendo CMARG")
cmarg_obj = cmarg.Cmarg(caminho_caso)
df_cmo = cmarg_obj.cmarg_dataframe
df_pld = cmarg_obj.pld_dataframe

#Dados de geracao hidreletrica
print("Lendo GHTOT")
ghtotm = ghtot.Ghtot(caminho_caso)
df_ghtot=ghtotm.ghtotm_dataframe

#Dados de geracao termeletrica
print("Lendo GTERT")
gtert_obj = gtert.Gtert(caminho_caso)
df_gtert=gtert_obj.gtert_dataframe

#Dados de geracao eolica, solar e mmgd
print("Lendo SISTEMA")
sistema_obj = sistema.Sistema(caminho_caso)
df_eolica = sistema_obj.geracaoEolica_dataframe
df_solar = sistema_obj.geracaoSolar_dataframe
df_mmgd = sistema_obj.geracaoMMGD_dataframe

#Dados de demanda de energia (carga)
df_mercado = sistema_obj.mercado_dataframe

#Dados de energia natural afluente
print("Lendo EAFB")
ena = eafb.Eafb(caminho_caso)
df_ena_percentual = ena.ena_perc_mlt

#Dados intercambio entre subsistemas
print("Lendo INTERCAMBIO")
intercambio_obj = intXX.Intxx(caminho_caso)
df_intercambio = intercambio_obj.int_dataframe

#Exportar os dados para CSV
print("Lendo EXPORTANTO CSV")
ed.exportaDados.exportaCsv(df_cmo,'cmo')
ed.exportaDados.exportaCsv(df_pld,'pld')
ed.exportaDados.exportaCsv(df_ghtot,'ghtot')
ed.exportaDados.exportaCsv(df_gtert,'gtert')
ed.exportaDados.exportaCsv(df_eolica,'eolica')
ed.exportaDados.exportaCsv(df_solar,'solar')
ed.exportaDados.exportaCsv(df_mmgd,'mmgd')
ed.exportaDados.exportaCsv(df_ena_percentual,'ena_percentual')
ed.exportaDados.exportaCsv(df_intercambio,'intercambio')
ed.exportaDados.exportaCsv(df_mercado,'mercado')








