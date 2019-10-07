"""
A module containing different functions for choosing the next question. 

These functions typically use the state of akinator model to choose the next question.

The goal of a question picker function is typically to minimise the number of questions to be asked before returning the correct prediction of the user's chosen state.
"""

import numpy as np
import akinator_model

def cutoff_function(questionno, alpha=0.10, minval=0.05, maxvalue=0.5):
    v = np.exp(-(float(questionno)-1.0)*alpha)*maxvalue
    return max(minval, v)

def nextquestion_entropy(akinator, verbose=False):
    """Chooses the next question using one-step look-ahead and information entropy.
    
    Returns:
        int: the key of the next question.
    
    """
    
    terminalquestionprobcutoff = cutoff_function(len(akinator.usedquestions))
    print("Question cut off:",terminalquestionprobcutoff)
    
    expectedentropies = np.zeros(shape=len(akinator.questions))
    currentmaxprob = np.max(akinator.stateprobs)
    for qkey in range(len(akinator.questions)):
        if (currentmaxprob > terminalquestionprobcutoff or akinator.questiontypes[qkey] != akinator_model.QuestionType.TERMINAL) and qkey not in akinator.usedquestions:
            expectedentropy = 0.0
            for akey in range(akinator.answerdim):
                avec = np.zeros(akinator.answerdim)
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
        if (currentmaxprob > terminalquestionprobcutoff or akinator.questiontypes[qkey] != akinator_model.QuestionType.TERMINAL) and expectedentropies[qkey] < minentropy and qkey not in akinator.usedquestions:
            minentropy = expectedentropies[qkey]
            minindex = qkey 
    return minindex

def nextquestion_maxprob(akinator, verbose=False):
    """Chooses the next question using one-step look-ahead and the maximum state probability.
    
    Returns:
        int: the key of the next question.
    
    """
    
    terminalquestionprobcutoff = cutoff_function(len(akinator.usedquestions))
    
    expectedmaxprobabilities = np.zeros(shape=len(akinator.questions))
    currentmaxprob = np.max(akinator.stateprobs)
    for qkey in range(len(akinator.questions)):
        if (currentmaxprob > terminalquestionprobcutoff or akinator.questiontypes[qkey] != akinator_model.QuestionType.TERMINAL) and qkey not in akinator.usedquestions:
            expectedmaxprobability = 0.0
            for akey in range(akinator.answerdim):
                avec = np.zeros(akinator.answerdim)
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
        if (currentmaxprob > terminalquestionprobcutoff or akinator.questiontypes[qkey] != akinator_model.QuestionType.TERMINAL) and expectedentropies[qkey] < minentropy and qkey not in akinator.usedquestions:
            if expectedmaxprobabilities[qkey] > expectedmax and qkey not in akinator.usedquestions:
                expectedmax = expectedmaxprobabilities[qkey]
                index = qkey 
    return index