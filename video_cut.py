import dashscope
import os
from config import API_KEY


def video_cut_func(text, video_path):
    messages = [
        {"role":"system",
         # "content":[{"text": """对这段视频进行裁剪，裁剪到10s内，保留关键信息。以JSON格式输出剪辑保留的视频片段信息：开始时间（start_time）、结束时间（end_time）、事件（event）。"""}]},
         "content":[{"text": text}]},
        {"role": "user",
            "content": [
                # fps 可参数控制视频抽帧频率，表示每隔1/fps 秒抽取一帧，完整用法请参见：https://help.aliyun.com/zh/model-studio/use-qwen-by-calling-api?#2ed5ee7377fum
                {"video": video_path,"fps":2},
                {"text": "遵循系统指令进行回答"}
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

    print(response)
    print("end")
    return response.output.choices[0].message.content[0]["text"]
