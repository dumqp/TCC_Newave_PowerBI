class Ree:
    def __init__(self, caminho):
        self.__caminho = caminho + "/ree.dat"
        self.__ree = []
        self.__subsistema = []

    def le_ree(self):
        with open(self.__caminho, "r") as file:
            for i in range(3):  #linhas de cabeçalho
                linha=file.readline()
            while True:
                linha = file.readline()
                if linha[0:4].strip() != "999":
                    self.__ree.append(int(linha[0:4].strip()))
                    self.__subsistema.append(int(linha[18:22].strip()))
                if linha[0:4].strip() == "999": break
            # Ordena a lista e retira repetidos
            self.__ree=sorted(list(set(self.__ree)))
            self.__subsistema=sorted(list(set(self.__subsistema)))
            # transforma valores para string
            self.__ree = [str(val) for val in self.__ree]
            self.__subsistema = [str(val) for val in self.__subsistema]

    @property
    def n_ree(self):
        return self.__ree
    @property
    def n_subsistemas(self):
        return self.__subsistema
    
#ree = Ree("deck-2408")
#ree.le_ree()
#print(ree.n_ree)
#print(ree.n_subsistemas)