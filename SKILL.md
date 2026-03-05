---
name: IndexTTS2
description: Voice cloning and TTS with emotion control (emo_vector, emo_audio_prompt, emo_text), pinyin annotation, pitch/speed/tone customization, multi-speaker synthesis, batch processing, GPU acceleration
---

# IndexTTS2 Voice Synthesis

## ⚠️⚠️⚠️ CRITICAL: NEVER SET TIMEOUT PARAMETER ⚠️⚠️⚠️

**When running IndexTTS2 commands via the `bash` tool, you MUST NOT set the `timeout` parameter.**

**IndexTTS2 audio generation takes 5-10 minutes. Setting timeout will cause the command to fail mid-generation.**

### CORRECT Usage:
```python
# ✅ CORRECT - NO timeout parameter
bash(command="cd /path/to/indextts2 && uv run python script.py")
# or explicitly set timeout=0
bash(command="cd /path/to/indextts2 && uv run python script.py", timeout=0)
```

### WRONG Usage:
```python
# ❌ WRONG - Setting timeout causes failure
bash(command="cd /path/to/indextts2 && uv run python script.py", timeout=120000)
bash(command="cd /path/to/indextts2 && uv run python script.py", timeout=600000)
```

**Key Points:**
- First generation: 5-10 minutes (models loading from disk)
- Subsequent runs: 1-3 minutes (models cached in memory)
- Command will complete naturally - no timeout needed
- Timeout interrupts generation, producing corrupted or no audio

## Quick Start

**IndexTTS2 audio generation takes 5-10 minutes. DO NOT set timeout parameter when running via bash tool.**

**When invoking IndexTTS2 commands:**
```bash
# ❌ WRONG - This will timeout and fail
bash(command="uv run python script.py", timeout=120000)  # TIMEOUT CAUSES FAILURE

# ✅ CORRECT - Run without timeout
bash(command="uv run python script.py", timeout=0)  # NO TIMEOUT
# or simply omit timeout parameter entirely
```

**First generation is slowest** (5-10 min). Subsequent runs are faster (1-3 min) once models are loaded in memory.

## Quick Start

Initialize IndexTTS2 with proper configuration:
```python
from indextts.infer_v2 import IndexTTS2
tts = IndexTTS2(
    cfg_path="checkpoints/config.yaml",
    model_dir="checkpoints",
    use_fp16=False,
    use_cuda_kernel=False,
    use_deepspeed=False
)
```

Run synthesis using `uv run` to ensure proper environment activation:
```bash
PYTHONPATH="$PYTHONPATH:." uv run your_script.py
```

## Deployment Detection

**Default Directory**: `E:\Developments\indextts2`

To detect if IndexTTS2 is locally deployed:

1. Check for `pyproject.toml` with `indextts` dependency in deployment directory
2. Verify uv environment exists (`uv run` works)
3. Confirm checkpoint files exist in `checkpoints/` directory
4. Check for example audio files in `examples/` directory

**Critical: Local Model Paths**

For offline use (no internet required), set these environment variables to point to local models:

```bash
# In E:\Developments\indextts2 directory, run before Python scripts:
set INDEXTTS_W2V_DIR=E:\Developments\indextts2\checkpoints\w2v_bert
set INDEXTTS_MASKGCT_CODEC_PATH=E:\Developments\indextts2\checkpoints\MaskGCT\semantic_codec\model.safetensors
set INDEXTTS_CAMPPLUS_CKPT_PATH=E:\Developments\indextts2\checkpoints\campplus\campplus_cn_common.bin
set INDEXTTS_BIGVGAN_DIR=E:\Developments\indextts2\checkpoints\bigvgan_v2_22khz_80band_256x
```

Or include in your Python script:
```python
import os
from pathlib import Path

# Set local model paths BEFORE importing IndexTTS2
PROJECT_DIR = Path(__file__).parent
os.environ["INDEXTTS_W2V_DIR"] = str(PROJECT_DIR / "checkpoints" / "w2v_bert")
os.environ["INDEXTTS_MASKGCT_CODEC_PATH"] = str(PROJECT_DIR / "checkpoints" / "MaskGCT" / "semantic_codec" / "model.safetensors")
os.environ["INDEXTTS_CAMPPLUS_CKPT_PATH"] = str(PROJECT_DIR / "checkpoints" / "campplus" / "campplus_cn_common.bin")
os.environ["INDEXTTS_BIGVGAN_DIR"] = str(PROJECT_DIR / "checkpoints" / "bigvgan_v2_22khz_80band_256x")
```

**Required Local Models**:
- `w2v_bert/` - Wav2Vec2Bert model (for audio feature extraction)
- `MaskGCT/semantic_codec/model.safetensors` - Semantic codec (1.7GB)
- `campplus/campplus_cn_common.bin` - CAMPPlus model (28MB)
- `bigvgan_v2_22khz_80band_256x/` - BigVGAN vocoder (449MB)

**Detection command**:
```bash
# Run from deployment directory E:\Developments\indextts2
python ~/.config/opencode/skill/index-tts2/scripts/detect_deployment.py
```

## Basic Voice Cloning

**Important**: Set local model paths before importing IndexTTS2 for offline use:

```python
import os
from pathlib import Path
from indextts.infer_v2 import IndexTTS2

# Configure local model paths (required for offline/ air-gapped environments)
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

# Initialize IndexTTS2 (do NOT set timeout - generation takes 5-10 minutes)
tts = IndexTTS2(
    cfg_path="checkpoints/config.yaml",
    model_dir="checkpoints",
    use_fp16=False,
    use_cuda_kernel=False,
    use_deepspeed=False
)
```

Run synthesis using `uv run` with **NO TIMEOUT** (generation takes 5-10 minutes):
```bash
# In E:\Developments\indextts2 directory
uv run python your_script.py
# ⚠️ DO NOT set timeout - first generation takes 5-10 minutes
```

Synthesize speech with a single reference audio file:

```python
## Complete Working Example

This is the recommended template for all IndexTTS2 scripts in E:\Developments\indextts2:

```python
#!/usr/bin/env python3
"""
IndexTTS2 Voice Synthesis - Complete Template
"""
import os
import sys
from pathlib import Path

# ⚠️ MUST be at the TOP, before any IndexTTS imports
# Configure all local model paths for offline use
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

# Now import IndexTTS2
from indextts.infer_v2 import IndexTTS2

def synthesize(text, output_path, **kwargs):
    """Synthesize speech with the given parameters."""
    tts = IndexTTS2(
        cfg_path="checkpoints/config.yaml",
        model_dir="checkpoints",
        use_fp16=False,
        use_cuda_kernel=False,
        use_deepspeed=False
    )
    tts.infer(
        spk_audio_prompt='examples/voice_01.wav',
        text=text,
        output_path=output_path,
        verbose=True,
        **kwargs
    )

# Example usage
if __name__ == "__main__":
    # ⚠️ CRITICAL: When running via bash tool, MUST NOT set timeout parameter
    # Run this script with: bash(command="uv run python your_script.py", timeout=0)
    # or simply omit timeout parameter entirely
    synthesize(
        text="朱门酒肉臭，路有冻死骨！",
        output_path="output.wav",
        emo_audio_prompt="examples/emo_hate.wav",
        emo_alpha=0.9
    )
```

**Execution** (from E:\Developments\indextts2 directory):
```bash
# ⚠️ CRITICAL: Run bash command WITHOUT timeout parameter
# ❌ DO NOT use: bash(command="...", timeout=120000)
# ✅ CORRECT: bash(command="...", timeout=0) or omit timeout entirely
uv run python your_script.py
```

**Important Notes**:
- ⚠️ **CRITICAL: NO TIMEOUT**: When running via bash tool, MUST NOT set timeout parameter. Audio generation takes 5-10 minutes.
- ⚠️ **Local models required**: Set environment variables before import
- ⚠️ **Local models required**: Set environment variables before import
- ⚠️ **Run from E:\Developments\indextts2**: Or adjust PROJECT_DIR accordingly
- ✅ **GPU recommended**: Much faster than CPU inference

## Emotion Control Examples

### Using Emotional Audio Reference
```python
tts.infer(
    spk_audio_prompt='examples/voice_07.wav',
    text="酒楼丧尽天良，开始借机竞拍房间，哎，一群蠢货。",
    output_path="gen.wav",
    emo_audio_prompt="examples/emo_sad.wav",
    emo_alpha=0.9,  # 90% emotional influence
    verbose=True
)
```

### Using Emotion Vector
```python
# [happy, angry, sad, afraid, disgusted, melancholic, surprised, calm]
tts.infer(
    spk_audio_prompt='examples/voice_10.wav',
    text="哇塞！这个爆率也太高了！欧皇附体了！",
    output_path="gen.wav",
    emo_vector=[0.9, 0, 0, 0, 0, 0, 0, 0],  # Very happy
    use_random=False,
    verbose=True
)
```

### Using Text-based Emotion
```python
tts.infer(
    spk_audio_prompt='examples/voice_12.wav',
    text="快躲起来！是他要来了！他要来抓我们了！",
    output_path="gen.wav",
    emo_alpha=0.6,
    use_emo_text=True,
    emo_text="你吓死我了！你是鬼吗？",
    use_random=False,
    verbose=True
)
```

## Pinyin Control
```python
text = "之前你做DE5很好，所以这一次也DEI3做DE2很好才XING2，如果这次目标完成得不错的话，我们就直接打DI1去银行取钱。"
```
tts.infer(
    spk_audio_prompt='examples/voice_01.wav',
    text=text,
    output_path="gen.wav",
    verbose=True
)
```

## Emotion Control

### Using Emotional Reference Audio

Apply emotional characteristics from a reference audio file:

```python
from indextts.infer_v2 import IndexTTS2
tts = IndexTTS2(cfg_path="checkpoints/config.yaml", model_dir="checkpoints")
text = "酒楼丧尽天良，开始借机竞拍房间，哎，一群蠢货。"
tts.infer(
    spk_audio_prompt='examples/voice_07.wav',
    text=text,
    output_path="gen.wav",
    emo_audio_prompt="examples/emo_sad.wav",
    verbose=True
)
```

Adjust emotional intensity with `emo_alpha` (0.0 - 1.0):

```python
tts.infer(
    spk_audio_prompt='examples/voice_07.wav',
    text=text,
    output_path="gen.wav",
    emo_audio_prompt="examples/emo_sad.wav",
    emo_alpha=0.9,  # 90% emotional influence
    verbose=True
)
```

### Using Emotion Vector

Specify emotion intensity as an 8-float list:

```python
from indextts.infer_v2 import IndexTTS2
tts = IndexTTS2(cfg_path="checkpoints/config.yaml", model_dir="checkpoints")
text = "哇塞！这个爆率也太高了！欧皇附体了！"
tts.infer(
    spk_audio_prompt='examples/voice_10.wav',
    text=text,
    output_path="gen.wav",
    emo_vector=[0, 0, 0, 0, 0, 0, 0.45, 0],  # [happy, angry, sad, afraid, disgusted, melancholic, surprised, calm]
    use_random=False,
    verbose=True
)
```

### Using Text-based Emotion

Generate emotions from text descriptions:

```python
from indextts.infer_v2 import IndexTTS2
tts = IndexTTS2(cfg_path="checkpoints/config.yaml", model_dir="checkpoints")
text = "快躲起来！是他要来了！他要来抓我们了！"
tts.infer(
    spk_audio_prompt='examples/voice_12.wav',
    text=text,
    output_path="gen.wav",
    emo_alpha=0.6,
    use_emo_text=True,  # Enable text-based emotion
    use_random=False,
    verbose=True
)
```

Separate text and emotion description:

```python
from indextts.infer_v2 import IndexTTS2
tts = IndexTTS2(cfg_path="checkpoints/config.yaml", model_dir="checkpoints")
text = "快躲起来！是他要来了！他要来抓我们了！"
emo_text = "你吓死我了！你是鬼吗？"
tts.infer(
    spk_audio_prompt='examples/voice_12.wav',
    text=text,
    output_path="gen.wav",
    emo_alpha=0.6,
    use_emo_text=True,
    emo_text=emo_text,
    use_random=False,
    verbose=True
)
```

## Randomness Control

Enable stochastic sampling for variation (reduces voice cloning fidelity):

```python
tts.infer(
    spk_audio_prompt='examples/voice_10.wav',
    text=text,
    output_path="gen.wav",
    use_random=True,  # Enable randomness
    verbose=True
)
```

## Pinyin Control

IndexTTS2 supports mixed Chinese characters and Pinyin for precise pronunciation control. Use Pinyin annotations for specific pronunciations:

```python
text = "之前你做DE5很好，所以这一次也DEI3做DE2很好才XING2，如果这次目标完成得不错的话，我们就直接打DI1去银行取钱。"
```

Valid Pinyin entries are defined in `checkpoints/pinyin.vocab`. Only valid Chinese Pinyin cases are supported.

## Advanced Configuration

### Performance Optimization

Use FP16 for faster inference:
```python
tts = IndexTTS2(
    cfg_path="checkpoints/config.yaml",
    model_dir="checkpoints",
    use_fp16=True,  # Enable half-precision
    use_cuda_kernel=False,
    use_deepspeed=False
)
```

### CUDA Kernel Acceleration

Enable CUDA kernel for better performance on NVIDIA GPUs:
```python
tts = IndexTTS2(
    cfg_path="checkpoints/config.yaml",
    model_dir="checkpoints",
    use_fp16=False,
    use_cuda_kernel=True,  # CUDA acceleration
    use_deepspeed=False
)
```

### DeepSpeed Integration

For large-scale inference, enable DeepSpeed:
```python
tts = IndexTTS2(
    cfg_path="checkpoints/config.yaml",
    model_dir="checkpoints",
    use_fp16=False,
    use_cuda_kernel=False,
    use_deepspeed=True  # DeepSpeed optimization
)
)
```

## Complete Workflow Examples

### Multi-emotion Speech Synthesis

```python
from indextts.infer_v2 import IndexTTS2

tts = IndexTTS2(cfg_path="checkpoints/config.yaml", model_dir="checkpoints")

# Initialize with different voice and emotion
voices = ['examples/voice_01.wav', 'examples/voice_07.wav', 'examples/voice_10.wav']
emotions = {
    'happy': [0.8, 0, 0, 0, 0, 0, 0, 0.2],
    'sad': [0, 0, 0.8, 0, 0, 0.2, 0, 0],
    'surprised': [0, 0, 0, 0, 0, 0, 0.8, 0.2]
}

for voice_file in voices:
    for emotion_name, emo_vector in emotions.items():
        text = f"这是一个{emotion_name}的情绪测试！"
        output_path = f"gen_{voice_file.split('/')[-1]}_{emotion_name}.wav"
        
        tts.infer(
            spk_audio_prompt=voice_file,
            text=text,
            output_path=output_path,
            emo_vector=emo_vector,
            use_random=False,
            verbose=True
        )
```

### Batch Synthesis with Text Emotion

```python
from indextts.infer_v2 import IndexTTS2

tts = IndexTTS2(cfg_path="checkpoints/config.yaml", model_dir="checkpoints")

dialogues = [
    ("快躲起来！是他要来了！他要来抓我们了！", "恐惧"),
    ("太好了！我们成功了！", "兴奋"),
    ("听到这个消息，我很难过。", "悲伤")
]

for text, emotion_desc in dialogues:
    output_path = f"gen_{emotion_desc}.wav"
    
    tts.infer(
        spk_audio_prompt='examples/voice_12.wav',
        text=text,
        output_path=output_path,
        emo_alpha=0.6,
        use_emo_text=True,
        emo_text=emotion_desc,
        use_random=False,
        verbose=True
    )
```

## Best Practices

1. **Voice Cloning Quality**: For best voice cloning results, use `use_random=False`
2. **Emotion Naturalness**: When using text-based emotions, keep `emo_alpha` around 0.6 or lower
3. **Pinyin Control**: Use Pinyin annotations only for pronunciation precision; not all CV combinations are valid
4. **Performance**: Enable `use_fp16` and `use_cuda_kernel` for faster inference on compatible hardware
5. **Randomness**: Enable `use_random` only when variation is needed; it reduces fidelity
6. **Path Handling**: Always use relative paths from project root and set PYTHONPATH

## Troubleshooting

- **ImportError**: Ensure IndexTTS2 is installed with `uv sync --all-extras`
- **Model Load Error**: Verify `checkpoints/` directory contains all required model files
- **Audio File Error**: Check that reference audio files exist and are in WAV format
- **Memory Issues**: Reduce batch size or enable `use_fp16` for memory optimization

## Legacy Support

Use IndexTTS1 for backward compatibility:

```python
from indextts.infer import IndexTTS
tts = IndexTTS(model_dir="checkpoints", cfg_path="checkpoints/config.yaml")
voice = "examples/voice_07.wav"
text = "大家好，我现在正在bilibili 体验 ai 科技..."
tts.infer(voice, text, 'gen.wav')
```
