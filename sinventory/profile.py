from sinventory import database
import random

class Profile(database.Database):
  def __init__(self):
    super().__init__("profile")
    self.alexa_id = None
    self.pin = None
    self.name = None
    self.email = None
    self.mobile = None

  def add(self):
    self._insert()

  def authorize(self, access_key):
    """
    Checks for the presence of access key and populates this class attributes
    
    Args:
      access_key: Access key or PIN (6 digits) provided by the user
      
    Returns:
      True if success, False otherwise
    """
    result = (self._select(["pin"], {"pin": access_key}))
    print("Result: " + str(result))
    if len(result) > 0:
      print(True)
      return True
    else:
      print(False)
      return False

    
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
    access_key = random.randint(100000, 999999)
    self.pin = access_key
    if (self._select(["alexa_id"], {"alexa_id": alexa_user_id})) is False:
      self.alexa_id = alexa_user_id
      self._insert()
    else:
      self._update({"pin": access_key}, {"alexa_id": alexa_user_id})
    return self.pin
    
  def update(self):
    """
    Updates profile data of an existing user
    
    Returns:
      True for success, None if user does not exist, False for DB errors
    """
    pass
    
  def delete(self, access_key):
    """
    Deletes an user account and all associations in other tables after re-authorization
    
    Args:
      access_key: Access key or PIN (6 digits) provided by the user
      
    Returns:
      True for success, None for authorization failure, False for DB errors
    """
    if (self._delete({"pin": access_key})) is True:
      print(True)
      return True
    else:
      print(False)
      return False
      
  def get_db_error(self):
    """
    Returns latest encountered DB error string
    
    Returns:
      Error string if present, None otherwise
    """
