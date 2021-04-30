import os
import sys

from AtlasChart import AtlasHandler
from Common.parse_args import argparser_init
from Common.ErrorHandler import baseException

# global
ROOT = os.path.dirname(os.path.realpath(__file__))

def main():
  args = argparser_init()
  args.config = os.path.join(ROOT, args.config)

  with AtlasHandler(args.inputs, args.config) as atlas:
    atlas.start_logging(atlas.config)
    atlas.start()

  return 0

if __name__ == '__main__':
  try:
    status = main()
  except Exception as e:
    status = 1
    # pylint: disable=no-member
    if isinstance(e, baseException):
      print(e.to_json())
    else:
      if hasattr(e, 'message'):
        print(baseException(e.message, 
              baseException.ERR_UNK_LEVEL, e).to_json())
      else:
        print(baseException('', 
              baseException.ERR_UNK_LEVEL, e).to_json()) 
  finally:
    sys.exit(status)