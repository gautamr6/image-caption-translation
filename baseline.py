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
selectPred = []
refs = []

for i in range(len(referenceData)):
    azureTrans = translationData[i][0]
    ibmTrans = translationData[i][1]
    ref = referenceData[i]

    azureScore = sacrebleu.corpus_bleu([azureTrans], [[ref]])
    ibmScore = sacrebleu.corpus_bleu([ibmTrans], [[ref]])
    selectTrans = azureTrans if azureScore.score > ibmScore.score else ibmTrans

    azurePred.append(azureTrans)
    ibmPred.append(ibmTrans)
    selectPred.append(selectTrans)
    refs.append(ref)

azureBleu = sacrebleu.corpus_bleu(azurePred, [refs])
print("Azure: " + str(azureBleu.score))

ibmBleu = sacrebleu.corpus_bleu(ibmPred, [refs])
print("IBM: " + str(ibmBleu.score))

selectBleu = sacrebleu.corpus_bleu(selectPred, [refs])
print("Correct Selections: " + str(selectBleu.score))

# bleuIdentical = sacrebleu.corpus_bleu(refs, [refs])
# print("Identical: " + str(bleuIdentical.score))