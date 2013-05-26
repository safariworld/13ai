import numpy as np
import sys


def apk(actual, predicted, k=10):
    """
    Computes the average precision at k.

    This function computes the average prescision at k between two lists of
    items.

    Parameters
    ----------
    actual : list
             A list of elements that are to be predicted (order doesn't matter)
    predicted : list
                A list of predicted elements (order does matter)
    k : int, optional
        The maximum number of predicted elements

    Returns
    -------
    score : double
            The average precision at k over the input lists

    """
    if len(predicted)>k:
        predicted = predicted[:k]

    score = 0.0
    num_hits = 0.0

    for i,p in enumerate(predicted):
        if p in actual and p not in predicted[:i]:
            num_hits += 1.0
            score += num_hits / (i+1.0)

    if not actual:
        return 1.0

    return score / min(len(actual), k)

def mapk(actual, predicted, k=10):
    """
    Computes the mean average precision at k.

    This function computes the mean average prescision at k between two lists
    of lists of items.

    Parameters
    ----------
    actual : list
             A list of lists of elements that are to be predicted 
             (order doesn't matter in the lists)
    predicted : list
                A list of lists of predicted elements
                (order matters in the lists)
    k : int, optional
        The maximum number of predicted elements

    Returns
    -------
    score : double
            The mean average precision at k over the input lists

    """
    return np.mean([apk(a,p,k) for a,p in zip(actual, predicted)])


predictions_f = open(sys.argv[1], "r")
groundTrues_f = open(sys.argv[2], "r")

predictions = predictions_f.readlines()
groundTrues = groundTrues_f.readlines()

predLists = []
trueLists = []
dats_len = len(predictions)

for i, prediction in enumerate(predictions):
    #debug
    if i%100000 == 0:
        print("%d/%d"%(i/100000,dats_len/100000))

    if i == 0:
        continue
    groundTrue = groundTrues[i]
    predList = [int(s) for s in (prediction.split(','))[1].split()]
    trueList = [int(s) for s in (groundTrue.split(','))[1].split()]
    
    predLists.append(predList)
    trueLists.append(trueList)


map3Val = mapk( trueLists, predLists, 3)
print "map@3 value = %f"%map3Val

