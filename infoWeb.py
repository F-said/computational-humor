import nltk
from nltk.corpus import stopwords
import wikipedia


class infoWeb:
    def __init__(self, prompt):
        self.prompt = prompt

        self.subject = None
        self.subject_list = []

        self.context = None
        self.web = None
        self.subvert_nodes = None

        self.subvert = False
        self.humor_detected = False

    def getSubject(self):
        """
        Function to get list of noun phrases of the prompt. To be passed to first wikipedia and then to narrow selection
        user to narrow subject matter selection. 
        :return: A list of noun phrases
        """
        # Tokenize words
        words = nltk.tokenize.word_tokenize(self.prompt)

        # Get English "stop" words
        stop = stopwords.words('english')

        # Remove stop words from prompt
        words = [word.lower() for word in words if word not in stop]
        # Save these filtered words to use for the contextual web
        self.context = words

        # Tag each word in the prompt as word classes
        pos_tag = nltk.pos_tag(words)

        # Define a simple grammar taken from https://www.nltk.org/book/ch07.html
        grammar = "NP: {<DT>?<JJ>*<NN>}"
        # Define a simple chunk parser from this grammar
        cp = nltk.RegexpParser(grammar)
        # Parse noun-phrases using this grammar
        result = cp.parse(pos_tag)

        # Return all noun-phrases
        noun_phrases = self.extractPhrases(result, 'NP')

        for phrase in noun_phrases:
            addend = []
            for i in range(len(phrase.leaves())):
                addend.append(str(phrase[i][0]))
            self.subject_list.append(' '.join(addend))

        return self.subject_list

    # Function to extract noun phrases taken from
    # https://www.winwaed.com/blog/2012/01/20/extracting-noun-phrases-from-parsed-trees/
    def extractPhrases(self, myTree, phrase):
        phrases = []

        if myTree.label() == phrase:
            phrases.append(myTree.copy(True))

        for child in myTree:
            if type(child) is nltk.tree.Tree:
                list_of_phrases = self.extractPhrases(child, phrase)
                if len(list_of_phrases) > 0:
                    phrases.extend(list_of_phrases)

        return phrases

    def confirmSubject(self, subject):
        self.subject = subject

    def createWeb(self):
        self.web = None
        return None

    def detectSubversion(self, outcome):
        self.subvert_nodes = None
        return self.subvert

    def detectHumor(self):
        return self.humor_detected
