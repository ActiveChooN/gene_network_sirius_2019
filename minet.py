import rpy2
import rpy2.robjects as ro
import rpy2.robjects.numpy2ri as rn
import numpy as np
import xml.dom.minidom as md
from sklearn.metrics import roc_curve, auc

dirname = "/home/user/Sirius/MutualInformation_2"
filename = dirname + "/experiment.txt"
filename2 = dirname + "/XMLparser/Graph.xml"

def run_minet(filename=filename):

    rn.activate()

    code = """library(minet)
    filename <- '""" + filename + """'
    first <- readLines(filename, n=1)
    names <- strsplit(first, '\t')
    names <- unlist(names, use.names=FALSE)
    d <- read.table(filename, skip=1, col.names = names)

    mim <- build.mim(d, estimator = "mi.empirical", disc = "equalfreq")

    weight_adjacency_matrix <- minet(mim, method="mrnetb", estimator="mi.empirical", disc="equalfreq");

    weight_adjacency_matrix;
    """

    f = ro.r(code)

    weight_adjacency_matrix = np.array(f)

    long_array = weight_adjacency_matrix[np.triu_indices(weight_adjacency_matrix.shape[0])]
    return long_array



def xml_graph_to_adjacency_matrix(filename=filename2):
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


long_array = run_minet()
true_matrix = xml_graph_to_adjacency_matrix()
true_array = true_matrix[np.triu_indices(true_matrix.shape[0])]

fpr, tpr, thresholds = roc_curve(true_array, long_array)
roc_auc = auc(fpr, tpr)

print(roc_auc)
