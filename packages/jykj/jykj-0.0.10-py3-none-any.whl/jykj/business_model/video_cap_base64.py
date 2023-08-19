from __future__ import division
import time
import cv2
import threading
import base64

#########################获取视频流base64图片#################################
class VideoCapBase64:
    '''
    根据输入视频地址新建一个摄像机实体类。
    参数：
        video_url (string): 摄像头地址;.
    成员函数：
        readVideo(): 读摄像视频流图片；
        getFrame(): 获取实时图像；
        getBase64Frame(): 获取实时图像的base64编码；
        __exit__(): 退出；
        stop_thread(): 停止读取摄像头线程；
    '''
    def __init__(self, video_url):
        self.video_url = video_url
        self.cap = cv2.VideoCapture(self.video_url)
        self.real_frame = None
        self.event = threading.Event()
        self.stop_event = threading.Event()
        self.p = threading.Thread(target=self.readVideo, daemon=True)
        self.p.start()

    def readVideo(self):
        while not self.stop_event.is_set():
            try:
                time.sleep(0.001)
                if self.cap.isOpened():
                    ret, frame = self.cap.read()
                    if frame is not None:
                        self.real_frame = frame
                        self.event.set()
                    else:
                        time.sleep(0.001)
                        self.cap = cv2.VideoCapture(self.video_url)
                else:
                    time.sleep(0.001)
                    self.cap = cv2.VideoCapture(self.video_url)
            except Exception as e:
                print(e)
                time.sleep(0.001)
                self.cap = cv2.VideoCapture(self.video_url)

    def getFrame(self):
        self.event.wait()
        return self.real_frame

    def getBase64Frame(self):
        self.event.wait()
        data = cv2.imencode('.jpg', self.real_frame)[1]
        image_bytes = data.tobytes()
        image_base4 = base64.b64encode(image_bytes).decode('utf8')
        return image_base4

    def stop_thread(self):
        print("停止线程")
        self.stop_event.set()


if __name__ == '__main__':
    camobj = VideoCapBase64('rtsp://admin:password01!@192.168.188.21:554/Streaming/Channels/601')
    i=10
    while i>0:
        base64_data = camobj.getBase64Frame()
        print(len(base64_data))
        i-=1
    camobj.stop_thread()
