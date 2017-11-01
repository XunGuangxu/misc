import numpy as np
import math
from scipy import sparse
    
def read_vocab(voca_pt):
    w2id, id2w = {}, {}
    for wid, l in enumerate(open(voca_pt)):
        ws = l.strip().split('\t')
        w2id[ws[0]] = wid
        id2w[wid] = ws[0]
    return w2id, id2w

def generatePyMatrix(years, DATA_DIR, output_path, n_words):
    for year in years:
        print('generating py matrix for year %d' % year)
        rows, cols, vals = [], [], []
        for l in open(DATA_DIR+str(year) + '.cooccur'):
            ws = l.strip().split('\t')
            assert len(ws)==3, 'length error:\t'+l
            if int(float(ws[2])) == 0: continue
            rows.append(int(ws[0]))
            cols.append(int(ws[1]))
            vals.append(int(float(ws[2])))
        mat_py = sparse.coo_matrix((vals, (rows, cols)), shape=(n_words, n_words), dtype='int32').tocsr()
        sparse.save_npz(output_path+str(year), mat_py)

def get_row(Y, i):
    '''Given a scipy.sparse.csr_matrix Y, get the values and indices of the
    non-zero values in i_th row'''
    lo, hi = Y.indptr[i], Y.indptr[i + 1]
    return Y.data[lo:hi], Y.indices[lo:hi]
       
def generateTrainingSamples(training_pt, py_mat_path, entropy_path, years, w2id):
    py_matrices = {}
    n_words_year = {}
    for year in years:
        py_matrices[year] = sparse.load_npz(py_mat_path+str(year)+'.npz')
        n_words_year[year] = py_matrices[year].data.sum()
    for l in open(training_pt):
        term, year, label = l.strip().split('\t')
        wid = w2id[term]
        entropy = []
        for i in range(10):
            cur_year = int(year) - 9 + i
            x_w, idx_w = get_row(py_matrices[cur_year], wid)
            sum_w = sum(x_w)
            cur_entropy = 0.0
            for cw in x_w:
                cur_entropy += cw * math.log(sum_w / cw)
            cur_entropy = cur_entropy / n_words_year[cur_year]
            entropy.append(cur_entropy)
        output_pt = entropy_path + 'entropy-' + year + '-' + term + '-' + label
        np.save(output_pt, np.nan_to_num(np.array(entropy)))

if __name__ == "__main__":
    DATA_DIR = 'C:/Users/vishrawa/Desktop/guang/ontology/cumCooccur/'
    vocab_pt = 'vocab.txt'
    training_pt = 'training_samples.txt'
    py_mat_path = 'py-cooccur-matrices/'
    entropy_path = 'entropies/'
    w2id, id2w = read_vocab(DATA_DIR+vocab_pt)
    years = [i for i in range(1992, 2017)]#was 89,17
#    generatePyMatrix(years, DATA_DIR, DATA_DIR+py_mat_path, len(w2id))
    generateTrainingSamples(DATA_DIR+training_pt, DATA_DIR+py_mat_path, DATA_DIR+entropy_path, years, w2id)
