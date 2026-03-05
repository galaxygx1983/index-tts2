# IndexTTS2 Cheat Sheet

## Quick Start Template

```python
#!/usr/bin/env python3
import os
from pathlib import Path
from indextts.infer_v2 import IndexTTS2

# ⚠️ MUST be at TOP - Configure local models
PROJECT_DIR = Path(__file__).parent
os.environ["INDEXTTS_W2V_DIR"] = str(PROJECT_DIR / "checkpoints" / "w2v_bert")
os.environ["INDEXTTS_MASKGCT_CODEC_PATH"] = str(
    PROJECT_DIR / "checkpoints" / "MaskGCT" / "semantic_codec" / "model.safetensors"
)
os.environ["INDEXTTS_CAMPPLUS_CKPT_PATH"] = str(
    PROJECT_DIR / "checkpoints" / "campplus" / "campplus_cn_common.bin"
)
os.environ["INDEXTTS_BIGVGAN_DIR"] = str(
    PROJECT_DIR / "checkpoints" / "bigvgan_v2_22khz_80band_256x"
)

# Initialize and synthesize
tts = IndexTTS2(cfg_path="checkpoints/config.yaml", model_dir="checkpoints")
tts.infer(spk_audio_prompt='examples/voice_01.wav', text="Hello!", output_path="out.wav", verbose=True)
```

## Deployment Directory

**Default**: `E:\Developments\indextts2`

## Critical Notes

⚠️ **NO TIMEOUT**: Audio generation takes 5-10 minutes
⚠️ **Local models required**: Set environment variables before import
⚠️ **Run from E:\Developments\indextts2**: Or adjust PROJECT_DIR
✅ **GPU recommended**: Much faster inference

### Basic Voice Cloning
```python
from indextts.infer_v2 import IndexTTS2
tts = IndexTTS2(cfg_path="checkpoints/config.yaml", model_dir="checkpoints")
tts.infer(spk_audio_prompt='examples/voice_01.wav', text="Hello world!", output_path="out.wav", verbose=True)
```

### With Emotion (Audio)
```python
tts.infer(spk_audio_prompt='voice.wav', text="悲伤的句子", output_path="out.wav", emo_audio_prompt="sad_voice.wav", emo_alpha=0.8, verbose=True)
```

### With Emotion (Vector)
```python
tts.infer(spk_audio_prompt='voice.wav', text="惊喜！", output_path="out.wav", emo_vector=[0,0,0,0,0,0,0.8,0.2], verbose=True)
```

### With Emotion (Text)
```python
tts.infer(spk_audio_prompt='voice.wav', text="快跑！", output_path="out.wav", emo_alpha=0.6, use_emo_text=True, verbose=True)
```

## Command Line Quick Tasks

### Check Deployment
```bash
python ~/.config/opencode/skill/index-tts2/scripts/detect_deployment.py
```

### Run Synthesis Script
```bash
PYTHONPATH="$PYTHONPATH:." uv run your_script.py
```

### Install Dependencies
```bash
uv sync --all-extras
```

## Parameter Quick Reference

| Task | Parameters | Values |
|------|-----------|--------|
| Basic clone | `spk_audio_prompt`, `text`, `output_path` | File paths |
| Add emotion (audio) | `emo_audio_prompt`, `emo_alpha` | `0.0-1.0` |
| Add emotion (vector) | `emo_vector` | 8 floats: `[happy, angry, sad, afraid, disgusted, melancholic, surprised, calm]` |
| Add emotion (text) | `use_emo_text`, `emo_alpha`, `emo_text` | `emo_alpha` ~0.6 |
| Random variation | `use_random` | `True`/`False` |
| Performance | `use_fp16`, `use_cuda_kernel` | `True`/`False` |

## Emotion Vector Guide

| Index | Emotion | Use Case |
|-------|---------|----------|
| 0 | happy | Joyful, excited content |
| 1 | angry | Frustrated, outraged content |
| 2 | sad | Sorrowful, melancholic content |
| 3 | afraid | Fearful, anxious content |
| 4 | disgusted | Repulsed, annoyed content |
| 5 | melancholic | Contemplative, nostalgic content |
| 6 | surprised | Shocked, amazed content |
| 7 | calm | Peaceful, relaxed content |

Example:
```python
# Very surprised, slightly afraid
emo_vector = [0.0, 0.0, 0.0, 0.2, 0.0, 0.0, 0.9, 0.0]
```

## Performance Flags

| Flag | Effect | Best For |
|------|--------|----------|
| `use_fp16=True` | 1.5-2x faster, 50% memory | GPU inference |
| `use_cuda_kernel=True` | 2-3x faster | NVIDIA GPUs |
| `use_deepspeed=True` | Large batch processing | Batch synthesis |

## File Locations

```
Project/
├── pyproject.toml          # Dependencies
├── checkpoints/
│   ├── config.yaml         # Model config
│   └── (model files)
├── examples/
│   ├── voice_01.wav        # Voice references
│   ├── voice_07.wav
│   └── emo_*.wav           # Emotion references
└── your_script.py
```

## Common Patterns

### Batch Synthesis
```python
voices = ['voice1.wav', 'voice2.wav']
texts = ["第一句", "第二句", "第三句"]

for voice in voices:
    for text in texts:
        tts.infer(spk_audio_prompt=voice, text=text, output_path=f"out_{voice}_{text}.wav", verbose=True)
```

### Multi-Emotion Test
```python
emo_vectors = {
    'happy': [0.8, 0, 0, 0, 0, 0, 0, 0.2],
    'sad': [0, 0, 0.8, 0, 0, 0.2, 0, 0],
    'surprised': [0, 0, 0, 0, 0, 0, 0.8, 0.2]
}

for name, vec in emo_vectors.items():
    tts.infer(spk_audio_prompt='voice.wav', text="测试文本", output_path=f"{name}.wav", emo_vector=vec, verbose=True)
```

### Voice Comparison
```python
reference_voices = ['voice1.wav', 'voice2.wav', 'voice3.wav']
text = "相同的文本，不同的声音"

for voice in reference_voices:
    tts.infer(spk_audio_prompt=voice, text=text, output_path=f"compare_{voice}.wav", verbose=True)
```

## Troubleshooting Quick Fixes

| Problem | Solution |
|---------|----------|
| Import error | `uv sync --all-extras` |
| CUDA out of memory | Add `use_fp16=True` |
| Low quality | Set `use_random=False` |
| Emotion too strong | Reduce `emo_alpha` (try 0.6) |
| Pinyin not working | Check `checkpoints/pinyin.vocab` |
| Slow inference | Enable `use_fp16` + `use_cuda_kernel` |
| File not found | Use full paths or set PYTHONPATH |

## Environment Variables

```bash
export PYTHONPATH="$PYTHONPATH:."  # Add project root to Python path
uv run your_script.py              # Run with uv environment
```

## Template: Complete Script

```python
#!/usr/bin/env python3
from indextts.infer_v2 import IndexTTS2

# Initialize with performance flags
tts = IndexTTS2(
    cfg_path="checkpoints/config.yaml",
    model_dir="checkpoints",
    use_fp16=True,
    use_cuda_kernel=False,
    use_deepspeed=False
)

# Your synthesis
tts.infer(
    spk_audio_prompt='examples/voice_01.wav',
    text="你的文本内容",
    output_path="output.wav",
    # Optional emotion control
    # emo_vector=[0,0,0,0,0,0,0.5,0],
    # emo_alpha=0.6,
    # use_emo_text=True,
    verbose=True
)

print("Synthesis complete: output.wav")
```
