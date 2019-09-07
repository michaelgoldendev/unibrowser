import akinator_model
import akinator_character_questionsanswers
import akinator_geography_questionsanswers
import numpy as np

if __name__== "__main__":    
    akinator = akinator_model.Akinator()
    akinator_geography_questionsanswers.setup_geography_akinator(akinator)
    questionno = 1
    while True:    
        qkey = akinator.getnextquestion()
        if qkey < 0:
            break
        akinator.usedquestions.append(qkey)
        answer = input("Q%d: %s " % (questionno, akinator.questions[qkey])).upper()
        akey = -1
        if answer.startswith("Y"):
            akey = akinator_character_questionsanswers.YES
        elif answer.startswith("M"):
            akey = akinator_character_questionsanswers.MAYBE
        elif answer.startswith("N"):
            akey = akinator_character_questionsanswers.NO
        else:
            break
        akinator.update(qkey, akey)
        questionno += 1

