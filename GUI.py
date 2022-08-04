import sys
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import *
from tkinter import messagebox
import os.path
import cv2
import os
import glob
import numpy as np
import mediapipe as mp

_script = sys.argv[0]
_location = os.path.dirname(_script)

_bgcolor = '#d9d9d9'  # X11 color: 'gray85'
_fgcolor = '#000000'  # X11 color: 'black'
_compcolor = 'gray40' # X11 color: #666666
_ana1color = '#c3c3c3' # Closest X11 color: 'gray76'
_ana2color = 'beige' # X11 color: #f5f5dc
_tabfg1 = 'black' 
_tabfg2 = 'black' 
_tabbg1 = 'grey75' 
_tabbg2 = 'grey89' 
_bgmode = 'light' 

def student_ID():
    student_ID = tk.Tk()
    student_ID.title('輸入學號')
    student_ID.geometry("300x80+750+350")
    def getTextInput():
        result=textExample.get(1.0, tk.END+"-1c")
        f = open('student_ID.txt', 'w')
        f.write(result)
        f.close()
        student_ID.quit()

    textExample=tk.Text(student_ID, height=1)
    textExample.pack()
    btnRead=tk.Button(student_ID, height=1, width=10, text="Read", 
                        command=getTextInput)

    btnRead.pack()

    student_ID.mainloop()

def Train():
    total = 10
    mp_face_detection = mp.solutions.face_detection   # 建立偵測方法
    mp_drawing = mp.solutions.drawing_utils           # 建立繪圖方法
    if not os.path.exists("library"):                    # 如果不存在library資料夾
        messagebox.showinfo('提示','文件夾中不存在library現在將自動創建\n請重新點[加入人臉模型]')
        os.mkdir("library")                              # 就建立library
    else:
        inputyml = tk.messagebox.askquestion('錄製人臉','是否啟動攝像頭 (y/n)')
        if inputyml == 'yes':
            student_ID()
            path = 'student_ID.txt'
            f = open(path, 'r')
            name = f.read()
            f.close()
            fileTest = r"student_ID.txt"
            os.remove(fileTest)
            if os.path.exists("library\\" + name):
                messagebox.showinfo('提示','此名字的人臉資料已經存在')
                print("此名字的人臉資料已經存在")
            else:
                os.mkdir("library\\" + name)
                cap = cv2.VideoCapture(0)                       # 開啟攝影機
                num = 1                                         # 影像編號
                with mp_face_detection.FaceDetection(             # 開始偵測人臉
        model_selection=1, min_detection_confidence=0.5) as face_detection:

                    if not cap.isOpened():
                        print("Cannot open camera")
                        exit()
                    while True:
                        ret, img = cap.read()
                        if not ret:
                            print("Cannot receive frame")
                            break
                        img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)   # 將 BGR 顏色轉換成 RGB
                        results = face_detection.process(img2)        # 偵測人臉

                        if results.detections:
                            for detection in results.detections:
                                bboxC = detection.location_data.relative_bounding_box
                                ih, iw, ic = img.shape
                                bbox = (int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height * ih))
                                cv2.rectangle(img, bbox, (255,255,255), 1)  # 標記人臉
                                cv2.putText(img, f"Name: {name} Now{num}", (bbox[0], bbox[1]-20),cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 1, cv2.LINE_AA)
                        cv2.imshow('oxxostudio', img)
                        x = int(bboxC.xmin * iw)
                        y = int(bboxC.ymin * ih)
                        w = int(bboxC.width * iw)
                        h = int(bboxC.height * ih)
                        key = cv2.waitKey(200)
                        if ret:                             # 讀取影像如果成功
                            imageCrop = img[y:y+h,x:x+w]                     # 裁切
                            imageResize = cv2.resize(imageCrop,(160,160))     # 重製大小
                            faceName = "library\\" + name + "\\" + name + str(num) + ".jpg"
                            cv2.imwrite(faceName, imageResize)      # 儲存人臉影像           
                            if num >= total:                        # 拍指定人臉數後才終止               
                                if num == total:
                                    print(f"拍攝第 {num} 次人臉成功")
                                break
                            print(f"拍攝第 {num} 次人臉成功")
                            num += 1
                        else:
                            print("請露出人臉或者摘掉遮蔽物!")
                cap.release()
                cv2.destroyAllWindows()
        else:
            print("將以存在的資料夾進行訓練")

    # 讀取人臉樣本和放入faces_db, 同時建立標籤與人名串列
    nameList = []                                       # 學生學號
    faces_db = []                                       # 儲存所有人臉
    labels = []                                         # 建立人臉標籤
    index = 0                                           # 學生編號索引
    dirs = os.listdir('library')                         # 取得所有資料夾及檔案
    for d in dirs:                                      # d是所有學生人臉的資料夾
        if os.path.isdir('library\\' + d):               # 獲得資料夾
            faces = glob.glob('library\\' + d + '\\*.jpg')  # 資料夾中所有人臉
            for face in faces:                          # 讀取人臉
                img = cv2.imread(face, cv2.IMREAD_GRAYSCALE)
                faces_db.append(img)                    # 人臉存入串列
                labels.append(index)                    # 建立數值標籤
            nameList.append(d)                          # 將學號加入串列
            index += 1
    print(f"標籤名稱 = {nameList}")
    print(f"標籤序號 ={labels}")
    # 儲存人名串列，可在未來辨識人臉時使用
    f = open('library\\employee.txt', 'w')

    f.write(','.join(nameList))
    f.close()

    print('建立人臉辨識資料庫')
    model = cv2.face.LBPHFaceRecognizer_create()        # 建立LBPH人臉辨識物件
    model.train(faces_db, np.array(labels))             # 訓練LBPH人臉辨識
    model.save('library\\deepmind.yml')                  # 儲存LBPH訓練數據
    messagebox.showinfo(f'提示',f'人臉辨識資料庫完成\n目前存在的學生:\n{nameList}')
    print(f'人臉辨識資料庫完成\n目前存在的學生:\n標籤名稱 = {nameList}')
#-------------------------------------------------------------------------------
def Identify():
    mp_face_detection = mp.solutions.face_detection   # 建立偵測方法
    mp_drawing = mp.solutions.drawing_utils           # 建立繪圖方法

    model = cv2.face.LBPHFaceRecognizer_create()
    model.read('library\\deepmind.yml')                  # 讀取已訓練模型
    f = open('library\\employee.txt', 'r')               # 開啟姓名標籤
    names = f.readline().split(',')                     # 將姓名存於串列

    def gocap():
        cap = cv2.VideoCapture(0)
        while(cap.isOpened()):                              # 如果開啟攝影機成功
            with mp_face_detection.FaceDetection(             # 開始偵測人臉
            model_selection=1, min_detection_confidence=0.5) as face_detection:
                while True:
                    ret, img = cap.read()
                    if not ret:
                        print("Cannot receive frame")
                        break
                    img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)   # 將 BGR 顏色轉換成 RGB
                    results = face_detection.process(img2)        # 偵測人臉

                    if results.detections:
                        for detection in results.detections:
                            bboxC = detection.location_data.relative_bounding_box
                            ih, iw, ic = img.shape
                            bbox = (int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height * ih))
                            cv2.rectangle(img, bbox, (255,255,255), 1)
                    cv2.imshow('oxxostudio', img)
                    x = int(bboxC.xmin * iw)
                    y = int(bboxC.ymin * ih)
                    w = int(bboxC.width * iw)
                    h = int(bboxC.height * ih)
                    key = cv2.waitKey(200)
                    if ret == True:       
                        print("已偵測到臉, 可按住空格鍵進行拍照檢測")
                        if key == ord(" "):          # 按 空格
                            imageCrop = img[y:y+h,x:x+w]                    # 裁切
                            imageResize = cv2.resize(imageCrop,(160,160))   # 重製大小
                            cv2.imwrite("library\\face.jpg", imageResize)    # 將測試人臉存檔
                            break
            cap.release()                                       # 關閉攝影機
            cv2.destroyAllWindows()
            gray = cv2.imread("library\\face.jpg", cv2.IMREAD_GRAYSCALE)
            val = model.predict(gray)
    gocap()
    # 讀取員工人臉
    gray = cv2.imread("library\\face.jpg", cv2.IMREAD_GRAYSCALE)
    val = model.predict(gray)
    if val[1] < 50:                                     #人臉辨識成功
        messagebox.showinfo( "歡迎DYU資工學生", f"歡迎DYU資工學生: {names[val[0]]}\n匹配值是: {val[1]:6.2f}")
        print(f"歡迎DYU資工學生: {names[val[0]]}")
        print(f"匹配值是: {val[1]:6.2f}")
    else:
        test22 = tk.messagebox.askquestion('提示!',f"你跟: {names[val[0]]}匹配值是: {val[1]:6.2f} | 非常接近")
        if test22 == 'yes':
            messagebox.showinfo( "歡迎DYU資工學生", f"歡迎DYU資工學生: {names[val[0]]}")
        else:
            messagebox.showerror( "Erro!","請洽詢辦公室或者教授 ")


class Toplevel1:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''

        top.geometry("566x265+723+328")
        top.minsize(0, 0)
        top.maxsize(1924, 1061)
        top.resizable(1,  1)
        top.title("人臉點名系統")
        top.configure(background="#ffffff", highlightbackground="#d9d9d9", highlightcolor="black")

        self.top = top

        self.Button1 = tk.Button(self.top)
        self.Button1.place(relx=0.004, rely=0.011, height=260, width=280)
        self.Button1.configure(activebackground="#e7e7e7", activeforeground="black", background="#efefef", compound='left', 
                                cursor="hand2", disabledforeground="#a3a3a3", foreground="#000000", highlightbackground="#d9d9d9", 
                                highlightcolor="black", pady="0", relief="ridge", text='''點名系統''', font=('微軟正黑體 Light', '14'), 
                                command=Identify)

        self.Button1_1 = tk.Button(self.top)
        self.Button1_1.place(relx=0.5, rely=0.011, height=130, width=280)
        self.Button1_1.configure(activebackground="#e7e7e7", activeforeground="black", background="#efefef", compound='left', 
                                    cursor="hand2", disabledforeground="#a3a3a3", foreground="#000000", highlightbackground="#d9d9d9", 
                                    highlightcolor="black", pady="0", relief="ridge", text='''加入人臉模型''', font=('微軟正黑體 Light', '12'), 
                                    command=Train)

        self.Button1_1_1 = tk.Button(self.top)
        self.Button1_1_1.place(relx=0.5, rely=0.506, height=130, width=280)
        self.Button1_1_1.configure(activebackground="#e7e7e7", activeforeground="black", background="#efefef", compound='left', 
                                    cursor="hand2", disabledforeground="#a3a3a3", foreground="#000000", highlightbackground="#d9d9d9", 
                                    highlightcolor="black", pady="0", relief="ridge", text='''查看點名詳情''', font=('微軟正黑體 Light', '12'))


if __name__ == '__main__':
    '''Main entry point for the application.'''
    global root
    root = tk.Tk()
    root.protocol( 'WM_DELETE_WINDOW' , root.destroy)
    # Creates a toplevel widget.
    global _top1, _w1
    _top1 = root
    _w1 = Toplevel1(_top1)
    root.mainloop() 
