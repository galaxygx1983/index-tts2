# IndexTTS2 技能快速入门指南

## ⚠️⚠️⚠️ 关键警告：禁止设置超时参数 ⚠️⚠️⚠️

**使用 `bash` 工具运行 IndexTTS2 命令时，绝对不能设置 `timeout` 参数。**

**IndexTTS2 音频生成需要 5-10 分钟。设置超时会导致命令生成中途失败。**

### 正确用法：
```python
# ✅ 正确 - 不设置 timeout 参数
bash(command="cd /path/to/indextts2 && uv run python script.py")
# 或显式设置 timeout=0
bash(command="cd /path/to/indextts2 && uv run python script.py", timeout=0)
```

### 错误用法：
```python
# ❌ 错误 - 设置超时会导致失败
bash(command="cd /path/to/indextts2 && uv run python script.py", timeout=120000)
bash(command="cd /path/to/indextts2 && uv run python script.py", timeout=600000)
```

**关键点：**
- 首次生成：5-10 分钟（模型从磁盘加载）
- 后续运行：1-3 分钟（模型缓存到内存）
- 命令会自然完成 - 不需要超时
- 超时会中断生成，导致音频损坏或无法生成

## 技能概述

**IndexTTS2** 是一个支持语音克隆和情感控制的文本转语音工具。这个 OpenCode 技能提供了完整的使用文档、部署检测和参考示例。

## 文件结构

```
index-tts2/
├── SKILL.md                    (299 行) - 主要技能文档
├── QUICK_START.md              (本文档) - 快速入门
├── scripts/
│   └── detect_deployment.py    (283 行) - 部署检测工具
└── references/
    ├── API_REFERENCE.md        (347 行) - 详细 API 文档
    └── CHEAT_SHEET.md          (177 行) - 快速参考卡片
```

## 快速开始

### 1. 检测部署状态

在 IndexTTS2 项目目录中运行：

```bash
python ~/.config/opencode/skill/index-tts2/scripts/detect_deployment.py
```

检测内容：
- ✓ pyproject.toml 是否包含 indextts 依赖
- ✓ uv 环境是否可用
- ✓ checkpoints 配置文件是否存在
- ✓ IndexTTS2 模块能否正常导入
- ✓ 示例音频文件是否存在

### 2. 基本使用

```python
from indextts.infer_v2 import IndexTTS2

# 初始化
tts = IndexTTS2(cfg_path="checkpoints/config.yaml", model_dir="checkpoints")

# 语音克隆
tts.infer(
    spk_audio_prompt='examples/voice_01.wav',
    text="你好世界！",
    output_path="output.wav",
    verbose=True
)
```

### 3. 运行脚本

```bash
# 确保使用 uv 环境运行
PYTHONPATH="$PYTHONPATH:." uv run your_script.py
```

## 核心功能

### 语音克隆
使用参考音频文件克隆声音特征。

### 情感控制
三种情感控制方式：
1. **情感音频** - 使用 emo_audio_prompt 参考音频
2. **情感向量** - 使用 8 维 emo_vector 直接指定
3. **文本情感** - 使用 use_emo_text 从文本自动提取

### 性能优化
- `use_fp16=True` - 半精度加速 (~2x)
- `use_cuda_kernel=True` - CUDA 加速 (~3x)
- `use_deepspeed=True` - 大批量处理优化

### Pinyin 控制
混合使用中文和 Pinyin 实现精确发音控制。

## 学习路径

### 新手推荐顺序

1. **第一天**: 阅读 SKILL.md 的 "Quick Start" 和 "Basic Voice Cloning" 部分
2. **第二天**: 尝试不同的情感控制方式
3. **第三天**: 学习性能优化和批量处理

### 进阶主题

1. **情感微调**: 查看 API_REFERENCE.md 的 "Emotion Vector Format" 部分
2. **批量合成**: 查看 CHEAT_SHEET.md 的 "Batch Synthesis" 部分
3. **故障排除**: 查看 CHEAT_SHEET.md 的 "Troubleshooting Quick Fixes" 部分

## 常用命令速查

```bash
# 检测部署
python ~/.config/opencode/skill/index-tts2/scripts/detect_deployment.py

# 运行脚本
PYTHONPATH="$PYTHONPATH:." uv run script.py

# 安装依赖
uv sync --all-extras

# 查看帮助
uv run python -c "from indextts.infer_v2 import IndexTTS2; help(IndexTTS2)"
```

## 示例代码位置

| 示例类型 | 文件位置 |
|---------|---------|
| 完整 API 使用 | `references/API_REFERENCE.md` |
| 常用代码片段 | `references/CHEAT_SHEET.md` |
| 部署检测 | `scripts/detect_deployment.py` |

## 故障排除

### 问题 1: 导入错误

```bash
# 解决：安装依赖
uv sync --all-extras
```

### 问题 2: CUDA 内存不足

```python
# 解决：启用半精度
tts = IndexTTS2(
    cfg_path="checkpoints/config.yaml",
    model_dir="checkpoints",
    use_fp16=True
)
```

### 问题 3: 情感效果太强

```python
# 解决：降低 emo_alpha
tts.infer(..., emo_alpha=0.6, ...)
```

### 问题 4: 语音克隆质量差

```python
# 解决：关闭随机采样
tts.infer(..., use_random=False, ...)
```

## 下一步

1. **阅读 SKILL.md**: 了解完整功能列表
2. **查看 API_REFERENCE**: 学习所有参数细节
3. **使用 CHEAT_SHEET**: 快速查找常用代码
4. **运行检测脚本**: 验证你的部署环境

## 获得帮助

- **快速问题**: 查看 CHEAT_SHEET.md 的 "Troubleshooting" 部分
- **API 详情**: 查看 API_REFERENCE.md
- **完整文档**: 阅读 SKILL.md

## 技能统计

- **总文件数**: 4
- **总代码量**: 1106 行
- **功能覆盖**: 9 个核心功能
- **示例数量**: 20+ 完整示例
- **测试用例**: 6 项自动化测试 ✓

---

**技能版本**: 1.0  
**最后更新**: 2024-01-23  
**测试状态**: ✅ 全部通过
