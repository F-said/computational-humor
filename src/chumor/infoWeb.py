import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import wikipedia


class infoWeb:
    def __init__(self, prompt):
        self.prompt = prompt

        self.subject = None
        self.subject_list = []

        self.context = None
        self.ref = None
        self.web = None
        self.outcome = None

        self.subvert = False
        self.humor_detected = False

    def getSubject(self):
        """
        Function to get list of noun phrases of the prompt. To be passed to Wikipedia and then to user to narrow
        subject matter selection.
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
        # Once subject is confirmed, create the web
        self.createWeb()

    def initialSearch(self):
        main_subjects = []

        # For each subject found in the prompt, do an initial search in Wikipedia.
        for subject in self.subject_list:
            search_results = wikipedia.search(subject)
            # For each result that was found
            for result in search_results:
                # Convert it into a list
                list_result = result.split(sep=" ")
                # Make list lower case
                list_result = [x.lower() for x in list_result]

                for other_subject in self.subject_list:
                    if other_subject in list_result:
                        main_subjects.append(" ".join(list_result))

        return main_subjects

    def createWeb(self):
        wiki_page = wikipedia.page(self.subject)
        self.web = wiki_page.content
        # Get references to use for later
        self.ref = wiki_page.references

        # Split web as a list
        self.web = self.web.split(sep=" ")

        # Get stem of wiki article
        ps = PorterStemmer()
        self.web = [ps.stem(word) for word in self.web]

        # Get stem of prompt
        self.context = [ps.stem(word) for word in self.context]

    def detectSubversion(self, outcome):
        # Save outcome to check for humor apart from subversion
        self.outcome = outcome
        self.outcome = self.outcome.split(sep=" ")

        fragments = []
        # Get all subsets of prompt
        for index, word in enumerate(self.context):
            for i in range(index + 1, len(self.context)):
                fragments.append(self.context[index:i])

        relevant_fragments = []
        for f in fragments:
            if set(f).issubset(self.web) and len(f) > 1:
                relevant_fragments.append(f)

        # Get ending statements of all relevant_fragments
        indices = []
        for frag in relevant_fragments:
            for e in frag:
                try:
                    indices.append(self.web.index(e))
                except ValueError:
                    continue

        # Remove duplicate indices
        indices = list(set(indices))

        outcomes = []
        for index in indices:
            atomic_outcome = []
            for i in range(index, len(self.web)):
                if (self.web[i][-1] is ".") or (self.web[i][-1] is ",") or (self.web[i][-1] is ";") or \
                        (self.web[i][-1] is "?") or (self.web[i][-1] is "!"):
                    break
                atomic_outcome.append(self.web[i])
            outcomes.append(atomic_outcome)

        # Split and stem the outcome to match the web
        outcome = outcome.split(sep=" ")

        ps = PorterStemmer()
        outcome = [ps.stem(word) for word in outcome]

        for ending in outcomes:
            if set(outcome).issubset(ending):
                self.subvert = False
        self.subvert = True

        return self.subvert

    def detectHumor(self):
        # Remove stop words from outcome
        stop = stopwords.words('english')
        self.outcome = [word.lower() for word in self.outcome if word not in stop]

        # TODO: Detect difference between humorous subversion and non-humorous subversion
