import cv2
import sys
import numpy as np
from .utils import goodness_of_fit, fit_line, rela_to_abs, pnpoly


def pd(centers: list, thr: float) -> int:
    '''
        是否排队  根据多个目标中心点拟合直线，根据r2阈值判断是否排队

        参数：

            centers (list) : [[x1,y1],[x2,y2],[x3,y3],[x4,y4],[x5,y5]]

            thr (float) : 取值范围0~1，越接近1，表示拟合效果越好

        返回：

            return (int) :0 不排队 、1 排队
    '''

    cen = np.array(centers)
    x_ = np.array(cen[:, 0])
    y_ = np.array(cen[:, 1])
    k, b = fit_line(x_, y_)
    y_fit = k * x_ + b
    if (goodness_of_fit(y_fit, y_) > thr):
        return 1
    return 0


def coal_quantity_grade(coal_position: list, belt_left: list, belt_right: list,
                        grade_list: list, resolution: list) -> int:
    '''
    根据皮带左右坐标、煤炭目标检测结果、以及煤量等级列表，输出煤量等级。如皮带左右坐标和煤炭检测结果坐标系不一致，则需提供分辨率参数。

    参数：

        coal_position (list): 煤炭目标检测结果框[x, y, w, h];

        belt_left (list): 皮带左坐标[x, y];

        belt_right (list): 皮带右坐标[x, y];

        grade_list (list): 煤量等级列表[threshold1, threshold2, ...]，等级分别是0-threshold1、threshold1-threshold2、threshold2-1...;

        resolution (list): 分辨率[w, h].

    返回值：

        煤量等级值;
    '''
    # 参数检查
    if np.array(coal_position).shape != (4, ) or np.array(belt_left).shape != (
            2, ) or np.array(belt_right).shape != (2, ):
        raise ValueError("参数维数有误！")
    if len(grade_list) == 0:
        raise ValueError("煤量等级列表为空序列！")
    # 判断相对/绝对坐标
    abs_coal = 0
    abs_left = 0
    abs_right = 0
    if coal_position[0] > 1 or coal_position[1] > 1 or coal_position[
            2] > 1 or coal_position[3] > 1:
        abs_coal = 1
    if belt_left[0] > 1 or belt_left[1] > 1:
        abs_left = 1
    if belt_right[0] > 1 or belt_right[1] > 1:
        abs_right = 1

    if abs_coal + abs_left + abs_right > 0 and abs_coal * abs_left * abs_right == 0 and len(
            resolution) == 0:
        raise ValueError("坐标不一致时，请提供分辨率参数！")
    if len(resolution) > 0 and np.array(resolution).shape != (2, ):
        raise ValueError("分辨率格式有误！")
    if belt_left[0] > belt_right[0]:
        raise ValueError("belt_left应在belt_right左边！")
    # 统一坐标
    if abs_coal == 0:
        coal_position = rela_to_abs(coal_position, resolution)
    if abs_left == 0:
        belt_left = rela_to_abs(belt_left, resolution)
    if abs_right == 0:
        belt_right = rela_to_abs(belt_right, resolution)
    # 计算煤量等级
    width_ratio = coal_position[2] / (belt_right[0] - belt_left[0])
    coal_level = 1
    last_grade = 0
    for grade in grade_list:
        if grade <= last_grade:
            raise ValueError("煤量等级列表应为大于0的升序序列！")
        if grade >= 1:
            raise ValueError("煤量等级列表应小于1！")
        last_grade = grade
        if width_ratio >= grade:
            coal_level += 1
    return coal_level


def belt_deviation(roller_position: list,
                   belt_mid: list,
                   differrent: int,
                   resolution=None) -> int:
    '''
    根据皮带左右托辊数目判断皮带跑偏情况。

    参数：

        roller_position (list): 托辊位置[[x1, y1, w1, h1],[x2, y2, w2, h2],...];

        belt_mid (list): 皮带中线附近的任意坐标[x1, y1];

        differrent (int): 托辊左右差阈值;

        resolution (list): 分辨率[w, h].

    返回值：

        1: 右跑偏;

        -1: 做跑偏;
        
        0: 未跑偏;
    '''
    if resolution is None:
        resolution = [1, 1]
    if len(roller_position) == 0:
        return 0
    # 参数检查
    if len(np.array(roller_position).shape) != 2 or np.array(
            roller_position).shape[1] != 4 or np.array(belt_mid).shape != (
                2, ):
        raise ValueError("参数维数有误！")
    # 判断相对/绝对坐标
    abs_roller = 0
    abs_mid = 0
    for roller in roller_position:
        for x in roller:
            if x >= 1:
                abs_roller = 1
                break
    for x in belt_mid:
        if x >= 1:
            abs_mid = 1

    if abs_roller + abs_mid > 0 and abs_roller * abs_mid == 0 and len(
            resolution) == 0:
        raise ValueError("坐标不一致时，请提供分辨率参数！")
    if len(resolution) > 0 and np.array(resolution).shape != (2, ):
        raise ValueError("分辨率格式有误！")
    # 统一坐标
    if abs_roller == 0:
        roller_position = rela_to_abs(roller_position, resolution)
    if abs_mid == 0:
        belt_mid = rela_to_abs(belt_mid, resolution)
    #判断跑偏
    roller_left = [r for r in roller_position if r[0] <= belt_mid[0]]
    roller_right = [r for r in roller_position if r[0] > belt_mid[0]]
    if len(roller_left) - len(roller_right) >= differrent:
        return 1
    elif len(roller_right) - len(roller_left) >= differrent:
        return -1
    else:
        return 0


reading_list = [[0, 0.5], [0.5, 1], [1, 1.5], [1.5, 2], [2, 2.5]]
scale_list = ["0", "0.5", "1", "1.5", "2", "2.5"]
index_buffer = {
    "0": [],
    "0.5": [],
    "1": [],
    "1.5": [],
    "2": [],
    "2.5": []
}  # 每半秒更新一下识别模型检测的数字，用这个buffer预防识别模型的抖动


def update_index_buffer(key: str, value: tuple) -> None:
    """
    向buffer里存放bbox中心点的坐标, buffer 的长度是10帧,目的是防止识别模型检测的抖动现象。

    参数：
        key: key
        value: value

    返回：
        None
    """
    if len(index_buffer[key]) < 10:
        index_buffer[key].append(value)
    else:
        index_buffer[key].pop(0)
        index_buffer[key].append(value)


def segment_detect(gray: np.ndarray) -> tuple:
    """
    利用霍夫曼直线检测原理，检测指针的直线特征

    参数：
        gray (ndarray): 指针的patch

    返回：
        4darray: 线段的起止点坐标
    """
    minValue = 50
    maxValue = 70
    SobelKernel = 3
    minLineLength = 50  # height/32
    maxLineGap = 10  # height/40

    edges = cv2.Canny(gray, minValue, maxValue, apertureSize=SobelKernel)
    lines = cv2.HoughLinesP(edges,
                            1,
                            np.pi / 180,
                            50,
                            minLineLength=minLineLength,
                            maxLineGap=maxLineGap)
    return lines[0]


def line_segment_inter(line: tuple, segment: tuple) -> tuple:
    """
    根据直线的斜截距方程,求直线和线段的交点

    参数：
        line (tuple): x0, y0, x1, y1
        segment (tuple): xs, ys, xe, ye
    
    返回：
        tuple: x, y
    """
    x0, y0, x1, y1 = np.squeeze(line)
    xa, ya, xb, yb = segment
    k_line = (y0 - y1) / (x0 - x1 + 1e-6)
    b_line = y0 - k_line * x0
    delta_ya = k_line * (xa - x0) + y0 - ya
    delta_yb = k_line * (xb - x0) + y0 - yb
    if delta_ya == 0:
        return xa, ya
    if delta_yb == 0:
        return xb, yb

    if delta_ya * delta_yb > 0:
        return -1, -1
    else:
        k_segment = (ya - yb) / (xa - xb + 1e-6)
        b_segment = ya - k_segment * xa
        x_inter = (b_segment - b_line) / (k_line - k_segment + 1e-6)
        y_inter = k_line * x_inter + b_line
        return x_inter, y_inter


def show_reading(seg: tuple, inter: tuple, index: int) -> float:
    """
    根据起止点的坐标,指针与起止点之间连线的交点,以及起止点所对应的刻度值,按照交点所对应的比例,还原出指针对应的读数。

    参数：
        seg (tuple or list): (start_x, start_y, end_x, end_y)
        inter (tuple): (x, y)
        index (int): int

    返回：
        reading (float): float
    """
    xs, ys, xe, ye = seg
    x0, y0 = inter
    ratio = np.linalg.norm((x0 - xs, y0 - ys)) / np.linalg.norm(
        (xe - xs, ye - ys))
    scale_min, scale_max = reading_list[index]
    reading = scale_min + ratio * (scale_max - scale_min)
    return reading


def get_coor(obj: dict, img_shape: tuple) -> tuple:
    """
    将相对坐标转换成绝对坐标。

    参数：
        obj (dict): {"class_id": , "name": "", "relative_coordinates": {"center_x": , "center_y": , "width": , "height": }, "confidence": } 
        img_shape (tuple): 视频帧的分辨率， (frame_width, frame_height)

    返回：
        tuple: cx, cy, w, h
    """
    cx = obj['relative_coordinates']['center_x'] * img_shape[0]
    cy = obj['relative_coordinates']['center_y'] * img_shape[1]
    w = obj['relative_coordinates']['width'] * img_shape[0]
    h = obj['relative_coordinates']['height'] * img_shape[1]
    return cx, cy, w, h


def topological_reading(objects: list, patch: np.ndarray,
                        img_shape: tuple) -> float:
    """
    识别仪表盘显示的读数。
    
    参数：
        objects (class list): list 里面存放了多个类,每个类里面保存了关于这个bbox的信息。[{"class_id": , "name": "", "relative_coordinates": {"center_x": , "center_y": , "width": , "height": }, "confidence": }, ...]
        patch (np.ndarray): 使用opencv读取图像后的ndarray格式。
        img_shape (tuple): 视频帧的分辨率， (frame_width, frame_height)
    
    返回：
        reading (float): 最终的读数
    """

    # 用来存放刻度的坐标
    bboxs = [(0, 0, 0, 0)] + [(0, 0) for i in range(6)]
    # 用来表示刻度围成的多边形区域
    reading_heatmap = []
    # 提取信息
    for obj in objects:
        if obj["name"] == "Zhizhen":
            cx, cy, w, h = get_coor(obj, img_shape)
            bboxs[0] = (cx, cy, w, h)

        if obj["name"] == "0":
            cx, cy, w, h = get_coor(obj, img_shape)
            bboxs[1] = (cx, cy)

            update_index_buffer("0", (cx, cy))

            bc_0 = (cx, int(min(cy + h / 2, img_shape[1])))
            br_0 = (int(min(cx + w / 2,
                            img_shape[0])), int(min(cy + h / 2, img_shape[1])))
            reading_heatmap.extend([bc_0, br_0])

        if obj["name"] == "05":
            cx, cy, w, h = get_coor(obj, img_shape)
            bboxs[2] = (cx, cy)

            update_index_buffer("0.5", (cx, cy))

            bc_05 = (cx, int(min(cy + h / 2, img_shape[1])))
            reading_heatmap.append(bc_05)

        if obj["name"] == "1":
            cx, cy, w, h = get_coor(obj, img_shape)
            bboxs[3] = (cx, cy)

            update_index_buffer("1", (cx, cy))

            lc_1 = (int(max(0, cx - w / 2)), cy)
            reading_heatmap.append(lc_1)

        if obj["name"] == "15":
            cx, cy, w, h = get_coor(obj, img_shape)
            bboxs[4] = (cx, cy)

            update_index_buffer("1.5", (cx, cy))

            lc_15 = (int(max(0, cx - w / 2)), cy)
            reading_heatmap.append(lc_15)

        if obj["name"] == "2":
            cx, cy, w, h = get_coor(obj, img_shape)
            bboxs[5] = (cx, cy)

            update_index_buffer("2", (cx, cy))

            tc_2 = (cx, int(max(0, cy - h / 2)))
            reading_heatmap.append(tc_2)

        if obj["name"] == "25":
            cx, cy, w, h = get_coor(obj, img_shape)
            bboxs[6] = (cx, cy)

            update_index_buffer("2.5", (cx, cy))

            tr_25 = (int(min(cx + w / 2,
                             img_shape[0])), int(max(0, cy - h / 2)))
            br_25 = (int(min(cx + w / 2,
                             img_shape[0])), int(min(cy + h / 2,
                                                     img_shape[1])))
            reading_heatmap.extend([tr_25, br_25])

    bboxs = [int(item) for box in bboxs for item in box]

    assert bboxs[:4] != [0, 0, 0, 0], "通用模型无法检测到指针"

    # 获得指针左上角和右下角的坐标
    cx, cy, w, h = bboxs[:4]
    t, l, b, r = max(0, cx - w / 2), max(0, cy - h / 2), min(
        img_shape[0], cx + w / 2), min(img_shape[1], cy + h / 2)
    t, l, b, r = [int(item) for item in [t, l, b, r]]
    # 霍夫曼直线检测
    line = segment_detect(patch)
    tl = np.array([t, l, t, l])
    # 将patch坐标转成图像坐标
    line = line + tl
    # 用来存放数字区域的中心位置
    scales = [(0, 0) for _ in range(6)]
    for index, item in enumerate(scale_list):
        scales[index] = np.mean(np.array(index_buffer[item]), axis=0)
    # 计算指针与读数片段的交点
    nums = len(scales)
    keep_inter = []
    keep_reading = []
    for i in range(nums - 1):
        if np.max(scales[i]) != 0 and np.max(scales[i + 1]) != 0:
            seg = (scales[i][0], scales[i][1], scales[i + 1][0],
                   scales[i + 1][1])
            inter_point = line_segment_inter(line, seg)
            if inter_point != (-1, -1):
                reading = show_reading(seg, inter_point, i)
                keep_inter.append(inter_point)
                keep_reading.append(reading)
        else:
            if np.max(scales[i]) == 0:
                print("识别模型无法识别 {} !!".format(scale_list[i]))
                sys.stdout.flush()
            if np.max(scales[i + 1]) == 0:
                print("识别模型无法识别 {} !!".format(scale_list[i + 1]))
                sys.stdout.flush()
    # 过滤交点
    # 获得指针bbox四个边的中心点
    bbox_edge_center = [(cx, l), (b, cy), (cx, r), (t, cy)]
    # 判断四个边的中点哪个不在指针读数围成的区域内，那个中点就是指针的方向
    anchor = []
    for tx, ty in bbox_edge_center:
        if not pnpoly(reading_heatmap, tx, ty):
            anchor.append((tx, ty))

    assert len(anchor) == 1, "无法获得指针的方向"

    anchor = np.array(anchor[0])
    keep_inter = np.array(keep_inter)
    dist = np.linalg.norm(anchor - keep_inter, axis=1)
    keep_index = np.argmin(dist)
    ret_reading = keep_reading[keep_index]
    return ret_reading
