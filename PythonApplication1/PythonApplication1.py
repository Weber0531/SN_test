# from genericpath import exists
import time
import os
import csv
from datetime import datetime
from watchdog.observers import Observer # 用來監控檔案系統的變動
from watchdog.events import FileSystemEventHandler # 定義檔案事件處理方式

# 監控處理器
class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, file_path, sn, output_directory, observer):
        self.file_path = file_path
        self.sn = sn
        self.output_directory = output_directory
        self.observer = observer
        self.file_modified = False
        # 讀取檔案初始內容，儲存在 last_content 變數中
        self.last_content = self.read_file()

    def read_file(self):
        """讀取檔案內容"""
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r', encoding='utf-8') as file:
                return file.read()
        print("檔案不存在")
        exit()
        # return "檔案不存在"

    def write_to_csv(self, content):
        current_date = datetime.now().strftime('%Y%m%d')
        current_time = datetime.now().strftime('%H-%M-%S')
        
        dir_path = os.path.join(self.output_directory, current_date, self.sn)
        os.makedirs(dir_path, exist_ok = True)

        csv_name = f'{self.sn}_{current_time}.csv'
        csv_path = os.path.join(dir_path, csv_name)

        with open(csv_path, 'w', newline = '') as csvfile:
            writer = csv.writer(csvfile)
            for line in content.split('\n'):
                writer.writerow([line])
        print(f"資料已儲存至: {csv_path}")

    def on_modified(self, event):
        """當檔案被修改時觸發"""
        if event.src_path == self.file_path:
            self.file_modified = True
            print(f"\n檔案已更新: {self.file_path}")
            new_content = self.read_file()
            
            print(f"\n檔案內容如下 :\n{new_content}")

            # 檢查改動部分
            if new_content != self.last_content:
                print("\n更新內容如下：")
                last_set = set(self.last_content.split("\n"))
                new_set = set(new_content.split("\n"))
                if len(last_set) > len(new_set):
                    diff = last_set - new_set
                else:
                    diff = new_set - last_set
                for line in diff:
                    print(line)
                self.last_content = new_content

            self.write_to_csv(new_content)

            self.observer.stop()
            print("\n監控已結束")


def monitor_file(file_path, sn, output_directory):
    observer = Observer()
    directory = os.path.dirname(file_path)
    event_handler = FileChangeHandler(file_path, sn, output_directory, observer)
    observer.schedule(event_handler, directory, recursive=False)
    observer.start()
    print(f"\n開始監控檔案: {file_path}")

    while True:
        if event_handler.file_modified:
            break
        print("檔案尚未更新，等待檔案變動")
        time.sleep(5)
    # while not event_handler.file_modified:
    #     print("檔案尚未更新，等待檔案變動")
    #     for _ in range(50):   5 秒內檢查 50 次，每次 0.1 秒
    #         if event_handler.file_modified:
    #             break
    #         time.sleep(0.1)

    # 等待監控結束
    observer.join()

sn = input("Please input sn, length limit is 18: ")
while len(sn) != 18 or not sn.isalnum():
    print(f"this is your input: {sn}, the length is not equal 18 or include other character.")
    sn = input("please input again: ")

line = input("Please input line, if you don't input, default value is 7G23: ")
if not line:
    line = "7G23"

station = input("Please input station, if you don't input, default value is 777: ")
if not station:
    station = "777"

ip = "10.228.24.38"
print("\nSN :",sn)
print("Line :",line)
print("STATION :",station)
print("IP :",ip)

# 指定要監控的檔案
file_path = "C:\\Users\\amy91\\Desktop\\code\\PythonApplication1\\PythonApplication1\\Result.txt"
output_directory = "./"
monitor_file(file_path, sn, output_directory)
