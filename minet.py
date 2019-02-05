import rpy2
import rpy2.robjects as ro
import rpy2.robjects.numpy2ri as rn
import numpy as np
import xml.dom.minidom as md
from sklearn.metrics import roc_curve, auc

'''res = [[0.60372905 0.62657756 0.56825025 0.62948082 0.68960059 0.59300139
  0.66541912 0.70009408 0.61183355]
 [0.60213914 0.59547026 0.58100637 0.52582041 0.54694731 0.52462026
  0.53027191 0.53841472 0.52438248]
 [0.57805153 0.62058477 0.58254752 0.60767324 0.65879136 0.58630081
  0.6214121  0.67315259 0.60500149]
 [0.60383887 0.61852466 0.56976022 0.62400038 0.67456203 0.59577896
  0.65409632 0.6837244  0.61136003]]'''


datadirname = "/home/user/Sirius/MutualInformation_2/MI/Data"
datafilename = datadirname + "/{0}/{0}_data.txt"
graphfilename = datadirname + "/{0}/{0}_graph.xml"

algolist = ['clr', 'aracne', 'mrnet', 'mrnetb']

datalist = ['exps_10', 'exps_10_2', 'exps_10_bgr', 'exps_50', 'exps_50_2', 'exps_50_bgr', 'exps_100', 'exps_100_2', 'exps_100_bgr']

def run_minet(filename, algo):

    rn.activate()

    code = """library(minet)
    filename <- '""" + filename + """'
    first <- readLines(filename, n=1)
    names <- strsplit(first, '\t')
    names <- unlist(names, use.names=FALSE)
    d <- read.table(filename, skip=1, col.names = names)

    mim <- build.mim(d, estimator = "mi.empirical", disc = "equalfreq")

    weight_adjacency_matrix <- minet(mim, method='""" + algo + """', estimator="mi.empirical", disc="equalfreq");

    weight_adjacency_matrix;
    """

    f = ro.r(code)

    weight_adjacency_matrix = np.array(f)

    long_array = weight_adjacency_matrix[np.triu_indices(weight_adjacency_matrix.shape[0])]
    return long_array



def xml_graph_to_adjacency_matrix(filename):
    dom = md.parse(filename)

    # print(dom.toprettyxml())

    nodes = dom.getElementsByTagName("Node")
    ids = [int(a.getAttribute('id')) for a in nodes]
    # parserint(ids)
    adjacency_matrix = np.zeros(shape=(len(ids), len(ids)))
    edges = dom.getElementsByTagName("Edge")
    for e in edges:
        source = int(e.getElementsByTagName('from')[0].firstChild.nodeValue)
        target = int(e.getElementsByTagName('to')[0].firstChild.nodeValue)
        adjacency_matrix[source][target] = 1
        adjacency_matrix[target][source] = 1
    return adjacency_matrix

aucs = np.zeros(shape=(len(algolist), len(datalist)))

for i, algo in enumerate(algolist):

    for j, dataname in enumerate(datalist):

        long_array = run_minet(datafilename.format(dataname), algo)
        true_matrix = xml_graph_to_adjacency_matrix(graphfilename.format(dataname))
        true_array = true_matrix[np.triu_indices(true_matrix.shape[0])]

        fpr, tpr, thresholds = roc_curve(true_array, long_array)
        roc_auc = auc(fpr, tpr)
        aucs[i][j] = roc_auc

print(aucs)