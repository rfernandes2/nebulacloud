from api.settings import default_path, path_regex
import os, re
from flask import jsonify

class ListSerializers:
    def __init__(self, current_user, path):
        self.current_user = current_user
        self.path = path
        self.user_dir = ''

    def list(self):
        if self.validate_path():
            return self.get_folder_list()
        else:
            return jsonify({'error'}), 400

    def validate_path(self):
        if self.path == '':
            self.user_dir = f"{default_path}{self.current_user}"
        else:
            if re.match(path_regex, self.path):
                self.user_dir = f"{default_path}{self.current_user}/{self.path}"
            else:
                #return jsonify({"error": "Invalid path. Only alphabetic characters are allowed."}), 400
                return False
        if not os.path.exists(self.user_dir):
            #return jsonify({"error": f"User directory does not exist: {self.user_dir}"}), 404
            return False
        return True

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
