import sacrebleu

refs = [[' the giants of Granollers , in front of the façade of the town Council , expecting the beginning of the ceremony of the public announcement of local festivity .']]
sys = ["the giants of Granollers, in front of the façade of the Town council, waiting for the start of the public proclamation of local festivity."]
bleu = sacrebleu.corpus_bleu(sys, refs)
print(bleu.score)