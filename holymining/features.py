
from abc import ABC, abstractmethod

from sentence_transformers import SentenceTransformer


class FeatureVectorGenerator(ABC):
    @abstractmethod
    def transform(self, texts):
        pass


class SentenceBERTSentenceFeatureVectorGenerator(FeatureVectorGenerator):
    def __init__(self, sentence_bert_model):
        self.model_name = sentence_bert_model
        self.model = SentenceTransformer(self.model_name)

    def transform(self, sentences):
        return self.model.encode(sentences)


