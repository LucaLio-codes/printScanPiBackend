from enum import Enum, auto
class FileType(Enum):
    PDF = "pdf"
    PNG = "png"
    TXT = "txt"

    @classmethod
    def getAll(cls):
        return list(map(lambda f: f.value, cls))

    def __str__(self):
        return self.value
