class Ree:
    def __init__(self, caminho):
        self.__caminho = caminho + "/ree.dat"
        self.__ree = []
        self.__subsistema = []
        self.__relacaoReeSubsistema = {}
        self.le_ree()

    def le_ree(self):
        with open(self.__caminho, "r") as file:
            for i in range(3):  #linhas de cabeçalho
                linha=file.readline()
            while True:
                linha = file.readline()
                if linha[0:4].strip() != "999":
                    ree = int(linha[0:4].strip())
                    subsistema = int(linha[18:22].strip())
                    self.__ree.append(ree)
                    self.__subsistema.append(subsistema)
                    self.__relacaoReeSubsistema[ree] = subsistema
                if linha[0:4].strip() == "999": break
            # Ordena a lista e retira repetidos
            self.__ree=sorted(list(set(int(val) for val in self.__ree)))
            self.__subsistema=sorted(list(set(int(val) for val in self.__subsistema)))
            # transforma valores para string
            self.__ree = [str(val) for val in self.__ree]
            self.__subsistema = [str(val) for val in self.__subsistema]

    @property
    def n_ree(self):
        return self.__ree
    @property
    def n_subsistemas(self):
        return self.__subsistema
    
    @property
    def rel_ree_subsistema(self):
        return self.__relacaoReeSubsistema
