# -*- coding: utf-8 -*-
"""
Created on Mon May 17 10:24:03 2021

@author: lzy
"""

import cv2
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import spline 
import math as mt

# 获得opencv的版本
(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')

if __name__ == '__main__':

    # 建立跟踪器，选择跟踪器的类型

    tracker_types = ['BOOSTING', 'MIL','KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']
    tracker_type = tracker_types[2]

    if int(minor_ver) < 3:
        tracker = cv2.Tracker_create(tracker_type)
    else:
        if tracker_type == 'BOOSTING':
            tracker = cv2.TrackerBoosting_create()
        if tracker_type == 'MIL':
            tracker = cv2.TrackerMIL_create()
        if tracker_type == 'KCF':
            tracker = cv2.TrackerKCF_create()
        if tracker_type == 'TLD':
            tracker = cv2.TrackerTLD_create()
        if tracker_type == 'MEDIANFLOW':
            tracker = cv2.TrackerMedianFlow_create()
        if tracker_type == 'GOTURN':
            tracker = cv2.TrackerGOTURN_create()
        if tracker_type == 'MOSSE':
            tracker = cv2.TrackerMOSSE_create()
        if tracker_type == "CSRT":
            tracker = cv2.TrackerCSRT_create()

    # 读取视频
    name = "kou_trans"
#    video = cv2.VideoCapture("./kou_trans.mp4")
    video = cv2.VideoCapture(name + ".mp4")
    size = (int(video.get(cv2.CAP_PROP_FRAME_WIDTH)), int(video.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    fps = video.get(cv2.CAP_PROP_FPS)

    
    videoWriter = cv2.VideoWriter(name + "_track.mp4", cv2.VideoWriter_fourcc('M','P','E','G'), fps, size)
#    videoWriter = cv2.VideoWriter(name + "_track.avi", cv2.VideoWriter_fourcc('X','V','I','D'), fps, size)
    if not video.isOpened():
        print("Could not open video")
        sys.exit()

    # 读取视频的第一帧
    ok, frame = video.read()
    if not ok:
        print ('Cannot read video file')
        sys.exit()

    # 定义初始边界框
    bbox = (287, 23, 86, 320)

    # Uncomment the line below to select a different bounding box
    # 选择不同的边界框
    bbox = cv2.selectROI(frame, False)

    # Initialize tracker with first frame and bounding box
    # 使用视频的第一帧和边界框初始化跟踪器
    ok = tracker.init(frame, bbox)

    center_vec = []
    while True:
        # Read a new frame
        ok, frame = video.read()
        if not ok:
            break
        
        # Start timer 记录开始时间
        timer = cv2.getTickCount()

        # Update tracker 更新检测器
        ok, bbox = tracker.update(frame)

        # Calculate Frames per second (FPS) 计算FPS
#        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);

        # Draw bounding box 绘制边界框
        if ok:
            # Tracking success 跟踪成功
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
            
            #画点
            center = (int(bbox[0] + 0.5 * bbox[2]), int(bbox[1] + 0.5 * bbox[3])) 
            center_vec.append(center)
            for p in center_vec:
                cv2.circle(frame, p, 1, (255, 0, 0), -1)
                
            
            videoWriter.write(frame)
#            画线
#            for i in len(center_vec):
#                if(i > 1):
#                    cv2.line(frame, center_vec[i - 1], center_vec[i], (255,0,0), 3, 1)
            
        else :  # 跟踪失败
            # Tracking failure
            cv2.putText(frame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)

        # Display result 显示跟踪结果
        cv2.imshow("Tracking", frame)

        # Exit if ESC pressed 按取消键退出
        k = cv2.waitKey(1) & 0xff
        if k == 27 : break
    
    video.release()
    cv2.destroyAllWindows()