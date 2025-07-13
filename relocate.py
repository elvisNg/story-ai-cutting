import json
import re

def extract_uuid_list(text):
   
    # 优先找带 UUID数组输出 的 json 代码块
    match = re.search(r'UUID数组输出[\s\S]*?```json\s*([\s\S]*?)```', text, re.MULTILINE)
    if not match:
        # 兜底：直接找第一个 json 代码块
        match = re.search(r'```json\s*([\s\S]*?)```', text, re.MULTILINE)
    if match:
        uuid_list = json.loads(match.group(1))
        return uuid_list
    else:
        # 再兜底：直接找第一个以 [ 开头、] 结尾的数组
        match = re.search(r'(\[\s*"(?:[a-f0-9\-]+",?\s*)+\])', text)
        if match:
            uuid_list = json.loads(match.group(1))
            return uuid_list
        raise ValueError("未找到 UUID 数组，请检查文本格式。")

    
def load_json_data(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def build_uuid_map(json_data):
    uuid_map = {}
    for segment in json_data:
        for clip in segment.get("clips", []):
            uuid_map[clip["uuid"]] = {
                "segment": segment["segment"],
                **clip
            }
    return uuid_map

def find_clips_by_uuid(uuid_list, uuid_map):
    found = []
    for uid in uuid_list:
        if uid in uuid_map:
            found.append(uuid_map[uid])
        else:
            print(f"未找到uuid: {uid}")
    return found

def main():
    story_path = './data/story.txt'  # 替换为你的story.txt路径
    with open(story_path, 'r', encoding='utf-8') as f:
        text = f.read()
    uuid_list = extract_uuid_list(text)
    json_path = './data/reformat_data.json'  # 替换为你的json文件路径
    json_data = load_json_data(json_path)
    uuid_map = build_uuid_map(json_data)
    result = find_clips_by_uuid(uuid_list, uuid_map)
    with open('./data/combine_video.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()