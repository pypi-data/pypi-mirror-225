import bisect
import datetime
import json
import logging
import logging.handlers
import os
import re
import time
from collections import Counter, OrderedDict
from queue import Queue
from threading import Barrier, Lock, Thread

import numpy as np
import requests


class FalseAlarmDetection():
    def __init__(self,
                 json_url,
                 config_id,
                 log_path="/false_alarm_det_log"):
        self.config_id = config_id
        self.json_url = json_url
        self.log_path = log_path

        self.ai_json = Queue()
        self.current_ai_json = None

        self.num_det_thread = 0
        self.lock = Lock()
        self.suspects = []

        self.fps = 25
        self.frame_id = 0

    def detection(self, business_json):
        '''
        传入发送前的业务模型json并添加疑似误报警相关信息
        '''
        suspected = 0
        reason = None

        if business_json["state"] == -1:
            to_be_del = []
            start_time = business_json["start_time"]
            end_time = business_json["end_time"]
            for suspect in self.suspects:
                alarm_time, alarm_type = suspect
                relation = self.compare_time_intervals(alarm_time,
                                                       [start_time, end_time])
                if relation == -1:
                    to_be_del.append(suspect)
                elif relation == 0:
                    suspected = 1
                    reason = alarm_type
                    alarm_value = " - ".join([
                        alarm_type, business_json["start_time"],
                        business_json["end_time"]
                    ])
                    self.false_alarm_logger.info(alarm_value)
                    to_be_del.append(suspect)
                    break
                elif relation == 1:
                    break
            for item in to_be_del:
                with self.lock:
                    self.suspects.remove(item)

        business_json["extra"]["suspected"] = suspected
        business_json["extra"]["reason"] = reason

        return business_json

    def start(self, *funcs):
        '''
        创建线程
        '''
        self.setup_logging()
        num_det_threads = len(funcs)
        self.barrier = Barrier(num_det_threads + 1)

        Thread(target=self.get_ai_json, daemon=True).start()
        Thread(target=self.read_ai_json, daemon=True).start()

        for func in funcs:
            Thread(target=func, daemon=True).start()

    def get_ai_json(self):
        '''
        读取识别模型json流并存储到队列self.ai_json中
        '''
        first = True
        while True:
            try:
                conn = requests.get(self.json_url, stream=True, timeout=50)
            except Exception as e:
                self.logger.traceback("无法连接识别模型json流")
                time.sleep(5)
                continue

            try:
                for json_dict in conn.iter_lines():
                    if first:
                        first = False
                        continue
                    else:
                        json_dict = re.search('^{.*}',
                                              json_dict.decode('utf-8'))
                        if json_dict:
                            json_dict = json_dict.group()
                        else:
                            continue
                    json_dict = json.loads(json_dict)
                    self.ai_json.put(json_dict)
            except:
                self.logger.traceback("未知异常")

    def read_ai_json(self):
        '''
        从队列self.ai_json中读取识别模型json
        '''
        while True:
            self.frame_id += 1
            self.current_ai_json = self.ai_json.get()
            self.barrier.wait()
            self.barrier.wait()

    def setup_logging(self, max_bytes=20 * 1024 * 1024, backup_count=5):
        os.makedirs(self.log_path, exist_ok=True)
        stdout = os.path.join(self.log_path,
                              "{}_alarm.log".format(self.config_id))

        self.false_alarm_logger = logging.getLogger("false_alarm_det")
        self.false_alarm_logger.setLevel(logging.INFO)
        formatter = logging.Formatter(
            "%(asctime)s - %(threadName)s - %(levelname)s - %(message)s")

        stdout_handler = logging.handlers.RotatingFileHandler(
            stdout, maxBytes=max_bytes, backupCount=backup_count)
        stdout_handler.setLevel(logging.INFO)
        stdout_handler.setFormatter(formatter)
        self.false_alarm_logger.addHandler(stdout_handler)

    def compare_time_intervals(self, interval1, interval2):
        '''
        对比两个时间段的关系
        '''
        start_time1 = datetime.datetime.strptime(interval1[0],
                                                 "%Y-%m-%d %H:%M:%S")
        end_time1 = datetime.datetime.strptime(interval1[1],
                                               "%Y-%m-%d %H:%M:%S")
        start_time2 = datetime.datetime.strptime(interval2[0],
                                                 "%Y-%m-%d %H:%M:%S")
        end_time2 = datetime.datetime.strptime(interval2[1],
                                               "%Y-%m-%d %H:%M:%S")

        if end_time1 < start_time2:
            return -1
        elif start_time1 <= end_time2 and start_time2 <= end_time1:
            return 0
        elif start_time1 > end_time2:
            return 1

    def confidence_det(self, name, conf_thresh, duration_sec=5, min_num=1):
        '''
        单类别置信度检测
        当存在多个目标时, 取最高置信度
        计算过去<duration_sec>秒内的平均置信度是否小于阈值<conf_thresh>, 小于则将此时间段放入self.suspects
        '''

        confidence_data = []
        while True:
            self.barrier.wait()
            if self.current_ai_json is not None:
                # 获取置信度
                objects = [
                    i for i in self.current_ai_json['objects']
                    if i["name"].lower() == name.lower()
                ]
                if objects:
                    objects_conf = [i['confidence'] for i in objects]
                    confidence_data.append(
                        [max(objects_conf), self.current_ai_json['time']])

            # 删除旧数据
            data_time = [
                datetime.datetime.strptime(data[1], "%Y-%m-%d %H:%M:%S")
                for data in confidence_data
            ]
            threshold = datetime.datetime.now() - datetime.timedelta(
                seconds=duration_sec)
            i = bisect.bisect_left(data_time, threshold)
            confidence_data = confidence_data[i:]

            # 判断平均置信度是否小于阈值
            if self.frame_id % self.fps == 0:
                if len(confidence_data) >= min_num:
                    mean = sum(
                        data[0]
                        for data in confidence_data) / len(confidence_data)
                    if mean < conf_thresh:
                        start_time = confidence_data[0][1]
                        end_time = confidence_data[-1][1]
                        with self.lock:
                            self.suspects.append([[start_time, end_time],
                                                  "过去{}秒{}平均置信度低于{}".format(
                                                      duration_sec, name,
                                                      conf_thresh)])

            self.barrier.wait()

    def unstable_det(self, name, threshold=0.5, duration_sec=5):
        '''
        单类别检测框不连续检测, 适用于漏识别导致的误报警
        每秒出现次数最多的目标数量占比是否小于阈值(threshold), 小于阈值时此秒不连续
        不连续持续duration_sec秒后, 则将此时间段放入self.suspects
        '''

        num_objs = []
        unstable_time = []
        while True:
            self.barrier.wait()
            if self.current_ai_json is not None:
                objects = [
                    i for i in self.current_ai_json['objects']
                    if i["name"].lower() == name.lower()
                ]
                num_objs.append([len(objects), self.current_ai_json["time"]])

            if self.frame_id % self.fps == 0:
                if len(num_objs) == self.fps:
                    counter = Counter([i[0] for i in num_objs])
                    sorted_counts = counter.most_common(1)
                    if sorted_counts[0][1] / self.fps < threshold:
                        unstable_time.append([num_objs[0][1], num_objs[-1][1]])
                    elif unstable_time:
                        if len(unstable_time) > duration_sec:
                            start_time = unstable_time[0][0]
                            end_time = unstable_time[-1][1]
                            with self.lock:
                                self.suspects.append([[start_time, end_time],
                                                      "{}检测框不连续超过{}秒".format(
                                                          name, duration_sec)])
                        unstable_time.clear()
                num_objs.clear()

            self.barrier.wait()

    def motionless_det(self,
                       name,
                       duration_min,
                       iou_threshold=0.7,
                       max_lost=250):
        '''
        单类别长期静止不动检测
        目标不动超过<duration_min>分钟, 则将此时间段放入self.suspects
        目标累积<max_lost>帧不在初始位置时删除此目标的记录
        '''

        objects_data = OrderedDict()
        object_id = 0

        while True:
            self.barrier.wait()
            if self.current_ai_json is not None:
                objects = [
                    i for i in self.current_ai_json['objects']
                    if i["name"].lower() == name.lower()
                ]
                objects_xywh = [[
                    i['relative_coordinates']["center_x"],
                    i['relative_coordinates']["center_y"],
                    i['relative_coordinates']["width"],
                    i['relative_coordinates']["height"]
                ] for i in objects]
                objects_xyxy = [[
                    i[0] - 0.5 * i[2], i[1] - 0.5 * i[3], i[0] + 0.5 * i[2],
                    i[1] + 0.5 * i[3]
                ] for i in objects_xywh]

                if objects_xyxy:
                    existed_xyxy = [
                        data["bbox"] for data in objects_data.values()
                    ]
                    matched_indices = []
                    if existed_xyxy:
                        ious = self.iou_batch(existed_xyxy, objects_xyxy)
                        for id, iou in zip(objects_data.keys(), ious):
                            if np.max(iou) > iou_threshold:
                                max_index = np.argmax(iou)
                                matched_indices.append(max_index)
                                objects_data[id]["count"] += 1
                                objects_data[id]["lost"] = 0
                            else:
                                objects_data[id]["lost"] += 1
                    for i, object_xyxy in enumerate(objects_xyxy):
                        if i not in matched_indices:
                            object_id += 1
                            objects_data[object_id] = {
                                "count": 1,
                                "lost": 0,
                                "bbox": object_xyxy,
                                "start_time": self.current_ai_json["time"]
                            }
                else:
                    for data in objects_data.values():
                        data["lost"] += 1

                objects_data = {
                    id: data
                    for id, data in objects_data.items()
                    if data["lost"] < max_lost
                }

                if self.frame_id % self.fps == 0:
                    for data in objects_data.values():
                        if data["count"] > (duration_min * 60 * 25):
                            start_time = data["start_time"]
                            end_time = self.current_ai_json['time']
                            with self.lock:
                                self.suspects.append([[start_time, end_time],
                                                      "{}静止不动超过{}分钟".format(
                                                          name, duration_min)])

            self.barrier.wait()

    def bbox_size_det(self, name, threshold, h_range=[0, 1], w_range=[0, 1]):
        '''
        单类别检测框尺寸检测
        每秒检测框异常比例大于阈值<threshold>时, 将此时间段放入self.suspects
        '''

        count_w = 0
        count_h = 0
        data_time = []
        while True:
            self.barrier.wait()
            if self.current_ai_json is not None:
                data_time.append(self.current_ai_json["time"])
                objects = [
                    i for i in self.current_ai_json['objects']
                    if i["name"].lower() == name.lower()
                ]
                for object in objects:
                    w = object['relative_coordinates']["width"]
                    h = object['relative_coordinates']["height"]
                    if h < h_range[0] or h > h_range[1]:
                        count_h += 1
                    if w < w_range[0] or w > w_range[1]:
                        count_w += 1

            if self.frame_id % self.fps == 0:
                if count_w > self.fps * threshold or count_h > self.fps * threshold:
                    with self.lock:
                        self.suspects.append([[data_time[0], data_time[-1]],
                                              "{}检测框尺寸异常".format(name)])
                count_w = 0
                count_h = 0
                data_time.clear()
            self.barrier.wait()

    def iou_batch(self, bb_test, bb_gt):
        """
        From SORT: Computes IOU between two bboxes in the form [x1,y1,x2,y2]
        """
        bb_gt = np.expand_dims(bb_gt, 0)
        bb_test = np.expand_dims(bb_test, 1)

        xx1 = np.maximum(bb_test[..., 0], bb_gt[..., 0])
        yy1 = np.maximum(bb_test[..., 1], bb_gt[..., 1])
        xx2 = np.minimum(bb_test[..., 2], bb_gt[..., 2])
        yy2 = np.minimum(bb_test[..., 3], bb_gt[..., 3])
        w = np.maximum(0., xx2 - xx1)
        h = np.maximum(0., yy2 - yy1)
        wh = w * h
        o = wh / ((bb_test[..., 2] - bb_test[..., 0]) *
                  (bb_test[..., 3] - bb_test[..., 1]) +
                  (bb_gt[..., 2] - bb_gt[..., 0]) *
                  (bb_gt[..., 3] - bb_gt[..., 1]) - wh)
        return o


if __name__ == "__main__":

    config_id = "test",
    json_url = "http://192.168.198.100:23576/",

    fad = FalseAlarmDetection(json_url, config_id)

    fad.start(lambda: fad.confidence_det("person", 0.3),
              lambda: fad.motionless_det("person", 10),
              lambda: fad.bbox_size_det("person", 0.7, w_range=[0, 0.66]))
