# IndexTTS2 Voice Synthesis

> Voice cloning and TTS with emotion control

## 功能特性

- 声音克隆 (Voice Cloning)
- 情感控制 (emo_vector, emo_audio_prompt, emo_text)
- 拼音标注
- 音高/速度/音调自定义
- 多说话人合成
- 批量处理
- GPU 加速

## 安装

```bash
git clone https://github.com/galaxygx1983/index-tts2.git
cd index-tts2
pip install -r requirements.txt
```

## 快速开始

```python
from indextts2 import TTS

tts = TTS()

# 基础合成
tts.synthesize("你好，世界!", output="output.wav")

# 声音克隆
tts.clone_voice(reference_audio="speaker.wav", text="克隆的语音", output="cloned.wav")

# 情感控制
tts.synthesize("开心的语音", emotion="happy", output="happy.wav")
```

## 注意事项

> ⚠️ **IndexTTS2 音频生成需要 5-10 分钟，不要设置 timeout 参数**

## 详细文档

查看 [SKILL.md](SKILL.md) 获取完整使用指南。

## 许可证

MIT License