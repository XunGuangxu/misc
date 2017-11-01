'''
Generating time.cooccur and time.vocab_flag and vocabulary.txt
time.cooccur: wid wid freq
time.vocab_flag: 100111....(vocab size) indicating this word has ever appeared in history
'''
w2cnt = {}
w2id = {}
#DATA_DIR = 'C:/Users/vishrawa/Desktop/guang/mesh_data/'
#DATA_DIR = 'C:/Users/vishrawa/Desktop/guang/PPMI_cooccur/'
DATA_DIR = 'C:/Users/vishrawa/Desktop/guang/ontology/cumCooccur/'

def processVocab(doc_pt, vocab_pt, vocab_freq_pt):
    print('counting vocabulary...')
    for line_file in open(filelist_pt):
        print('\tin ' + line_file.strip())
        for l in open(DATA_DIR+line_file.strip()):
            ws = l.strip().split('\t')
            assert len(ws) == 3, 'length is not 3'
            for w in ws[0:2]:
                w2cnt[w] = w2cnt.get(w,0) + 1
                if w not in w2id:
                    w2id[w] = len(w2id) #id starts from 0
    
    print('writing vocabulary...')
    vocab = open(vocab_pt, 'w')
    for w, wid in sorted(w2id.items(), key=lambda d:d[1]):#, reverse=True):
        vocab.writelines('%s\t%d:%d\n' % (w, wid, w2cnt[w]))
    vocab.close()
    vocab_freq = open(vocab_freq_pt, 'w')
    for w, freq in sorted(w2cnt.items(), key=lambda d:d[1], reverse=True):
        vocab_freq.writelines('%s\t%d\t%d\n' % (w, freq, w2id[w]))
    vocab_freq.close()

def read_vocab(voca_pt):
    w2id, w2cnt = {}, {}
    for l in open(voca_pt):
        ws = l.strip().split('\t')
        wid, wcnt = ws[1].strip().split(':')
        w2id[ws[0]] = int(wid)
        w2cnt[ws[0]] = int(wcnt)
    return w2id, w2cnt
    
def processIndividualFile(indi_pt):
    print('processing ' + indi_pt)
    #print(sum(vocab_flag))
    cooccur_pt = open(indi_pt+'.cooccur', 'w')
    for l in open(indi_pt):
        ws = l.strip().split('\t')
        assert len(ws) == 3, 'length is not 3'+indi_pt
        if ws[0] == ws[1]:
            continue
        cooccur_pt.writelines('%d\t%d\t%s\n' % (w2id[ws[0]], w2id[ws[1]], ws[2]))
        vocab_flag[w2id[ws[0]]] = 1
        vocab_flag[w2id[ws[1]]] = 1
    cooccur_pt.close()
    flag_pt = open(indi_pt+'.vocab_flag', 'w')
    for flag in vocab_flag:
        flag_pt.writelines('%d\n' % (flag))
    flag_pt.close()
    #print(sum(vocab_flag))

if __name__ == '__main__':
    #doc_pt = DATA_DIR+'2013' #use the very last cumulative file to generate vocabulary
    vocab_pt = DATA_DIR+'vocab.txt'
    vocab_freq_pt = DATA_DIR+'vocab_freq.txt'
    filelist_pt = DATA_DIR+'filelist.txt'
    #processVocab(filelist_pt, vocab_pt, vocab_freq_pt)
    w2id, w2cnt = read_vocab(vocab_pt)
    
    vocab_flag = [0] * len(w2id)
    for l in open(filelist_pt):
        processIndividualFile(DATA_DIR+l.strip())
    print('done')
