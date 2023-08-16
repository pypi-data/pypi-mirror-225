import os
import sys
import argparse
from .file_creator import FileCreator
from .filename_validator import is_valid_filename
from .classifier_validator import is_valid_classifier

def cli():
    parser = argparse.ArgumentParser(description="Ara tools for creating files and directories.")
    parser.add_argument("action", help="Action to perform (e.g. 'create', 'delete', 'list')")
    parser.add_argument("filename", help="Filename for the file to be created or deleted", nargs="?")
    parser.add_argument("classifier", help="Classifier for the file to be created or deleted", nargs="?")

    args = parser.parse_args()

    file_creator = FileCreator()

    if args.action.lower() == "create":
        if not is_valid_filename(args.filename):
            print("Invalid filename provided. Please provide a valid filename.")
            sys.exit(1)

        if not is_valid_classifier(args.classifier):
            print("Invalid classifier provided. Please provide a valid classifier.")
            sys.exit(1)

        template_path = os.path.join(os.path.dirname(__file__), 'templates')
        file_creator.run(args.filename, args.classifier, template_path)
    elif args.action.lower() == "delete":
        file_creator.delete(args.filename, args.classifier)
    elif args.action.lower() == "list":
        file_creator.list_files()
    else:
        print("Invalid action provided. Type ara -h for help")
        sys.exit(1)

if __name__ == "__main__":
    cli()
