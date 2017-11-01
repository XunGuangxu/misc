w2cnt = {}
w2cntWithA = {}
w2cntWithB = {}
w2gtScore = {}
end_year = 2013
start_year = 1986
termA, termB = 'fish oils', 'raynaud disease' # test case 1
#start_year = 1989
#termA, termB = 'migraine disorders', 'magnesium' # test case 2
#start_year = 1995
#termA, termB = 'indomethacin', 'alzheimer disease' # test case 3
#start_year = 1990
#termA, termB = 'insulin-like growth factor i', 'arginine' # test case 4
#start_year = 1998
#termA, termB = 'schizophrenia', 'phospholipases a2, calcium-independent' # test case 5
DATA_DIR = 'C:/Users/vishrawa/Desktop/guang/cooccur/'

for year in range(start_year, end_year+1):
    cooccur_pt = DATA_DIR + str(year)
    print('working on the year of ' + str(year))
    for l in open(cooccur_pt):
        ws = l.strip().split('\t')
        assert len(ws) == 3, 'length is not 3'
        w2cnt[ws[0]] = w2cnt.get(ws[0], 0) + float(ws[2])
        #w2cnt[ws[1]] = w2cnt.get(ws[1], 0) + float(ws[2])
        if ws[1] == termA:
            w2cntWithA[ws[0]] = w2cntWithA.get(ws[0], 0) + float(ws[2])
        if ws[1] == termB:
            w2cntWithB[ws[0]] = w2cntWithB.get(ws[0], 0) + float(ws[2])
            
for w, cnt in w2cnt.items():
    if w in w2cntWithA and w in w2cntWithB:
        w2gtScore[w] = pow(2.718281828459045, (w2cntWithA[w] + w2cntWithB[w]) / w2cnt[w])
        
output_pt = DATA_DIR + 'groundtruth-' + termA + '-' + termB + '.txt'
output = open(output_pt, 'w')
for w, score in sorted(w2gtScore.items(), key=lambda d:d[1], reverse=True):
    output.writelines('%s\t%lf\n' % (w, score))
output.close()
