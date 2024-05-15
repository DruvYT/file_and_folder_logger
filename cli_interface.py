import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='Traverse directory tree and store in a database.')
    parser.add_argument('root_folder', type=str, help='Root folder to traverse and store in the database')
    return parser.parse_args()
