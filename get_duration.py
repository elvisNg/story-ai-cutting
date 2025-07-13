import cv2

def get_video_duration_func(video_path):
    """ 使用 OpenCV 获取视频时长 """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError("无法打开视频文件。请检查路径和文件格式。")
    
    fps = cap.get(cv2.CAP_PROP_FPS)  # 获取帧率
    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)  # 获取总帧数
    
    # 打印 fps 和 frame_count，检查是否为合理值
    print(f"FPS: {fps}, Frame Count: {frame_count}")
    
    if fps == 0 or frame_count == 0:
        raise ValueError("无法获取帧率或帧数，视频文件可能损坏或格式不受支持。")
    
    duration = frame_count / fps  # 计算时长
    cap.release()
    return duration

def main():
    #video_path = '/Users/elvis/workspace/code/ai-cutting/source/202011/118_1123/MVI_0665.mp4'  # 请替换为你的视频文件路径
    video_path = '/Users/elvis/workspace/code/ai-cutting/source/202011/119_1124/MVI_0675.MP4'  # 请替换为你的视频文件路径
    try:
        duration = get_video_duration_func(video_path)
        print(f"视频时长: {duration} 秒")
    except Exception as e:
        print(f"计算视频时长时发生错误: {e}")

if __name__ == "__main__":
    main()
