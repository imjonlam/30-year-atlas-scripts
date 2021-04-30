import json
import logging
from datetime import datetime

class baseException(Exception):
  ERR_UNK_LEVEL = 'CIS000'
  ERR_DB_LEVEL = 'CIS001'
  ERR_CODE_LEVEL = 'CIS002'
  ERR_CFG_LEVEL = 'CIS003'
  ERR_INPUT_LEVEL = 'CIS004'
  ERR_FTP_LEVEL = 'CIS005'
  ERR_NOTFOUND_LEVEL = 'CIS404'
  ERR_INTERNAL_LEVEL = 'CIS500'
  ERR_UNAVAILABLE_LEVEL = 'CIS503'

  def __init__(self, message: str, code: str = ERR_UNK_LEVEL, Exception=None):
    self.code = code
    self.message = message
    self.date = datetime.now()
    self.stack = Exception

    baseMsg = f'{datetime.now()} ERROR: code {code}.{message}'

    if Exception:
      baseMsg = f'{baseMsg} [{Exception}]'
    self.base = baseMsg
    logging.error(self.base)

  def __str__(self):
    '''Returns string form of base message'''
    return self.base

  def to_json(self):
    '''Returns json form of the exception'''
    return baseException.generate_json(self.code, self.base)

  @staticmethod
  def generate_json(errorCode: str, details: str):
    '''Returns a serialized class as json'''
    data = {}
    data['success'] = False
    data['errorCode'] = errorCode
    data['details'] = details
    data['ftpError'] = True if errorCode == baseException.ERR_FTP_LEVEL else False

    return json.dumps(data)