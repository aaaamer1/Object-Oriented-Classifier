# Copyright 2020-2022 Paul Lu
import sys
import copy     # for deepcopy()
import string


Debug = False   # Sometimes, print for debugging.  Overridable on command line.
InputFilename = "file.input.txt"
TargetWords = [
    'outside', 'today', 'weather', 'raining', 'nice', 'rain', 'snow',
    'day', 'winter', 'cold', 'warm', 'snowing', 'out', 'hope', 'boots',
    'sunny', 'windy', 'coming', 'perfect', 'need', 'sun', 'on', 'was',
    '-40', 'jackets', 'wish', 'fog', 'pretty', 'summer'
]
# Global List
Stop_Words = [
    "i", "me", "my", "myself", "we", "our",
    "ours", "ourselves", "you", "your",
    "yours", "yourself", "yourselves", "he",
    "him", "his", "himself", "she", "her",
    "hers", "herself", "it", "its", "itself",
    "they", "them", "their", "theirs",
    "themselves", "what", "which", "who",
    "whom", "this", "that", "these", "those",
    "am", "is", "are", "was", "were", "be",
    "been", "being", "have", "has", "had",
    "having", "do", "does", "did", "doing",
    "a", "an", "the", "and", "but", "if",
    "or", "because", "as", "until", "while",
    "of", "at", "by", "for", "with",
    "about", "against", "between", "into",
    "through", "during", "before", "after",
    "above", "below", "to", "from", "up",
    "down", "in", "out", "on", "off", "over",
    "under", "again", "further", "then",
    "once", "here", "there", "when", "where",
    "why", "how", "all", "any", "both",
    "each", "few", "more", "most", "other",
    "some", "such", "no", "nor", "not",
    "only", "own", "same", "so", "than",
    "too", "very", "s", "t", "can", "will",
    "just", "don", "should", "now"
]

############################################ WE 4 CODE ###########################################


def to_lower(words):
    wordList = list()  # creates empty list
    for word in words:  # for each word in words, take every element and convert to lowercase
        wordList.append(word.lower())
    return wordList


def remove_punc(words):
    wordList = list()
    for word in words:  # for each word in words, remove punctuation marks and non alphanumeric letters
        tempWord = ""
        for letter in word:
            if letter in string.ascii_letters or letter in string.digits:
                tempWord += letter
        wordList.append(tempWord)
    return wordList


def remove_digits(words):
    wordList = list()
    for word in words:  # removes elements that have both letters and numbers
        cumulative_word = ""
        for letter in word:
            if letter not in string.digits:
                cumulative_word += letter
        if cumulative_word == "":
            wordList.append(word)  # because the word is a number fully.
        else:
            wordList.append(cumulative_word)
    return wordList


def remove_stop_words(words):
    wordList = list()
    for word in words:  # removes any word in Stop_Words array
        if not word in Stop_Words:
            wordList.append(word)
    return wordList


def processed_words(words):
    processed = list()
    for word in words:  # removes empty elements from string arrays
        if not word == "" and not word in processed:
            processed.append(word)
    return processed

####################################### END PREPROCESS DEFS ########################################


def open_file(filename=InputFilename):
    try:
        f = open(filename, "r")
        return (f)
    except FileNotFoundError:
        # FileNotFoundError is subclass of OSError
        if Debug:
            print("File Not Found")
        return (sys.stdin)
    except OSError:
        if Debug:
            print("Other OS Error")
        return (sys.stdin)


def safe_input(f=None, prompt=""):
    try:
        # Case:  Stdin
        if f is sys.stdin or f is None:
            line = input(prompt)
        # Case:  From file
        else:
            assert not (f is None)
            assert (f is not None)
            line = f.readline()
            if Debug:
                print("readline: ", line, end='')
            if line == "":  # Check EOF before strip()
                if Debug:
                    print("EOF")
                return ("", False)
        return (line.strip(), True)
    except EOFError:
        return ("", False)


class C274:
    def __init__(self):
        self.type = str(self.__class__)
        return

    def __str__(self):
        return (self.type)

    def __repr__(self):
        s = "<%d> %s" % (id(self), self.type)
        return (s)


class ClassifyByTarget(C274):

    def __init__(self, lw=[]):
        super().__init__()      # Call superclass
        # self.type = str(self.__class__)
        self.allWords = 0
        self.theCount = 0
        self.nonTarget = []
        self.set_target_words(lw)
        self.initTF()
        return

    def initTF(self):
        self.TP = 0
        self.FP = 0
        self.TN = 0
        self.FN = 0
        return

    # FIXME:  Incomplete.  Finish get_TF() and other getters/setters.
    def get_TF(self):
        return (self.TP, self.FP, self.TN, self.FN)

    # TODO: Could use Use Python properties
    #     https://www.python-course.eu/python3_properties.php
    def set_target_words(self, lw):
        # Could also do self.targetWords = lw.copy().  Thanks, TA Jason Cannon
        self.targetWords = copy.deepcopy(lw)
        return

    def get_target_words(self):
        return (self.targetWords)

    def get_allWords(self):
        return (self.allWords)

    def incr_allWords(self):
        self.allWords += 1
        return

    def get_theCount(self):
        return (self.theCount)

    def incr_theCount(self):
        self.theCount += 1
        return

    def get_nonTarget(self):
        return (self.nonTarget)

    def add_nonTarget(self, w):
        self.nonTarget.append(w)
        return

    def print_config(self, printSorted=True):
        print("-------- Print Config --------")
        ln = len(self.get_target_words())
        print("TargetWords (%d): " % ln, end='')
        if printSorted:
            print(sorted(self.get_target_words()))
        else:
            print(self.get_target_words())
        return

    def print_run_info(self, printSorted=True):
        print("-------- Print Run Info --------")
        print("All words:%3s. " % self.get_allWords(), end='')
        print(" Target words:%3s" % self.get_theCount())
        print("Non-Target words (%d): " % len(self.get_nonTarget()), end='')
        if printSorted:
            print(sorted(self.get_nonTarget()))
        else:
            print(self.get_nonTarget())
        return

    def print_confusion_matrix(self, targetLabel, doKey=False, tag=""):
        assert (self.TP + self.TP + self.FP + self.TN) > 0
        print(tag+"-------- Confusion Matrix --------")
        print(tag+"%10s | %13s" % ('Predict', 'Label'))
        print(tag+"-----------+----------------------")
        print(tag+"%10s | %10s %10s" % (' ', targetLabel, 'not'))
        if doKey:
            print(tag+"%10s | %10s %10s" % ('', 'TP   ', 'FP   '))
        print(tag+"%10s | %10d %10d" % (targetLabel, self.TP, self.FP))
        if doKey:
            print(tag+"%10s | %10s %10s" % ('', 'FN   ', 'TN   '))
        print(tag+"%10s | %10d %10d" % ('not', self.FN, self.TN))
        return

    def eval_training_set(self, tset, targetLabel, lines=True):
        print("-------- Evaluate Training Set --------")
        self.initTF()
        # zip is good for parallel arrays and iteration
        z = zip(tset.get_instances(), tset.get_lines())
        for ti, w in z:
            lb = ti.get_label()
            cl = ti.get_class()
            if lb == targetLabel:
                if cl:
                    self.TP += 1
                    outcome = "TP"
                else:
                    self.FN += 1
                    outcome = "FN"
            else:
                if cl:
                    self.FP += 1
                    outcome = "FP"
                else:
                    self.TN += 1
                    outcome = "TN"
            explain = ti.get_explain()
            # Format nice output
            if lines:
                w = ' '.join(w.split())
            else:
                w = ' '.join(ti.get_words())
                w = lb + " " + w

            # TW = testing bag of words words (kinda arbitrary)
            print("TW %s: ( %10s) %s" % (outcome, explain, w))
            if Debug:
                print("-->", ti.get_words())
        self.print_confusion_matrix(targetLabel)
        return

    def classify_by_words(self, ti, update=False, tlabel="last"):
        inClass = False
        evidence = ''
        lw = ti.get_words()
        for w in lw:
            if update:
                self.incr_allWords()
            if w in self.get_target_words():    # FIXME Write predicate
                inClass = True
                if update:
                    self.incr_theCount()
                if evidence == '':
                    evidence = w            # FIXME Use first word, but change
            elif w != '':
                if update and (w not in self.get_nonTarget()):
                    self.add_nonTarget(w)
        if evidence == '':
            evidence = '#negative'
        if update:
            ti.set_class(inClass, tlabel, evidence)
        return (inClass, evidence)

    # Could use a decorator, but not now
    def classify(self, ti, update=False, tlabel="last"):
        cl, e = self.classify_by_words(ti, update, tlabel)
        return (cl, e)

    def classify_all(self, ts, update=True, tlabel="classify_all"):
        for ti in ts.get_instances():
            cl, e = self.classify(ti, update=update, tlabel=tlabel)
        return


class ClassifyByTopN(ClassifyByTarget):
    def target_top_n(self, tset, num=5, label=''):
        matching_label = []
        # Add all labels that match to the list
        for instance in  tset.get_instances():
            if (instance.get_label() == label):
                matching_label.append(instance)
                
        words = list()
        # put all words in all matching labels into one list.
        for instance in matching_label:
            for word in instance.get_words():
                words.append(word)
            # words.append(instance.get_words())
        
        word_freq = dict()

        if not words:
            self.set_target_words([])
            return 
        
        words = sorted(words) #sorts list of words lexicographically
        counter = dict() #creates empty dictionary
        for word in words:
            if word in counter:
                counter[word] += 1 #add element to dictionary
            else:
                counter[word] = 1
        numb = len(words) #counts number of words in list of sorted words
        for word in counter:
            word_freq[word] = counter[word] / numb
            
        max_freq_list = dict()
        temp_word_freq = word_freq
        # loop the minimum amount needed for top num target words
        for i in range(num):            
            max_freq = 0
            max_freq_word = ""
            for word in temp_word_freq: # loop over all words
                if temp_word_freq[word] > max_freq: # find the largest
                    max_freq = temp_word_freq[word]
                    max_freq_word = word
            max_freq_list[max_freq_word] = max_freq # add to top num freq dictionary      
            temp_word_freq.pop(max_freq_word) # remove word from freq dictionary so we dont add it again.
        
        # check for ties
        new_freq = dict()
        
        for word in max_freq_list: # loop over all found max frequicies
            for w in temp_word_freq: # now loop over remaining frequicies after inital king of the hill algorothm
                if max_freq_list[word] == temp_word_freq[w]: # if there is a word with the same freq then also add to the list.
                    new_freq[w] = temp_word_freq[w]
                    # max_freq_list[w] = temp_word_freq[w]
        all_freq = new_freq | max_freq_list
        self.set_target_words(list(all_freq.keys()))
        return


class TrainingInstance(C274):
    instances = []

    def __init__(self):
        super().__init__()              # Call superclass
        # self.type = str(self.__class__)
        self.inst = dict()

        # self.label = "N/A"
        # self.words = []
        # self._class = ""
        # self.explain = ""
        # self.experiments = dict()
        self.instances.append(self)
        # FIXME:  Get rid of dict, and use attributes
        self.inst["label"] = "N/A"      # Class, given by oracle
        self.inst["words"] = []         # Bag of words
        self.inst["class"] = ""         # Class, by classifier
        self.inst["explain"] = ""       # Explanation for classification
        self.inst["experiments"] = dict()   # Previous classifier runs
        return

    # When Invoked applies all the preprocessing functions to all words in training instance.

    def preprocess_words(self, mode=''):
        self.inst["words"] = to_lower(self.inst["words"])
        if mode == "keep-symbols":
            self.inst["words"] = remove_digits(self.inst["words"])
            self.inst["words"] = remove_stop_words(self.inst["words"])

        if mode == "keep-digits":
            self.inst["words"] = remove_punc(self.inst["words"])
            self.inst["words"] = remove_stop_words(self.inst["words"])

        if mode == "keep-stops":
            self.inst["words"] = remove_punc(self.inst["words"])
            self.inst["words"] = remove_digits(self.inst["words"])

        if not mode:
            self.inst["words"] = remove_punc(self.inst["words"])
            self.inst["words"] = remove_digits(self.inst["words"])
            self.inst["words"] = remove_stop_words(self.inst["words"])
        return

    def get_label(self):
        # return (self.label)
        return (self.inst["label"])

    def get_words(self):
        # return (self.words)
        return (self.inst["words"])

    def set_class(self, theClass, tlabel="last", explain=""):
        # tlabel = tag label
        # self._class = theClass
        # self.experiments[tlabel] = theClass
        # self.explain = explain

        self.inst["class"] = theClass
        self.inst["experiments"][tlabel] = theClass
        self.inst["explain"] = explain
        return

    def get_class_by_tag(self, tlabel):             # tlabel = tag label
        # cl = self.experiments.get(tlabel)
        cl = self.inst["experiments"].get(tlabel)
        if cl is None:
            return ("N/A")
        else:
            return (cl)

    def get_explain(self):
        # cl = self.explain
        cl = self.inst.get("explain")
        if cl is None:
            return ("N/A")
        else:
            return (cl)

    def get_class(self):
        # return self._class
        return self.inst["class"]

    def process_input_line(self, line, run=None, tlabel="read", inclLabel=False):
        for word in line.split():
            if word[0] == "#":
                self.label = word
                self.inst["label"] = word
                if inclLabel:
                    # self.words.append(word)
                    self.inst["words"].append(word)
            else:
                # self.words.append(word)
                self.inst["words"].append(word)

        if not (run is None):
            cl, e = run.classify(self, update=True, tlabel=tlabel)
        return (self)


class TrainingSet(C274):
    instances = []  # Reference counting

    def __init__(self):
        super().__init__()      # Call superclass
        # self.type = str(self.__class__)
        self.inObjList = []     # Unparsed lines, from training set
        self.inObjHash = []     # Parsed alines, in dictionary/hash
        self.variable = dict()  # NEW: Configuration/environment variables
        self.instances.append(self)
        return

    # round robin dist algoeithm, it finds a number of lists needed in order to sort elements 
    # it then sorts them like a deck of cards, giving a element to each sublist from the super list
    # then once all lists are given an element it resets back to the first list.
    def round_robin_dist(self, lst, n = 3):
        list = lst
        # prepare a list of sublists of the original.
        # so we divide the number of elements in original list by elements each list should have and round up to get max list size.
        result = []
        for x in range(n):
            result.append([])
        i = 0
        while list:
            result[i].append(list[0])
            list.pop(0)
            i += 1
            if (i > len(result) - 1):
                i = 0
                
        return result
    
    def copy(self):
        tset = TrainingSet()
        
        tset.inObjHash = copy.deepcopy(self.inObjHash)
        
        tset.inObjList = copy.deepcopy(self.inObjList)
        
        tset.variable = copy.deepcopy(self.variable)
        
        return tset
    
    def add_training_set(self, tset):
        for i in range(len(tset.get_instances())):
            self.inObjHash.append(copy.deepcopy(tset.get_instances()[i]))
            self.inObjList.append(copy.deepcopy(tset.get_lines()[i]))
                

    def return_nfolds(self, num=3):
        instances = []
        lines = []
        for i in self.get_instances():
            instances.append(copy.deepcopy(i))
        dist_instances = self.round_robin_dist(instances, num)
        
        for i in self.get_lines():
            lines.append(copy.deepcopy(i))
        dist_lines = self.round_robin_dist(lines, num)
        
        new_tsets = []
        for i in range(len(dist_instances)):
            ntset = TrainingSet()
            ntset.variable = copy.deepcopy(self.variable)
            ntset.inObjHash = copy.deepcopy(dist_instances[i])
            ntset.inObjList = copy.deepcopy(dist_lines[i])
            new_tsets.append(ntset)
            
        return new_tsets 

    def preprocess(self, mode=''):
        for instance in self.inObjHash:
            instance.preprocess_words(mode)
        return

    def set_env_variable(self, k, v):
        self.variable[k] = v
        return

    def get_env_variable(self, k):
        if k in self.variable:
            return (self.variable[k])
        else:
            return ""

    def inspect_comment(self, line):
        if len(line) > 1 and line[1] != ' ':      # Might be variable
            v = line.split(maxsplit=1)
            self.set_env_variable(v[0][1:], v[1])
        return

    def get_instances(self):
        # can be protected by returning a copy of the instancs and list.
        # return (copy.deepcopy(self.inObjHash))
        return (self.inObjHash)      # FIXME Should protect this more

    def get_lines(self):
        # return (copy.deepcopy(self.inObjList))
        return (self.inObjList)      # FIXME Should protect this more

    def print_training_set(self):
        print("-------- Print Training Set --------")
        z = zip(self.inObjHash, self.inObjList)
        for ti, w in z:
            lb = ti.get_label()
            cl = ti.get_class_by_tag("last")     # Not used
            explain = ti.get_explain()
            print("( %s) (%s) %s" % (lb, explain, w))
            if Debug:
                print("-->", ti.get_words())
        return

    def process_input_stream(self, inFile, run=None):
        assert not (inFile is None), "Assume valid file object"
        cFlag = True
        while cFlag:
            line, cFlag = safe_input(inFile)
            if not cFlag:
                break
            assert cFlag, "Assume valid input hereafter"

            if len(line) == 0:   # Blank line.  Skip it.
                continue

            # Check for comments *and* environment variables
            if line[0] == '%':  # Comments must start with % and variables
                self.inspect_comment(line)
                continue

            # Save the training data input, by line
            self.inObjList.append(line)
            # Save the training data input, after parsing
            ti = TrainingInstance()
            ti.process_input_line(line, run=run)
            self.inObjHash.append(ti)
        return


# Very basic test of functionality
def basemain():
    global Debug
    tset = TrainingSet()
    run1 = ClassifyByTarget(TargetWords)
    if Debug:
        print(run1)     # Just to show __str__
        lr = [run1]
        print(lr)       # Just to show __repr__

    argc = len(sys.argv)
    if argc == 1:   # Use stdin, or default filename
        inFile = open_file()
        assert not (inFile is None), "Assume valid file object"
        tset.process_input_stream(inFile, run1)
        inFile.close()
    else:
        for f in sys.argv[1:]:
            # Allow override of Debug from command line
            if f == "Debug":
                Debug = True
                continue
            if f == "NoDebug":
                Debug = False
                continue

            inFile = open_file(f)
            assert not (inFile is None), "Assume valid file object"
            tset.process_input_stream(inFile, run1)
            inFile.close()

    print("--------------------------------------------")
    plabel = tset.get_env_variable("pos-label")
    print("pos-label: ", plabel)
    print("NOTE: Not using any target words from the file itself")
    print("--------------------------------------------")

    if Debug:
        tset.print_training_set()
    run1.print_config()
    run1.print_run_info()
    run1.eval_training_set(tset, plabel)

    return


if __name__ == "__main__":
    basemain()
