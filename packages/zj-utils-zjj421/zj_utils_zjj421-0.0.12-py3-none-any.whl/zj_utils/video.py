#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: zhangjian
# date: 2023/7/13
import _queue
import logging
import os
import time
from queue import Queue
from threading import Thread

import cv2

from .files import makedirs
from .helper import get_time_str, setup_logger
from .timer import MyTimer, FPSRealTime

__all__ = ['FrameInfo', 'VideoReader', 'read_video_demo', 'record_video_demo']


class FrameInfo(object):
    def __init__(self, image, frame_idx=None, frame_elapsed_ms=None):
        self.image = image
        self.frame_idx = frame_idx
        self.frame_elapsed_ms = frame_elapsed_ms
        self.process_ret = None

    def get_image(self):
        return self.image

    def set_image(self, image):
        self.image = image

    def get_frame_idx(self):
        return self.frame_idx

    def get_frame_elapsed_s(self):
        return self.frame_elapsed_ms / 1000

    def get_frame_elapsed_ms(self):
        return self.frame_elapsed_ms

    def set_ret(self, result):
        self.process_ret = result

    def get_ret(self):
        return self.process_ret


class VideoReader(object):
    def __init__(self, video_input_param, auto_drop_frame=True, skip_frames=0, reload_video=True):
        self.video_input_param = video_input_param
        self.stopped = False
        self.skip_frames = skip_frames + 1
        self.auto_drop_frame = auto_drop_frame
        self.reload_video = reload_video
        self.mylogger = logging.getLogger('demo')
        self.mylogger.info('VideoStreamReader init done.')

    def load_camera(self, ):
        cap = cv2.VideoCapture(self.video_input_param)
        self.mylogger.info(
            f'Video is {"opened." if cap.isOpened() else "not opened."}')
        self.cap_fps = cap.get(5)
        self.cap_height, self.cap_width = cap.get(cv2.CAP_PROP_FRAME_HEIGHT), cap.get(
            cv2.CAP_PROP_FRAME_WIDTH)
        self.mylogger.info(
            f'Video stream FPS: {self.cap_fps}\tshape: ({self.cap_height}, {self.cap_width})')
        self.mylogger.info(
            f'Load video stream from {self.video_input_param} done.')
        return cap

    def run(self, queue_i):
        self.mylogger.info('VideoStreamReader running ...')
        cap = self.load_camera()
        frame_idx = 0
        mytimer = MyTimer()

        while not self.stopped:
            mytimer.restart()
            ret = cap.grab()
            frame_idx += 1
            if not ret:
                self.mylogger.info(
                    f'---VideoStreamReader--- Grab NONE FRAME, Cap is opened: {cap.isOpened()}'
                )
                if self.reload_video:
                    cap = self.load_camera()
            if self.auto_drop_frame:
                if queue_i.full():
                    continue
            else:
                if frame_idx % self.skip_frames != 0:
                    continue
            ret, image = cap.retrieve()
            self.mylogger.debug(
                f'---VideoStreamReader--- cap read elapsed: {mytimer.elapsed():.2f}ms'
            )
            if ret:
                frame = FrameInfo(image=image,
                                  frame_idx=frame_idx,
                                  frame_elapsed_ms=cap.get(
                                      cv2.CAP_PROP_POS_MSEC))
                queue_i.put(frame)
                self.mylogger.debug(
                    f'---VideoStreamReader--- Put Frame-{frame_idx} to the list ---- len:{queue_i.qsize()} '
                    f'elapsed: {mytimer.elapsed():.2f}ms')
            else:
                self.mylogger.info(
                    f'---VideoStreamReader--- READ NONE FRAME, Cap is opened: {cap.isOpened()}'
                )
                if self.reload_video:
                    cap = self.load_camera()

        cap.release()
        self.mylogger.info('Camera is closed.')

    def stop(self):
        self.stopped = True


class VideoRecoder(object):
    def __init__(self, record_save_root, imgshow=False, write=True, write_interval=(True, 5)):
        self.record_save_root = record_save_root
        self.imgshow = imgshow
        self.write = write
        self.write_interval = write_interval
        self.mylogger = logging.getLogger('demo')
        self.mylogger.info('VideoRecoder init done.')

    def reset_cap_writer(self, fps, width, height):
        time_str = get_time_str()
        video_save_path = os.path.join(self.record_save_root, time_str[:10], time_str + '.avi')
        makedirs(os.path.dirname(video_save_path))

        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        cap_writer = cv2.VideoWriter(video_save_path, fourcc, fps, (int(width), int(height)))
        self.mylogger.info('CapWriter reset.')
        return cap_writer

    def run(self, queue_i, save_fps, save_width, save_height):
        run_time_total = -1
        mytimer = MyTimer()
        mytimer2 = MyTimer()
        if self.write:
            cap_writer = self.reset_cap_writer(save_fps, save_width, save_height)
        if self.imgshow:
            cv2.namedWindow("Demo", 0)  # 0可调大小，注意：窗口名必须imshow里面的一窗口名一直
            cv2.resizeWindow("Demo", save_width, save_height)  # 设置宽和高
        while True:
            if self.write and self.write_interval[0] and \
                    mytimer2.elapsed(restart=False, unit='min') >= self.write_interval[1]:
                mytimer2.restart()
                cap_writer.release()
                self.reset_cap_writer(save_fps, save_width, save_height)
            mytimer.restart()
            try:
                frame = queue_i.get()
                frame_idx = frame.get_frame_idx()
                image_bgr = frame.get_image()
                image_bgr = cv2.resize(image_bgr, (int(save_width), int(save_height)))
            except:
                import traceback
                print(traceback.format_exc())
                frame = None
            if frame is not None:
                if self.write:
                    cap_writer.write(image_bgr)
                if self.imgshow:
                    if cv2.waitKey(1) & 0xFF == ord("q"):
                        break
                    cv2.imshow('Demo', image_bgr)

                self.mylogger.debug(
                    f'---VideoRecoder--- Get Frame-{frame_idx} *** last elapsed: {run_time_total:.1f}ms')
            else:
                self.mylogger.warning(
                    f'---VideoRecoder--- read image timeout, break.')
                break
            run_time_total = mytimer.elapsed(unit='ms')
        if self.write:
            cap_writer.release()
            self.mylogger.info('CapWriter is released.')
        if self.imgshow:
            cv2.destroyAllWindows()
            cv2.setMouseCallback('Demo', onMouse)


def onMouse(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f'({x}, {y})')


def show_video(queue_i, video_name="Video", window_size=(540, 960)):
    cv2.namedWindow(video_name, 0)  # 0可调大小，注意：窗口名必须imshow里面的一窗口>名一直
    cv2.resizeWindow(video_name, window_size[1], window_size[0])  # 设置宽和高
    fps_obj = FPSRealTime(buffer_len=250)
    while True:
        try:
            frame = queue_i.get(timeout=5)
        except _queue.Empty:
            print(f'no frame, exit.')
            exit()
        image = frame.get_image()
        h, w = image.shape[:2]
        position = (int(0.02 * w), int(0.02 * h))
        fps = fps_obj.get_fps(number=1)
        cv2.putText(image, f'FPS: {fps}', position, cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 4)
        cv2.imshow(video_name, image)
        cv2.setMouseCallback(video_name, onMouse)
        # Process Key (ESC: end) #################################################
        # key = cv2.waitKey(10)
        # if key == 27:  # ESC
        #     break
        if cv2.waitKey(10) & 0xFF == ord('q'):
            print(f'user exit.')
            break


def read_video_demo(video_url):
    timer_str = get_time_str()
    log_root = f'logs/{timer_str[:10]}'
    setup_logger('demo', log_root=log_root, log_file_save_basename=f'{timer_str}.log', level='INFO', screen=True,
                 tofile=False, msecs=True)
    video_reader = VideoReader(video_url)
    queue_i = Queue(maxsize=1)
    video_reader_worker = Thread(target=video_reader.run, kwargs={"queue_i": queue_i}, daemon=True)
    video_reader_worker.start()
    show_video(queue_i)


def record_video_demo(video_url, record_save_root, save_fps=None, save_width=None, save_height=None, imgshow=False,
                      write=True,
                      write_interval=(True, 5)):
    timer_str = get_time_str()
    log_root = f'logs/{timer_str[:10]}'
    setup_logger('demo', log_root=log_root, log_file_save_basename=f'{timer_str}.log', level='INFO', screen=True,
                 tofile=False, msecs=True)
    video_reader = VideoReader(video_url)
    queue_i = Queue(maxsize=1)
    video_reader_worker = Thread(target=video_reader.run, kwargs={"queue_i": queue_i}, daemon=True)
    video_reader_worker.start()
    time.sleep(2)
    if save_fps is None or save_width is None or save_height is None:
        save_fps = video_reader.cap_fps
        save_width = video_reader.cap_width
        save_height = video_reader.cap_height

    video_recorder = VideoRecoder(record_save_root, imgshow=imgshow, write=write, write_interval=write_interval)
    video_recorder_worker = Thread(target=video_recorder.run,
                                   kwargs={"queue_i": queue_i, "save_fps": save_fps, "save_width": save_width,
                                           "save_height": save_height}, daemon=True)
    video_recorder_worker.start()

    video_reader_worker.join()
    video_recorder_worker.join()


def main():
    pass


if __name__ == '__main__':
    main()
