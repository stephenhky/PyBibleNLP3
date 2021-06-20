
import sqlite3

from .books.biblebooks import idx2books, numchaps


class BibleSQLiteConnector:
    def __init__(self, url):
        self.url = url
        self.conn = sqlite3.connect(self.url)
        self.cursor = self.conn.cursor()

    def iterate_all_chapters(self, preprocess=lambda x: x):
        iterator = self.cursor.execute("select Book, Chapter, group_concat(Scripture, ' ') " \
                                       "from Bible group by book, chapter order by book, chapter")
        for bookid, chapter, text in iterator:
            yield {
                'bookid': bookid,
                'chapter': chapter,
                'text': preprocess(text)
            }

    def iterate_all_verses(self, preprocess=lambda x: x):
        iterator = self.cursor.execute("select Book, Chapter, Verse, Scripture from Bible " \
                                       "order by Book, Chapter, Verse")
        for bookid, chapter, verse, text in iterator:
            yield {
                'bookid': bookid,
                'chapter': chapter,
                'verse': verse,
                'text': preprocess(text)
            }

    def iterate_all_chapters_verselist(self, preprocess=lambda x: x):
        for bookid in range(len(idx2books)):
            for chapter in range(numchaps[idx2books[bookid+1]]):
                iterator = self.cursor.execute("select Verse, Scripture from Bible " \
                                               "where Book={} and Chapter={} " \
                                               "order by Verse".format(bookid+1, chapter+1))
                yield {
                    'bookid': bookid+1,
                    'chapter': chapter+1,
                    'verse_text': [
                        (verse, preprocess(text))
                        for verse, text in iterator
                    ]
                }
