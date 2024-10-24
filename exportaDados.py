import pandas as pd
import os

class exportaDados:
    def criaDiretorio(diretorio):
        if not os.path.isdir(diretorio):
            os.mkdir(diretorio)
        return None

    def exportaCsv(df,nomeArquivo):
        exportaDados.criaDiretorio('saidas_csv')
        return df.to_csv('saidas_csv/' + nomeArquivo + '.csv', index=False, sep=";")
    
    def exportaExcel(df,nomeArquivo):
        exportaDados.criaDiretorio('saidas_xlsx')
        return df.to_excel('saidas_xlsx/' + nomeArquivo + '.xlsx', index=False)