import pyautogui
import os
import shutil

position={
    'github':[1015,1050],
    'folder':[1070,1050],
    'commit_text':[490,650],
    'commit_button':[450,850]
}

DataPath = "E:\\manga\\."
GitLocalPath = "C:\\Users\\trong\\OneDrive\\Documents\\GitHub\\manga1\\manga"


#Hàm tính kích thước folder
def get_folder_size(folder_path):
    total_size = 0

    # Kiểm tra xem folder_path có tồn tại không
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        # Lặp qua tất cả các tệp và thư mục trong folder_path
        for path, dirs, files in os.walk(folder_path):
            for file in files:
                # Lấy thông tin kích thước của từng tệp
                file_path = os.path.join(path, file)
                total_size += os.path.getsize(file_path)
    return total_size/1024/1024 #mb

#Hàm đếm số lượng file con 
def count_files(folder_path):
    file_count = 0

    # Kiểm tra xem folder_path có tồn tại không
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        # Lấy danh sách các tệp tin trong folder_path
        files = os.listdir(folder_path)

        # Đếm số lượng tệp tin
        file_count = len(files)

    return file_count

def read_folders(folder_path):
    # Kiểm tra xem folder_path có tồn tại không
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        # Đọc danh sách các thư mục con
        subfolders = next(os.walk(folder_path))[1]
        # Kiểm tra nếu không còn thư mục con, dừng đệ quy
        if len(subfolders) == 0:
            return
        # In đường dẫn đến từng thư mục con
        for subfolder in subfolders:
            subfolder_path = os.path.join(folder_path, subfolder)
            print(subfolder_path)
            # print(get_folder_size(subfolder_path))
            # print(count_files(subfolder_path))
            
            # Đệ quy để đọc các thư mục con
            read_folders(subfolder_path)
    else:
        print("Thư mục không tồn tại!")

# read_folders(DataPath)

shutil.copytree(DataPath, GitLocalPath)

pyautogui.click(position["github"])
pyautogui.click(position["commit_text"])
pyautogui.typewrite("up")
pyautogui.click(position["commit_button"])
pyautogui.hotkey('ctrl','p')
# while True:
#     current_position = pyautogui.position()

#     print(current_position)
#     # if current_position[0] > 1000:
#     #     pyautogui.hotkey('ctrl','alt','m')


