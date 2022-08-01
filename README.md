# -DYU-face_roll_call_system
執行GUI.py即可, 其他均為單文件。

![image](https://user-images.githubusercontent.com/50831121/181445835-683041d6-ba22-46a2-983f-0a0f439de4c2.png)


--------------------------------------------
#7/29
新增MessageBox

![image](https://user-images.githubusercontent.com/50831121/181757125-3520e309-ec97-4dda-b7dc-0c2eb824abed.png)

![image](https://user-images.githubusercontent.com/50831121/181757185-450e9490-f4f8-4e91-a32e-d02533099a76.png)

![image](https://user-images.githubusercontent.com/50831121/181757243-85a7bcd1-e6b3-435e-bb3b-33000ae613b8.png)

![image](https://user-images.githubusercontent.com/50831121/181800083-fff254bc-60ba-4023-afa2-489fc6aefa59.png)

7/30
新增有上方提示拍照數量

![image](https://user-images.githubusercontent.com/50831121/181800602-1c6e0034-64eb-4a01-8060-07b83941efdd.png)

![image](https://user-images.githubusercontent.com/50831121/181800838-d50c86f0-a9a4-4700-b8aa-425b1e240f5a.png)

--------------------------------------------
7/31 更新測試版模組NewTrain.py

因opencv模組無法辨識口罩及側臉, 改使用google家的mediapipe替代, 目前為測試階段。

![image](https://user-images.githubusercontent.com/50831121/181903882-004e1d3b-aa6d-4218-a3ae-9c7e6e4e41c6.png)

![image](https://user-images.githubusercontent.com/50831121/181904059-5e8e1129-452e-473e-ab1e-1eb328793308.png)

--------------------------------------------
8/1 更新NewTrain.py 提示 名字 + 拍照數量

優化NewTrain.py

![image](https://user-images.githubusercontent.com/50831121/182035464-b5090eac-0a1c-4b48-95ea-dfa9bae4eedb.png)

--------------------------------------------
8/1 將主程式GUI套用NewTrain.py, 並優化程式碼。

目前自行測試所有功能皆為穩定，將不會把Identify()部分更改為mediapipe

因為還是希望用戶正臉進行拍攝識別!
