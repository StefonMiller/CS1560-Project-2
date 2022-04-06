from re import S
import Classes.Path as Path
import math

# Efficiency and memory cost should be paid with extra attention.
class MyIndexWriter:

    # Global document dictionary
    docDict = {}

    def __init__(self, type):
        # Current document ID
        self.currIndex = 0

        # File pointer
        if type == 'trecweb':
            self.dictWriter = open(f"{Path.IndexWebDir}termDict", "w+", encoding="utf8")
            self.postingsWriter = open(f"{Path.IndexWebDir}postingsList", "w+", encoding="utf8")
        else:
            self.dictWriter = open(f"{Path.IndexTextDir}termDict", "w+", encoding="utf8")
            self.postingsWriter = open(f"{Path.IndexTextDir}postingsList", "w+", encoding="utf8")

        # Term dictionary for the corpus
        self.termDict = {}

        # Postings list for the corpus
        self.postingsList = []
        return

    # This method build index for each document.
	# NT: in your implementation of the index, you should transform your string docno into non-negative integer docids,
    # and in MyIndexReader, you should be able to request the integer docid for each docno.
    def index(self, docNo, content):
        # Check if the docNo is in the dictionary of terms, if not add it and increment the current document ID
        if docNo not in self.docDict:
            self.currIndex = self.currIndex + 1
            self.docDict[docNo] = self.currIndex
        # Iterate over terms in content
        for term in content.split():
            # Check if the term is in the term dictionary
            if term not in self.termDict:
                # If not in the list of terms, create an entry in the dictionary and postings list. Store the line of the postings list corresponding to the new term
                self.termDict[term] = [1, len(self.termDict)]
                self.postingsList.append({})
            else:
                # If the term is in the term dictionary, increment the frequency
                self.termDict[term][0] = self.termDict[term][0] + 1

            # Check if the postings list for that term has an entry for this document, if so increment that entry. If not, create it
            if self.currIndex in self.postingsList[self.termDict[term][1]]:
                self.postingsList[self.termDict[term][1]][self.currIndex] = self.postingsList[self.termDict[term][1]][self.currIndex] + 1
            else:
                self.postingsList[self.termDict[term][1]][self.currIndex] = 1
        return



    # Close the index writer, and you should output all the buffered content (if any).
    def close(self):
        # Write data for the term dictionary
        self.dictWriter.write(''.join(''.join([k, ':',  str(self.termDict[k][0]), ',', str(self.termDict[k][1]), '\n']) for k in self.termDict))
        # Write data for the postings list
        self.postingsWriter.write(''.join(''.join([str(p), '\n']) for p in self.postingsList))
        self.dictWriter.close()
        self.postingsWriter.close()
        return