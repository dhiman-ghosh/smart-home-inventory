from sinventory import database


class Profile(database.Database):
  def __init__(self):
    super().__init__("profile", "postgres://postgres@localhost/wc")
    self.alexa_id = None
    self.pin = None
    self.name = None
    self.email = None
    self.mobile = None

  def add(self):
    self._insert()

  def delete(self, val):
    self._delete(val)

  def select(self):
    self._select()