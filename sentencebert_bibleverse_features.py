
from argparse import ArgumentParser

from holymining.BibleDBConnector import BibleSQLiteConnector
from holymining.features import SentenceBERTSentenceFeatureVectorGenerator
from holymining.featurestore import BibleVerseH5FeatureStoreCreator


def get_argparser():
    argparser = ArgumentParser('Convert Bible chapters to Sentence BERT Embedding.')
    argparser.add_argument('bible_db', help='SQLiteDB file for the translation')
    argparser.add_argument('sbert_model', help='Name of the Sentence BERT model from huggingface.co (see sbert.net), or the path of the Sentence BERT model')
    argparser.add_argument('output_h5', help='Path of the output H5 file containing embeddings for each chapter.')
    return argparser


def write_out_embedding(bible_db, sbert_model, output_h5_path):
    connector = BibleSQLiteConnector(bible_db)
    sbert_transformer = SentenceBERTSentenceFeatureVectorGenerator(sbert_model)
    vecdim = sbert_transformer.get_embedding_dimension()
    embedding_featurestore_creator = BibleVerseH5FeatureStoreCreator(output_h5_path, vecdim)
    for biblechapter in connector.iterate_all_chapters_verselist():
        embeddings = sbert_transformer.transform([
            text for _, text in biblechapter['verse_text']
        ])
        for (verse, _), embedding in zip(biblechapter['verse_text'], embeddings):
            embedding_featurestore_creator.write_embedding(
                biblechapter['bookid'],
                biblechapter['chapter'],
                verse,
                embedding
            )
    embedding_featurestore_creator.close()


if __name__ == '__main__':
    args = get_argparser().parse_args()
    bible_db = args.bible_db
    sbert_model = args.sbert_model
    output_h5_path = args.output_h5

    write_out_embedding(bible_db, sbert_model, output_h5_path)
