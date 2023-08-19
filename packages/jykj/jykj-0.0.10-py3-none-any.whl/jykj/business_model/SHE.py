import cv2
import numpy as np
from .utils import rela_to_abs, pnpoly, min_bbox


def persons_in_areas(persons_coords: list,
                     areas: list,
                     resolution: list = [],
                     h_offset: float = 0,
                     w_thresh: float = -1,
                     h_thresh: float = -1) -> bool:
    '''
    判断人是否在区域内, 支持单人坐标和多人坐标, 支持单区域和多区域, 支持过滤人检测框的宽度和高度, 支持人的位置偏移。
    坐标可以使用相对坐标或绝对坐标, 人和区域的坐标类型不一致时必须指定分辨率。使用过滤高度、宽度功能且人使用绝对坐标时须指定分辨率。

    参数:
        persons_coords (list): 单人[cx, cy, w, h], 多人[[cx1, cy1, w1, h1],[cx2, cy2, w2, h2],...]

        area (list): 单区域[[x1, y1], [x2, y2], [x3, y3]], 多区域[[[x1, y1], [x2, y2], [x3, y3]], [[x4, y4], [x5, y5], [x6, y6], [x7, 7]], ...]

        resolution (list): 视频分辨率, [width, height] 

        h_offset (float): 人的位置纵向偏移量, -0.5 <= h_thresh <= 0.5

        w_thresh (float): 检测框宽度过滤阈值, 0 <= w_thresh <= 1

        h_thresh (flost): 检测框高度过滤阈值, 0 <= h_thresh <= 1

    返回:
        True: 有人在区域内

        False: 无人在区域内
    '''

    # 全部转换为多人和多区域
    assert np.array(persons_coords).ndim in [1, 2]
    assert np.array(areas).ndim in [2, 3]
    if np.array(persons_coords).ndim == 1:
        persons_coords = [persons_coords]
    if np.array(areas).ndim == 2:
        areas = [areas]

    assert -0.5 <= h_offset <= 0.5

    # 判断是相对坐标还是绝对坐标(不严格)
    if (np.array(persons_coords).dtype == float) and (np.array(persons_coords) <= 1).all():
        abs_person = False
    else:
        abs_person = True

    if (np.array(areas[0]).dtype == float) and (np.array(areas[0]) <= 1).all():
        abs_area = False
    else:
        abs_area = True

    if abs_person != abs_area and not resolution:
        raise ValueError("未指定视频分辨率")

    # 如果坐标类型不一致就全部转为绝对坐标
    if abs_person == True and abs_area == False:
        new_areas = []
        for area in areas:
            new_areas.append(rela_to_abs(area, resolution))
        areas = new_areas
    elif abs_person == False and abs_area == True:
        persons_coords = rela_to_abs(persons_coords, resolution)

    # 宽度过滤
    if w_thresh != -1:
        assert 0 < w_thresh <= 1
        if abs_person:
            if not resolution:
                raise ValueError("未指定视频分辨率")
            else:
                w_thresh = int(w_thresh * resolution[0])
        else:
            if abs_area:
                w_thresh = int(w_thresh * resolution[0])
        persons_coords = [p for p in persons_coords if p[2] <= w_thresh]

    # 高度过滤
    if h_thresh != -1:
        assert 0 < h_thresh <= 1
        if abs_person:
            if not resolution:
                raise ValueError("未指定视频分辨率")
            else:
                h_thresh = int(h_thresh * resolution[1])
        else:
            if abs_area:
                h_thresh = int(h_thresh * resolution[1])
        persons_coords = [p for p in persons_coords if p[3] <= h_thresh]

    for p in persons_coords:
        cx = p[0]
        cy = p[1] + int(h_offset * p[3])
        for area in areas:
            if pnpoly(area, cx, cy):
                return True
    return False


def move_and_cover(picture_previous: np.ndarray, picture_now: np.ndarray,
                   shutter_th: float, move_th: float) -> int:
    """
    判断摄像头是否遮挡或移动。
    
    参数：
        picture_previous (np.ndarray): 初始帧，使用opencv读取图像后的ndarray格式；
        picture_now (np.ndarray): 当前帧，使用opencv读取图像后的ndarray格式；
        shutter_th (float): 遮挡阈值，为0-1之间的小数，可默认0.5；
        move_th (float): 移动阈值，为0-1之间的小数，可默认0.3；
    返回：
        result (int): 0为正常；1为遮挡；2为移动
    """
    def calculate(image1: np.ndarray, image2: np.ndarray) -> float:
        """
        计算图像单通道的直方图的相似值。
        
        参数：
            image1 (np.ndarray): 使用opencv读取图像后的ndarray格式；
            image2 (np.ndarray): 使用opencv读取图像后的ndarray格式；
        返回：
            degree (float): 两张图片单通道的相似度
        """

        hist1 = cv2.calcHist([image1], [0], None, [256], [0.0, 255.0])
        hist2 = cv2.calcHist([image2], [0], None, [256], [0.0, 255.0])
        degree = 0
        for i in range(len(hist1)):
            if hist1[i] != hist2[i]:
                degree = degree + \
                    (1 - abs(hist1[i] - hist2[i]) / max(hist1[i], hist2[i]))
            else:
                degree = degree + 1
        degree = degree / len(hist1)
        return degree

    def classify_hist_with_split(image1: np.ndarray, image2: np.ndarray,
                                 size: tuple) -> float:
        """
        将图像resize后，分离为RGB三个通道，再计算每个通道的相似值。
        
        参数：
            image1 (np.ndarray): 使用opencv读取图像后的ndarray格式；
            image2 (np.ndarray): 使用opencv读取图像后的ndarray格式；
            size (tuple): resize后的宽高，默认（256，256）
        返回：
            sub_data  (float): 两张图片RGB每个通道的直方图相似度的平均
        """

        image1 = cv2.resize(image1, size)
        image2 = cv2.resize(image2, size)
        sub_image1 = cv2.split(image1)
        sub_image2 = cv2.split(image2)
        sub_data = 0
        for im1, im2 in zip(sub_image1, sub_image2):
            sub_data += calculate(im1, im2)
        sub_data = sub_data / 3
        return sub_data

    corner = 150
    size = picture_previous.shape
    corner_list = [[0, corner, 0, corner],\
                [0, corner, size[0] - corner, size[0]],\
                [size[1] - corner, size[1], 0, corner],\
                [size[1] - corner, size[1], size[0] - corner, size[0]]]
    cropImg_previous = list()
    for i in range(0, 4):
        cropImg_previous.append(
            picture_previous[corner_list[i][0]:corner_list[i][1],
                             corner_list[i][2]:corner_list[i][3]])

    cropImg_current = list()
    for i in range(0, 4):
        cropImg_current.append(
            picture_now[corner_list[i][0]:corner_list[i][1],
                        corner_list[i][2]:corner_list[i][3]])

    es = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 4))
    differ_count = []
    for i in range(0, 4):
        n4 = classify_hist_with_split(cropImg_previous[i], cropImg_current[i],
                                      (256, 256))
        differ_count.append(float(n4))

    blurred = cv2.GaussianBlur(picture_now, (3, 3), 0)
    img_gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
    edge_all = cv2.Canny(img_gray, 0, 20)
    edge_all_dilate = cv2.dilate(edge_all, es, iterations=2)
    if int(np.sum(edge_all_dilate == 255)) / (size[0] * size[1]) < shutter_th:
        result = 1
        print("遮挡")
    elif np.mean(differ_count) < move_th:
        result = 2
        print("移动")
    else:
        result = 0
        print("正常")

    return result


def sleeping_monitor(kpts: np.array, kpts_score: np.array, area: list,
                     resolution: tuple) -> tuple:
    """
    根据人体骨骼关键点的坐标、置信度，判断人体是否在睡觉

    参数：
        kpts (np.array): 人体骨骼关键点的坐标
        kpts_score (np.array): 人体骨骼关键点的置信度
        area (2d list): 工作台区域的坐标点集合， [[x1, y1], [x2, y2], ..., [xn, yn]]
        resolution (tuple): 视频的分辨率

    返回：
        is_sleeping (bool): 是否在睡觉
        ave_angle_y (float): 视线与图像坐标系y正半轴的夹角
        ave_gaze_score (float): 视线的置信度
    """

    # 保留关键点的最低置信度
    use_kpt_threshold = 0.05
    # 关键点在列表中的位置
    kpts_map = {
        "nose": 0,
        "leye": 1,
        "reye": 2,
        "lear": 3,
        "rear": 4,
        "lshoulder": 5,
        "rshoulder": 6,
        "lelbow": 7,
        "relbow": 8,
        "lwrist": 9,
        "rwrist": 10,
        "lhip": 11,
        "rhip": 12,
        "lknee": 13,
        "rknee": 14,
        "lankle": 15,
        "rankle": 16
    }
    # 姿态角度的阈值
    gaze_angle = 30  #视线与y正半轴的夹角
    spine_angle = 30  #脊柱与x正半轴的夹角
    look_up_angle_gaze = 145  # 仰睡视线角度的阈值
    look_up_angle_spine = 120  # 仰睡脊柱角度的阈值
    big_leg_angle_diff = 25  # 大腿方向向量与x轴正半轴的夹角，小于这个阈值判定为站立
    pose_area_ratio = 0.5  # 包含pose的矩形框占图像的百分比

    # initial
    frame_w, frame_h = resolution
    is_sleeping = False
    # 过滤掉score小于use_kpt_threshold(0.05)的keypoints
    kpts_index = np.where(kpts_score > use_kpt_threshold)[0]
    kpts_keep = np.zeros((17, 2), dtype=float)
    kpts_keep[kpts_index] = kpts[kpts_index]
    # 取出关键点
    lear_kpt, leye_kpt, rear_kpt, reye_kpt = kpts_keep[
        kpts_map["lear"]], kpts_keep[kpts_map["leye"]], kpts_keep[
            kpts_map["rear"]], kpts_keep[kpts_map["reye"]]
    ls_kpt, rs_kpt, lhip_kpt, rhip_kpt = kpts_keep[
        kpts_map["lshoulder"]], kpts_keep[kpts_map["rshoulder"]], kpts_keep[
            kpts_map["lhip"]], kpts_keep[kpts_map["rhip"]]
    lk_kpt, rk_kpt, la_kpt, ra_kpt = kpts_keep[kpts_map["lknee"]], kpts_keep[
        kpts_map["rknee"]], kpts_keep[kpts_map["lankle"]], kpts_keep[
            kpts_map["rankle"]]
    nose_kpt, lelbow_kpt, relbow_kpt = kpts_keep[kpts_map["nose"]], kpts_keep[
        kpts_map["lelbow"]], kpts_keep[kpts_map["relbow"]]
    lw_kpt, rw_kpt = kpts_keep[kpts_map["lwrist"]], kpts_keep[
        kpts_map["rwrist"]]
    ch_kpt = np.array([0, 0])
    if np.max(kpts_keep[:5, :]) != 0:
        ch_kpt = np.sum(kpts_keep[:5, :],
                        axis=0) / np.sum(kpts_score[:5] > use_kpt_threshold)
    # 计算同侧耳朵到眼睛方向向量与y轴的夹角
    y_axis = np.array([0, 1])
    count, l_angle_y, r_angle_y, ave_angle_y, l_gaze_score, r_gaze_score, ave_gaze_score = 0, 0, 0, 90, 0, 0, 0
    if max(lear_kpt) != 0 and max(leye_kpt) != 0:
        lear_index, leye_index = 3, 1
        l_ear2eye = leye_kpt - lear_kpt
        cost = np.dot(l_ear2eye, y_axis) / (np.linalg.norm(l_ear2eye) + 1e-6)
        l_angle_y = np.arccos(cost) * 180 / np.pi
        # 计算左侧视线的置信度
        l_gaze_score = (kpts_score[lear_index] + kpts_score[leye_index]) / 2
        count += 1
    if max(rear_kpt) != 0 and max(reye_kpt) != 0:
        rear_index, reye_index = 4, 2
        r_ear2eye = reye_kpt - rear_kpt
        cost = np.dot(r_ear2eye, y_axis) / (np.linalg.norm(r_ear2eye) + 1e-6)
        r_angle_y = np.arccos(cost) * 180 / np.pi
        # 计算右侧视线的置信度
        r_gaze_score = (kpts_score[rear_index] + kpts_score[reye_index]) / 2
        count += 1
    if count != 0:
        ave_angle_y = (l_angle_y + r_angle_y) / count
        ave_gaze_score = (l_gaze_score + r_gaze_score) / count
        ave_gaze_score = ave_gaze_score[0]
    # 计算脊柱方向向量与x轴的夹角
    x_axis = np.array([1, 0])
    count, l_angle_x, r_angle_x, ave_angle_x = 0, 0, 0, 90
    if max(ls_kpt) != 0 and max(lhip_kpt) != 0:
        l_hip2s = ls_kpt - lhip_kpt
        cost = np.dot(l_hip2s, x_axis) / (np.linalg.norm(l_hip2s) + 1e-6)
        l_angle_x = np.arccos(cost) * 180 / np.pi
        count += 1
    if max(rs_kpt) != 0 and max(rhip_kpt) != 0:
        r_hip2s = rs_kpt - rhip_kpt
        cost = np.dot(r_hip2s, x_axis) / (np.linalg.norm(r_hip2s) + 1e-6)
        r_angle_x = np.arccos(cost) * 180 / np.pi
        count += 1
    if count != 0:
        ave_angle_x = (l_angle_x + r_angle_x) / count
    # 计算大腿(膝臀向量)与x正半轴的夹角，从而判断人体是否直立
    count, l_angle_leg, r_angle_leg, ave_angle_leg = 0, 0, 0, 0
    if max(lk_kpt) != 0 and max(lhip_kpt) != 0:
        l_k2hip = lhip_kpt - lk_kpt
        cost = np.dot(l_k2hip, x_axis) / (np.linalg.norm(l_k2hip) + 1e-6)
        l_angle_leg = np.arccos(cost) * 180 / np.pi
        count += 1
    if max(rk_kpt) != 0 and max(rhip_kpt) != 0:
        r_k2hip = rhip_kpt - rk_kpt
        cost = np.dot(r_k2hip, x_axis) / (np.linalg.norm(r_k2hip) + 1e-6)
        r_angle_leg = np.arccos(cost) * 180 / np.pi
        count += 1
    if count != 0:
        ave_angle_leg = (l_angle_leg + r_angle_leg) / count
    # 判断头部的中心点是否在工作台上
    in_area = pnpoly(area, ch_kpt[0], ch_kpt[1])
    # 综合夹角和区域分析，得出是否是睡姿的结果
    # 1.1 如果低头，脊柱的角度低于阈值，而且面部中心点在案台区域的话，判定为睡觉。
    if (abs(ave_angle_y) < gaze_angle and abs(ave_angle_x) < spine_angle
            and in_area):
        is_sleeping = True
    # 1.2 如果脊柱倾斜，视线的置信度低于0.5（很有可能视线不可见是预估的），而且面部中心点在案台区域的话，判定为睡觉。
    if (abs(ave_angle_x) < spine_angle and ave_gaze_score < 0.4 and in_area):
        is_sleeping = True
    # 2.如果头往后仰卧的角度太大而且脊柱的角度也要大于阈值，判定为睡觉
    lhip_id, rhip_id = 11, 12
    ave_hip_score = (kpts_score[lhip_id] + kpts_score[rhip_id]) / 2
    # 主要用来排除臀部不可见的那种误识别现象
    ave_hip_thresh = 0.16
    if abs(ave_angle_y) > look_up_angle_gaze and (
            abs(ave_angle_x) > look_up_angle_spine
            and ave_hip_score[0] > ave_hip_thresh):
        is_sleeping = True
    # 3.如果站立的话，肯定没睡觉
    diff = np.abs(ave_angle_leg - 90)
    if diff < big_leg_angle_diff:
        is_sleeping = False
    # 4.如果人体挨着镜头太近的话应该不是在睡觉
    min_x, min_y, max_x, max_y = min_bbox(kpts[kpts_index])
    pose_area = (max_x - min_x) * (max_y - min_y)
    pose_area_ratio = pose_area / (frame_w * frame_h)
    if pose_area_ratio > pose_area_ratio:
        is_sleeping = False
    # 5.如果很确信视线正对着屏幕的话，不管脊椎的角度再怎么弯曲都不管用
    if np.abs(ave_angle_y - 90) < 25 and ave_gaze_score > 0.4:
        is_sleeping = False
    # 6. 如果脊柱的角度大于35度，且视线的角度小于30度的时候，认为人们在案台上写字（排除误识别！！）
    if (abs(ave_angle_y) < 30 and abs(ave_angle_x) > 40):
        is_sleeping = False
    # 7. 在前面6个逻辑的基础上，再加强逻辑限定人在正睡的情况(这种情况没有考虑视线的角度，因为有不准的情况，所以就采用了绝对距离的判断准则)
    dist_ear2eye = np.linalg.norm(rear_kpt - reye_kpt)
    dist_rw2re = np.linalg.norm(rw_kpt - reye_kpt)
    dist_lw2re = np.linalg.norm(lw_kpt - reye_kpt)
    if dist_rw2re < dist_ear2eye and dist_lw2re < dist_ear2eye and abs(
            ave_angle_x) < 50 and in_area:
        is_sleeping = True
    # 8. 在前边6个逻辑的基础上，再加强逻辑限定人在左睡的情况（这里边视线和脊椎与坐标轴的夹角就不要动了）
    l_arm_angle, l_arm_angle_diff = 0, 20
    if max(ls_kpt) != 0 and max(lelbow_kpt) != 0 and max(lw_kpt) != 0:
        l_elbow2s = ls_kpt - lelbow_kpt
        l_elbow2w = lw_kpt - lelbow_kpt
        cost = np.dot(l_elbow2s, l_elbow2w) / (
            (np.linalg.norm(l_elbow2s) * np.linalg.norm(l_elbow2w)) + 1e-6)
        l_arm_angle = np.arccos(cost) * 180 / np.pi
        dist_lelbow2reye = np.linalg.norm(lelbow_kpt - reye_kpt)
        l_elbow_in_area = pnpoly(area, lelbow_kpt[0], lelbow_kpt[1])
        l_wrist_in_area = pnpoly(area, lw_kpt[0], lw_kpt[1])
        if abs(
                l_arm_angle - 180
        ) < l_arm_angle_diff and dist_lelbow2reye < dist_ear2eye and l_elbow_in_area and l_wrist_in_area and abs(
                ave_angle_x) < 55 and abs(ave_angle_y) < 50 and in_area:
            is_sleeping = True
    # 9. 在前边6个逻辑的基础上， 再加强逻辑限定人在左侧手臂弯曲的情况
    l_arm_length = np.linalg.norm(ls_kpt -
                                  lelbow_kpt) + np.linalg.norm(lelbow_kpt -
                                                               lw_kpt)
    r_arm_length = np.linalg.norm(rs_kpt -
                                  relbow_kpt) + np.linalg.norm(relbow_kpt -
                                                               rw_kpt)
    l_s_x, r_s_x = ls_kpt[0], rs_kpt[0]
    delta_x = (10 / 1280) * frame_w
    if abs(ave_angle_x) < 50 and abs(ave_angle_y) < 50 and (
            l_s_x - r_s_x) > delta_x and l_arm_length < (
                r_arm_length /
                2) and l_elbow_in_area and l_wrist_in_area and in_area:
        is_sleeping = True
    return is_sleeping, ave_angle_y, ave_gaze_score
