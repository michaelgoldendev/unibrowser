"""
A module containing different functions for choosing the next question. 

These functions typically use the state of akinator model to choose the next question.

The goal ofm a question picker function is typically to minimise the number of questions to be asked before returning the correct prediction of the user's chosen state.
"""

import numpy as np

def nextquestion_entropy(akinator, verbose=False):
    """Chooses the next question using one-step look-ahead and information entropy.
    
    Returns:
        int: the key of the next question.
    
    """
    
    expectedentropies = np.zeros(shape=len(akinator.questions))
    for qkey in range(len(akinator.questions)):
        expectedentropy = 0.0
        for akey in range(akinator.answerdim):
            avec = np.zeros(3)
            avec[akey] = 1.0 # create an answer probability vector with no input noise
            tempstatelogprobs,tempstateprobs = akinator.calculate_state_probs(np.copy(akinator.statelogprobs), np.copy(akinator.stateprobs), qkey, avec) # copy's ensure that the akinator model is not updated
            
            entropy = 0.0
            for (logp,p) in zip(tempstatelogprobs, tempstateprobs):
                entropy += -p*logp
            for ckey in range(akinator.numstates):
                statequestionkey = (akinator.statelist[ckey],qkey)
                condanswerprob = 1.0/akinator.answerdim # use a flat answer prior if this state doesn't have this question
                if statequestionkey in akinator.answerdict:
                    condanswerprob = akinator.answerdict[statequestionkey][akey]
                expectedentropy += entropy*condanswerprob*akinator.stateprobs[ckey]
                
        expectedentropies[qkey] = expectedentropy
        if verbose:
            print("Q%d: %s (expected: %0.7f)" % (qkey, akinator.questions[qkey], expectedentropy))
            
    minentropy = np.inf
    minindex = -1
    for qkey in range(len(akinator.questions)): # choose the question that will result in the minimum expected information entropy
        if expectedentropies[qkey] < minentropy and qkey not in akinator.usedquestions:
            minentropy = expectedentropies[qkey]
            minindex = qkey 
    return minindex

def nextquestion_maxprob(akinator, verbose=False):
    """Chooses the next question using one-step look-ahead and the maximum state probability.
    
    Returns:
        int: the key of the next question.
    
    """
    
    expectedmaxprobabilities = np.zeros(shape=len(akinator.questions))
    for qkey in range(len(akinator.questions)):
        expectedmaxprobability = 0.0
        for akey in range(akinator.answerdim):
            avec = np.zeros(3)
            avec[akey] = 1.0 # create an answer probability vector with no input noise
            tempstatelogprobs,tempstateprobs = akinator.calculate_state_probs(np.copy(akinator.statelogprobs), np.copy(akinator.stateprobs), qkey, avec) # copy's ensure that the akinator model is not updated
            
            maxstateprob = np.max(tempstateprobs)
            for ckey in range(akinator.numstates):
                statequestionkey = (akinator.statelist[ckey],qkey)
                condanswerprob = 1.0/akinator.answerdim # use a flat answer prior if this state doesn't have this question
                if statequestionkey in akinator.answerdict:
                    condanswerprob = akinator.answerdict[statequestionkey][akey]
                expectedmaxprobability += maxstateprob*condanswerprob*akinator.stateprobs[ckey]
                
        expectedmaxprobabilities[qkey] = expectedmaxprobability
        if verbose:
            print("Q%d: %s (expected: %0.7f)" % (qkey, akinator.questions[qkey], expectedmaxprobability))
            
    expectedmax = -np.inf
    index = -1
    for qkey in range(len(akinator.questions)): # choose the question that will result in the minimum expected information entropy
        if expectedmaxprobabilities[qkey] > expectedmax and qkey not in akinator.usedquestions:
            expectedmax = expectedmaxprobabilities[qkey]
            index = qkey 
    return index