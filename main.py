import os
from db_conn import create_database_engine, create_session
from file_crawler import list_items_in_folder, is_directory
from errs import handle_error
from cli_interface import parse_arguments
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base

# Create SQLAlchemy engine
engine = create_database_engine('sqlite:///folder_structure.db')
Base = declarative_base()

# Define the Folder model with new columns
class Folder(Base):
    __tablename__ = 'folders'
    id = Column(Integer, primary_key=True)
    path = Column(String)  # Full path of the item
    name = Column(String)  # Name of the item
    is_file = Column(Boolean)  # Indicates whether the item is a file
    parent_id = Column(Integer, ForeignKey('folders.id'))

# Create the database schema
Base.metadata.create_all(engine)

# Function to traverse directory tree and store in the database
def store_folder_structure(session, folder_path, parent_folder_id=None):
    # Get the folder name and path
    folder_name = os.path.basename(folder_path)
    folder_path = os.path.abspath(folder_path)
    # Create a new folder record
    folder = Folder(path=folder_path, name=folder_name, is_file=False, parent_id=parent_folder_id)
    session.add(folder)
    session.commit()
    
    # Iterate over all items in the folder
    for item in list_items_in_folder(folder_path):
        item_path = os.path.join(folder_path, item)
        is_file = not is_directory(item_path)
        # Create a new record for the item
        item_record = Folder(path=item_path, name=item, is_file=is_file, parent_id=folder.id)
        session.add(item_record)
        session.commit()
        # If the item is a directory, recursively call the function
        if not is_file:
            store_folder_structure(session, item_path, folder.id)  # Pass the current folder id as parent

def main():
    # Parse command-line arguments
    args = parse_arguments()

    # Create database session
    session = create_session(engine)

    # Call the function to store folder structure
    try:
        store_folder_structure(session, args.root_folder)
    except Exception as e:
        handle_error(f"An error occurred: {str(e)}")

    # Close session
    session.close()

if __name__ == "__main__":
    main()
