from reformat_context import parse_segments
from split_video import split_all_videos_in_dir
from video_cut import video_cut_func
from video_understand import video_understand_func
from get_duration import get_video_duration_func
from context_create import ctx_creator
from relocate import extract_uuid_list, load_json_data, build_uuid_map, find_clips_by_uuid
from combine_video import extract_and_concat
import os
import json

if __name__ == '__main__':

    input_dir = "/Users/elvis/workspace/code/ai-cutting/source/"  # 替换为你的输入视频路径
    output_dir = "/Users/elvis/workspace/code/ai-cutting/video_part/"  # 输出目录
    operation_dir = "/Users/elvis/workspace/code/ai-cutting/video_part/source/"  # 输出目录

    split_all_videos_in_dir (input_dir, output_dir, segment_duration=30)#分割原始视频，分片为30秒内的片段，AI理解语义效率更高

    # 创建数据目录和理解结果文件
    data_dir = "./output_data"
    os.makedirs(data_dir, exist_ok=True)
    understand_json_path = os.path.join(data_dir, "understand.json")
    reformat_data_path = os.path.join(data_dir, "reformat_data.json")
    storty_path = os.path.join(data_dir, "story.txt")
    combine_video_json_path = os.path.join(data_dir, "combine_video.json")
    result_path = os.path.join(data_dir, "result.mp4")
    res_list = []
   # 遍历所有子目录和文件，找到所有mp4文件
    for root, dirs, files in os.walk(output_dir):
        for filename in files:
            if filename.lower().endswith(('.mp4', '.mov', '.avi', '.mkv')):
                video_path = os.path.join(root, filename)
                duration = get_video_duration_func(video_path)
                log_msg = f"理解视频内容 starting for video: {video_path} with duration: {duration} seconds"
                print(log_msg)
                try:
                    res = video_understand_func(video_path, duration)
                    print(f"视频理解结果: {res}")
                    res_list.append({
                        "log": log_msg,
                        "result": res
                    })
                    # 每次追加后写入，保证并发和时序性
                    with open(understand_json_path, 'w', encoding='utf-8') as f:
                        json.dump(res_list, f, ensure_ascii=False, indent=2)
                except Exception as e:
                    print(f"理解视频内容时发生错误: {e}")

    # 读取understand.json内容作为parse_segments的入参
    with open(understand_json_path, 'r', encoding='utf-8') as f:
        json_list = json.load(f)
    #整理格式
    reformat_data, uuid_map = parse_segments(json_list)

    # 写入到 ./data/reformat_data.json
    with open(reformat_data_path, 'w', encoding='utf-8') as f:
        f.write(reformat_data)

    # 生成剧情
     # 读取 reformat_data.json 作为 ctx_creator 的输入

    req = """要一个海滩旅游的短视频，视频总时长需要120秒，希望有记忆点以及有对应的开头高潮起伏，使得视频观看者更容易留下持续观看。"""
    res = ctx_creator(req, reformat_data)
    with open(storty_path, 'w', encoding='utf-8') as f:
        f.write(str(res))

    # 根据剧情编排完成视频定位
    uuid_list = extract_uuid_list(res)
    reformat_data_obj = json.loads(reformat_data)  # 先解析为对象
    uuid_map = build_uuid_map(reformat_data_obj)
    result = find_clips_by_uuid(uuid_list, uuid_map)
    with open(combine_video_json_path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(result, ensure_ascii=False, indent=2))

    # 视频剪辑
    extract_and_concat(result, operation_dir, result_path)
