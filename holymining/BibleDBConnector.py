
import sqlite3


class BibleSQLiteConnector:
    def __init__(self, url):
        self.url = url
        self.conn = sqlite3.connect(self.url)
        self.cursor = self.conn.cursor()

    def iterate_all_chapters(self):
        iterator = self.cursor.execute("select Book, Chapter, group_concat(Scripture, ' ')" \
                                       "from Bible group by book, chapter order by book, chapter")
        for bookid, chapter, text in iterator:
            yield {
                'bookid': bookid,
                'chapter': chapter,
                'text': text
            }
