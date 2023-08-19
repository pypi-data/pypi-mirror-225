import os
import cv2
import math
import numpy as np
from typing import Union
from scipy.optimize import linear_sum_assignment
from filterpy.kalman import KalmanFilter


def rela_to_abs(coords: list, resolution: list) -> list:
    '''
    相对坐标转换为绝对坐标。

    参数:
        coords (list): [center_x, center_y, width, height]

        resolution (list):  [width, height]
    
    返回:
        list: 绝对坐标
    '''
    coords = np.array(coords)
    single = False

    if len(coords.shape) == 1:
        single = True
        coords = coords[np.newaxis, :]

    if (coords.dtype == float) and (coords <= 1).all():
        w, h = resolution
        coords[:, ::2] *= w
        coords[:, 1::2] *= h
    coords = coords.astype(int)

    if single:
        coords = coords[0]

    return coords.tolist()


def pnpoly(verts: list, testx: int, testy: int) -> bool:
    '''
    判断点是否在多边形内部, PNPoly算法。

    参数:
        verts (list): 由多边形顶点组成的列表, 例如[[129,89],[342,68],[397,206],[340,373],[87,268]]

        testx (int): 点的x坐标, 例如123

        testy (int): 点的y坐标, 例如234

    返回:
        True: 点在多边形内

        False: 点不在多边形内
    '''

    vertx = [xyvert[0] for xyvert in verts]
    verty = [xyvert[1] for xyvert in verts]
    nvert = len(verts)
    c = False
    j = nvert - 1
    for i in range(nvert):
        if ((verty[i] > testy) !=
            (verty[j] > testy)) and (testx < (vertx[j] - vertx[i]) *
                                     (testy - verty[i]) /
                                     (verty[j] - verty[i]) + vertx[i]):
            c = not c
        j = i
    return c


def compute_polygon_area(x: list, y: list) -> float:
    '''
    计算多边形面积

    参数：
        x(list):[x1,x2,...,xn]
        y(list):[y1,y2,...,yn]

    返回：
        float :多边形面积

    '''

    point_num = len(x)
    if (point_num < 3): return 0.0

    s = y[0] * (x[point_num - 1] - x[1])
    for i in range(1, point_num):
        s += y[i] * (x[i - 1] - x[(i + 1) % point_num])
    return abs(s / 2.0)


def mean_fliter(x: list, y: list, step: int) -> (list, list):
    '''
    自定义均值滤波：将数据滤波，然后按等间隔提取坐标值（中值滤波同时减少数据量，减少计算时间，提高效率）

    参数：
        x(list):[x1,x2,...,xn]

        y(list):[y1,y2,...,yn]

        step(int): n
    返回：
        #滤波和筛选后的坐标值

        x(list):[x1,x2,...,xn]

        y(list):[y1,y2,...,yn]
    '''
    result_x = np.array(x)
    result_y = np.array(y)

    column = step
    rank = int(np.size(result_x) / column)

    result_x = np.resize(result_x, (rank, column))
    result_y = np.resize(result_y, (rank, column))

    result_x = np.mean(result_x, axis=1)
    result_y = np.mean(result_y, axis=1)

    return result_x.tolist(), result_y.tolist()


def mid_filter(x: list, y: list, step: int) -> (list, list):
    '''
    自定义中值滤波：将数据滤波，然后按等间隔提取坐标值（中值滤波同时减少数据量，减少计算时间，提高效率）

    参数：
        x(list):[x1,x2,...,xn]

        y(list):[y1,y2,...,yn]

        step(int): n
    返回：
        #滤波和筛选后的坐标值

        x(list):[x1,x2,...,xn]

        y(list):[y1,y2,...,yn]
    '''
    result_x = np.array(x)
    result_y = np.array(y)

    column = step
    rank = int(np.size(result_x) / column)

    result_x = np.resize(result_x, (rank, column))
    result_y = np.resize(result_y, (rank, column))

    result_x = np.median(result_x, axis=1)
    result_y = np.median(result_y, axis=1)

    return result_x.tolist(), result_y.tolist()


def get_scan_area(basis_x: list, basis_y: list, cur_x: list, cur_y: list,
                  step: int) -> float:
    '''
    计算当前坐标和基础坐标构成多边形面积

    参数：
        basis_x(list):基础x坐标[x1,x2,x3,.....,xn]

        basis_y(list):基础y坐标[y1,y2,y3,.....,yn]

        cur_x(list): 当前x坐标[x1,x2,x3,.....,xn]

        cur_y(list): 当前y坐标[y1,y2,y3,.....,yn]
    返回：
        result(float):两次激光点云构成多边形的面积
    '''
    basis_x, basis_y = mean_fliter(basis_x, basis_y, step=step)
    basis_x = list(reversed(basis_x))
    basis_y = list(reversed(basis_y))

    cur_x, cur_y = mean_fliter(cur_x, cur_y, step)
    cur_x += basis_x
    cur_y += basis_y
    return compute_polygon_area(cur_x, cur_y)


def get_IOU(gt_box: Union[list, tuple], b_box: Union[list, tuple]) -> float:
    '''
        计算两个矩形区域的IOU

        参数：
            gt_box (list) : 真实区域坐标 [100,100,500,500] ,shape: [1,4]

            b_box (list) : 目标区域坐标 [150,150,400,400] ,shape: [1,4]

        返回：
            两个框的重叠程度(IOU)
    '''
    assert len(gt_box) == 4 and len(b_box) == 4, '请输入正确的坐标'
    gt_box = [int(i) for i in gt_box]
    b_box = [int(i) for i in b_box]

    width0 = gt_box[2] - gt_box[0]
    height0 = gt_box[3] - gt_box[1]
    width1 = b_box[2] - b_box[0]
    height1 = b_box[3] - b_box[1]
    max_x = max(gt_box[2], b_box[2])
    min_x = min(gt_box[0], b_box[0])
    width = width0 + width1 - (max_x - min_x)
    max_y = max(gt_box[3], b_box[3])
    min_y = min(gt_box[1], b_box[1])
    height = height0 + height1 - (max_y - min_y)

    interArea = width * height
    boxAArea = width0 * height0
    boxBArea = width1 * height1
    iou = interArea / (boxAArea + boxBArea - interArea)

    return iou


def compute_density(target_area: Union[list, tuple],
                    coords: Union[list, tuple]) -> (int, float):
    '''
        输入一个目标区域，一组目标坐标，计算目标数量、密度

        参数：
            target_area (list) : [[129,89],[342,68],[397,206],[340,373],[87,268]] ,shape : [n,2]

            coords (list) : [[[左上x,左上y],[右下x,右下y]]]   [[[0,0],[500,500]],[[700,700],[400,400]], [[0,0],[100,100]],[[200,200],[300,300]]] ,shape : [3,n,2]

        返回：
            return (int、float) : 目标在区域中的数量、密度
    '''
    assert len(coords) != 0, '目标数量不能为0'
    assert np.array(target_area).shape[0] > 2, '区域坐标不能少于2'
    assert len(np.array(coords).shape) >= 3, '请输入正确目标坐标'
    assert np.array(coords).shape[1] >= 2 and np.array(
        coords).shape[2] == 2, '请输入正确区域坐标'
    number = len(coords)
    if type(coords) == list:
        coords = np.array(coords)
    minx = np.min(coords[:, :, 0])
    miny = np.min(coords[:, :, 1])
    maxx = np.max(coords[:, :, 0])
    maxy = np.max(coords[:, :, 1])
    p1, p2 = ((minx, miny, maxx, maxy)), (target_area[0][0], target_area[0][1],
                                          target_area[2][0], target_area[2][1])
    iou = get_IOU(p1, p2)
    # print(iou)
    density = iou / number
    return number, float(density)


def __sst(y_no_fitting: list) -> float:
    '''
        计算SST(total sum of squares) 总平方和

        参数：

           y_no_predicted: 待拟合的y

        返回：

           总平方和SST
    '''
    y_mean = sum(y_no_fitting) / len(y_no_fitting)
    s_list = [(y - y_mean)**2 for y in y_no_fitting]
    sst = sum(s_list)
    return sst


def __ssr(y_fitting: list, y_no_fitting: list) -> float:
    '''
        计算SSR(regression sum of squares) 回归平方和

        参数：

            y_fitting: 拟合好的y值

            y_no_fitting: 待拟合y值

        返回:

            回归平方和SSR
    '''
    y_mean = sum(y_no_fitting) / len(y_no_fitting)
    s_list = [(y - y_mean)**2 for y in y_fitting]
    ssr = sum(s_list)
    return ssr


def __sse(y_fitting: list, y_no_fitting: list) -> float:
    '''
        计算SSE(error sum of squares) 残差平方和

        参数：

            y_fitting:  拟合好的y值

            y_no_fitting: 待拟合y值

        返回：

            残差平方和SSE
    '''
    s_list = [(y_fitting[i] - y_no_fitting[i])**2
              for i in range(len(y_fitting))]
    sse = sum(s_list)
    return sse


def goodness_of_fit(y_fitting: list, y_no_fitting: list) -> float:
    '''
        计算拟合优度R^2
        
        参数：

             y_fitting: 拟合好的y值

             y_no_fitting: 待拟合y值

        返回:

            拟合优度R^2
    '''
    SSR = __ssr(y_fitting, y_no_fitting)
    SST = __sst(y_no_fitting)
    rr = SSR / SST
    return rr


def fit_line(x_: list, y_: list) -> (float, float):
    '''
        最小二乘法拟合点集为直线
           参数：
              x_ : 拟合好的y值
              y_ : 待拟合y值
           返回:
              k: 直线斜率
              b: 直线偏移
        '''
    k, b = np.polyfit(x_, y_, 1)
    k, b = round(k, 3), round(b, 3)
    return k, b


def find_max_contour(src: np.ndarray = None, path: str = None) -> np.ndarray:
    '''
    输入一个图片或图片的路径，将图片中最大的轮廓找到并裁剪出来

    参数：
        src (np.mdarray) : 读取的图片 shape : [w,h,3]

        path (str) : 输入图像路径

    返回：
        return (np.ndarray) : 裁剪后的图片
    '''

    if src is None and path is None:
        raise '请输入图像或图片路径'
    if src is not None and path is not None:
        raise '不能同时输入图像和图片路径'
    img = None
    # x,y,w,h=None,None,None,None
    if path is not None:
        if os.path.exists(path):
            # print(str(len(img_list))+'--读取文件--')
            img = cv2.imread(path)
    if src is not None:
        img = src
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 应用阈值
    thresh = cv2.adaptiveThreshold(gray_image, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                   cv2.THRESH_BINARY, 11, 2)

    thresh_inv = cv2.bitwise_not(thresh)

    # 找到所有的轮廓
    contours, hierarchy = cv2.findContours(thresh_inv, cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_SIMPLE)
    area = []
    # 找到最大的轮廓
    height, width, channel = img.shape

    for i in range(len(contours)):
        area.append(cv2.contourArea(contours[i]))
    max_idx = np.argmax(np.array(area))
    max_contour = contours[max_idx]
    hull = cv2.convexHull(max_contour, returnPoints=True)
    point = np.squeeze(hull)
    new_list = sorted(point.tolist(), key=lambda x: x[0]**2 + x[1]**2)
    top_right = sorted(point.tolist(),
                       key=lambda x: (0 - x[0])**2 + (height - x[1])**2)
    left_buttom = sorted(point.tolist(),
                         key=lambda x: (width - x[0])**2 + (0 - x[1])**2)
    pts1 = np.float32(
        [new_list[0], top_right[0], new_list[-1], left_buttom[0]])
    pts2 = np.float32([[0, 0], [0, height], [width, height], [width, 0]])
    M = cv2.getPerspectiveTransform(pts1, pts2)
    warped = cv2.warpPerspective(img, M, (width, height))
    return warped


def vague_detection(src: np.ndarray,
                    blur_threshold: int = 1000) -> (bool, float):
    '''
    判断图像是否模糊

    参数：

        src (np.mdarray) : 读取的图片 shape : [w,h,3]

        blur_threshold : 模糊阈值

    返回值：

        是否模糊
        图像方差值
    
    '''
    assert src is not None, '输入图像不能为空'
    im_gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    fm = cv2.Canny(im_gray, 500, 100).var()
    if fm < blur_threshold:
        return True, fm
    return False, fm


def get_points_rect_contours(points: list) -> list:
    '''
	    求解点的最小外接矩形。

	    参数:
	        points (list): 由多边形顶点组成的列表, 例如[[129,89],[342,68],[397,206],[340,373],[87,268]]

	    返回:
	        list: 最小外接矩形的四个顶点 [[106 178],[124 142],[200 180],[182 216]]
	    '''
    points = np.array([points], dtype=np.int32)
    rect = cv2.minAreaRect(points)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    return box


def get_points_mincircle(points: list) -> tuple:
    '''
	求解点的最小外接圆。

	    参数:
	        points (list): 由多边形顶点组成的列表, 例如[[129,89],[342,68],[397,206],[340,373],[87,268]]

	    返回:
	        x,y,radius(tuple): 最小外接圆的中心坐标和半径
	'''
    cnt = np.array(points)
    (x, y), radius = cv2.minEnclosingCircle(cnt)
    return tuple(int(item) for item in (x, y, radius))


def _iou(bb_test, bb_gt):
    """
    在两个box间计算IOU
    :param bb_test: box1 = [x1y1x2y2]
    :param bb_gt: box2 = [x1y1x2y2]
    :return: 交并比IOU
    """
    xx1 = np.maximum(bb_test[0], bb_gt[0])
    yy1 = np.maximum(bb_test[1], bb_gt[1])
    xx2 = np.minimum(bb_test[2], bb_gt[2])
    yy2 = np.minimum(bb_test[3], bb_gt[3])
    w = np.maximum(0., xx2 - xx1)
    h = np.maximum(0., yy2 - yy1)
    wh = w * h
    o = wh / ((bb_test[2] - bb_test[0]) * (bb_test[3] - bb_test[1]) +
              (bb_gt[2] - bb_gt[0]) * (bb_gt[3] - bb_gt[1]) - wh)
    return o


def convert_bbox_to_z(bbox):
    """
    将[x1,y1,x2,y2]形式的检测框转为滤波器的状态表示形式[x,y,s,r]。其中x，y是框的中心坐标，s是面积，尺度，r是宽高比
    参数:
       bbox: [x1,y1,x2,y2] 分别是左上角坐标和右下角坐标
    返回：
       [x,y,s,r] 4行1列，其中x,y是box中心位置的坐标，s是面积，r是纵横比w/h
    """
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    x = bbox[0] + w / 2.
    y = bbox[1] + h / 2.
    s = w * h
    r = w / float(h)
    return np.array([x, y, s, r]).reshape((4, 1))


def convert_x_to_bbox(x, score=None):
    """
    将[cx，cy，s，r]的目标框表示转为[x_min，y_min，x_max，y_max]的形式
    参数:
        x:[ x, y, s, r ],其中x,y是box中心位置的坐标，s是面积，r
        score: 置信度
    返回:
        [x1,y1,x2,y2],左上角坐标和右下角坐标
    """
    w = np.sqrt(x[2] * x[3])
    h = x[2] / w
    if score is None:
        return np.array(
            [x[0] - w / 2., x[1] - h / 2., x[0] + w / 2.,
             x[1] + h / 2.]).reshape((1, 4))
    else:
        return np.array([
            x[0] - w / 2., x[1] - h / 2., x[0] + w / 2., x[1] + h / 2., score
        ]).reshape((1, 5))


class KalmanBoxTracker(object):
    count = 0

    def __init__(self, bbox):
        """
        初始化边界框和跟踪器
        """
        # 定义等速模型
        # 内部使用KalmanFilter，7个状态变量和4个观测输入
        self.kf = KalmanFilter(dim_x=7, dim_z=4)
        self.kf.F = np.array([[1, 0, 0, 0, 1, 0, 0], [0, 1, 0, 0, 0, 1, 0],
                              [0, 0, 1, 0, 0, 0, 1], [0, 0, 0, 1, 0, 0, 0],
                              [0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 1, 0],
                              [0, 0, 0, 0, 0, 0, 1]])
        self.kf.H = np.array([[1, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0],
                              [0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0]])
        self.kf.R[2:, 2:] *= 10.
        self.kf.P[
            4:,
            4:] *= 1000.  # give high uncertainty to the unobservable initial velocities
        self.kf.P *= 10.
        self.kf.Q[-1, -1] *= 0.01
        self.kf.Q[4:, 4:] *= 0.01
        self.kf.x[:4] = convert_bbox_to_z(bbox)
        self.time_since_update = 0  # 记录从上次更新到当前帧的预测次数，每次更新后清0(update函数中)
        self.id = KalmanBoxTracker.count
        KalmanBoxTracker.count += 1
        self.history = []
        self.hits = 0
        self.hit_streak = 0  # 记录跟踪上的次数，一旦一帧没有跟上直接清0(predict函数中)
        self.age = 0

    def update(self, bbox):
        """
        使用观察到的目标框更新状态向量。filterpy.kalman.KalmanFilter.update 会根据观测修改内部状态估计self.kf.x。
        重置self.time_since_update，清空self.history。
        参数:
           bbox:目标框
        """
        self.time_since_update = 0
        self.history = []
        self.hits += 1
        self.hit_streak += 1
        self.kf.update(convert_bbox_to_z(bbox))

    def predict(self):
        """
        推进状态向量并返回预测的边界框估计。
        将预测结果追加到self.history。由于 get_state 直接访问 self.kf.x，所以self.history没有用到
        """
        if (self.kf.x[6] + self.kf.x[2]) <= 0:
            self.kf.x[6] *= 0.0
        self.kf.predict()
        # 预测次数
        self.age += 1
        # 若跟踪过程中未进行更新，将hit_streak = 0
        if self.time_since_update > 0:
            self.hit_streak = 0
        self.time_since_update += 1
        # 将预测结果追加到history
        self.history.append(convert_x_to_bbox(self.kf.x))
        return self.history[-1]

    def get_state(self):
        """
        返回当前边界框估计值
        """
        # print("x_speed:{}".format(self.kf.x))
        return convert_x_to_bbox(self.kf.x)


def associate_detections_to_trackers(detections, trackers, iou_threshold=0.3):
    """
    将检测框bbox与卡尔曼滤波器的跟踪框进行关联匹配
    参数:
         detections:检测框
         trackers:跟踪框，即跟踪目标
         iou_threshold:IOU阈值
    返回:  跟踪成功目标的矩阵：matchs
          新增目标的矩阵：unmatched_detections
          跟踪失败即离开画面的目标矩阵：unmatched_trackers
    """
    # 跟踪目标数量为0，直接构造结果
    if (len(trackers) == 0) or (len(detections) == 0):
        return np.empty(
            (0, 2), dtype=int), np.arange(len(detections)), np.empty((0, 5),
                                                                     dtype=int)

    # iou 不支持数组计算。逐个计算两两间的交并比，调用 linear_assignment 进行匹配
    iou_matrix = np.zeros((len(detections), len(trackers)), dtype=np.float32)
    # 遍历目标检测的bbox集合，每个检测框的标识为d
    for d, det in enumerate(detections):
        # 遍历跟踪框（卡尔曼滤波器预测）bbox集合，每个跟踪框标识为t
        for t, trk in enumerate(trackers):
            iou_matrix[d, t] = _iou(det, trk)
    # 通过匈牙利算法将跟踪框和检测框以[[d,t]...]的二维矩阵的形式存储在match_indices中
    result = linear_sum_assignment(-iou_matrix)
    matched_indices = np.array(list(zip(*result)))

    # 记录未匹配的检测框及跟踪框
    # 未匹配的检测框放入unmatched_detections中，表示有新的目标进入画面，要新增跟踪器跟踪目标
    unmatched_detections = []
    for d, det in enumerate(detections):
        if d not in matched_indices[:, 0]:
            unmatched_detections.append(d)
    # 未匹配的跟踪框放入unmatched_trackers中，表示目标离开之前的画面，应删除对应的跟踪器
    unmatched_trackers = []
    for t, trk in enumerate(trackers):
        if t not in matched_indices[:, 1]:
            unmatched_trackers.append(t)
    # 将匹配成功的跟踪框放入matches中
    matches = []
    for m in matched_indices:
        # 过滤掉IOU低的匹配，将其放入到unmatched_detections和unmatched_trackers
        if iou_matrix[m[0], m[1]] < iou_threshold:
            unmatched_detections.append(m[0])
            unmatched_trackers.append(m[1])
        # 满足条件的以[[d,t]...]的形式放入matches中
        else:
            matches.append(m.reshape(1, 2))
    # 初始化matches,以np.array的形式返回
    if len(matches) == 0:
        matches = np.empty((0, 2), dtype=int)
    else:
        matches = np.concatenate(matches, axis=0)

    return matches, np.array(unmatched_detections), np.array(
        unmatched_trackers)


class Sort(object):
    """
        多目标跟踪算法，通过卡尔曼滤波来传播目标物体到未来帧中，
        再通过IOU作为度量指标来建立关系，实现多目标追踪
    """
    def __init__(self, max_age=1, min_hits=3):
        # 最大检测数：目标未被检测到的帧数，超过之后会被删
        self.max_age = max_age
        # 目标命中的最小次数，小于该次数不返回
        self.min_hits = min_hits
        # 卡尔曼跟踪器
        self.trackers = []
        # 帧计数
        self.frame_count = 0

    def update(self, dets):
        self.frame_count += 1
        # 在当前帧逐个预测轨迹位置，记录状态异常的跟踪器索引
        # 根据当前所有的卡尔曼跟踪器个数（即上一帧中跟踪的目标个数）创建二维数组：行号为卡尔曼滤波器的标识索引，列向量为跟踪框的位置和ID
        trks = np.zeros((len(self.trackers), 5))  # 存储跟踪器的预测
        to_del = []  # 存储要删除的目标框
        ret = []  # 存储要返回的追踪目标框
        # 循环遍历卡尔曼跟踪器列表
        for t, trk in enumerate(trks):
            # 使用卡尔曼跟踪器t产生对应目标的跟踪框
            pos = self.trackers[t].predict()[0]
            # 遍历完成后，trk中存储了上一帧中跟踪的目标的预测跟踪框
            trk[:] = [pos[0], pos[1], pos[2], pos[3], 0]
            # 如果跟踪框中包含空值则将该跟踪框添加到要删除的列表中
            if np.any(np.isnan(pos)):
                to_del.append(t)
        # numpy.ma.masked_invalid 屏蔽出现无效值的数组（NaN 或 inf）
        # numpy.ma.compress_rows 压缩包含掩码值的2-D 数组的整行，将包含掩码值的整行去除
        # trks中存储了上一帧中跟踪的目标并且在当前帧中的预测跟踪框
        trks = np.ma.compress_rows(np.ma.masked_invalid(trks))
        # 逆向删除异常的跟踪器，防止破坏索引
        for t in reversed(to_del):
            self.trackers.pop(t)
        # 将目标检测框与卡尔曼滤波器预测的跟踪框关联获取跟踪成功的目标，新增的目标，离开画面的目标
        matched, unmatched_dets, unmatched_trks = associate_detections_to_trackers(
            dets, trks)

        # 将跟踪成功的目标框更新到对应的卡尔曼滤波器
        for t, trk in enumerate(self.trackers):
            if t not in unmatched_trks:
                d = matched[np.where(matched[:, 1] == t)[0], 0]
                # 使用观测的边界框更新状态向量
                trk.update(dets[d, :][0])

        # 为新增的目标创建新的卡尔曼滤波器对象进行跟踪
        for i in unmatched_dets:
            trk = KalmanBoxTracker(dets[i, :])
            self.trackers.append(trk)

        # 自后向前遍历，仅返回在当前帧出现且命中周期大于self.min_hits（除非跟踪刚开始）的跟踪结果；如果未命中时间大于self.max_age则删除跟踪器。
        # hit_streak忽略目标初始的若干帧
        i = len(self.trackers)
        for trk in reversed(self.trackers):
            # 返回当前边界框的估计值
            d = trk.get_state()[0]
            # 跟踪成功目标的box与id放入ret列表中
            if (trk.time_since_update <
                    1) and (trk.hit_streak >= self.min_hits
                            or self.frame_count <= self.min_hits):
                ret.append(np.concatenate((d, [trk.id + 1])).reshape(
                    1, -1))  # +1 as MOT benchmark requires positive
            i -= 1
            # 跟踪失败或离开画面的目标从卡尔曼跟踪器中删除
            if trk.time_since_update > self.max_age:
                self.trackers.pop(i)
        # 返回当前画面中所有目标的box与id,以二维矩阵形式返回
        if len(ret) > 0:
            return np.concatenate(ret)
        return np.empty((0, 5))


def track(tracker, dets):
    '''
        跟踪检测框
        参数：
            dets (list) : [[lx1,ly1,rx2,ry2,conf],...]     lx1,ly1,rx2,ry2,conf1分别为 检测框左上点(lx1,ly1)、右下点(rx2,ry2)和置信度conf
        返回：
            return list: [[lx1,ly1,rx2,ry2,track_id],...]   跟踪框坐标 左上点(lx1,ly1),右下点(rx2,ry2),跟踪编号(track_id)
    '''
    tracks = tracker.update(dets)
    return tracks


def get_angle(dot1, dot0, dot2):
    """
        dot0->dot1，dot0—>dot2,两个向量的夹角
        参数:
            dot1: [x0,y0]
            dot0: [x1,y1]
            dot2: [x2,y2]
        返回：
            角度值，范围 0~360
    """
    x1 = dot1[0] - dot0[0]
    y1 = dot1[1] - dot0[1]
    # 向量 b（x2，y2）
    x2 = dot2[0] - dot0[0]
    y2 = dot2[1] - dot0[1]
    angle = math.degrees(
        math.acos((x1 * x2 + y1 * y2) / (((x1**2 + y1**2)**0.5) *
                                         ((x2**2 + y2**2)**0.5))))
    return angle


# 关键点距离
def eu_2(a, b):
    """
            dot0->dot1，dot0—>dot2,两个向量的夹角
            参数:
                dot1: [x0,y0]
                dot0: [x1,y1]
                dot2: [x2,y2]
            返回：
                角度值，范围 0~360
    """
    distance = np.sqrt(
        (a[0] - b[0])**2 + (a[1] - b[1])**2)  #求两点的距离用两点横纵坐标的差值开根号
    return distance


def cross_point(line1, line2):
    """
        两条直线交叉点是否存在,存在时的交点坐标
        参数:
            line1: [x0,y0,x1,y1]
            line2: [x2,y2,x3,y3]
        返回：
            是否存在交叉点(true,false),交叉点坐标[x,y]
    """
    point_is_exist = False
    x = y = 0
    x1, y1, x2, y2 = line1
    x3, y3, x4, y4 = line2

    if (x2 - x1) == 0:
        k1 = None
        b1 = 0
    else:
        k1 = (y2 - y1) * 1.0 / (x2 - x1)  # 计算k1,由于点均为整数，需要进行浮点数转化
        b1 = y1 * 1.0 - x1 * k1 * 1.0  # 整型转浮点型是关键

    if (x4 - x3) == 0:  # L2直线斜率不存在
        k2 = None
        b2 = 0
    else:
        k2 = (y4 - y3) * 1.0 / (x4 - x3)  # 斜率存在
        b2 = y3 * 1.0 - x3 * k2 * 1.0

    if k1 is None:
        if not k2 is None:
            x = x1
            y = k2 * x1 + b2
            point_is_exist = True
    elif k2 is None:
        x = x3
        y = k1 * x3 + b1
    elif not k2 == k1:
        x = (b2 - b1) * 1.0 / (k1 - k2)
        y = k1 * x * 1.0 + b1 * 1.0
        point_is_exist = True

    return point_is_exist, [x, y]


#终止手势判断
def fgesture(kp, thresh):
    '''
        输入人体关键点，判断是否终止手势
        参数:
           kp:[    [x0,y0], 鼻
                   [x1,y1], 左肘
                   [x2,y2], 左腕
                   [x3,y3], 右肘
                   [x4,y4], 右腕
           ]
           thresh:
               交叉点到鼻子的距离阈值
        返回：
           是否是终止手势
    '''
    # 左腕左肘 与 右腕右肘   是否交叉
    line1 = [kp[1][0], kp[1][1], kp[2][0], kp[2][1]]
    line2 = [kp[3][0], kp[3][1], kp[4][0], kp[4][1]]
    nose = kp[0]
    point_is_exist, p = cross_point(line1, line2)
    ret = False
    if (point_is_exist):
        if (eu_2(nose, p) < thresh):
            ret = True
    return ret


def min_bbox(kpts: np.array) -> tuple:
    """
    求最小外接矩形的坐标

    参数：
        kpts (ndarray): 17个骨骼关键点的坐标

    返回：
        tuple: x1, y1, x2, y2
    """
    kpts = np.array(kpts)
    min_x, min_y = np.min(kpts, axis=0)
    max_x, max_y = np.max(kpts, axis=0)
    return min_x, min_y, max_x, max_y

