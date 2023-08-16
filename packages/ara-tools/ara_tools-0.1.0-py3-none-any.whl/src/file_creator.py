import os

class FileCreator:
    
    valid_classifiers = {
        "vision": "vision",
        "businessgoal": "goals",
        "capability": "capabilities",
        "keyfeature": "keyfeatures",
        "feature": "features",
        "epic": "epics",
        "story": "stories",
        "task": "tasks",
        "example": "examples",
    }
        
    def __init__(self, file_system=None):
        self.file_system = file_system or os

    def create_file(self, file_path, template_path=None, classifier=None, filename=None):
        if template_path and classifier:
            template_file_path = self.file_system.path.join(template_path, f"template.{classifier}")
            if self.file_system.path.exists(template_file_path):
                with open(template_file_path, "r") as template_file:
                    template_content = template_file.read()

                template_content = template_content.replace("< descriptive title >", filename.replace("-", " "))

                with open(file_path, "w") as file:
                    file.write(template_content)
            else:
                with open(file_path, "w") as file:
                    pass
        else:
            with open(file_path, "w") as file:
                pass

    def create_directory(self, dir_path):
        self.file_system.makedirs(dir_path, exist_ok=True)

    def template_exists(self, template_path, template_name):
        if not template_path:
            return False

        full_path = self.file_system.path.join(template_path, template_name)

        if not self.file_system.path.isfile(full_path):
            print(f"Template file '{template_name}' not found at: {full_path}")
            return False

        return True



    def run(self, filename, classifier, template_path=None):
        if classifier not in self.valid_classifiers:
            print("Invalid classifier provided. Please provide a valid classifier.")
            return

        sub_directory = self.valid_classifiers[classifier]
        self.file_system.makedirs(sub_directory, exist_ok=True)

        file_path = self.file_system.path.join(sub_directory, f"{filename}.{classifier}")
        dir_path = self.file_system.path.join(sub_directory, f"{filename}.data")

        if self.file_system.path.exists(file_path) or self.file_system.path.exists(dir_path):
            user_choice = input("File or directory already exists. Do you want to overwrite the existing file and directory? (Y/N): ")

            if user_choice.lower() != "y":
                print("No changes were made to the existing file and directory.")
                return

        template_name = f"template.{classifier}"
        if template_path and not self.template_exists(template_path, template_name):
            print(f"Template file '{template_name}' not found in the specified template path.")
            return

        self.create_file(file_path, template_path, classifier, filename)
        self.create_directory(dir_path)
        print(f"Created file: {file_path}")
        print(f"Created directory: {dir_path}")


    def delete(self, filename, classifier):
        if classifier not in self.valid_classifiers:
            print("Invalid classifier provided. Please provide a valid classifier.")
            return

        sub_directory = self.valid_classifiers[classifier]
        file_path = self.file_system.path.join(sub_directory, f"{filename}.{classifier}")
        dir_path = self.file_system.path.join(sub_directory, f"{filename}.data")

        if not self.file_system.path.exists(file_path) or not self.file_system.path.exists(dir_path):
            print("File or directory not found.")
            return

        user_choice = input("Are you sure you want to delete the file and directory? (Y/N): ")

        if user_choice.lower() != "y":
            print("No changes were made.")
            return

        self.file_system.remove(file_path)
        self.file_system.rmdir(dir_path)
        print(f"Deleted file: {file_path}")
        print(f"Deleted directory: {dir_path}")

    def list_files(self):
        classifier_order = [
            "vision",
            "businessgoal",
            "capability",
            "keyfeature",
            "epic",
            "story",
            "example",
            "feature",
            "task",
            "issue",
        ]

        files_by_classifier = {classifier: [] for classifier in classifier_order}

        for root, dirs, files in self.file_system.walk("."):
            for file in files:
                for classifier in classifier_order:
                    if file.endswith(f".{classifier}"):
                        files_by_classifier[classifier].append(self.file_system.path.join(root, file))

        for classifier in classifier_order:
            if files_by_classifier[classifier]:
                print(f"{classifier.capitalize()} files:")
                for file in files_by_classifier[classifier]:
                    print(f"  - {file}")
                print()
