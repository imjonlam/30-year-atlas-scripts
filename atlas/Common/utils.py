import os
import sys
import stat
import time
import errno
import shutil
import logging
import importlib
from Common.ErrorHandler import baseException

'''''''''
Logging
'''''''''
def log_to_gitlab(config: dict, chart: str):
  '''Initialize logging, post errors to GITLAB'''
  icePyScripts = os.getenv('ICEPY_SCRIPTS')
  spec = importlib.util.spec_from_file_location('pylogger', os.path.join(icePyScripts, 'pylogger/__init__.pyc'))
  logger = importlib.util.module_from_spec(spec)
  sys.modules['pylogger'] = logger
  spec.loader.exec_module(logger)

  # create log file
  log_date = time.strftime('%Y-%m-%d_%H-%M-%S')
  log_dir = os.path.join(*config['logdir']).format(os.getenv('username'))
  log_file = config['logfile'].format(chart, log_date)

  # setup GitAPI logging
  logger.logging_init(config['projectid'], log_dir, log_file)

def logging_init(config: dict, chart: str):
  '''Initialize logging'''
  # create log file
  log_date = time.strftime('%Y-%m-%d_%H-%M-%S')
  log_dir = os.path.join(*config['logdir']).format(os.getenv('username'))
  log_file = config['logfile'].format(chart, log_date)

  logging.basicConfig(filename=os.path.join(log_dir, log_file),
                      format ='%(asctime)s, %(levelname)-8s [%(filename)s:%(module)s:%(funcName)s:%(lineno)d] %(message)s',
                      datefmt='%Y-%m-%d:%H:%M:%S',
                      level=logging.DEBUG)

'''''''''''
OS METHODS
'''''''''''
def make_dir(path: str):
  '''Create a new dictory given path'''
  if not os.path.exists(path):
    try:
      os.makedirs(path)
      logging.info(f'created directory {path}')
    except OSError as e:
      if e.errno != errno.EEXIST:
        raise baseException(f'There was an issue creating the directory {path}.', baseException.ERR_UNK_LEVEL, e)

def del_dir(folder: str, remake: bool=False):
  '''Delete a folder, remake if required'''
  try:
    def on_rm_error(action, path, exc):
      os.chmod(path, stat.S_IWRITE)
      os.remove(path)

    if os.path.exists(folder) and os.path.isdir(folder):
      shutil.rmtree(folder, onerror=on_rm_error)
      logging.info(f'removed directory {folder}')

  except OSError:
    logging.warning(f'There was an issue deleting the directory {folder}. Manual intervention required.')
    return

  if remake:
    make_dir(folder)