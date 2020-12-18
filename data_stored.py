from index_map import indexes
from get_objects import get_objects

def get_stored_data(full=False):
    englishFile = open("en-es/source.final.file-found")
    spanishFile = open("en-es/reference.final.file-found")
    metadataFile = open("en-es/metadata.final.file-found")

    azureFile = open("machine-translations/azure.txt")
    ibmFile = open("machine-translations/ibm.txt")

    indexMap = indexes()
    objects = get_objects()

    referenceData = []
    translationData = []
    objectData = []

    if full:
        sourceData = []
        imageNameData = []

    for i in range(27367):
        # Machine translations
        azureLine = azureFile.readline()
        ibmLine = ibmFile.readline()
        translationData.append([azureLine[:-1], ibmLine[:-1]])

        # English reference caption
        referenceData.append(englishFile.readline())

        # Spanish source caption
        if full:
            sourceData.append(spanishFile.readline())

        # Image name
        metadataLine = metadataFile.readline()
        if full:
            imageNameData.append(metadataLine[:-1])

        # Objects
        imageIndex = indexMap[metadataLine[:-1]]
        imageNumber = int(imageIndex[3:]) - 1
        objectData.append(objects[imageNumber])
    
    if full:
        return (referenceData, translationData, objectData, imageNameData, sourceData)
    else:
        return (referenceData, translationData, objectData)