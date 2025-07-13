# AI-Cutting 视频智能理解与自动剪辑流程

## 项目简介

本项目实现了从原始视频自动分割、AI语义理解、结构化脚本生成、智能片段编排到自动剪辑合成的全流程。适用于短视频自动化生产、AI辅助剪辑等场景。

---

## 目录结构

```
.
├── source/                # 原始视频文件夹
├── video_part/            # 分割后的视频片段
├── output_data/           # 过程数据与结果输出目录
│   ├── understand.json        # AI理解结果
│   ├── reformat_data.json     # 结构化片段数据
│   ├── story.txt              # AI生成的剧情脚本及UUID数组
│   ├── combine_video.json     # 剪辑所需片段定位信息
│   └── result.mp4             # 最终合成视频
├── split_video.py         # 视频分割（ffmpeg，保留音频）
├── video_understand.py    # AI理解视频内容
├── reformat_context.py    # 结构化理解结果
├── context_create.py      # AI生成剧情脚本
├── relocate.py            # 根据UUID定位片段
├── combine_video.py       # 合成最终视频
├── creator_main.py        # 全流程主控脚本
└── config.py              # API Key等配置
```

---

## 依赖环境

- Python 3.7+
- ffmpeg（需安装并配置到环境变量）
- OpenCV（如需用到）
- dashscope（百炼API，需API Key）
- 其它依赖见 requirements.txt

---

## 一键全流程运行

1. **准备原始视频**  
   将待处理视频放入 `source/` 目录。

2. **运行主控脚本**  
   ```bash
   python creator_main.py
   ```

3. **输出结果**  
   - 分割片段在 `video_part/`
   - 过程数据在 `output_data/`
   - 最终合成视频为 `output_data/result.mp4`

---

## 主要流程说明

1. **视频分割**  
   `split_video.py` 使用 ffmpeg 按指定时长分割视频，保留音频。

2. **AI理解**  
   `video_understand.py` 对每个片段调用大模型理解，输出到 `understand.json`。

3. **结构化处理**  
   `reformat_context.py` 将理解结果转为结构化 JSON，便于后续处理。

4. **剧情生成**  
   `context_create.py` 调用大模型生成剧情脚本和 UUID 编排。

5. **片段定位**  
   `relocate.py` 根据 UUID 数组定位所需片段。

6. **自动剪辑合成**  
   `combine_video.py` 用 ffmpeg 按剧情顺序拼接片段，输出最终视频。

---

## 常见问题

- **分割片段无声音？**  
  请确保分割用的是 ffmpeg 且参数为 `-c copy` 或 `-c:a aac`，不要用 OpenCV 分割。

- **API Key 配置？**  
  请在 `config.py` 中填写你的 dashscope 百炼 API Key。

- **ffmpeg 未找到？**  
  请确保 ffmpeg 已安装并加入系统环境变量。

---

## 联系与支持

如有问题或建议，请提交 issue 或联系项目维护者。

---

