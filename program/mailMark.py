class mailMark:
    def __init__(self, seriesCode, name, text):
        self.seriesCode = seriesCode
        self.name = name
        self.text = text

    def isSameMark(self, seriesCd, name):
        if self.seriesCode == seriesCd and self.name == name:
            return True
        return False
