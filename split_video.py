import os
import subprocess

def split_video_by_duration_ffmpeg(video_path, output_dir, segment_duration=30):
    os.makedirs(output_dir, exist_ok=True)
    # 获取视频总时长
    import cv2
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / fps
    cap.release()

    segment_index = 1
    start = 0
    while start < duration:
        end = min(start + segment_duration, duration)
        output_path = os.path.join(output_dir, f"segment_{segment_index:03d}.mp4")
        cmd = [
            "ffmpeg",
            "-y",
            "-ss", str(start),
            "-to", str(end),
            "-i", video_path,
            "-c", "copy",  # 直接拷贝音视频流，不重新编码
            output_path
        ]
        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        segment_index += 1
        start += segment_duration
    print(f"视频分割完成，共生成 {segment_index-1} 个片段")

def split_all_videos_in_dir(input_dir, output_dir, segment_duration=30):
    """
    批量分割 input_dir 下所有视频文件
    """
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.mp4', '.mov', '.avi', '.mkv')):
            video_path = os.path.join(input_dir, filename)
            sub_output_dir = os.path.join(output_dir, os.path.splitext(filename)[0])
            split_video_by_duration_ffmpeg(video_path, sub_output_dir, segment_duration)

# 示例调用
if __name__ == "__main__":
    input_dir = "/Users/elvis/workspace/code/ai-cutting/source"  # 替换为你的输入视频路径
    output_dir = "/Users/elvis/workspace/code/ai-cutting/part_of_video/"  # 输出目录

    split_all_videos_in_dir (input_dir, output_dir, segment_duration=30)#分割原始视频，分片为30秒内的片段，让ai理解和剪辑更容易

