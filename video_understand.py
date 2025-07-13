import dashscope
import os
from config import API_KEY
import json
from get_duration import get_video_duration_func

def video_understand_func(video_path,duration):
    messages = [
        {"role":"system",
         "content":[
            {"text": """# 角色
你是一位视频内容和运镜理解专家，擅长按时间先后顺序给出每个子片段的视频内容和运镜风格，视频内容的表达需要有逻辑性，给到后期阅读编排视频脚本参考：
#### 开始时间-结束时间，格式:0s-3s
**视频内容：**
**运镜风格：** """}]},
    #          {"text": """# 角色
    # 你是一位视频内容和运镜理解专家，擅长按时间先后顺序给出每个子片段的视频内容和运镜风格"""}]},
        {"role": "user",
            "content": [
                # fps 可参数控制视频抽帧频率，表示每隔1/fps 秒抽取一帧，完整用法请参见：https://help.aliyun.com/zh/model-studio/use-qwen-by-calling-api?#2ed5ee7377fum
                # {"video": "https://cloud.video.taobao.com/vod/C6gCj5AJ3Qrd_UQ9kaMVRY9Ig9G-WToxVYSPRdNXCao.mp4","fps":2},
                {"video": video_path,"fps":1},
                {"text": f"这段视频的时长为{duration}s"} #这个时长信息对于模型理解时间轴很重要
            ]
        }
    ]

    response = dashscope.MultiModalConversation.call(
        # 若没有配置环境变量， 请用百炼API Key将下行替换为： api_key ="sk-xxx"
        api_key=API_KEY,
        model='qwen-vl-max-latest',
        messages=messages,
        temperature=0
    )
    return response.output.choices[0].message.content[0]["text"]

def main():
    output_dir = "/Users/elvis/workspace/code/ai-cutting/video_part/"  # 拆分后的片段目录
    data_dir = "./data"
    os.makedirs(data_dir, exist_ok=True)
    understand_json_path = os.path.join(data_dir, "understand.txt")
    res_list = []

    # 遍历所有子目录和文件，找到所有mp4文件
    for root, dirs, files in os.walk(output_dir):
        for filename in files:
            if filename.lower().endswith(('.mp4', '.mov', '.avi', '.mkv')):
                video_path = os.path.join(root, filename)
                duration = get_video_duration_func(video_path)  # 获取视频时长

                log_msg = f"理解视频内容 starting for video: {video_path} with duration: {duration} seconds"
                print(log_msg)
                try:
                    res = video_understand_func(video_path, duration)
                    print(f"视频理解结果: {res}")
                    # 将log和res一起写入
                    res_list.append({
                        "log": log_msg,
                        "result": res
                    })
                    # 每次追加后写入，保证并发和时序性
                    with open(understand_json_path, 'w', encoding='utf-8') as f:
                        json.dump(res_list, f, ensure_ascii=False, indent=2)
                except Exception as e:
                    print(f"理解视频内容时发生错误: {e}")
    # print("开始理解视频内容...")
    # video_dir = '/Users/elvis/workspace/code/ai-cutting/video_part'  # 文件夹路径
    # duration = 30  # 你可以根据实际情况获取每个视频的时长

    # for filename in os.listdir(video_dir):
    #     video_path = os.path.join(video_dir, filename)
    #     if not os.path.isfile(video_path):
    #         continue  # 跳过子文件夹等非文件项
    #     get_video_duration_func = __import__('get_duration').get_video_duration_func
    #     duration = get_video_duration_func(video_path)  # 获取视频时长

    #     print(f"理解视频内容 starting for video: {video_path} with duration: {duration} seconds")
    #     try:
    #         res = video_understand_func(video_path, duration)
    #         print(f"视频理解结果: {res}")
    #     except Exception as e:
    #         print(f"理解视频内容时发生错误: {e}")
#     print("视频理解完成。")   

    # video_path = '/Users/elvis/workspace/code/ai-cutting/video_part/segment_002.mp4'  # 请替换为你的视频文件路径
    # duration = 30  # 假设视频时长为30秒 
    # try:
    #     res = video_understand_func(video_path, duration)
    #     print(f"视频理解结果: {res}")
    # except Exception as e:
    #     print(f"理解视频内容时发生错误: {e}")


if __name__ == "__main__":
    main()