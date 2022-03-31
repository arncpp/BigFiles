import ast
import os
import shutil
from flask import Flask, request

app = Flask(__name__)

path = os.getcwd()
UPLOAD_FOLDER = os.path.join(path, "uploads")

if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)


class UploadFileData:
    def __init__(self, user_id: str, file_size: int, threads_count: int, file_name: str) -> None:
        self.user_id = user_id
        self.file_size = file_size
        self.threads_count = threads_count
        self.file_name = file_name
        self.parts_are_uploaded = [False for _ in range(0, threads_count)]
        self.file_is_upload = False
        self.number_of_parts = 0
        self.size_of_transferred_file = 0
        self.USER_FOLDER = UPLOAD_FOLDER + "\\" + self.user_id
        self.USER_TEMP_FOLDER = self.USER_FOLDER + "\\" + "temp"

    def part_of_file_is_uploaded(self, part_id: int):
        self.number_of_parts += 1
        self.parts_are_uploaded[part_id] = True

    def file_is_uploaded(self):
        if all(self.parts_are_uploaded):
            self.file_is_upload = True

    def save_part(self, piece, piece_id):
        if not os.path.isdir(self.USER_FOLDER):
            os.mkdir(self.USER_FOLDER)
        if not os.path.isdir(self.USER_TEMP_FOLDER):
            os.mkdir(self.USER_TEMP_FOLDER)

        piece_name = f"{self.user_id}" + "_filename_part_" + str(piece_id)
        with open(f"{self.USER_TEMP_FOLDER}" + "/" + f"{piece_name}", "wb") as file_part:
            file_part.write(piece)

    def save_file(self):
        if self.file_is_upload is True:
            with open(f"{self.USER_FOLDER}" + "/" + f"{self.file_name}", "wb") as user_file:
                for i in range(self.number_of_parts):
                    cur_piece = self.user_id + "_filename_part_" + f"{i}"
                    with open(f"{self.USER_TEMP_FOLDER}" + "/" + f"{cur_piece}", "rb") as file_part:
                        bytes_to_write = file_part.read()
                        user_file.write(bytes_to_write)
                        self.size_of_transferred_file = os.path.getsize(f"{user_file.name}")
            shutil.rmtree(self.USER_TEMP_FOLDER)

    def integrity_check(self) -> bool:
        if self.file_is_upload is True:
            if self.size_of_transferred_file == self.file_size:
                return True
        return False


current_users = {}
users = {}


@app.route('/upload', methods=["POST", "GET"])
def upload_file():
    file_data = current_users[request.remote_addr]
    part_id = request.json["id"]
    part = request.json["piece"]
    part = ast.literal_eval(part)
    part = bytes(part)
    file_data.save_part(part, part_id)
    file_data.part_of_file_is_uploaded(part_id)
    file_data.file_is_uploaded()
    file_data.save_file()
    if file_data.integrity_check():
        return request.json
    del current_users[request.remote_addr]
    return request.json


@app.route('/params', methods=["POST"])
def get_params():
    file_data = UploadFileData(request.remote_addr, request.json["file_size"], request.json["threads_count"],
                               request.json["file_name"])
    current_users[request.remote_addr] = file_data
    if users:
        new_id = max(users, key=users.get) + 1
        users[request.remote_addr] = new_id
    else:
        users[request.remote_addr] = 0

    return request.json


if __name__ == '__main__':
    app.run()
