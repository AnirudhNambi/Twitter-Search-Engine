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
#retrieval of data
def retrieve(storedir, query):
    searchDir = NIOFSDirectory(Paths.get(storedir))
    searcher = IndexSearcher(DirectoryReader.open(searchDir))

    parser = QueryParser('normalized_tweet', StandardAnalyzer())
    parsed_query = parser.parse(query)

    topDocs = searcher.search(parsed_query, 10).scoreDocs
    topkdocs = []
    for hit in topDocs:
        doc = searcher.doc(hit.doc)
        topkdocs.append({
            "score": hit.score,
            "text": doc.get("tweet"),
            "tid":doc.get("Tid"),
            "user":doc.get("username")
            })
    for doc in topkdocs:
        print("user:",doc["user"],'\t',"With a score:",doc["score"],'\n')
        print("tweet:",doc["text"],'\n')
query=input("enter query\n")
lucene.initVM(vmargs=['-Djava.awt.headless=true'])
retrieve('final_index/',query)
