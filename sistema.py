import dger

class Sistema:
    def __init__(self, caminho, n_anos, ano_inicio):
        self.__n_anos = n_anos
        self.__ano_inicio = ano_inicio
        self.__caminho = caminho
        self.__n_patamares_deficit = "0"
        self.__custo_deficit = {}
        self.__intercambio = {}
        self.__mercado = {}
        self.__geracaoPQ = {}

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
                while linha [0:4] != " 999":
                    linha = file.readline()
                    self.__custo_deficit.update({linha[1:4].strip():linha[19:26].strip()}) # cod sistema : valor deficit pat1
            
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

sistema = Sistema("deck-2408/sistema.dat","5","2024")
sistema.le_sistema()