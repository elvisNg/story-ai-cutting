import json
import os
import subprocess

def parse_time_range(timestamp):
    """将 '00:06-00:09' 转为 (6, 9) 秒"""
    start_str, end_str = timestamp.split('-')
    def to_sec(t):
        m, s = map(int, t.split(':'))
        return m * 60 + s
    return to_sec(start_str), to_sec(end_str)

def load_json(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def extract_and_concat(json_data, video_dir, output_path):
    temp_files = []
    for idx, item in enumerate(json_data):
        segment = item['segment']
        timestamp = item['timestamp']
        video_file = os.path.join(video_dir, f"{segment}.mp4")
        if not os.path.exists(video_file):
            print(f"视频文件不存在: {video_file}")
            continue
        start, end = parse_time_range(timestamp)
        temp_file = f"temp_clip_{idx}.mp4"
        # cmd = [
        #     "ffmpeg",
        #     "-y",
        #     "-i", video_file,
        #     "-ss", str(start),
        #     "-to", str(end),
        #     "-c:v", "libx264",
        #     "-c:a", "aac",
        #     temp_file
        # ]
        cmd = [
            "ffmpeg",
            "-y",
            "-ss", str(start),
            "-to", str(end),
            "-i", video_file,
            "-map", "0",
            "-c:v", "libx264",
            "-c:a", "aac",
            "-strict", "-2",
            temp_file
        ]
        print(" ".join(cmd))
        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        temp_files.append(temp_file)

    # 生成 concat 文件列表
    concat_list = "concat_list.txt"
    with open(concat_list, "w") as f:
        for temp in temp_files:
            f.write(f"file '{os.path.abspath(temp)}'\n")

    # 合并所有片段
    concat_cmd = [
        "ffmpeg",
        "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", concat_list,
        "-c", "copy",
        output_path
    ]
    print(" ".join(concat_cmd))
    subprocess.run(concat_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # 清理临时文件
    for temp in temp_files:
        os.remove(temp)
    os.remove(concat_list)

def main():
    json_path = "./data/combine_video.json"  # 你的json文件路径
    video_dir = "./video_part"        # 视频片段目录
    output_path = "result.mp4"        # 输出视频路径

    json_data = load_json(json_path)
    extract_and_concat(json_data, video_dir, output_path)

if __name__ == '__main__':
    main()