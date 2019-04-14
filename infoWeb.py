import nltk
from nltk import ne_chunk
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
        for index, r in enumerate(result):
            if type(r) == nltk.tree.Tree and type(result[index + 1]):
                self.subject_list.append(r)
            elif type(r) == nltk.tree.Tree:
                self.subject_list.append(r)

        return self.subject_list

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
