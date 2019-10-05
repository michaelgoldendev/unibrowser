"""
A state guesser based on the popular akinator game.
"""

import numpy as np
import akinator_questionpicker
import random

from enum import IntEnum
class DefaultResponse(IntEnum):
    YES = 0
    NO = 1
    
class QuestionType(IntEnum):
    TERMINAL = 0
    NONTERMINAL = 1
    

class Akinator:
    """A class representing states (e.g. character, country, object, etc.) together with questions and expected answers about those states. Also contains a probabilistic model that attempts to guess the user's chosen state based on the user's responses to questions."""
    
    def __init__(self, responseenum=DefaultResponse, choosenextquestionfunc=akinator_questionpicker.nextquestion_entropy):
        """Initialiser
        
        Parameters:
            responseenum(IntEnum): an enumeration listing the possible user responses.
            choosenextquestionfunc(function): a function for choosing the next question based on the model's current probabilities.
        """
        
        self.answerdim = len(responseenum)
        self.questions = []
        self.questiontypes = []
        self.questiontokeymapping = {}
        self.answerdict = {}
        self.statelist = []
        self.stateset = set()
        self.numstates = 0        
        self.stateprobs = None
        self.statelogprobs = None
        self.usedquestions = []
        
        self.responseenum = responseenum
        self.choosenextquestionfunc = choosenextquestionfunc
    
    def __reset(self):        
        """Helper method that resets the size of the state probability vectors. Used when a state is added to the model"""
        
        self.numstates = len(self.statelist)
        print("States: %d, questions %d" % (self.numstates, len(self.questions)))
        self.stateprobs = np.ones(shape=(self.numstates))/self.numstates
        self.statelogprobs = np.ones(shape=(self.numstates))*-np.log(self.numstates)
        
    def addquestion(self, questiontext, questiontype=QuestionType.NONTERMINAL):
        """Add a question to the model,
        
        Parameters:
            questiontext(str): the text of the question to be added.
            
        Returns:
            int: a question key that is unique to the question text."
        """        
        
        if questiontext not in self.questiontokeymapping:
            qkey = len(self.questions)
            self.questions.append(questiontext)
            self.questiontypes.append(questiontype)
            self.questiontokeymapping[questiontext] = qkey
            return qkey
        else:
            return self.questiontokeymapping[questiontext]
    
    def addquestionanswer(self, questiontext, statename, answervec, questiontype=QuestionType.NONTERMINAL):
        """Add a question and a corresponding answer to the model for a particular state
        
        Parameters:
            questiontext(str): the text of the question to be added.
            statename(str): the name of state to which the answer refers
            answervec(ndarray): a probability vector representing how a typical user is likely to answer this question.
        
        """
        
        qkey = self.addquestion(questiontext, questiontype=questiontype)
        self.addanswer(qkey, statename, answervec)
        
    
    def addanswer(self, qkey, statename, answervec):
        """Set the (question key,state) pair answer probability vector. The probabilities reflect how users are likely to answer a question about a particular state. The answer probabilities should exclude input noise (keyboard/mouse/EEG errors).
        
         Parameters:
            qkey (int): the question key.
            statename(str): the name of state to which the answer refers
            answervec(ndarray): a probability vector representing how a typical user is likely to answer this question.        
         """
        
        if statename not in self.stateset:
            self.statelist.append(statename)
            self.stateset.add(statename)
            self.__reset()
        self.answerdict[(statename,qkey)] = answervec
    
    def bayesianupdate_discreteanswer(self, qkey, akey):
        """Updates the state probability vector based on the user's answer to the given question.
        
        Parameters:
            qkey (int): the question key.
            akey (int): the users answer in the form of a discrete integer representing the user's answer (for example: 0. yes, 1. don't know, 2. no) with no input noise.
        
        Returns:
            int: the question key.
        
        """
     
        avec = np.zeros(self.answerdim)
        avec[akey] = 1.0 # create an answer probability vector with no input noise
        self.bayesianupdate_probanswer(qkey, avec)
    
    def bayesianupdate_probanswer(self, qkey, avec):
        """Updates the state probability vector based on the user's answer to the given question.
        
        Parameters:
            qkey (int): the question key.
            avec (ndarray): the users answer in the form of a probability vector that reflects potential input noise.
        
        Returns:
            int: the question key.
        
        """
        
        self.statelogprobs, self.stateprobs = self.calculate_state_probs(self.statelogprobs, self.stateprobs, qkey, avec)
        """
        sortedstates = [(p, state) for (p, state)  in zip(self.stateprobs,self.statelist)]
        sortedstates.sort()
        
        for (p, state) in sortedstates:
            print(" %s: %0.6f" % (state,p))
        #print(self.statelogprobs)
        #print(np.sum(self.stateprobs))
        print("------------------------------")
        """
        
    def calculate_state_probs(self, statelogprobs, stateprobs, qkey, avec):
        """Helper method that performs the Bayesian update with probabilities calculated in log-space to avoid numerical precision errors.
        
        Returns:
            tuple: a log probability vector and a probability vector representing the model's guess of the user's chosen state. 
        """
        hasquestionlogsum = -np.inf
        noquestionlogsum = -np.inf
        for ckey in range(self.numstates):
            statequestionkey = (self.statelist[ckey],qkey)
            if statequestionkey in self.answerdict:
                likelihood = np.dot(self.answerdict[statequestionkey], avec)
                v = np.log(likelihood+1.0e-100) + statelogprobs[ckey]
                statelogprobs[ckey] = v
                hasquestionlogsum = np.logaddexp(hasquestionlogsum, v)
            else:
                noquestionlogsum = np.logaddexp(noquestionlogsum, statelogprobs[ckey])
                #print("No question for state %s" % self.statelist[ckey])
        
        
        logsum = -np.inf # variable for accumulating normalisation constant
        # if one or more states don't have a particular question, keep their marginal probability the same when performing this update:
        hasquestionmultiplier = np.log(1.0 - np.exp(noquestionlogsum))
        for ckey in range(self.numstates):
            statequestionkey = (self.statelist[ckey],qkey)
            if statequestionkey in self.answerdict:
                statelogprobs[ckey] += hasquestionmultiplier-hasquestionlogsum           
            logsum = np.logaddexp(logsum, statelogprobs[ckey]) # normalisation constant
                
        statelogprobs -= logsum
        stateprobs = np.exp(statelogprobs)
        
        return statelogprobs, stateprobs
    
    def getnextquestion(self):
        return self.choosenextquestionfunc(self)

