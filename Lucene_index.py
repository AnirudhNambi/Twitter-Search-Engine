import logging, sys
logging.disable(sys.maxsize)

import lucene
import json
import os
from org.apache.lucene.store import MMapDirectory, SimpleFSDirectory, NIOFSDirectory
from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.index import FieldInfo, IndexWriter, IndexWriterConfig, IndexOptions, DirectoryReader
from org.apache.lucene.search import IndexSearcher, BoostQuery, Query
from org.apache.lucene.search.similarities import BM25Similarity
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords

nltk.download('punkt')
nltk.download('stopwords')


# Function to normalize text
def normalize_text(text):
    # Lowercase the text
    text = text.lower()

    # Tokenize the text
    tokens = word_tokenize(text)

    # Remove stop words
    stop_words = set(stopwords.words("english"))
    tokens = [token for token in tokens if token not in stop_words]

    # Stem the tokens
    stemmer = SnowballStemmer("english")
    tokens = [stemmer.stem(token) for token in tokens]

    # Return the normalized text
    return " ".join(tokens)
def create_index(dir):
    if not os.path.exists(dir):
        os.mkdir(dir)
    store = SimpleFSDirectory(Paths.get(dir))
    analyzer = StandardAnalyzer()
    config = IndexWriterConfig(analyzer)
    config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
    writer = IndexWriter(store, config)

    metaType = FieldType()
    metaType.setStored(True)
    metaType.setTokenized(False)

    contextType = FieldType()
    contextType.setStored(True)
    contextType.setTokenized(True)
    contextType.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)

    # Iterate over the documents in the JSONL file
    with open("data.jsonl") as f:
        for line in f:
            data = json.loads(line)
            doc = Document()
            tid = data['data']['id']
            user=data['includes']['users'][0].get('username')
            FullText=data['data']['text']
            keyFullText=normalize_text(FullText)
            doc.add(Field('Tid', str(tid), metaType))
            doc.add(Field('username',str(user), metaType))
            doc.add(Field('tweet',str(FullText), metaType))
            doc.add(Field('normalized_tweet', str(keyFullText), contextType))
            writer.addDocument(doc)
        print("Indexing is done\n")
        writer.close()
lucene.initVM(vmargs=['-Djava.awt.headless=true'])
create_index('final_index/')

