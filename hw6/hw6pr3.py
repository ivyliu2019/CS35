# coding: utf-8
#
# hw6 problem 3
#

## Problem 3: Paraphrasing!

import textblob
from textblob import Word

# A starter function that substitutes each word with it's top match
#   in word2vec.  Your task: improve this with POS tagging, lemmatizing,
#   and/or at least three other ideas of your own (more details below)
#
def paraphrase_sentence( sentence, model ):
    """ paraphrase_sentence's docstring - be sure to include it!
    """
    blob = textblob.TextBlob( sentence )
    # print("The sentence's words are")
    LoW = blob.words
    # print(LoW)

    taggingL = blob.tags
    LoA = []
    NewLoW = []
    index = -1
    for w in LoW:
        index += 1
        tag = taggingL[index]
        if w not in model:
            NewLoW += [w]
        else:
            alternativeList = [w]
            w_alternatives = model.most_similar(positive=[w], topn=100)
            # wAlternativeList = []
            # print("w_alternatives is", w_alternatives)
            for alternative in w_alternatives:
                # lemmatizing
                if Word(alternative[0]).lemmatize().lower() != Word(w).lemmatize().lower():
                    # the replacement word can't have the same first letter
                    # as the originalthe replacement word can't have the same
                    # first letter as the original
                    if alternative[0][0].lower()!= w[0].lower():
                        alterTag = textblob.TextBlob(alternative[0]).tags[0][1]
                       # part-of-speech tagging to ensure
                        if tag[1] == alterTag:
                            first_alternative, first_alternative_score = alternative
                            alternativeList += [first_alternative]
                            break
            NewLoW += [alternativeList[-1]]

    # you should change this so that it returns a new string (a new sentence),
    # NOT just print a list of words (that's what's provided in this starter code)
    # print( "NewLoW is" )
    return( ' '.join(NewLoW) + '.')  # this is a new low!

#
# Once the above function is more sophisticated (it certainly does _not_ need to be
#   perfect -- that would be impossible...), then write a file-paraphrasing function:
#
def paraphrase_file(filename, model):
    """ paraphrase_file's docstring - be sure to include it!
    """
    import nltk.data
    sentences = []
    paraphrasedtext = []
    # read sentences from file
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    fp = open(filename)
    data = fp.read()
    sentences += tokenizer.tokenize(data)
    # paraphrasing
    paraphrasedtext += [str(paraphrase_sentence(sentence, model)) for sentence in sentences]
    # write out the paragraph to the txt file
    with open('test_paraphrased.txt', 'w') as f:
        f.write(' '.join(paraphrasedtext))
    return

#
# Results and commentary...
#

# (1) Try paraphrase_sentence as it stands (it's quite bad...)  E.g.,
#         Try:    paraphrase_sentence("Don't stop thinking about tomorrow!", m)
#         Result: ['Did', "n't", 'stopped', 'Thinking', 'just', 'tonight']

#     First, change this so that it returns (not prints) a string (the paraphrased sentence),
#         rather than the starter code it currently has (it prints a list) Thus, after the change:

#         Try:    paraphrase_sentence("Don't stop thinking about tomorrow!", m)
#         Result: "Did n't stopped Thinking just tonight"  (as a return value)

#     But paraphrase_sentence is bad, in part, because words are close to variants of themselves, e.g.,
#         + stop is close to stopped
#         + thinking is close to thinking


# (2) Your task is to add at least three things that improve this performance (though it
#     will necessarily still be far from perfect!) Choose at least one of these two ideas to implement:

#     #1:  Use lemmatize to check if two words have the same stem/root - and _don't_ use that one!
#             + Instead, go _further_ into the similarity list (past the initial entry!)
#     #2:  Use part-of-speech tagging to ensure that two words can be the same part of speech

#     Then, choose two more ideas that use NLTK, TextBlob, or Python strings -- either to guard against
#     bad substitutions OR to create specific substitutions you'd like, e.g., just some ideas:
#        + the replacement word can't have the same first letter as the original
#        + the replacement word is as long as possible (up to some score cutoff)
#        + the replacement word is as _short_ as possible (again, up to some score cutoff...)
#        + replace things with their antonyms some or all of the time
#        + use the spelling correction or translation capabilities of TextBlob in some cool way
#        + use as many words as possible with the letter 'z' in them!
#        + don't use the letter 'e' at all...
#     Or any others you might like!


# (3) Share at least 4 examples of input/output sentence pairs that your paraphraser creates
#        + include at least one "very successful" one and at least one "very unsuccessful" ones
#           Try:    paraphrase_sentence("Don't stop thinking about tomorrow!", m) - very unsuccessfuL
#           NewLoW is: Do n't keep dreaming over morning
#           Try:    paraphrase_sentence("happy birthday!",m) - successful
#           NewLoW is: pleased anniversary
#           Try: paraphrase_sentence("Students often use too many direct quotations when they take notes", m)
#           NewLoW is: Undergraduates sometimes use so several reciprocal translations how we take writes
#           Try :   paraphrase_sentence("Reread the original passage until you understand its full meaning.",m)
#           NewLoW is: Reread another actual enactment before I understand their complete denote

# (4) Create a function paraphrase_file that opens a plain-text file, reads its contents,
#     tokenizes it into sentences, paraphrases all of the sentences, and writes out a new file
#     containing the full, paraphrased contents with the word paraphrased in its name, e.g.,
#        + paraphrase_file( "test.txt", model )
#             should write out a file names "test_paraphrased.txt"  with paraphrased contents...
#        + include an example file, both its input and output -- and make a comment on what you
#             chose and how it did!



# (Optional EC) For extra-credit (up to +5 pts or more)
#        + [+2] write a function that takes in a sentence, converts it (by calling the function above) and
#          then compares the sentiment score (the polarity and/or subjectivity) before and after
#          the paraphrasing
#        + [+3 or more beyond this] create another function that tries to create the most-positive or
#          most-negative or most-subjective or least-subjective -- be sure to describe what your
#          function does and share a couple of examples of its input/output...
