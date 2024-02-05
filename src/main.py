import sys
from . import main_cli
from ztron import Mcp

if __name__ == '__main__':
    sys.exit(main_cli())

def main_cli():
    mcp = Mcp(sys.argv)
    mcp.run_pipeline()
    mcp.finish()