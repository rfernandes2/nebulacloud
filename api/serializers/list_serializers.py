from api.settings import default_path, path_regex
import os, re, shutil
from flask import jsonify, send_file
from werkzeug.utils import secure_filename

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
                return {"error": f"Invalid path. Only alphanumeric, underscores, and slashes are allowed."}, False

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

        if self.path != "":
            self.user_dir = f"{default_path}{self.current_user}/{self.path}"
        else:
            self.user_dir = f"{default_path}{self.current_user}"

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

    def upload_files(self, files):
        # Validate the path
        error, is_valid = self.validate_path()
        if not is_valid:
            return jsonify({"error": error}), 400

        # Ensure the directory exists
        if not os.path.exists(self.user_dir):
            os.makedirs(self.user_dir)

        # Initialize a list to store upload results
        upload_results = []

        for file in files:
            # Get the filename and ensure it's safe
            filename = secure_filename(file.filename)
            file_path = os.path.join(self.user_dir, filename)

            # Save the file
            try:
                file.save(file_path)
                upload_results.append({
                    "filename": filename,
                    "message": f"File '{filename}' uploaded successfully to {self.user_dir}."
                })
            except Exception as e:
                upload_results.append({
                    "filename": filename,
                    "error": f"Failed to upload file '{filename}': {str(e)}"
                })

        # Return the result of all uploads
        return jsonify(upload_results), 201

    def download_file(self):
        error, is_valid = self.validate_path()
        if not is_valid:
            return jsonify(error), 400
        
        file_path = os.path.join(self.user_dir)

        if not os.path.isfile(file_path):
            return jsonify({'error': 'The specified file does not exist'}), 404
        
        try:
            return send_file(file_path, as_attachment = True)
        except Exception as e:
            return jsonify({'error': 'Failed to download file: {str(e)}'}), 500
        
    def preview_image(self):
        # Validate the path
        error, is_valid = self.validate_path()
        if not is_valid:
            return jsonify(error), 400

        file_path = os.path.join(self.user_dir)

        # Check if the file exists and is an image
        if not os.path.isfile(file_path):
            return jsonify({'error': 'The specified file does not exist'}), 404

        # Check if it's an image file (can add more types if needed)
        if not file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            return jsonify({'error': 'The file is not a valid image type'}), 400

        try:
            return send_file(file_path, mimetype='image/jpeg')  # You can set a different MIME type based on the image
        except Exception as e:
            return jsonify({'error': f'Failed to load the image: {str(e)}'}), 500