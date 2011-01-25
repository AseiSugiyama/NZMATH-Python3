import sqlite3
import os.path


class QuadraticFieldClassNumbersTable(object):
    """
    A database connector to the quadratic field class number table.
    """
    # SQL command strings
    CREATE_TABLES = ["CREATE TABLE qfcn (d INTEGER PRIMARY KEY, h INTEGER)",
                     "CREATE VIEW real_qfcn AS SELECT d, h FROM qfcn WHERE d>0",
                     "CREATE VIEW imag_qfcn AS SELECT d, h FROM qfcn WHERE d<0"]
    INSERT = "INSERT INTO qfcn VALUES (?, ?)"
    UPDATE = "UPDATE qfcn SET h=? WHERE d=?"
    DELETE = "DELETE FROM qfcn WHERE d=?"
    # TABLE / VIEW names
    TABLE = 'qfcn'
    VIEW = 'qfcn'

    def __init__(self, name='class_num_2'):
        """
        initialize connection and cursor to the database file named
        'class_num_2' (or specified with an argument).
        """
        self.conn = self.cursor = None
        exists = os.path.exists(name)
        self.conn = sqlite3.connect(name)
        self.cursor = self.conn.cursor()
        if not exists:
            for command in self.CREATE_TABLES:
                self.conn.execute(command)
            self.conn.commit()

    def __del__(self):
        """
        Prepare for deletion.  This is just for object deletion; db
        deletion is another story.
        """
        if self.cursor is not None:
            self.cursor.close()
        if self.conn is not None:
            self.conn.close()

    def __getitem__(self, disc):
        """
        'qfcn[disc]'
        """
        return self._select_single(disc)

    def __setitem__(self, disc, class_num):
        """
        'qfcn[disc] = class_num'
        """
        if disc in self:
            self._update_single(disc, class_num)
        else:
            self._insert_single(disc, class_num)

    def __delitem__(self, disc):
        """
        'del qfcn[disc]'
        """
        if disc in self:
            self._delete_single(disc)
        else:
            raise KeyError(str(disc))

    def __contains__(self, disc):
        """
        'disc in qfcn'
        """
        try:
            self._select_single(disc)
            return True
        except KeyError:
            return False

    def __len__(self):
        """
        number of registered class numbers
        """
        return self._count()

    def __iter__(self):
        return iter(self._select_all())

    def discs(self, class_num=0, key=None, reverse=False):
        """
        Return a list of discriminants.

        Optional arguments:
        - class_num: pick up with class number (default unspecified)
        - key: sort key, can be 'd' (for discriminant) or 'h' (for class number)
        - reverse: if true, descending. o.w., ascending
        If key is not specified, no sorting order be assumed.
        """
        if class_num > 0:
            return self._select_by_value(class_num, key, reverse)
        return self._select_discs()

    def bulk_update(self, iterable):
        """
        Update many at once.

        iterable yields (discriminant, class number) pairs.
        """
        inserted, updated = [], []
        for d, h in iterable:
            if d in self:
                updated.append((d, h))
            else:
                inserted.append((d, h))
        self._update_bulk(updated)
        self._insert_bulk(inserted)

    # underlying db calls
    def _select_single(self, disc):
        """
        Return the class number of quadratic order specified by
        discriminant.  If the class number is not on the table It
        raises KeyError.

        PRECONDITION: disc is a discriminant for a certain quadratic order.
        """
        sqlstmt = "SELECT h FROM %s WHERE d=?" % self.VIEW
        pickup = self.cursor.execute(sqlstmt, (disc,))
        picked = pickup.fetchone()
        if picked is not None:
            # picked = (h,)
            return picked[0]
        else:
            raise KeyError(str(disc))

    def _select_all(self):
        """
        Return a list of (disc, class_num) pairs.
        """
        sqlstmt = "SELECT d, h FROM %s" % self.VIEW
        return list(self.cursor.execute(sqlstmt))

    def _select_discs(self):
        """
        Return a list of (disc, class_num) pairs.
        """
        sqlstmt = "SELECT d FROM %s" % self.VIEW
        return [d[0] for d in self.cursor.execute(sqlstmt)]

    def _select_by_value(self, class_num, key=None, reverse=False):
        """
        Select all discriminants associated with given class number.

        Optional arguments:
        - table: table/view name (default to 'qfcn')
        - class_num: pick up with class number (default unspecified)
        - key: sort key, can be 'd' (for discriminant) or 'h' (for class number)
        - reverse: if true, descending. o.w., ascending
        If key is not specified, no sorting order be assumed.
        """
        sqlstmt = "SELECT d FROM %s WHERE h=?" % self.VIEW
        if key is not None:
            sqlstmt = self._augment_order(sqlstmt, key, reverse)
        pickup = self.cursor.execute(sqlstmt, (class_num,))
        return [d[0] for d in pickup]

    def _augment_order(self, stmt, key, reverse):
        """
        Return sql statement that is augmnted by ORDER BY clause.
        """
        sqlstmt = stmt + " ORDER BY %s" % key
        if reverse:
            sqlstmt += " DESC"
        else:
            sqlstmt += " ASC"
        return sqlstmt

    def _select_by_range(self, disc_low, disc_high):
        """
        Select class numbers for range of discriminants.
        disc_low < disc_high.
        """
        sqlstmt = "SELECT h FROM %s WHERE d>=? and d<=?" % self.VIEW
        pickup = self.cursor.execute(sqlstmt, (disc_low, disc_high,))
        return [h[0] for h in pickup]

    def _count(self):
        """
        Return count
        """
        sqlstmt = 'SELECT COUNT(*) FROM %s' % self.VIEW
        return self.cursor.execute(sqlstmt).fetchone()[0]

    # INSERT / UPDATE / DELETE
    def _insert_single(self, disc, class_num):
        """
        Insert a (discriminant, class number) pair into the table.
        """
        self.cursor.execute(self.INSERT, (disc, class_num))
        self.conn.commit()

    def _insert_bulk(self, iterable):
        """
        Insert multiple (discriminant, class number) pairs into the
        table.
        """
        self.cursor.executemany(self.INSERT, iterable)
        self.conn.commit()

    def _update_single(self, disc, class_num):
        """
        Update value of class number corresponding to the discriminant.
        """
        self.cursor.execute(self.UPDATE, (class_num, disc))
        self.conn.commit()

    def _update_bulk(self, iterable):
        """
        Update multiple pairs of (class number, disc).
        """
        self.cursor.executemany(self.UPDATE, iterable)

    def _delete_single(self, disc):
        """
        Delete class number datum corresponding to the discriminant.
        """
        self.cursor.execute(self.DELETE, (disc,))
        self.conn.commit()

    def _delete_bulk(self, iterable):
        """
        Delete class numbers data corresponding to the discriminants.
        """
        self.cursor.executemany(self.DELETE, iterable)
        self.conn.commit()


class ImaginaryQuadraticFieldClassNumbersTable(QuadraticFieldClassNumbersTable):
    """
    All 'disc' means the absolute value of discriminant.
    """
    # VIEW name
    VIEW = 'imag_qfcn'

    def discs(self, class_num=0, key=None, reverse=False):
        """
        Return a list of negative discriminants.

        Optional arguments:
        - class_num: pick up with class number (default unspecified)
        - key: sort key, can be 'd' (for discriminant) or 'h' (for class number)
        - reverse: if true, descending. o.w., ascending
        If key is not specified, no sorting order be assumed.
        """
        if class_num > 0:
            return self._select_by_value(class_num, key, reverse)
        return self._select_discs(tablename)

    def bulk_update(self, iterable):
        """
        Update many at once.

        iterable yields (discriminant, class number) pairs.
        """
        inserted, updated = [], []
        for d, h in iterable:
            if -d in self:
                updated.append((-d, h))
            else:
                inserted.append((-d, h))
        self._update_bulk(updated)
        self._insert_bulk(inserted)

    # underlying db calls
    def _select_single(self, disc):
        """
        Return the class number of quadratic order specified by
        discriminant.  If the class number is not on the table It
        raises KeyError.

        PRECONDITION: disc is a discriminant for a certain quadratic order.
        """
        return QuadraticFieldClassNumbersTable._select_single(self, -disc)

    def _select_all(self):
        """
        Return a list of (disc, class_num) pairs.
        """
        sqlstmt = "SELECT d, h FROM %s" % self.VIEW
        return [(-d, h) for (d, h) in self.cursor.execute(sqlstmt)]

    def _select_discs(self):
        """
        Return a list of (disc, class_num) pairs.
        """
        sqlstmt = "SELECT d FROM %s" % self.VIEW
        return [-d[0] for d in self.cursor.execute(sqlstmt)]

    def _select_by_value(self, class_num, key=None, reverse=False):
        """
        Select all discriminants associated with given class number.

        Optional arguments:
        - table: table/view name (default to 'imag_qfcn')
        - class_num: pick up with class number (default unspecified)
        - key: sort key, can be 'd' (for discriminant) or 'h' (for class number)
        - reverse: if true, descending. o.w., ascending
        If key is not specified, no sorting order be assumed.
        """
        sqlstmt = "SELECT d FROM %s WHERE h=?" % self.VIEW
        if key == 'h':
            sqlstmt = self._augment_order(sqlstmt, key, reverse)
        elif key == 'd':
            sqlstmt = self._augment_order(sqlstmt, key, not reverse)
        pickup = self.cursor.execute(sqlstmt, (class_num,))
        return [-d[0] for d in pickup]

    def _select_by_range(self, disc_low, disc_high):
        """
        Select class numbers for range of discriminants.
        disc_low < disc_high, both ends included.
        """
        sqlstmt = "SELECT h FROM %s WHERE d>=? and d<=?" % self.VIEW
        pickup = self.cursor.execute(sqlstmt, (-disc_high, -disc_low))
        return [h[0] for h in pickup]


class RealQuadraticFieldClassNumbersTable(QuadraticFieldClassNumbersTable):
    # VIEW name
    VIEW = 'real_qfcn'


## Utility
import csv

def csv_to_db(db, filename):
    """
    insert bulk data from csv file.
    """
    csv_table = open(filename, 'r')
    updater = [(int(dstr), int(hstr)) for (dstr, hstr) in csv.reader(csv_table)]
    db.bulk_update(updater)

def db_to_csv(db, filename):
    """
    output db entries to a file
    """
    csv_table = open(filename, 'w')
    csv.writer(csv_table).writerows(iter(db))
