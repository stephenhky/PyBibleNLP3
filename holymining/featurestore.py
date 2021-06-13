
import tables as tb


class BibleChapterH5FeatureStoreCreator:
    def __init__(self, path, vecdim):
        self.path = path
        self.vecdim = vecdim
        self.rowdes = {
            'bookid': tb.IntCol(pos=0),
            'chapter': tb.IntCol(pos=1),
            'embedding': tb.FloatCol(shape=(1, vecdim))
        }
        self.h5file = tb.open_file(self.path, 'w')
        self.table = self.h5file.create_table('/', 'bible_embedding', self.rowdes, title='bible_embedding')

    def write_embedding(self, bookid, chapter, embedding):
        row = self.table.row
        row['bookid'] = bookid
        row['chapter'] = chapter
        row['embedding'] = embedding
        row.append()

        self.table.flush()

    def close(self):
        self.h5file.close()


class BibleChapterH5FeatureStoreRetriever:
    def __init__(self, path):
        self.path = path
        self.h5file = tb.open_file(self.path, 'r')
        self.table = self.h5file.root.bible_embedding

    def extract_embedding(self, bookid, chapter):
        for row in self.table.where('bookid=={} and chapter=={}'.format(bookid, chapter)):
            return row['embedding']

    def iterate_all_records(self):
        for row in self.table:
            yield row['bookid'], row['chapter'], row['embedding']

    def close(self):
        self.h5file.close()
