
from argparse import ArgumentParser
from operator import itemgetter

from scipy.spatial.distance import cosine

from reformedcatutils.biblebooks import idx2books, getBookName
from holymining.features import SentenceBERTSentenceFeatureVectorGenerator
from holymining.featurestore import BibleChapterH5FeatureStoreRetriever


def get_argparser():
    argparser = ArgumentParser(description='Retrieving relevant bible chapters.')
    argparser.add_argument('sbert_model', help='Name of the Sentence BERT model from huggingface.co (see sbert.net), or the path of the Sentence BERT model')
    argparser.add_argument('featurestore_h5', help='H5 file for feature-store.')
    argparser.add_argument('--nbrecords', type=int, default=5, help='Number of record to show. (Default: 5)')
    argparser.add_argument('--threshold', type=float, default=0.0, help='Threshold to truncate. (Default: 0.0)')
    return argparser


def retrieve_bible_chapters(text, sbert_transformer, featurestore_retriever, threshold=0.0):
    input_embedding = sbert_transformer.transform([text])
    allmatches = [
        {
            'bookid': bookid,
            'bookabbr': idx2books[bookid],
            'book': getBookName(idx2books[bookid]),
            'chapter': chapter,
            'similarity': 1 - cosine(input_embedding, embedding)
        }
        for bookid, chapter, embedding in featurestore_retriever.iterate_all_records()
    ]
    allmatches = [match for match in allmatches if match['similarity'] > threshold]
    allmatches = sorted(allmatches, key=itemgetter('similarity'), reverse=True)
    return allmatches


def bible_retriever_console(
        sbert_model,
        featurestore_h5_path,
        nbrecords=5,
        threshold=0.0
):
    sbert_transformer = SentenceBERTSentenceFeatureVectorGenerator(sbert_model)
    featurestore_retriever = BibleChapterH5FeatureStoreRetriever(featurestore_h5_path)

    done = False
    while not done:
        text = input('Text> ')
        if text is None or len(text) <= 0:
            done = True
        else:
            sorted_chapters = retrieve_bible_chapters(text, sbert_transformer, featurestore_retriever, threshold=threshold)
            for i, chapter in enumerate(sorted_chapters):
                if i > nbrecords:
                    break
                print('-------------')
                print('Record {}'.format(i+1))
                print('Book: {}; Chapter: {}'.format(chapter['book'], chapter['chapter']))
                print('Similarity: {:.6f}'.format(chapter['similarity']))

    featurestore_retriever.close()


if __name__ == '__main__':
    args = get_argparser().parse_args()
    sbert_model = args.sbert_model
    featurestore_h5_path = args.featurestore_h5
    nbrecords = args.nbrecords
    threshold = args.threshold

    bible_retriever_console(
        sbert_model,
        featurestore_h5_path,
        nbrecords=nbrecords,
        threshold=threshold
    )
