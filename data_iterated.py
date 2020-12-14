from index_map import indexes
from get_objects import get_objects
from PIL import Image
import numpy as np

class Data:
    def __init__(self) -> None:
        self.englishFile = open("en-es/source.final.file-found")
        self.spanishFile = open("en-es/reference.final.file-found")
        self.metadataFile = open("en-es/metadata.final.file-found")

        self.azureFile = open("machine-translations/azure.txt")
        self.ibmFile = open("machine-translations/ibm.txt")

        self.indexMap = indexes()
        self.objects = get_objects()
            
    def __iter__(self):
        self.index = 1
        return self
    
    def __next__(self):
        if self.index < 27367:
            # Machine translations
            azureLine = self.azureFile.readline()
            ibmLine = self.ibmFile.readline()
            translations = [azureLine, ibmLine]

            # Original Spanish caption
            spanishLine = self.spanishFile.readline()

            # English reference caption
            englishLine = self.englishFile.readline()

            # Image
            metadataLine = self.metadataFile.readline()
            imageIndex = self.indexMap[metadataLine[:-1]]
            imageFilename = "images-en-es/files/" + imageIndex[:-1]

            try:
                imageFile = Image.open(imageFilename)
                imageArray = np.asarray(imageFile)
            except:
                imageArray = np.zeros([100, 100, 3])

            # Objects
            imageNumber = int(imageIndex[3:]) - 1
            imageObjects = self.objects[imageNumber]

            self.index += 1
            return (imageArray, imageObjects, spanishLine, translations, englishLine)
        else:
            raise StopIteration