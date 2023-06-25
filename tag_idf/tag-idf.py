from p_columbus.p_columbus import get_clusters
import pickle

def tag_idf(filelist):
    clusters = get_clusters(filelist)
    f = open(r"cls_Tag_LR.pickle", 'rb')
    cls_Tag = pickle.load(f)
    f.close()

