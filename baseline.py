import sacrebleu
from data_stored import get_stored_data

(referenceData, translationData, objectData) = get_stored_data()

# (referenceDataRaw, translationDataRaw, objectData) = get_stored_data()

# translationData = []
# for elem in translationDataRaw:
#     newElem = []
#     for trans in elem:
#         if trans[-2:] == ' .':
#             newElem.append(trans[:-2] + '.')
#         else:
#             newElem.append(trans)
#     translationData.append(newElem)

# referenceData = []
# for elem in referenceDataRaw:
#     if elem[-2:] == ' .':
#         # print('hi')
#         referenceData.append(elem[:-2] + '.')
#     else:
#         referenceData.append(elem)

azurePred = []
ibmPred = []
refs = []

for i in range(len(referenceData)):
    azurePred.append(translationData[i][0])
    ibmPred.append(translationData[i][1])
    refs.append(referenceData[i])

azureBleu = sacrebleu.corpus_bleu(azurePred, [refs])
print("Azure: " + str(azureBleu.score))

ibmBleu = sacrebleu.corpus_bleu(ibmPred, [refs])
print("IBM: " + str(ibmBleu.score))

# bleuIdentical = sacrebleu.corpus_bleu(refs, [refs])
# print("Identical: " + str(bleuIdentical.score))