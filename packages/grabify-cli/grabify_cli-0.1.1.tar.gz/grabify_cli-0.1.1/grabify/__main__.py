import sys

from .cli import grabify, COMMANDS

for cmd in COMMANDS:
    grabify.add_command(cmd)
        
def main():
    return grabify()

if __name__ == "__main__":
    sys.exit(main())