from codalab.common import precondition


class DatabaseObject(object):
  # To use this class, subclass it and set its COLUMNS class attribute to be the
  # non-id columns of a SQLALchemy table.
  COLUMNS = None

  def __init__(self, row):
    self.update_in_memory(dict(row), strict=True)

  def update_in_memory(self, row, strict=False):
    '''
    Initialize the attributes on this object from the data in the row.
    The attributes of the row are inferred from the table columns.

    If strict is True, checks that all columns are included in the row.
    '''
    if strict:
      for column in self.COLUMNS:
        precondition(column in row, 'Row %s missing column: %s' % (row, column))
    for (key, value) in row.iteritems():
      message = 'Row %s has extra column: %s' % (row, key)
      precondition(key in self.COLUMNS, message)
      setattr(self, key, value)

  def to_dict(self):
    '''
    Return a JSON-serializable and database-uploadable dictionary that
    represents this object.
    '''
    return {column: getattr(self, column) for column in self.COLUMNS}
