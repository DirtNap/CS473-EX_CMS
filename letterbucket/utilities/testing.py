import unittest
from sqlalchemy.exc import IntegrityError

class DbModelTestCase(unittest.TestCase):
    """A Utility class for easier testing of SQLAlchemy Models."""

    # Constant regular expression fragments
    NOT_NULL_ASSERTION_RE = r'\bNOT\b.*?\bNULL\b'
    UNIQUE_ASSERTION_RE = r'\bUNIQUE\b'

    def _AssertConstraintError(self, db, type_re, column, callable, msg='', * args, ** kwargs):
        re = ''.join((r'^(?=.*', type_re, r')(?=.*\b', column.lower(), r'\b)(?i)'))
        if msg:
            try:
                with self.assertRaisesRegexp(IntegrityError, re):
                    callable(*args, ** kwargs)
            except AssertionError as ex:
                raise AssertionError('%s (%s)' % (msg, ex.message))
        else:
            self.assertRaisesRegexp(IntegrityError, re, callable, * args, ** kwargs)
        db.session.rollback()

