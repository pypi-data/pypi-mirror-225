import numpy as np
import gurobipy as grb
from numba import jit, int64

def binarization(mat, binarization_threshold = 0):
    mat_bi = (mat > binarization_threshold)*1
    return mat_bi

def SensList(mat, CellTypeLabels, CellTypeNames):
    sens_list=[]
    for i in range(len(CellTypeNames)):
        ct = CellTypeNames[i]
        data = mat_bi[CellTypeLabels == ct,:]
        sens = (data.sum(axis = 1) / data.shape[1]).values
        sens_list.append(sens)
        return np.array(sens_list)



def covering(Z, minSize=1, alpha=0.05, weights = 1., prev = None ,output=None, callBack = None,
             poolSolutions=None, poolSearchMode=None, poolGap = None, timeLimit=None, mipfocus = None):

    if np.isscalar(minSize):
        minSize = [minSize]
    if np.isscalar(alpha):
        alpha = [alpha]*len(minSize)
    N = Z.shape[0]
    d = Z.shape[1]
    if type(weights) == str and weights=='prob':
        w = 1 - 0.01 * np.mean(Z, axis=0)
    elif np.isscalar(weights):
        w = weights * np.ones(d)
    else:
        w = weights
    cov = grb.Model()
    if output is not None:
        cov.Params.OutputFlag=output
    if poolSolutions is not None:
        cov.Params.PoolSolutions = poolSolutions
    if poolSearchMode is not None:
        cov.Params.PoolSearchMode = poolSearchMode
    if poolGap is not None:
        cov.Params.PoolGap = poolGap
    if timeLimit is not None:
        cov.Params.TimeLimit = timeLimit
    #cov.Params.LogToConsole = 0
    if mipfocus is not None:
        cov.Params.MIPFocus = mipfocus
    nlevels = len(minSize)
    x = []
    y = []
    for l in range(nlevels):
        x.append(cov.addMVar(d, vtype=grb.GRB.BINARY))
    for l in range(nlevels):
        y.append(cov.addMVar(N, vtype=grb.GRB.BINARY))

    for l in range(nlevels):
        expr = y[l].sum()
        cov.addConstr(expr >= N*(1-alpha[l]), 'Coverage_'+str(l))


    for l in range(nlevels):
        expr = Z @ x[l] - minSize[l]*y[l]
        cov.addConstr(expr >= 0, 'covered_' + str(l))
    if prev is not None:
        previous_ans = [int(i) for i in prev.x]
        for j in range(d):
            cov.addConstr(x[0].tolist()[j] - previous_ans[j] >= 0, "nested")

    expr = grb.LinExpr()
    c = {j: w[j] for j in range(d)}
    for l in range(nlevels):
        expr += w.T @ x[l]
    # for j in range(d):
    #     expr += w[j]*x[j + (nlevels-1)*d]
    cov.setObjective(expr, grb.GRB.MINIMIZE)

    if callBack is None:
        cov.optimize()
    else:
        cov.optimize(callBack)
    return cov

def getCoveringVariables(cov, ngenes, geneNames = None, nlevels = 1):
    covx = np.array(cov.x)
    genes = []
    if geneNames is None:
        geneNames = [str(x) for x in range(ngenes)]
    for l in range(nlevels):
        I = np.nonzero(covx[ngenes*l:ngenes*(l+1)] > 0.5)[0]
        genes.append([geneNames[k] for k in I])
    #print(genes)
    return genes[0]

def weight_component(sens,celltypes,ct,w_type = "mean"):
    ct_index = np.where(celltypes == ct)[0].item()
    not_ct_index = [i for i in range(len(celltypes)) if i != ct_index]
    denominator = sens[ct_index]
    if w_type == "mean":         
        numerator = sens[not_ct_index].mean(axis = 0)
    if w_type == "max":
        numerator = sens[not_ct_index].max(axis = 0)
    return numerator, denominator

def weight(X,sens,celltypes,ct,gene,te = 0.1,top_num_gene = 6000,w_type = "mean",epsilon = 0.00001):
    #CT = np.unique(y)
    if w_type != "rank":
        numerator, denominator = weight_component(sens,celltypes,ct,w_type)
    margin = denominator/(numerator + epsilon)
    #print(len(margin))
    #w = numerator / (denominator + epsilon)
    result = np.argpartition(margin,-top_num_gene)
    td = margin[result[-top_num_gene:]].min()
    #print(td)
    #print(td)
    if td < 1:
        td = 1
    
    index_to_keep = []
    for i in range(len(gene)):
        if (denominator[i] >= te) and (margin[i] > td):
            index_to_keep.append(i)
    X_new = X[:,index_to_keep]
    gene_new = gene[index_to_keep]
    w_new = 1/ (margin[index_to_keep] -td + epsilon)
    return X_new, w_new, gene_new