"""
A state guesser based on the popular akinator game.
"""

import numpy as np

def nextquestion_entropy(akinator, verbose=False):
    """Chooses the next question using one-step look-ahead and information entropy.
    
    Returns:
        int: the question key.
    
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
                condanswerprob = 1.0/len(answers) # use a flat answer prior if this state doesn't have this question
                if statequestionkey in akinator.answerdict:
                    condanswerprob = akinator.answerdict[statequestionkey][akey]
                expectedentropy += entropy*condanswerprob*akinator.stateprobs[ckey]
                #expectedentropy -= np.max(tempstateprobs)*condanswerprob*akinator.stateprobs[ckey]
                
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
        
    def addquestion(self, question):
        qkey = len(self.questions)
        self.questions.append(question)
        return qkey
    
    def addanswer(self, qkey, statename, answervec):
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
        


answers = ["Yes", "Maybe", "No"]
YES = 0
MAYBE = 1
NO = 2
        
def setup_character_akinator(akinator):
    defaultyes = [0.90, 0.05, 0.05]
    defaultmaybe = [0.2, 0.60, 0.2]
    defaultno = [0.05, 0.05, 0.90]
    
    qkey = akinator.addquestion("Are they male?")
    #akinator.addanswer(qkey, "Harry Potter", defaultyes)
    akinator.addanswer(qkey, "Donald Trump", defaultyes)
    akinator.addanswer(qkey, "Pikachu", defaultyes)
    akinator.addanswer(qkey, "Heidi", defaultno)
    akinator.addanswer(qkey, "Popeye", defaultyes)
    akinator.addanswer(qkey, "Queen Victoria", defaultno)
    akinator.addanswer(qkey, "PewDiePie", defaultyes)
    akinator.addanswer(qkey, "Britney Spears", defaultno)
    akinator.addanswer(qkey, "Leonardo DiCaprio", defaultyes)
    akinator.addanswer(qkey, "Gandalf", defaultyes)
    akinator.addanswer(qkey, "Hillary Clinton", defaultno)
    akinator.addanswer(qkey, "Nelson Mandela", defaultyes)
    akinator.addanswer(qkey, "Pythagoras", defaultyes)
    akinator.addanswer(qkey, "Spiderman", defaultyes)
    akinator.addanswer(qkey, "Albert Einstein", defaultyes)
    akinator.addanswer(qkey, "Marilyn Monroe", defaultno)
    akinator.addanswer(qkey, "Marie Curie", defaultno)
    akinator.addanswer(qkey, "J. K. Rowling", defaultno)
    akinator.addanswer(qkey, "Usain Bolt", defaultyes)
    akinator.addanswer(qkey, "Bill Gates", defaultyes)
    akinator.addanswer(qkey, "Elon Musk", defaultyes)
    akinator.addanswer(qkey, "Julius Caesar", defaultyes)
    akinator.addanswer(qkey, "Pacman", defaultyes)
    akinator.addanswer(qkey, "Snow White", defaultno)
    akinator.addanswer(qkey, "Charlie from Charlie and the Chocolate Factory", defaultyes)
    
    
    qkey = akinator.addquestion("Are they real?")
    akinator.addanswer(qkey, "Harry Potter", defaultno)
    akinator.addanswer(qkey, "Donald Trump", defaultyes)
    akinator.addanswer(qkey, "Pikachu", defaultno)
    akinator.addanswer(qkey, "Heidi", defaultno)
    akinator.addanswer(qkey, "Popeye", defaultno)
    akinator.addanswer(qkey, "Queen Victoria", defaultyes)
    akinator.addanswer(qkey, "PewDiePie", defaultyes)
    akinator.addanswer(qkey, "Britney Spears", defaultyes)
    akinator.addanswer(qkey, "Leonardo DiCaprio", defaultyes)
    akinator.addanswer(qkey, "Gandalf", defaultno)
    akinator.addanswer(qkey, "Hillary Clinton", defaultyes)
    akinator.addanswer(qkey, "Nelson Mandela", defaultyes)
    akinator.addanswer(qkey, "Pythagoras", defaultyes)
    akinator.addanswer(qkey, "Spiderman", defaultno)
    akinator.addanswer(qkey, "Albert Einstein", defaultyes)
    akinator.addanswer(qkey, "Marilyn Monroe", defaultyes)
    akinator.addanswer(qkey, "Marie Curie", defaultyes)
    akinator.addanswer(qkey, "J. K. Rowling", defaultyes)
    akinator.addanswer(qkey, "Usain Bolt", defaultyes)
    akinator.addanswer(qkey, "Bill Gates", defaultyes)
    akinator.addanswer(qkey, "Elon Musk", defaultyes)
    akinator.addanswer(qkey, "Julius Caesar", defaultyes)
    akinator.addanswer(qkey, "Pacman", defaultno)
    akinator.addanswer(qkey, "Snow White", defaultno)
    akinator.addanswer(qkey, "Charlie from Charlie and the Chocolate Factory", defaultno)
    
    qkey = akinator.addquestion("Are they animated?")
    akinator.addanswer(qkey, "Harry Potter", defaultno)
    akinator.addanswer(qkey, "Donald Trump", defaultno)
    akinator.addanswer(qkey, "Pikachu", defaultyes)
    akinator.addanswer(qkey, "Heidi", defaultmaybe)
    akinator.addanswer(qkey, "Popeye", defaultyes)
    akinator.addanswer(qkey, "Queen Victoria", defaultno)
    akinator.addanswer(qkey, "PewDiePie", defaultno)
    akinator.addanswer(qkey, "Britney Spears", defaultno)
    akinator.addanswer(qkey, "Leonardo DiCaprio", defaultno)
    akinator.addanswer(qkey, "Gandalf", defaultno)
    akinator.addanswer(qkey, "Hillary Clinton", defaultno)
    akinator.addanswer(qkey, "Nelson Mandela", defaultno)
    akinator.addanswer(qkey, "Pythagoras", defaultno)
    akinator.addanswer(qkey, "Spiderman", defaultmaybe)
    akinator.addanswer(qkey, "Albert Einstein", defaultno)
    akinator.addanswer(qkey, "Marilyn Monroe", defaultno)
    akinator.addanswer(qkey, "Marie Curie", defaultno)
    akinator.addanswer(qkey, "J. K. Rowling", defaultno)
    akinator.addanswer(qkey, "Usain Bolt", defaultno)
    akinator.addanswer(qkey, "Bill Gates", defaultno)
    akinator.addanswer(qkey, "Elon Musk", defaultno)
    akinator.addanswer(qkey, "Julius Caesar", defaultno)
    akinator.addanswer(qkey, "Pacman", defaultyes)
    akinator.addanswer(qkey, "Snow White", defaultyes)
    akinator.addanswer(qkey, "Charlie from Charlie and the Chocolate Factory", defaultyes)
    
    qkey = akinator.addquestion("Are they tall?")
    akinator.addanswer(qkey, "Harry Potter", defaultmaybe)
    akinator.addanswer(qkey, "Donald Trump", defaultyes)
    akinator.addanswer(qkey, "Pikachu", defaultno)
    akinator.addanswer(qkey, "Heidi", defaultno)
    akinator.addanswer(qkey, "Popeye", defaultmaybe)
    akinator.addanswer(qkey, "Queen Victoria", defaultmaybe)
    akinator.addanswer(qkey, "PewDiePie", defaultmaybe)
    akinator.addanswer(qkey, "Britney Spears", defaultno)
    akinator.addanswer(qkey, "Leonardo DiCaprio", defaultno)
    akinator.addanswer(qkey, "Gandalf", defaultyes)
    akinator.addanswer(qkey, "Hillary Clinton", defaultno)
    akinator.addanswer(qkey, "Nelson Mandela", defaultyes)
    akinator.addanswer(qkey, "Pythagoras", defaultmaybe)
    akinator.addanswer(qkey, "Spiderman", defaultmaybe)
    akinator.addanswer(qkey, "Albert Einstein", defaultmaybe)
    akinator.addanswer(qkey, "Marilyn Monroe", defaultmaybe)
    akinator.addanswer(qkey, "Marie Curie", defaultmaybe)
    akinator.addanswer(qkey, "J. K. Rowling", defaultmaybe)
    akinator.addanswer(qkey, "Usain Bolt", defaultyes)
    akinator.addanswer(qkey, "Bill Gates", defaultmaybe)
    akinator.addanswer(qkey, "Elon Musk", defaultmaybe)
    akinator.addanswer(qkey, "Julius Caesar", defaultmaybe)
    akinator.addanswer(qkey, "Pacman", defaultno)
    akinator.addanswer(qkey, "Snow White", defaultmaybe)
    akinator.addanswer(qkey, "Charlie from Charlie and the Chocolate Factory", defaultno)
    
    qkey = akinator.addquestion("Are they a YouTuber?")
    akinator.addanswer(qkey, "Harry Potter", defaultno)
    akinator.addanswer(qkey, "Donald Trump", defaultno)
    akinator.addanswer(qkey, "Pikachu", defaultno)
    akinator.addanswer(qkey, "Heidi", defaultno)
    akinator.addanswer(qkey, "Popeye", defaultno)
    akinator.addanswer(qkey, "Queen Victoria", defaultno)
    akinator.addanswer(qkey, "PewDiePie", defaultyes)
    akinator.addanswer(qkey, "Britney Spears", defaultno)
    akinator.addanswer(qkey, "Leonardo DiCaprio", defaultno)
    akinator.addanswer(qkey, "Gandalf", defaultno)
    akinator.addanswer(qkey, "Hillary Clinton", defaultno)
    akinator.addanswer(qkey, "Nelson Mandela", defaultno)
    akinator.addanswer(qkey, "Pythagoras", defaultno)
    akinator.addanswer(qkey, "Spiderman", defaultno)
    akinator.addanswer(qkey, "Albert Einstein", defaultno)
    akinator.addanswer(qkey, "Marilyn Monroe", defaultno)
    akinator.addanswer(qkey, "Marie Curie", defaultno)
    akinator.addanswer(qkey, "J. K. Rowling", defaultno)
    akinator.addanswer(qkey, "Usain Bolt", defaultno)
    akinator.addanswer(qkey, "Bill Gates", defaultno)
    akinator.addanswer(qkey, "Elon Musk", defaultno)
    akinator.addanswer(qkey, "Julius Caesar", defaultno)
    akinator.addanswer(qkey, "Pacman", defaultno)
    akinator.addanswer(qkey, "Snow White", defaultno)
    akinator.addanswer(qkey, "Charlie from Charlie and the Chocolate Factory", defaultno)
    
    qkey = akinator.addquestion("Are they magic?")
    akinator.addanswer(qkey, "Harry Potter", defaultyes)
    akinator.addanswer(qkey, "Donald Trump", defaultno)
    akinator.addanswer(qkey, "Pikachu", defaultmaybe)
    akinator.addanswer(qkey, "Heidi", defaultno)
    akinator.addanswer(qkey, "Popeye", defaultno)
    akinator.addanswer(qkey, "Queen Victoria", defaultno)
    akinator.addanswer(qkey, "PewDiePie", defaultno)
    akinator.addanswer(qkey, "Britney Spears", defaultno)
    akinator.addanswer(qkey, "Leonardo DiCaprio", defaultno)
    akinator.addanswer(qkey, "Gandalf", defaultyes)
    akinator.addanswer(qkey, "Hillary Clinton", defaultno)
    akinator.addanswer(qkey, "Nelson Mandela", defaultno)
    akinator.addanswer(qkey, "Pythagoras", defaultno)
    akinator.addanswer(qkey, "Spiderman", defaultno)
    akinator.addanswer(qkey, "Albert Einstein", defaultno)
    akinator.addanswer(qkey, "Marilyn Monroe", defaultno)
    akinator.addanswer(qkey, "Marie Curie", defaultno)
    akinator.addanswer(qkey, "J. K. Rowling", defaultno)
    akinator.addanswer(qkey, "Usain Bolt", defaultno)
    akinator.addanswer(qkey, "Bill Gates", defaultno)
    akinator.addanswer(qkey, "Elon Musk", defaultno)
    akinator.addanswer(qkey, "Julius Caesar", defaultno)
    akinator.addanswer(qkey, "Pacman", defaultno)
    akinator.addanswer(qkey, "Snow White", defaultmaybe)
    akinator.addanswer(qkey, "Charlie from Charlie and the Chocolate Factory", defaultno)
    
    qkey = akinator.addquestion("Do they have special powers?")
    akinator.addanswer(qkey, "Harry Potter", defaultyes)
    akinator.addanswer(qkey, "Donald Trump", defaultmaybe)
    akinator.addanswer(qkey, "Pikachu", defaultyes)
    akinator.addanswer(qkey, "Heidi", defaultno)
    akinator.addanswer(qkey, "Popeye", defaultyes)
    akinator.addanswer(qkey, "Queen Victoria", defaultmaybe)
    akinator.addanswer(qkey, "PewDiePie", defaultno)
    akinator.addanswer(qkey, "Britney Spears", defaultno)
    akinator.addanswer(qkey, "Leonardo DiCaprio", defaultno)
    akinator.addanswer(qkey, "Gandalf", defaultyes)
    akinator.addanswer(qkey, "Hillary Clinton", defaultno)
    akinator.addanswer(qkey, "Nelson Mandela", defaultno)
    akinator.addanswer(qkey, "Pythagoras", defaultno)
    akinator.addanswer(qkey, "Spiderman", defaultyes)
    akinator.addanswer(qkey, "Albert Einstein", defaultno)
    akinator.addanswer(qkey, "Marilyn Monroe", defaultno)
    akinator.addanswer(qkey, "Marie Curie", defaultno)
    akinator.addanswer(qkey, "J. K. Rowling", defaultno)
    akinator.addanswer(qkey, "Usain Bolt", defaultmaybe)
    akinator.addanswer(qkey, "Bill Gates", defaultno)
    akinator.addanswer(qkey, "Elon Musk", defaultno)
    akinator.addanswer(qkey, "Julius Caesar", defaultno)
    akinator.addanswer(qkey, "Pacman", defaultmaybe)
    akinator.addanswer(qkey, "Snow White", defaultno)
    akinator.addanswer(qkey, "Charlie from Charlie and the Chocolate Factory", defaultno)
    
    qkey = akinator.addquestion("Are they alive?")
    akinator.addanswer(qkey, "Harry Potter", defaultno)
    akinator.addanswer(qkey, "Donald Trump", defaultyes)
    akinator.addanswer(qkey, "Pikachu", defaultno)
    akinator.addanswer(qkey, "Heidi", defaultno)
    akinator.addanswer(qkey, "Popeye", defaultno)
    akinator.addanswer(qkey, "Queen Victoria", defaultno)
    akinator.addanswer(qkey, "PewDiePie", defaultyes)
    akinator.addanswer(qkey, "Britney Spears", defaultyes)
    akinator.addanswer(qkey, "Leonardo DiCaprio", defaultyes)
    akinator.addanswer(qkey, "Gandalf", defaultno)
    akinator.addanswer(qkey, "Hillary Clinton", defaultyes)
    akinator.addanswer(qkey, "Nelson Mandela", defaultno)
    akinator.addanswer(qkey, "Pythagoras", defaultno)
    akinator.addanswer(qkey, "Spiderman", defaultno)
    akinator.addanswer(qkey, "Albert Einstein", defaultno)
    akinator.addanswer(qkey, "Marilyn Monroe", defaultno)
    akinator.addanswer(qkey, "Marie Curie", defaultno)
    akinator.addanswer(qkey, "J. K. Rowling", defaultyes)
    akinator.addanswer(qkey, "Usain Bolt", defaultyes)
    akinator.addanswer(qkey, "Bill Gates", defaultyes)
    akinator.addanswer(qkey, "Elon Musk", defaultyes)
    akinator.addanswer(qkey, "Julius Caesar", defaultno)
    akinator.addanswer(qkey, "Pacman", defaultno)
    akinator.addanswer(qkey, "Snow White", defaultno)
    akinator.addanswer(qkey, "Charlie from Charlie and the Chocolate Factory", defaultno)
    
    qkey = akinator.addquestion("Are they a child?")
    akinator.addanswer(qkey, "Harry Potter", defaultmaybe)
    akinator.addanswer(qkey, "Donald Trump", defaultno)
    akinator.addanswer(qkey, "Pikachu", defaultmaybe)
    akinator.addanswer(qkey, "Heidi", defaultyes)
    akinator.addanswer(qkey, "Popeye", defaultno)
    akinator.addanswer(qkey, "Queen Victoria", defaultno)
    akinator.addanswer(qkey, "PewDiePie", defaultno)
    akinator.addanswer(qkey, "Britney Spears", defaultno)
    akinator.addanswer(qkey, "Leonardo DiCaprio", defaultno)
    akinator.addanswer(qkey, "Gandalf", defaultno)
    akinator.addanswer(qkey, "Hillary Clinton", defaultno)
    akinator.addanswer(qkey, "Nelson Mandela", defaultno)
    akinator.addanswer(qkey, "Pythagoras", defaultno)
    akinator.addanswer(qkey, "Spiderman", defaultno)
    akinator.addanswer(qkey, "Albert Einstein", defaultno)
    akinator.addanswer(qkey, "Marilyn Monroe", defaultno)
    akinator.addanswer(qkey, "Marie Curie", defaultno)
    akinator.addanswer(qkey, "J. K. Rowling", defaultno)
    akinator.addanswer(qkey, "Usain Bolt", defaultno)
    akinator.addanswer(qkey, "Bill Gates", defaultno)
    akinator.addanswer(qkey, "Elon Musk", defaultno)
    akinator.addanswer(qkey, "Julius Caesar", defaultno)
    akinator.addanswer(qkey, "Pacman", defaultno)
    akinator.addanswer(qkey, "Snow White", defaultmaybe)
    akinator.addanswer(qkey, "Charlie from Charlie and the Chocolate Factory", defaultyes)
    
    qkey = akinator.addquestion("Are they human?")
    akinator.addanswer(qkey, "Harry Potter", defaultyes)
    akinator.addanswer(qkey, "Donald Trump", defaultyes)
    akinator.addanswer(qkey, "Pikachu", defaultno)
    akinator.addanswer(qkey, "Heidi", defaultyes)
    akinator.addanswer(qkey, "Popeye", defaultyes)
    akinator.addanswer(qkey, "Queen Victoria", defaultyes)
    akinator.addanswer(qkey, "PewDiePie", defaultyes)
    akinator.addanswer(qkey, "Britney Spears", defaultyes)
    akinator.addanswer(qkey, "Leonardo DiCaprio", defaultyes)
    akinator.addanswer(qkey, "Gandalf", defaultmaybe)
    akinator.addanswer(qkey, "Hillary Clinton", defaultyes)
    akinator.addanswer(qkey, "Nelson Mandela", defaultyes)
    akinator.addanswer(qkey, "Pythagoras", defaultyes)
    akinator.addanswer(qkey, "Spiderman", defaultyes)
    akinator.addanswer(qkey, "Albert Einstein", defaultyes)
    akinator.addanswer(qkey, "Marilyn Monroe", defaultyes)
    akinator.addanswer(qkey, "Marie Curie", defaultyes)
    akinator.addanswer(qkey, "J. K. Rowling", defaultyes)
    akinator.addanswer(qkey, "Usain Bolt", defaultyes)
    akinator.addanswer(qkey, "Bill Gates", defaultyes)
    akinator.addanswer(qkey, "Elon Musk", defaultyes)
    akinator.addanswer(qkey, "Julius Caesar", defaultyes)
    akinator.addanswer(qkey, "Pacman", defaultno)
    akinator.addanswer(qkey, "Snow White", defaultyes)
    akinator.addanswer(qkey, "Charlie from Charlie and the Chocolate Factory", defaultyes)
    
    qkey = akinator.addquestion("Are they popular with children?")
    akinator.addanswer(qkey, "Harry Potter", defaultyes)
    akinator.addanswer(qkey, "Donald Trump", defaultno)
    akinator.addanswer(qkey, "Pikachu", defaultyes)
    akinator.addanswer(qkey, "Heidi", defaultyes)
    akinator.addanswer(qkey, "Popeye", defaultyes)
    akinator.addanswer(qkey, "Queen Victoria", defaultno)
    akinator.addanswer(qkey, "PewDiePie", defaultyes)
    akinator.addanswer(qkey, "Britney Spears", defaultmaybe)
    akinator.addanswer(qkey, "Leonardo DiCaprio", defaultno)
    akinator.addanswer(qkey, "Gandalf", defaultmaybe)
    akinator.addanswer(qkey, "Hillary Clinton", defaultno)
    akinator.addanswer(qkey, "Nelson Mandela", defaultmaybe)
    akinator.addanswer(qkey, "Pythagoras", defaultno)
    akinator.addanswer(qkey, "Spiderman", defaultyes)
    akinator.addanswer(qkey, "Albert Einstein", defaultno)
    akinator.addanswer(qkey, "Marilyn Monroe", defaultno)
    akinator.addanswer(qkey, "Marie Curie", defaultno)
    akinator.addanswer(qkey, "J. K. Rowling", defaultyes)
    akinator.addanswer(qkey, "Usain Bolt", defaultmaybe)
    akinator.addanswer(qkey, "Bill Gates", defaultno)
    akinator.addanswer(qkey, "Elon Musk", defaultno)
    akinator.addanswer(qkey, "Julius Caesar", defaultno)
    akinator.addanswer(qkey, "Pacman", defaultyes)
    akinator.addanswer(qkey, "Snow White", defaultyes)
    akinator.addanswer(qkey, "Charlie from Charlie and the Chocolate Factory", defaultyes)
    
    qkey = akinator.addquestion("Are they an entertainer?")
    akinator.addanswer(qkey, "Harry Potter", defaultno)
    akinator.addanswer(qkey, "Donald Trump", defaultmaybe)
    akinator.addanswer(qkey, "Pikachu", defaultno)
    akinator.addanswer(qkey, "Heidi", defaultno)
    akinator.addanswer(qkey, "Popeye", defaultno)
    akinator.addanswer(qkey, "Queen Victoria", defaultno)
    akinator.addanswer(qkey, "PewDiePie", defaultyes)
    akinator.addanswer(qkey, "Britney Spears", defaultyes)
    akinator.addanswer(qkey, "Leonardo DiCaprio", defaultyes)
    akinator.addanswer(qkey, "Gandalf", defaultno)
    akinator.addanswer(qkey, "Hillary Clinton", defaultno)
    akinator.addanswer(qkey, "Nelson Mandela", defaultno)
    akinator.addanswer(qkey, "Pythagoras", defaultno)
    akinator.addanswer(qkey, "Spiderman", defaultno)
    akinator.addanswer(qkey, "Albert Einstein", defaultno)
    akinator.addanswer(qkey, "Marilyn Monroe", defaultyes)
    akinator.addanswer(qkey, "Marie Curie", defaultno)
    akinator.addanswer(qkey, "J. K. Rowling", defaultno)
    akinator.addanswer(qkey, "Usain Bolt", defaultno)
    akinator.addanswer(qkey, "Bill Gates", defaultno)
    akinator.addanswer(qkey, "Elon Musk", defaultno)
    akinator.addanswer(qkey, "Julius Caesar", defaultno)
    akinator.addanswer(qkey, "Pacman", defaultno)
    akinator.addanswer(qkey, "Snow White", defaultno)
    akinator.addanswer(qkey, "Charlie from Charlie and the Chocolate Factory", defaultno)
    
    qkey = akinator.addquestion("Are they a politician?")
    akinator.addanswer(qkey, "Harry Potter", defaultno)
    akinator.addanswer(qkey, "Donald Trump", defaultyes)
    akinator.addanswer(qkey, "Pikachu", defaultno)
    akinator.addanswer(qkey, "Heidi", defaultno)
    akinator.addanswer(qkey, "Popeye", defaultno)
    akinator.addanswer(qkey, "Queen Victoria", defaultmaybe)
    akinator.addanswer(qkey, "PewDiePie", defaultno)
    akinator.addanswer(qkey, "Britney Spears", defaultno)
    akinator.addanswer(qkey, "Leonardo DiCaprio", defaultno)
    akinator.addanswer(qkey, "Gandalf", defaultno)
    akinator.addanswer(qkey, "Hillary Clinton", defaultyes)
    akinator.addanswer(qkey, "Nelson Mandela", defaultyes)
    akinator.addanswer(qkey, "Pythagoras", defaultno)
    akinator.addanswer(qkey, "Spiderman", defaultno)
    akinator.addanswer(qkey, "Albert Einstein", defaultno)
    akinator.addanswer(qkey, "Marilyn Monroe", defaultno)
    akinator.addanswer(qkey, "Marie Curie", defaultno)
    akinator.addanswer(qkey, "J. K. Rowling", defaultno)
    akinator.addanswer(qkey, "Usain Bolt", defaultno)
    akinator.addanswer(qkey, "Bill Gates", defaultno)
    akinator.addanswer(qkey, "Elon Musk", defaultno)
    akinator.addanswer(qkey, "Julius Caesar", defaultmaybe)
    akinator.addanswer(qkey, "Pacman", defaultno)
    akinator.addanswer(qkey, "Snow White", defaultno)
    akinator.addanswer(qkey, "Charlie from Charlie and the Chocolate Factory", defaultno)
    
    qkey = akinator.addquestion("Are they American?")
    akinator.addanswer(qkey, "Harry Potter", defaultno)
    akinator.addanswer(qkey, "Donald Trump", defaultyes)
    akinator.addanswer(qkey, "Pikachu", defaultno)
    akinator.addanswer(qkey, "Heidi", defaultno)
    akinator.addanswer(qkey, "Popeye", defaultyes)
    akinator.addanswer(qkey, "Queen Victoria", defaultno)
    akinator.addanswer(qkey, "PewDiePie", defaultno)
    akinator.addanswer(qkey, "Britney Spears", defaultyes)
    akinator.addanswer(qkey, "Leonardo DiCaprio", defaultyes)
    akinator.addanswer(qkey, "Gandalf", defaultno)
    akinator.addanswer(qkey, "Hillary Clinton", defaultyes)
    akinator.addanswer(qkey, "Nelson Mandela", defaultno)
    akinator.addanswer(qkey, "Pythagoras", defaultno)
    akinator.addanswer(qkey, "Spiderman", defaultyes)
    akinator.addanswer(qkey, "Albert Einstein", defaultmaybe)
    akinator.addanswer(qkey, "Marilyn Monroe", defaultyes)
    akinator.addanswer(qkey, "Marie Curie", defaultno)
    akinator.addanswer(qkey, "J. K. Rowling", defaultno)
    akinator.addanswer(qkey, "Usain Bolt", defaultno)
    akinator.addanswer(qkey, "Bill Gates", defaultyes)
    akinator.addanswer(qkey, "Elon Musk", defaultmaybe)
    akinator.addanswer(qkey, "Julius Caesar", defaultno)
    akinator.addanswer(qkey, "Pacman", defaultno)
    akinator.addanswer(qkey, "Snow White", defaultno)
    akinator.addanswer(qkey, "Charlie from Charlie and the Chocolate Factory", defaultno)
    
    qkey = akinator.addquestion("Are they considered attractive?")
    akinator.addanswer(qkey, "Harry Potter", defaultmaybe)
    akinator.addanswer(qkey, "Donald Trump", defaultno)
    akinator.addanswer(qkey, "Pikachu", defaultno)
    akinator.addanswer(qkey, "Heidi", defaultno)
    akinator.addanswer(qkey, "Popeye", defaultmaybe)
    akinator.addanswer(qkey, "Queen Victoria", defaultno)
    akinator.addanswer(qkey, "PewDiePie", defaultmaybe)
    akinator.addanswer(qkey, "Britney Spears", defaultmaybe)
    akinator.addanswer(qkey, "Leonardo DiCaprio", defaultyes)
    akinator.addanswer(qkey, "Gandalf", defaultno)
    akinator.addanswer(qkey, "Hillary Clinton", defaultno)
    akinator.addanswer(qkey, "Nelson Mandela", defaultno)
    akinator.addanswer(qkey, "Pythagoras", defaultno)
    akinator.addanswer(qkey, "Spiderman", defaultyes)
    akinator.addanswer(qkey, "Albert Einstein", defaultno)
    akinator.addanswer(qkey, "Marilyn Monroe", defaultyes)
    akinator.addanswer(qkey, "Marie Curie", defaultno)
    akinator.addanswer(qkey, "J. K. Rowling", defaultmaybe)
    akinator.addanswer(qkey, "Usain Bolt", defaultmaybe)
    akinator.addanswer(qkey, "Bill Gates", defaultno)
    akinator.addanswer(qkey, "Elon Musk", defaultmaybe)
    akinator.addanswer(qkey, "Julius Caesar", defaultno)
    akinator.addanswer(qkey, "Pacman", defaultno)
    akinator.addanswer(qkey, "Snow White", defaultyes)
    akinator.addanswer(qkey, "Charlie from Charlie and the Chocolate Factory", defaultno)
    
    qkey = akinator.addquestion("Are the considered intelligent or wise?")
    akinator.addanswer(qkey, "Harry Potter", defaultno)
    akinator.addanswer(qkey, "Donald Trump", defaultno)
    akinator.addanswer(qkey, "Pikachu", defaultno)
    akinator.addanswer(qkey, "Heidi", defaultno)
    akinator.addanswer(qkey, "Popeye", defaultno)
    akinator.addanswer(qkey, "Queen Victoria", defaultyes)
    akinator.addanswer(qkey, "PewDiePie", defaultno)
    akinator.addanswer(qkey, "Britney Spears", defaultno)
    akinator.addanswer(qkey, "Leonardo DiCaprio", defaultno)
    akinator.addanswer(qkey, "Gandalf", defaultyes)
    akinator.addanswer(qkey, "Hillary Clinton", defaultmaybe)
    akinator.addanswer(qkey, "Nelson Mandela", defaultmaybe)
    akinator.addanswer(qkey, "Pythagoras", defaultyes)
    akinator.addanswer(qkey, "Spiderman", defaultno)
    akinator.addanswer(qkey, "Albert Einstein", defaultyes)
    akinator.addanswer(qkey, "Marilyn Monroe", defaultmaybe)
    akinator.addanswer(qkey, "Marie Curie", defaultyes)
    akinator.addanswer(qkey, "J. K. Rowling", defaultyes)
    akinator.addanswer(qkey, "Usain Bolt", defaultmaybe)
    akinator.addanswer(qkey, "Bill Gates", defaultyes)
    akinator.addanswer(qkey, "Elon Musk", defaultyes)
    akinator.addanswer(qkey, "Julius Caesar", defaultmaybe)
    akinator.addanswer(qkey, "Pacman", defaultno)
    akinator.addanswer(qkey, "Snow White", defaultno)
    akinator.addanswer(qkey, "Charlie from Charlie and the Chocolate Factory", defaultno)
    
    qkey = akinator.addquestion("Did they live in ancient times?")
    akinator.addanswer(qkey, "Harry Potter", defaultno)
    akinator.addanswer(qkey, "Donald Trump", defaultno)
    akinator.addanswer(qkey, "Pikachu", defaultno)
    akinator.addanswer(qkey, "Heidi", defaultno)
    akinator.addanswer(qkey, "Popeye", defaultno)
    akinator.addanswer(qkey, "Queen Victoria", defaultno)
    akinator.addanswer(qkey, "PewDiePie", defaultno)
    akinator.addanswer(qkey, "Britney Spears", defaultno)
    akinator.addanswer(qkey, "Leonardo DiCaprio", defaultno)
    akinator.addanswer(qkey, "Gandalf", defaultmaybe)
    akinator.addanswer(qkey, "Hillary Clinton", defaultno)
    akinator.addanswer(qkey, "Nelson Mandela", defaultno)
    akinator.addanswer(qkey, "Pythagoras", defaultyes)
    akinator.addanswer(qkey, "Spiderman", defaultno)
    akinator.addanswer(qkey, "Albert Einstein", defaultno)
    akinator.addanswer(qkey, "Marilyn Monroe", defaultno)
    akinator.addanswer(qkey, "Marie Curie", defaultno)
    akinator.addanswer(qkey, "J. K. Rowling", defaultno)
    akinator.addanswer(qkey, "Usain Bolt", defaultno)
    akinator.addanswer(qkey, "Bill Gates", defaultno)
    akinator.addanswer(qkey, "Elon Musk", defaultno)
    akinator.addanswer(qkey, "Julius Caesar", defaultyes)
    akinator.addanswer(qkey, "Pacman", defaultno)
    akinator.addanswer(qkey, "Snow White", defaultmaybe)
    akinator.addanswer(qkey, "Charlie from Charlie and the Chocolate Factory", defaultno)
    
    qkey = akinator.addquestion("Are they a scientist or mathematician?")
    akinator.addanswer(qkey, "Harry Potter", defaultno)
    akinator.addanswer(qkey, "Donald Trump", defaultno)
    akinator.addanswer(qkey, "Pikachu", defaultno)
    akinator.addanswer(qkey, "Heidi", defaultno)
    akinator.addanswer(qkey, "Popeye", defaultno)
    akinator.addanswer(qkey, "Queen Victoria", defaultno)
    akinator.addanswer(qkey, "PewDiePie", defaultno)
    akinator.addanswer(qkey, "Britney Spears", defaultno)
    akinator.addanswer(qkey, "Leonardo DiCaprio", defaultno)
    akinator.addanswer(qkey, "Gandalf", defaultno)
    akinator.addanswer(qkey, "Hillary Clinton", defaultno)
    akinator.addanswer(qkey, "Nelson Mandela", defaultno)
    akinator.addanswer(qkey, "Pythagoras", defaultyes)
    akinator.addanswer(qkey, "Spiderman", defaultno)
    akinator.addanswer(qkey, "Albert Einstein", defaultyes)
    akinator.addanswer(qkey, "Marilyn Monroe", defaultno)
    akinator.addanswer(qkey, "Marie Curie", defaultyes)
    akinator.addanswer(qkey, "J. K. Rowling", defaultno)
    akinator.addanswer(qkey, "Usain Bolt", defaultno)
    akinator.addanswer(qkey, "Bill Gates", defaultmaybe)
    akinator.addanswer(qkey, "Elon Musk", defaultmaybe)
    akinator.addanswer(qkey, "Julius Caesar", defaultno)
    akinator.addanswer(qkey, "Pacman", defaultno)
    akinator.addanswer(qkey, "Snow White", defaultno)
    akinator.addanswer(qkey, "Charlie from Charlie and the Chocolate Factory", defaultno)
    
    qkey = akinator.addquestion("Are they based on an animal?")
    akinator.addanswer(qkey, "Harry Potter", defaultno)
    akinator.addanswer(qkey, "Donald Trump", defaultno)
    akinator.addanswer(qkey, "Pikachu", defaultyes)
    akinator.addanswer(qkey, "Heidi", defaultno)
    akinator.addanswer(qkey, "Popeye", defaultno)
    akinator.addanswer(qkey, "Queen Victoria", defaultno)
    akinator.addanswer(qkey, "PewDiePie", defaultno)
    akinator.addanswer(qkey, "Britney Spears", defaultno)
    akinator.addanswer(qkey, "Leonardo DiCaprio", defaultno)
    akinator.addanswer(qkey, "Gandalf", defaultno)
    akinator.addanswer(qkey, "Hillary Clinton", defaultno)
    akinator.addanswer(qkey, "Nelson Mandela", defaultno)
    akinator.addanswer(qkey, "Pythagoras", defaultno)
    akinator.addanswer(qkey, "Spiderman", defaultyes)
    akinator.addanswer(qkey, "Albert Einstein", defaultno)
    akinator.addanswer(qkey, "Marilyn Monroe", defaultno)
    akinator.addanswer(qkey, "Marie Curie", defaultno)
    akinator.addanswer(qkey, "J. K. Rowling", defaultno)
    akinator.addanswer(qkey, "Usain Bolt", defaultno)
    akinator.addanswer(qkey, "Bill Gates", defaultno)
    akinator.addanswer(qkey, "Elon Musk", defaultno)
    akinator.addanswer(qkey, "Julius Caesar", defaultno)
    akinator.addanswer(qkey, "Pacman", defaultno)
    akinator.addanswer(qkey, "Snow White", defaultno)
    akinator.addanswer(qkey, "Charlie from Charlie and the Chocolate Factory", defaultno)
    
    qkey = akinator.addquestion("Do they appear as a main state in a movie?")
    akinator.addanswer(qkey, "Harry Potter", defaultyes)
    akinator.addanswer(qkey, "Donald Trump", defaultno)
    akinator.addanswer(qkey, "Pikachu", defaultyes)
    akinator.addanswer(qkey, "Heidi", defaultyes)
    akinator.addanswer(qkey, "Popeye", defaultyes)
    akinator.addanswer(qkey, "Queen Victoria", defaultyes)
    akinator.addanswer(qkey, "PewDiePie", defaultno)
    akinator.addanswer(qkey, "Britney Spears", defaultno)
    akinator.addanswer(qkey, "Leonardo DiCaprio", defaultyes)
    akinator.addanswer(qkey, "Gandalf", defaultyes)
    akinator.addanswer(qkey, "Hillary Clinton", defaultno)
    akinator.addanswer(qkey, "Nelson Mandela", defaultyes)
    akinator.addanswer(qkey, "Pythagoras", defaultno)
    akinator.addanswer(qkey, "Spiderman", defaultyes)
    akinator.addanswer(qkey, "Albert Einstein", defaultno)
    akinator.addanswer(qkey, "Marilyn Monroe", defaultyes)
    akinator.addanswer(qkey, "Marie Curie", defaultno)
    akinator.addanswer(qkey, "J. K. Rowling", defaultno)
    akinator.addanswer(qkey, "Usain Bolt", defaultno)
    akinator.addanswer(qkey, "Bill Gates", defaultno)
    akinator.addanswer(qkey, "Elon Musk", defaultno)
    akinator.addanswer(qkey, "Julius Caesar", defaultyes)
    akinator.addanswer(qkey, "Pacman", defaultno)
    akinator.addanswer(qkey, "Snow White", defaultyes)
    akinator.addanswer(qkey, "Charlie from Charlie and the Chocolate Factory", defaultyes)
    
    for (state,qkey) in akinator.answerdict:
        if state not in akinator.states:
            akinator.states.append(state)
    akinator.numstates = len(akinator.states)
    print("States: %d, questions %d" % (akinator.numstates, len(akinator.questions)))
    
    """
    for state in states:
        qkey = akinator.addquestion("Is your state %s?" % state)
        for c in states:
            akinator.answerdict[(c,qkey)] = [0.005, 0.005, 0.99]
        akinator.answerdict[(state,qkey)] = [0.99, 0.005, 0.005] 
    """
    akinator.stateprobs = np.ones(shape=(akinator.numstates))/akinator.numstates
    akinator.statelogprobs = np.ones(shape=(akinator.numstates))*-np.log(akinator.numstates)

if __name__== "__main__":    
    akinator = Akinator()
    setup_character_akinator(akinator)
    questionno = 1
    while True:    
        qkey = akinator.getnextquestion()
        if qkey < 0:
            break
        akinator.usedquestions.append(qkey)
        answer = input("Q%d: %s " % (questionno, akinator.questions[qkey])).upper()
        akey = -1
        if answer.startswith("Y"):
            akey = YES
        elif answer.startswith("M"):
            akey = MAYBE
        elif answer.startswith("N"):
            akey = NO
        else:
            break
        akinator.update(qkey, akey)
        questionno += 1

