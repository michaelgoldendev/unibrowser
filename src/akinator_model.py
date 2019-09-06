"""
A state guesser based on the popular akinator game.
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
            tempstatelogprobs,tempstateprobs = akinator.calculate_state_probs(np.copy(akinator.statelogprobs), np.copy(akinator.stateprobs), qkey, avec)
            
            entropy = 0.0
            for (logp,p) in zip(tempstatelogprobs, tempstateprobs):
                entropy += -p*logp
            for ckey in range(akinator.numstates):
                statequestionkey = (akinator.states[ckey],qkey)
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
    """Chooses the next question using one-step look-ahead and the maximum state probability
    
    Returns:
        int: the key of the next question.
    
    """
    
    expectedmaxprobabilities = np.zeros(shape=len(akinator.questions))
    for qkey in range(len(akinator.questions)):
        expectedmaxprobability = 0.0
        for akey in range(akinator.answerdim):
            avec = np.zeros(3)
            avec[akey] = 1.0 # create an answer probability vector with no input noise
            tempstatelogprobs,tempstateprobs = akinator.calculate_state_probs(np.copy(akinator.statelogprobs), np.copy(akinator.stateprobs), qkey, avec)
            
            maxstateprob = np.max(tempstateprobs)
            for ckey in range(akinator.numstates):
                statequestionkey = (akinator.states[ckey],qkey)
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

class Akinator:
    def __init__(self, answerdim=3, choosenextquestionfunc=nextquestion_entropy):
        self.answerdim = answerdim
        self.questions = []
        self.answerdict = {}
        self.states = []
        self.numstates = 0        
        self.stateprobs = None
        self.statelogprobs = None
        self.usedquestions = []
        self.choosenextquestionfunc = choosenextquestionfunc
        
    def addquestion(self, questiontext):
        qkey = len(self.questions)
        if questiontext not in self.questions:
            self.questions.append(questiontext)
        else:
            qkey = self.questions.index(questiontext)
        return qkey
    
    def addquestionanswer(self, questiontext, statename, answervec):
        qkey = self.addquestion(questiontext)
        self.addanswer(qkey, statename, answervec)
        
    
    def addanswer(self, qkey, statename, answervec):
        """Set the (question,state) pair answer probability vector. The probabilities reflect how users are likely to answer the question about the particular state."""
        
        self.answerdict[(statename,qkey)] = answervec
    
    def update(self, qkey, akey):
        avec = np.zeros(3)
        avec[akey] = 1.0 # create an answer probability vector with no input noise
        self.update_helper(qkey, avec)
    
    def update_helper(self, qkey, avec):
        """Updates the state probability vector based on the user's answer.
        
        Parameters:
            qkey (int): the question key.
            avec (ndarray): the users answer in the form of a probability vector that reflects potential input noise.
        
        Returns:
            int: the question key.
        
        """
        
        self.statelogprobs, self.stateprobs = self.calculate_state_probs(self.statelogprobs, self.stateprobs, qkey, avec)
        sortedstates = [(p, state) for (p, state)  in zip(self.stateprobs,self.states)]
        sortedstates.sort()
        for (p, state) in sortedstates:
            print(" %s: %0.6f" % (state,p))
        print(self.statelogprobs)
        print(np.sum(self.stateprobs))
        print("------------------------------")
        
    def calculate_state_probs(self, statelogprobs, stateprobs, qkey, avec):        
        hasquestionlogsum = -np.inf
        noquestionlogsum = -np.inf
        for ckey in range(self.numstates):
            statequestionkey = (self.states[ckey],qkey)
            if statequestionkey in self.answerdict:
                likelihood = np.dot(self.answerdict[statequestionkey],avec)            
                v = np.log(likelihood) + statelogprobs[ckey]
                statelogprobs[ckey] = v
                hasquestionlogsum = np.logaddexp(hasquestionlogsum, v)
            else:
                noquestionlogsum = np.logaddexp(noquestionlogsum, statelogprobs[ckey])
                print("No question for state %s" % self.states[ckey])
        
        
        logsum = -np.inf # variable for accumulating normalisation constant
        # if one or more states don't have a particular question, keep their marginal probability the same by multiplying the states with the question by the following quantity:
        hasquestionmultiplier = np.log(1.0 - np.exp(noquestionlogsum))
        for ckey in range(self.numstates):
            statequestionkey = (self.states[ckey],qkey)
            if statequestionkey in self.answerdict:
                statelogprobs[ckey] += hasquestionmultiplier-hasquestionlogsum           
            logsum = np.logaddexp(logsum, statelogprobs[ckey]) # normalisation constant
                
        statelogprobs -= logsum
        stateprobs = np.exp(statelogprobs)
        
        return statelogprobs, stateprobs
    
    def getnextquestion(self):
        return self.choosenextquestionfunc(self)

