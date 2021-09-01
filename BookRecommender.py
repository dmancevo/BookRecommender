import pandas as pd
from contextlib import contextmanager
from typing import List, Tuple, Dict
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.preprocessing import normalize


class BookRecommender:

    def __init__(self, books:List[Dict[str, str]]) -> None:
        
        # Model
        self.transformer = SentenceTransformer(
#             "paraphrase-mpnet-base-v2" # English.
#             "paraphrase-multilingual-mpnet-base-v2" # Multilingual.
            "msmarco-distilbert-base-tas-b"
        )

        # List of books.
        self.books = pd.DataFrame(books)

        # Embeddings.
        self.emb = normalize(
            self.transformer.encode(
                self.books.apply(
                    lambda row: f"{row.title} {row.description}",
                    axis=1)))

        
    def __call__(self, text:str, top_n:int=1) -> List[Tuple[str, str, str, str]]:
        query = self.transformer.encode([text]).T
        similarities = self.emb.dot(query)[:,0]
        ids = np.argpartition(similarities, len(similarities)-top_n)[-top_n:]
        top_books = [(b,s) for b,s in zip(self.books.iloc[ids].values.tolist(),
                                          similarities[ids])]
        top_books.sort(key=lambda t: t[1], reverse=True)
        return [b for b,_ in top_books]