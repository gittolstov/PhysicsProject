class Log_parser:#saves dictionaries into the file and reads them
    def __init__(self):
        self.filepath = "logs.txt"
        self.plaintext = ""
        self.pointers = []
        self.readfile()

    def fetch(self, header):
        return self.log0(self.cut(header))

    def save(self, header, obj):
        self.append(header, self.convert_to_log0(obj))

    def readfile(self):#inner function
        with open(self.filepath, "r", encoding="utf-8") as file:
            text = file.read()
            lst = text.split("¶", 1)
            lst[0] = lst[0].split(" ")#whitespace
            lst[1] = lst[1].split("	")#tab
            return lst

    def cut(self, name):#reads and returns a text with header [name] from the file
        pointers_texts = self.readfile()
        a = 0
        try:
            a = pointers_texts[0].index(name)
        except:
            print("no such index")
            print("pointers")
        return pointers_texts[1][a]

    def convert_to_log0(self, dct=dict):#converts log dictionary to encoded txt
        text = dct["simulation_type"]
        for i in dct:
            if i == "simulation_type":
                continue
            text += "{" + i + self.convert_to_log1(dct[i])
        return text

    def convert_to_log1(self, dct):
        txt = ""
        if type(dct) == type({}):
            for i in dct:
                txt += ":" + i + "[" + "[".join(map(str, dct[i]))
        elif type(dct) == type([]):
            txt += ":" + "self" + "[" + "[".join(map(str, dct))
        return txt

    def log0(self, text):#converts encoded text back to dictionary
        dictionary = {}
        a = text.split("{")
        dictionary["simulation_type"] = a[0]
        for i in range(1, len(a)):
            sectors = a[i].split(":")
            dictionary[sectors[0]] = self.log1(sectors)
        return dictionary

    def log1(self, arr):
        dct = {}
        for i in range(1, len(arr)):
            b = arr[i].split("[")
            if b[0] == "self":
                dct = list(map(float, b[1:]))
                break
            dct[b[0]] = list(map(float, b[1:]))
        return dct

    def append(self, header, text):#adds a text with a header into the file. The header should be unique
        if header.count(" ") > 0:
            print("can't use header with whitespaces")
            return
        pointers_texts = self.readfile()
        if header in pointers_texts[0]:
            print("header already exists")
            return
        pointers_texts[0].append(header)
        pointers_texts[1].append(text)
        with open(self.filepath, "w", encoding="utf-8") as file:
            file.write(" ".join(pointers_texts[0]) + "¶" + "	".join(pointers_texts[1]))##conv


def add_to_log(log, appendage):
    for a in log:
        if log[a] is dict:
            for b in log[a]:
                log[a][b] = appendage[a][b]


def cut_log(log, index):
    for a in log:
        if isinstance(log[a], dict):
            for b in log[a]:
                log[a][b] = log[a][b][:index]


if __name__ == "__main__":
    PARSER = Log_parser()
    print(PARSER.fetch("testlog"))
