import sacrebleu
from data import Data

dt = Data()
dt_iter = iter(dt)

pred = []
refs = []

for inst in dt_iter:
    pred.append(inst[2][0])
    refs.append(inst[3])

bleu = sacrebleu.corpus_bleu(pred, [refs])
print(bleu.score)

# bleuIdentical = sacrebleu.corpus_bleu(refs, [refs])
# print(bleuIdentical.score)