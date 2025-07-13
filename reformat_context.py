import re
import json
import uuid

def parse_segments(json_list):
    """
    直接从 understand.json 的 log/result 字段解析结构化片段数据
    """
    result = []
    uuid_map = {}

    for item in json_list:
        # 从 log 字段提取 segment_xxx.mp4
        log = item.get("log", "")
        m = re.search(r'segment_(\d{3})\.mp4', log)
        if not m:
            continue
        seg_id = m.group(1)
        segment_name = f"segment_{seg_id}.mp4"

        seg_content = item.get("result", "")
        # 匹配每一段时间、内容、运镜风格
        pattern = re.compile(
            r'(?:####\s*)?(\d+(?:\.\d+)?s-\d+(?:\.\d+)?s)[\s\S]*?\*\*视频内容：\*\*([\s\S]*?)\*\*运镜风格：\*\*([\s\S]*?)(?=(?:####|\Z|\d+(?:\.\d+)?s-\d+(?:\.\d+)?s))',
            re.MULTILINE
        )
        matches = pattern.findall(seg_content)
        clips = []
        current_time = 0
        for m in matches:
            time_range = m[0].replace(' ', '')
            try:
                start, end = [float(x.replace('s','')) for x in time_range.split('-')]
                duration = end - start
            except Exception:
                duration = ""
            # 计算timestamp
            ts_start = int(current_time)
            ts_end = int(current_time + duration) if duration != "" else int(current_time)
            def fmt(sec):
                return f"{int(sec)//60:02d}:{int(sec)%60:02d}"
            timestamp = f"{fmt(ts_start)}-{fmt(ts_end)}"
            current_time = ts_end

            content = m[1].strip() + "\n运镜风格：" + m[2].strip()
            uid = str(uuid.uuid4())
            clip = {
                "uuid": uid,
                "duration": duration,
                "timestamp": timestamp,
                "content": content
            }
            clips.append(clip)
            uuid_map[uid] = clip
        result.append({
            "segment": segment_name.replace('.mp4', ''),
            "clips": clips
        })  
    return json.dumps(result, ensure_ascii=False, indent=2), uuid_map

# 示例用法
if __name__ == "__main__":
    # 从 ./data/understand.json 读取内容
    with open('./data/understand.json', 'r', encoding='utf-8') as f:
        json_list = json.load(f)  # 这是一个包含log/result的字典列表

    data, uuid_map = parse_segments(json_list)

    # 写入到 ./data/reformat_data.json
    with open('./data/reformat_data.json', 'w', encoding='utf-8') as f:
        f.write(data)