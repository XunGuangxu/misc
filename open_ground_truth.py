w2cnt = {}
w2cntWithA = {}
w2gtScore = {}
prev_occur = set()
end_year = 2013
#start_year = 1986
#termA = 'raynaud disease'#, 'fish oils' # test case 1
#start_year = 1989
#termA = 'migraine disorders'#, 'magnesium' # test case 2
#start_year = 1995
#termA = 'alzheimer disease'#, 'indomethacin' # test case 3
#start_year = 1990
#termA = 'arginine'#, 'insulin-like growth factor i' # test case 4
start_year = 1998
termA = 'schizophrenia'#, 'phospholipases a2, calcium-independent' # test case 5
DATA_DIR = 'C:/Users/vishrawa/Desktop/guang/cooccur/'

print('counting previous cooccurence ' + str(start_year-1))
for l in open('C:/Users/vishrawa/Desktop/guang/PostCooccur/' + str(start_year-1)):
    ws = l.strip().split('\t')
    assert len(ws) == 3, 'length is not 3'
    if ws[1] == termA:
        prev_occur.add(ws[0])

for year in range(start_year, end_year+1):
    cooccur_pt = DATA_DIR + str(year)
    print('working on the year of ' + str(year))
    for l in open(cooccur_pt):
        ws = l.strip().split('\t')
        assert len(ws) == 3, 'length is not 3'
        w2cnt[ws[0]] = w2cnt.get(ws[0], 0) + float(ws[2])
        #w2cnt[ws[1]] = w2cnt.get(ws[1], 0) + float(ws[2])
        if ws[1] == termA and ws[0] not in prev_occur:
            w2cntWithA[ws[0]] = w2cntWithA.get(ws[0], 0) + float(ws[2])
            
for w, cnt in w2cnt.items():
    if w in w2cntWithA:
        w2gtScore[w] = w2cntWithA[w] / w2cnt[w]
        
output_pt = DATA_DIR + 'groundtruth-' + termA + '.txt'
output = open(output_pt, 'w')
for w, score in sorted(w2gtScore.items(), key=lambda d:d[1], reverse=True):
    output.writelines('%s\t%f\n' % (w, score))
output.close()
