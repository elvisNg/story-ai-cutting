import dashscope
import os
from config import API_KEY
from dashscope import Generation
import ast

def ctx_creator(req, text):
    messages = [
        {"role":"system", "content":f"输入内容里面的duration的值为当段视频内容的时长，按照片段视频的时长计算总时长，将输入内容按{req}的需求，编排成高质量的视频脚本，并输出对应的视频片段的uuid数组"},
        {"role": "user", "content": text}
    ]

    response = Generation.call(
        # 若没有配置环境变量， 请用百炼API Key将下行替换为： api_key ="sk-xxx"
        api_key=API_KEY,
        model='qwen-max-latest',
        messages=messages,
        result_format="message"
    )
    print("response:", response)
    if not hasattr(response, "output") or not response.output:
        print("API 未返回 output 字段")
        return None
    if not hasattr(response.output, "choices") or not response.output.choices:
        print("API output 未返回 choices 字段")
        return None
    if not hasattr(response.output.choices[0], "message") or not hasattr(response.output.choices[0].message, "content"):
        print("choices[0] 未返回 message.content")
        return None
    print(response.output.choices[0].message.content)
    res = response.output.choices[0].message.content
    return res




if __name__ == '__main__':
    # 从 ./data/reformat_data.json 读取内容
    with open('./data/reformat_data.json', 'r', encoding='utf-8') as f:
        text = f.read()
    req = """要一个海滩旅游的短视频，视频总时长需要120秒，希望有记忆点以及有对应的开头高潮起伏，使得视频观看者更容易留下持续观看。"""
    res = ctx_creator(req, text)
    # 将结果写入 ./data/story.txt
    with open('./data/story.txt', 'w', encoding='utf-8') as f:
        f.write(str(res))
    print("end")

