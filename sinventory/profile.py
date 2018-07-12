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

  def authorize(self, access_key):
    print(self._select(access_key))
    """
    Checks for the presence of access key and populates this class attributes
    
    Args:
      access_key: Access key or PIN (6 digits) provided by the user
      
    Returns:
      True if success, False otherwise
    """
    pass
    
  def get_access_key(self, alexa_user_id):
    """
    Creates a new user profile if does not exists and return an unique access key.
    The other columns of the profile table should be kept blank for new user.
    In case of existing user, this method will reset the access key and returns.
    
    The access key is to be stored as MD5 hash string, to be used for authorization.
    As a result, for better security, recovery of existing access key will not be possible.
    
    Args:
      alexa_user_id: Unique user id string provided by Alexa device
      
    Returns:
      6 digits unique access key (string)
    """
    pass
    
  def update(self):
    """
    Updates profile data of an existing user
    
    Returns:
      True for success, None if user does not exist, False for DB errors
    """
    pass
    
  def delete(self, access_key):
    print(self._delete(access_key))
    """
    Deletes an user account and all associations in other tables after re-authorization
    
    Args:
      access_key: Access key or PIN (6 digits) provided by the user
      
    Returns:
      True for success, None for authorization failure, False for DB errors
    """
      
  def get_db_error(self):
    """
    Returns latest encountered DB error string
    
    Returns:
      Error string if present, None otherwise
    """
