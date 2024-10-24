from datetime import datetime

import numpy as np
import cv2


def culatePoint(filename:str):

    # 读取图像
    img = cv2.imread(filename)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 使用双边滤波进行平滑处理
    bilateral = cv2.bilateralFilter(gray, 10, 50, 50)

    # 使用 Canny 边缘检测
    edges = cv2.Canny(bilateral, 50, 150, apertureSize=3)

    # 使用闭运算填充可能的断裂
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (30, 30))
    closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

    # HoughCircles 参数
    minDist = 30
    param1 = 50  # 提高边缘检测的高阈值
    param2 = 30  # 累加器阈值
    minRadius = 5
    maxRadius = 100

    # 检测圆
    circles = cv2.HoughCircles(bilateral, cv2.HOUGH_GRADIENT, 1, minDist, param1=param1, param2=param2,
                               minRadius=minRadius,
                               maxRadius=maxRadius)

    count = 0
    if circles is not None:
        # 转换为整数坐标
        circles = np.round(circles[0, :]).astype("int")

        # 应用非极大值抑制
        overlapThresh = 0.5  # 重叠阈值
        circles = non_max_suppression(circles, overlapThresh)

        cout = len(circles)
        print(f"检测到的圆的数量: {len(circles)}")

        # 在图像上绘制每个圆
        for (x, y, r) in circles:
            cv2.circle(img, (x, y), r, (0, 255, 0), 2)
            cv2.circle(img, (x, y), 2, (0, 0, 255), 3)  # 标记圆心

        # 设置目标显示尺寸
        target_width = 800  # 目标宽度
        target_height = 600  # 目标高度

        # 调整图像大小
        resized_image = cv2.resize(img, (target_width, target_height), interpolation=cv2.INTER_AREA)

        now = datetime.now()
        print("当前日期和时间:", now)

        # 格式化输出
        formatted_now = now.strftime("%Y-%m-%d %H:%M:%S")
        print("格式化后的当前日期和时间:", formatted_now)
        output_path = 'img/formatted_now_'+str(count)+'.png'
        cv2.imwrite(output_path, resized_image)
        print(f"调整大小后的图像已保存到: {output_path}")
        # 显示结果图像
        # cv2.imshow('Detected Circles', resized_image)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        return cout
    else:
        print("没有检测到圆")
        return -1

def non_max_suppression(circles, overlapThresh):
    # 如果没有检测到圆，则返回空列表
    if len(circles) == 0:
        return []

    # 初始化被选中的圆
    pick = []

    # 获取每个圆的 (x, y) 坐标和半径
    x = circles[:, 0]
    y = circles[:, 1]
    r = circles[:, 2]

    # 计算每个圆的面积
    area = np.pi * r * r

    # 按照圆的半径从大到小排序
    idxs = np.argsort(r)[::-1]

    while len(idxs) > 0:
        # 当前最大的圆
        last = len(idxs) - 1
        i = idxs[last]
        pick.append(i)

        # 计算当前圆与其他圆之间的距离
        xx1 = np.maximum(x[i] - r[i], x[idxs[:last]] - r[idxs[:last]])
        yy1 = np.maximum(y[i] - r[i], y[idxs[:last]] - r[idxs[:last]])
        xx2 = np.minimum(x[i] + r[i], x[idxs[:last]] + r[idxs[:last]])
        yy2 = np.minimum(y[i] + r[i], y[idxs[:last]] + r[idxs[:last]])

        # 计算交集的宽度和高度
        w = np.maximum(0, xx2 - xx1)
        h = np.maximum(0, yy2 - yy1)

        # 计算交集的面积
        inter_area = w * h

        # 计算并集的面积
        union_area = area[i] + area[idxs[:last]] - inter_area

        # 计算 IoU (Intersection over Union)
        iou = inter_area / union_area

        # 移除重叠度大于阈值的圆
        idxs = np.delete(idxs, np.concatenate(([last], np.where(iou > overlapThresh)[0])))

    return circles[pick].astype("int")
