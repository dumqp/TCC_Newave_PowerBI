# Le dados do arquivo dger
#
# Parâmetros do dger.dat
#
# ['PMO - AGOSTO - 2024 -', 'TIPO DE EXECUCAO', 'DURACAO DO PERIODO', 'No. DE ANOS DO EST', 'MES INICIO PRE-EST',
#  'MES INICIO DO ESTUDO', 'ANO INICIO DO ESTUDO', 'No. DE ANOS PRE', 'No. DE ANOS POS', 'No. DE ANOS POS FINAL',
#  'IMPRIME DADOS', 'IMPRIME MERCADOS', 'IMPRIME ENERGIAS', 'IMPRIME M. ESTOCAS', 'IMPRIME SUBSISTEMA', 'No MAX. DE ITER.',
#  'No DE SIM. FORWARD', 'No DE ABERTURAS', 'No DE SERIES SINT.', 'ORDEM MAX. PAR(P)', 'ANO INICIAL HIST.', 'CALCULA VOL.INICIAL',
#  'VOLUME INICIAL  -%', 'POR REE', 'TOLERANCIA      -%', 'TAXA DE DESCONTO-%', 'TIPO SIMUL. FINAL', 'IMPRESSAO DA OPER',
#  'IMPRESSAO DA CONVERG.', 'INTERVALO P/ GRAVAR', 'No. MIN. ITER.', 'RACIONAMENTO PREVENT.', "No. ANOS MANUT.UTE'S", 
#  'TENDENCIA HIDROLOGICA', 'RESTRICA0 DE ITAIPU', 'BID', 'PERDAS P/ TRANSMISSAO', 'EL NINO', 'ENSO INDEX', 'DURACAO POR PATAMAR',
#  'OUTROS USOS DA AGUA', 'CORRECAO DESVIO', 'C.AVERSAO/PENAL.VMINP', 'TIPO DE GERACAO ENAS', 'RISCO DE DEFICIT', 
#  'ITERACAO P/SIM.FINAL', 'AGRUPAMENTO LIVRE', 'EQUALIZACAO PEN.INT.', 'REPRESENT.SUBMOT.', 'ORDENACAO AUTOMATICA', 
#  'CONS. CARGA ADICIONAL', 'DELTA ZSUP', 'DELTA ZINF', 'DELTAS CONSECUT.', 'DESP. ANTEC.  GNL', 'MODIF.AUTOM.ADTERM', 
#  'CONSIDERA GHMIN', 'S.F. COM DATA', 'GER.PLs E NV1 E NV2', 'SAR', 'CVAR', 'CONS. ZSUP MIN. CONV.', 'DESCONSIDERA VAZMIN', 
#  'RESTRICOES ELETRICAS', 'SELECAO DE CORTES', 'JANELA DE CORTES', 'REAMOST. CENARIOS', 'CONVERGE NO ZERO', 'CONSULTA FCF', 
#  'IMPRESSAO AFL/VENTO', 'IMP. CATIVO S.FINAL', 'REP. AGREGACAO', 'MATRIZ CORR.ESPACIAL', 'DESCONS. CONV. ESTAT', 
#  'MOMENTO REAMOSTRAGEM', 'ARQUIVOS ENA', 'INICIO TESTE CONVERG.', 'SAZ. VMINT PER. EST.', 'SAZ. VMAXT PER. EST.', 
#  'SAZ. VMINP PER. EST.', 'SAZ. CFUGA E CMONT', 'REST. EMISSAO GEE', 'AFLUENCIA ANUAL PARP', 'REST. FORNEC. GAS', 
#  'MEM. CALCULO CORTES', 'GERACAO EOLICA', 'REST. TURBINAMENTO', 'REST. DEFL. MAXIMA', 'BASE PLS BACKWARD', 
#  'ESTADOS GER. CORTES', 'REST.LPP TURB.MAX REE', 'REST.LPP DEFL.MAX REE', 'REST.LPP TURB.MAX UHE', 'REST.LPP DEFL.MAX UHE', 
#  'REST.ELETRI ESPECIAIS', 'FUNCAO DE PROD. UHE', 'FCF POS ESTUDO', 'ESTACOES BOMBEAMENTO', 'CANAL DE DESVIO', 
#  'REST.HID. VAZAO(RHQ)', 'REST.HID. VOLUME(RHV)', 'TRATA ARQS CORTES']
#
class Dger:
    #cria objeto com os dados do arquivo dger.dat
    def __init__ (self, caminho):
        self.__content= {}
        self.__caminho = caminho + "/dger.dat"
        self.leDger()

    def leDger(self):
        with open (self.__caminho,'r') as file:
            for line in file:
                chave = line[0:21].strip()
                valor = line[21:25].strip()
                self.__content.update({chave : valor})
        return None
    
    @property
    def tipo_exec(self):
        return self.__content['TIPO DE EXECUCAO']

    @property
    def duracao_periodo(self):
        return self.__content['DURACAO DO PERIODO']

    @property
    def n_anos_estudo(self):
        return self.__content['No. DE ANOS DO EST']
    
    @property
    def mes_inicio_pre_estudo(self):
        return self.__content['MES INICIO PRE-EST']
    
    @property
    def mes_inicio_estudo(self):
        return self.__content['MES INICIO DO ESTUDO']
    
    @property
    def ano_inicio_estudo(self):
        return self.__content['ANO INICIO DO ESTUDO']

    @property
    def n_anos_pre(self):
        return self.__content['No. DE ANOS PRE']

    @property
    def n_anos_pos(self):
        return self.__content['No. DE ANOS POS']

    @property
    def n_anos_pos_final(self):
        return self.__content['No. DE ANOS POS FINAL']

    @property
    def n_series_sinteticas(self):
        return self.__content['No DE SERIES SINT.']    
