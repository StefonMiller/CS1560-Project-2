import Classes.Path as Path
from Indexing.MyIndexWriter import MyIndexWriter

# Efficiency and memory cost should be paid with extra attention.
class MyIndexReader:

    def __init__(self, type):
        print("finish reading the index")
         # File pointer
        if type == 'trecweb':
            self.dictReader = open(Path.IndexWebDir + "termDict", encoding="utf8")
            self.postingsReader = open(Path.IndexWebDir + "postingsList", encoding="utf8")
        else:
            self.dictReader = open(Path.IndexTextDir + "termDict", encoding="utf8")
            self.postingsReader = open(Path.IndexTextDir + "postingsList", encoding="utf8")
        # Dictionary of terms read in from the file
        self.termDict = {}

        # Read in the term dictionary from the termDict file
        for line in self.dictReader:
            # Strip colon and take first entry for the term, second entry is everything else
            temp = line.strip().split(':')
            term = temp[0]
            temp = temp[1]
            # Split the rest by comma to get the collection frequency and pointer to the postings list
            temp = temp.split(',')
            freq = temp[0]
            start = temp[1]
            self.termDict[term] = [freq, start]

    # Return the integer DocumentID of input string DocumentNo.
    def getDocId(self, docNo):
        # Get the corresponding document ID from the MyIndexWriter class
        return MyIndexWriter.docDict[docNo]

    # Return the string DocumentNo of the input integer DocumentID.
    def getDocNo(self, docId):
        # Iterate over the dictionary in the MyIndexWriter class to find the corresponding key to this value
        for key, value in MyIndexWriter.docDict.items():
            if docId == value:
                return key
        return None


    # Return DF.
    def DocFreq(self, token):
        # Get the corresponding pointer(line number) from the term dictionary for this term
        lineNum = self.termDict[token][1]
        # Enumerate all lines in the file without storing in memory
        for i, line in enumerate(self.postingsReader):
            # Check if the lines match up, if so convert the string to a dict
            if i == int(lineNum):
                temp = eval(line)
                assert type(temp) is dict
                # Reset file pointer and return the length of the dict(# of documents the term appears in)
                self.postingsReader.seek(0)
                return len(temp)
        # Reset file pointer
        self.postingsReader.seek(0)
        return 0

    # Return the frequency of the token in whole collection/corpus.
    def CollectionFreq(self, token):
        # Return the collection frequency from the term dictionary
        return self.termDict[token][0]

    # Return posting list in form of {documentID:frequency}.
    def getPostingList(self, token):
        # Get the corresponding pointer(line number) from the term dictionary for this term
        lineNum = self.termDict[token][1]
        # Enumerate all lines in the file without storing in memory
        for i, line in enumerate(self.postingsReader):
            # Check if the lines match up, if so convert the string to a dict
            if i == int(lineNum):
                temp = eval(line)
                assert type(temp) is dict
                # Return the corresponding postings list
                return temp
            