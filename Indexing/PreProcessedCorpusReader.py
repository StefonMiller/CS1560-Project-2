import Classes.Path as Path

class PreprocessedCorpusReader:

    def __init__(self, type):
        # File pointer
        self.f = open(Path.ResultHM1 + type, encoding="utf8")
        return

    # Read a line for docNo from the corpus, read another line for the content, and return them in [docNo, content].
    def nextDocument(self):
        docNo = self.f.readline()
        content = self.f.readline()
        if len(docNo.strip()) == 0:
            return None
        return [docNo, content]