import math
import os
import requests
import threading
import urls as url


def send_part_data(part_id, part):
    file_data = {"id": part_id, "piece": str(list(part))}
    requests.post(url.upload_file, json=file_data)


if __name__ == "__main__":
    print("Hello, dear friend, i'm going to transfer you file.")
    command = None
    file_name = None
    threads_count = 1
    while command != "exit":
        command = input("available commands:\t\n count_threads \t\n file_name \t\n transfer_file \t\n exit \t\n").split()
        match command[0]:
            case "count_threads":
                threads_count = " ".join(command[1:len(command)])
            case "file_name":
                file_name = " ".join(command[1:len(command)])
            case "transfer_file":
                if file_name is None:
                    print("Please, enter the file name!\n")
                else:
                    reply = input((f"Your file name is {file_name}, "
                                   f"number of threads is {threads_count}. Are you sure? \t\n YES/NO \n"))
                    if reply == "YES":
                        file_size = os.path.getsize(file_name)
                        data = {"threads_count": threads_count, "file_name": file_name, "file_size": file_size}
                        requests.post(url.upload_params, json=data)
                        with open(f"{file_name}", "rb") as file:
                            new_part_id = 0
                            div_counter = threads_count
                            while True:
                                part_size = file_size
                                if file_size % div_counter != 0:
                                    part_size = math.ceil(file_size / div_counter)
                                    file_size -= part_size
                                    div_counter -= 1
                                new_part = file.read(part_size)
                                t = threading.Thread(target=send_part_data, args=(new_part_id, new_part))
                                t.daemon = True
                                t.start()
                                new_part_id += 1
                                if new_part_id == threads_count:
                                    break
                        result = requests.get(url.upload_file)
                        if result.status_code == 200:
                            print("Your file has been uploaded successfully!\n")
                        else:
                            print("Oh, something went wrong...\n")
            case "exit":
                print("Ok, goodbye!")
                break
