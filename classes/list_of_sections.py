class ListOfSections:
    def __init__(self):
        self.sections = []

    def addSection(self, section):
        self.sections.append(section)

    def getSection(self, id):
        return self.sections[id]
