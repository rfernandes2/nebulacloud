from api.settings import default_path, path_regex
import os, re, shutil
from flask import jsonify

# Shutil - copying, moving, deleting, and archiving files and directories

class ListSerializers:
    def __init__(self, current_user, path):
        self.current_user = current_user
        self.path = path
        self.user_dir = ''

    def list(self):
        error, is_valid = self.validate_path()
        if not is_valid:
            return jsonify(error), 400

        return self.get_folder_list()

    def validate_path(self):
        # If no path is provided, use the default user directory
        if not self.path:
            self.user_dir = f"{default_path}{self.current_user}"
        else:
            # Validate path using regex
            if re.match(path_regex, self.path):
                self.user_dir = f"{default_path}{self.current_user}/{self.path}"
            else:
                return {"error": "Invalid path. Only alphanumeric, underscores, and slashes are allowed."}, False

        # Check if the directory exists
        if not os.path.exists(self.user_dir):
            return {"error": f"User directory does not exist: {self.user_dir}"}, False
        return {}, True

    def get_folder_list(self):
        try:
            # Initialize lists to store folder and file names
            folder_list = []
            file_list = []

            for item_name in os.listdir(self.user_dir):
                item_path = os.path.join(self.user_dir, item_name)

                if os.path.isdir(item_path):  # It's a directory
                    folder_list.append(item_name)
                elif os.path.isfile(item_path):  # It's a file
                    file_list.append(item_name)

            return jsonify({
                "path": self.user_dir,
                "folders": folder_list,
                "files": file_list
            })

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def create_folder(self, folder_name):
        error, is_valid = self.validate_path()
        if not is_valid:
            return jsonify(error), 400

        self.user_dir = f"{default_path}{self.current_user}/{self.path}"
        new_path = f"{self.user_dir}/{folder_name}"

        if not os.path.exists(new_path):
            os.makedirs(new_path)
            return jsonify({"message": f"Success: Folder created at {new_path}"}), 201
        else:
            return jsonify({"error": "Folder already exists"}), 400

    def delete_item(self):
        error, is_valid = self.validate_path()
        if not is_valid:
            return jsonify(error), 400

        target_path = f"{default_path}{self.current_user}/{self.path}" or ""

        try:
            if os.path.isfile(target_path):
                os.remove(target_path)  # Delete file
                return jsonify({"message": f"File '{self.path}' deleted successfully."}), 200
            elif os.path.isdir(target_path):
                shutil.rmtree(target_path)  # Delete folder and its contents
                return jsonify({"message": f"Folder '{self.path}' deleted successfully."}), 200
            else:
                return jsonify({"error": "The specified path does not exist."}), 404
        except PermissionError:
            return jsonify({"error": "Permission denied. Unable to delete."}), 403
        except Exception as e:
            return jsonify({"error": str(e)}), 500