import sys

def handle_error(message, exit_code=1):
    print(message, file=sys.stderr)
    sys.exit(exit_code)
