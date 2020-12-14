from index_map import indexes
from get_objects import get_objects

def get_stored_data():
    englishFile = open("en-es/source.final.file-found")
    metadataFile = open("en-es/metadata.final.file-found")

    azureFile = open("machine-translations/azure.txt")
    ibmFile = open("machine-translations/ibm.txt")

    indexMap = indexes()
    objects = get_objects()

    referenceData = []
    translationData = []
    objectData = []

    for i in range(27367):
        # Machine translations
        azureLine = azureFile.readline()
        ibmLine = ibmFile.readline()
        translationData.append([azureLine[:-1], ibmLine[:-1]])

        # English reference caption
        referenceData.append(englishFile.readline())

        # Objects
        metadataLine = metadataFile.readline()
        imageIndex = indexMap[metadataLine[:-1]]
        imageNumber = int(imageIndex[3:]) - 1
        objectData.append(objects[imageNumber])
    
    return (referenceData, translationData, objectData)