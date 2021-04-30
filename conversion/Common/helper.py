import sys
import os
import tarfile
import stat
import errno
import shutil

# PARSER
def is_valid_e00(parser, arg):
  if not (os.path.isfile(arg) and arg.endswith('.e00')):
    parser.error('The provided e00: {} is invalid'.format(arg))
  return arg

def is_valid_directory(parser, arg):
  if not os.path.isdir(arg):
    parser.error('The provided directory {} is invalid'.format(arg))
  return arg

# OS 
def makeDir(fp):
  if not os.path.exists(fp):
    try:
      os.makedirs(fp)
    except OSError as ex:
      if ex.errno != errno.EEXIST:
        raise

def removeDir(fp, recreate=False):
  def on_rm_error(action, fp, exc):
    os.chmod(fp, stat.S_IWRITE)
    os.remove(fp)

  if os.path.exists(fp):
    shutil.rmtree(fp, onerror=on_rm_error)

  if recreate:
    makeDir(fp)

def toTar(inDir, dest):
  fn,_ = os.path.splitext(os.path.basename(inDir))
  tar = os.path.join(dest, fn + '.tar')

  with tarfile.open(tar, 'w') as t:
    for f in os.listdir(inDir):
      t.add(os.path.join(inDir, f), arcname=f)