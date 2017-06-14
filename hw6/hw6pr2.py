# coding: utf-8


#
# hw6 problem 2 (also a lab problem, _if_ you join two labs!)
#

## Problem 2: Analogies!


# A helper function - are all words in the model?
#
def all_words_in_model( wordlist, model ):
    """ returns True if all w in wordlist are in model
        and False otherwise
    """
    for w in wordlist:
        if w not in model:
            return False
    return True


# Here's a demonstration of the fundamental capability of word2vec on which
#   you'll be building:  most_similar

def test_most_similar(model):
    """ example of most_similar """
    print("Testing most_similar on the king - man + woman example...")
    LoM = model.most_similar(positive=['woman', 'king'], negative=['man'], topn=10)
    # note that topn will be 100 below in check_analogy...
    return LoM
#
#
# Start of functions to write + test...
#
#

#
# Write your generate_analogy function
#
def generate_analogy(word1, word2, word3, model):
    """ generate_analogy's solve the analogy word1:word :: word3:? using the
        word2vec model model and return the best out of the list of the 100-best
        results.
    """
    LoM = model.most_similar(positive=[word2, word3], negative=[word1], topn=100)
    return LoM

#
# Write your check_analogy function
#
def check_analogy(word1, word2, word3, word4, model):
    """ check_analogy's ask word2vec to grade or check the analogy
        word1:word :: word3:word4 using the word2vec model model and
        returns a score for word4.
    """
    LoM = model.most_similar(positive=[word2, word3], negative=[word1], topn=100)
    topNList = [x[0]for x in LoM]
    if word4 not in topNList:
        return 0
    else:
        score = 100
        for word in topNList:
            if word != word4:
                score -= 1
            else:
                return score
#
# Results and commentary...
#

#
# (1) Write generate_analogy and try it out on several examples of your own
#     choosing (be sure that all of the words are in the model --
#     use the all_words_in_model function to help here)
#
# (2) Report two analogies that you create (other than the ones we looked at in class)
#     that _do_ work reaonably well and report on two that _don't_ work well
#     Finding ones that _do_ work well is more difficult! Maybe in 2025, it'll be the opposite (?)
#       generate_analogy("father","mother","uncle",m)
#       [('aunt', 0.904949426651001)]
#
#       generate_analogy("pilot","plane","driver", m)
#       [('car', 0.5955188274383545)]
#
# (3) Write check_analogy that should return a "score" on how well word2vec_model
#     does at solving the analogy given (for word4)
#     + it should determine where word4 appears in the top 100 (use topn=100) most-similar words
#     + if it _doens't_ appear in the top-100, it should give a score of 0
#     + if it _does_ appear, it should give a score between 1 and 100: the distance from the
#       _far_ end of the list. Thus, a score of 100 means a perfect score. A score of 1 means that
#       word4 was the 100th in the list (index 99)
#     + Try it out:   check_analogy( "man", "king", "woman", "queen", m ) -> 100
#                     check_analogy( "woman", "man", "bicycle", "fish", m ) -> 0
#                     check_analogy( "woman", "man", "bicycle", "pedestrian", m ) -> 96

#
# (4) Create at least five analogies that perform at varying levels of "goodness" based on the
#     check_analogy scoring criterion -- share those (and any additional analysis) with us here!
#           generate_analogy("agenda","meeting","function",m)
#           [('functions', 0.4402162730693817)]
#           generate_analogy("dusk","night","infant",m)
#           [('baby', 0.5449514985084534)]
#           generate_analogy("canvas","painter","marble",m)
#           [('sculptor', 0.5535140037536621)]
#           generate_analogy("fox","cunning","ant", m)
#           [('devious', 0.465126097202301)]
#           generate_analogy("orange","fruit", "tomatoes",m)
#           [('vegetables', 0.6388487815856934)]
#
