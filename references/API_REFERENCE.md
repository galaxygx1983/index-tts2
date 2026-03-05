# IndexTTS2 API Reference

## Prerequisites

### Deployment Directory
**Default**: `E:\Developments\indextts2`

### Required Local Models

For offline/air-gapped environments, set these environment variables **BEFORE** importing IndexTTS2:

```python
import os
from pathlib import Path

# Configure local model paths
PROJECT_DIR = Path(__file__).parent  # Should be E:\Developments\indextts2
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
```

### Local Model Locations

| Model | Default Path | Size |
|-------|-------------|------|
| Wav2Vec2Bert | `checkpoints/w2v_bert/` | ~2.3GB |
| Semantic Codec | `checkpoints/MaskGCT/semantic_codec/model.safetensors` | 1.7GB |
| CAMPPlus | `checkpoints/campplus/campplus_cn_common.bin` | 28MB |
| BigVGAN | `checkpoints/bigvgan_v2_22khz_80band_256x/` | 449MB |

### Execution

```bash
cd E:\Developments\indextts2
uv run python your_script.py

# ⚠️ NO TIMEOUT - First generation takes 5-10 minutes!
```

**Important Notes**:
- ⚠️ **NO TIMEOUT**: Audio generation takes 5-10 minutes
- ⚠️ **GPU recommended**: Much faster than CPU
- ⚠️ **Run from E:\Developments\indextts2**: Or adjust PROJECT_DIR

### Constructor Parameters

```python
IndexTTS2(
    cfg_path: str = "checkpoints/config.yaml",
    model_dir: str = "checkpoints",
    use_fp16: bool = False,
    use_cuda_kernel: bool = False,
    use_deepspeed: bool = False
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `cfg_path` | `str` | `"checkpoints/config.yaml"` | Path to model configuration YAML file |
| `model_dir` | `str` | `"checkpoints"` | Directory containing model checkpoint files |
| `use_fp16` | `bool` | `False` | Enable half-precision (FP16) inference for faster performance |
| `use_cuda_kernel` | `bool` | `False` | Enable CUDA kernel acceleration (requires NVIDIA GPU) |
| `use_deepspeed` | `bool` | `False` | Enable DeepSpeed optimization for large-scale inference |

### infer() Method

```python
tts.infer(
    spk_audio_prompt: str,
    text: str,
    output_path: str,
    emo_audio_prompt: Optional[str] = None,
    emo_vector: Optional[List[float]] = None,
    emo_alpha: float = 1.0,
    use_emo_text: bool = False,
    emo_text: Optional[str] = None,
    use_random: bool = False,
    verbose: bool = False
)
```

#### Required Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `spk_audio_prompt` | `str` | Path to reference audio file for voice cloning |
| `text` | `str` | Input text to synthesize (supports Chinese characters and Pinyin) |
| `output_path` | `str` | Path for output WAV file |

#### Optional Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `emo_audio_prompt` | `Optional[str]` | `None` | Path to emotional reference audio file |
| `emo_vector` | `Optional[List[float]]` | `None` | 8-float list: [happy, angry, sad, afraid, disgusted, melancholic, surprised, calm] |
| `emo_alpha` | `float` | `1.0` | Emotional influence intensity (0.0 - 1.0) |
| `use_emo_text` | `bool` | `False` | Enable automatic emotion extraction from text |
| `emo_text` | `Optional[str]` | `None` | Separate text description for emotion guidance |
| `use_random` | `bool` | `False` | Enable stochastic sampling (adds variation, reduces fidelity) |
| `verbose` | `bool` | `False` | Enable detailed logging output |

#### Emotion Vector Format

The `emo_vector` parameter accepts an 8-element list representing emotion intensities:

```python
emo_vector = [
    0.0,  # happy
    0.0,  # angry
    0.0,  # sad
    0.0,  # afraid
    0.0,  # disgusted
    0.0,  # melancholic
    0.45, # surprised
    0.0   # calm
]
```

Each value ranges from 0.0 to 1.0, where:
- `0.0`: No influence from that emotion
- `1.0`: Maximum influence from that emotion

## Usage Examples by Scenario

### Scenario 1: Simple Voice Cloning

**Use case**: Clone a voice and synthesize basic speech

```python
from indextts.infer_v2 import IndexTTS2

tts = IndexTTS2(cfg_path="checkpoints/config.yaml", model_dir="checkpoints")
text = "Hello, this is a test of voice cloning."
tts.infer(
    spk_audio_prompt='examples/voice_01.wav',
    text=text,
    output_path="basic_clone.wav",
    verbose=True
)
```

### Scenario 2: Emotional Speech with Audio Reference

**Use case**: Apply emotion from a reference audio file

```python
from indextts.infer_v2 import IndexTTS2

tts = IndexTTS2(cfg_path="checkpoints/config.yaml", model_dir="checkpoints")
text = "今天天气真好，我们去散步吧！"
tts.infer(
    spk_audio_prompt='examples/voice_07.wav',
    text=text,
    output_path="emotional_speech.wav",
    emo_audio_prompt="examples/emo_happy.wav",  # Happy emotional reference
    emo_alpha=0.8,
    verbose=True
)
```

### Scenario 3: Controlled Emotion Vector

**Use case**: Precisely control emotion intensity with values

```python
from indextts.infer_v2 import IndexTTS2

tts = IndexTTS2(cfg_path="checkpoints/config.yaml", model_dir="checkpoints")
text = "听到这个消息，我非常震惊！"

# High surprise (0.9), moderate fear (0.3), low calm (0.1)
emo_vector = [0.0, 0.0, 0.0, 0.3, 0.0, 0.0, 0.9, 0.1]

tts.infer(
    spk_audio_prompt='examples/voice_12.wav',
    text=text,
    output_path="vector_emotion.wav",
    emo_vector=emo_vector,
    use_random=False,
    verbose=True
)
```

### Scenario 4: Text-based Emotion Generation

**Use case**: Generate emotions automatically from text content

```python
from indextts.infer_v2 import IndexTTS2

tts = IndexTTS2(cfg_path="checkpoints/config.yaml", model_dir="checkpoints")
text = "快跑！危险！有人追来了！"

tts.infer(
    spk_audio_prompt='examples/voice_12.wav',
    text=text,
    output_path="text_emotion.wav",
    emo_alpha=0.6,  # Recommended: keep around 0.6 for natural results
    use_emo_text=True,  # Enable automatic emotion extraction
    use_random=False,
    verbose=True
)
```

### Scenario 5: Separate Content and Emotion Text

**Use case**: Provide different text for content and emotion guidance

```python
from indextts.infer_v2 import IndexTTS2

tts = IndexTTS2(cfg_path="checkpoints/config.yaml", model_dir="checkpoints")
text = "今天工作很累。"  # Content: "Today work is tiring."
emo_text = "我真的快要崩溃了！"  # Emotion guidance: "I'm about to break down!"

tts.infer(
    spk_audio_prompt='examples/voice_07.wav',
    text=text,
    output_path="separate_emotion.wav",
    emo_alpha=0.6,
    use_emo_text=True,
    emo_text=emo_text,
    use_random=False,
    verbose=True
)
```

### Scenario 6: High Performance Inference

**Use case**: Maximize inference speed with optimization flags

```python
from indextts.infer_v2 import IndexTTS2

# Enable all performance optimizations
tts = IndexTTS2(
    cfg_path="checkpoints/config.yaml",
    model_dir="checkpoints",
    use_fp16=True,        # Half-precision
    use_cuda_kernel=True, # CUDA acceleration
    use_deepspeed=False   # Keep False for single inference
)

text = "性能优化测试语音。"
tts.infer(
    spk_audio_prompt='examples/voice_01.wav',
    text=text,
    output_path="optimized.wav",
    verbose=True
)
```

### Scenario 7: Stochastic Variation

**Use case**: Generate varied output for the same input

```python
from indextts.infer_v2 import IndexTTS2

tts = IndexTTS2(cfg_path="checkpoints/config.yaml", model_dir="checkpoints")
text = "同样的内容，不同的表达。"

# Generate multiple variations
for i in range(3):
    tts.infer(
        spk_audio_prompt='examples/voice_10.wav',
        text=text,
        output_path=f"variation_{i}.wav",
        use_random=True,  # Enable randomness
        verbose=True
    )
```

### Scenario 8: Pinyin Precision Control

**Use case**: Control pronunciation with Pinyin annotations

```python
from indextts.infer_v2 import IndexTTS2

tts = IndexTTS2(cfg_path="checkpoints/config.yaml", model_dir="checkpoints")

# Mix Chinese characters with Pinyin for specific pronunciations
text = "你好DE5世界，我DEI3来CHI1到ZHE4这里了。"

tts.infer(
    spk_audio_prompt='examples/voice_07.wav',
    text=text,
    output_path="pinyin_control.wav",
    verbose=True
)
```

## Performance Optimization Guide

### Inference Speed Comparison

| Configuration | Relative Speed | Memory Usage | Quality Impact |
|--------------|----------------|--------------|----------------|
| Default | 1.0x | Normal | Best |
| `use_fp16=True` | 1.5-2.0x | ~50% | Slight reduction |
| `use_cuda_kernel=True` | 2-3x | Normal | None |
| `use_fp16=True` + `use_cuda_kernel=True` | 3-4x | ~50% | Slight reduction |

### Recommended Configurations

**Best Quality**:
```python
tts = IndexTTS2(cfg_path="checkpoints/config.yaml", model_dir="checkpoints")
```

**Fast Inference** (GPU recommended):
```python
tts = IndexTTS2(
    cfg_path="checkpoints/config.yaml",
    model_dir="checkpoints",
    use_fp16=True,
    use_cuda_kernel=True
)
```

**Memory Constrained**:
```python
tts = IndexTTS2(
    cfg_path="checkpoints/config.yaml",
    model_dir="checkpoints",
    use_fp16=True
)
```

## Error Handling

### Common Errors and Solutions

#### Error: `ImportError: No module named 'indextts'`

**Solution**: Install IndexTTS2 dependencies
```bash
uv sync --all-extras
```

#### Error: `FileNotFoundError: checkpoints/config.yaml not found`

**Solution**: Download model checkpoints or verify path
```bash
ls -la checkpoints/
```

#### Error: `ValueError: emo_vector must be list of 8 floats`

**Solution**: Ensure emo_vector is exactly 8 elements
```python
# Wrong: emo_vector = [0.5, 0.3]  # Only 2 elements
# Correct:
emo_vector = [0.5, 0.3, 0.0, 0.0, 0.0, 0.0, 0.0, 0.2]  # 8 elements
```

#### Error: `RuntimeError: CUDA out of memory`

**Solution**: Reduce memory usage
```python
tts = IndexTTS2(
    cfg_path="checkpoints/config.yaml",
    model_dir="checkpoints",
    use_fp16=True,  # Reduce memory
    use_cuda_kernel=False  # Disable CUDA kernel
)
```

#### Error: `ValueError: emo_alpha must be between 0.0 and 1.0`

**Solution**: Clamp emo_alpha value
```python
# Ensure emo_alpha is in valid range
emo_alpha = max(0.0, min(1.0, emo_alpha))
```

## Best Practices Summary

1. **Always use `verbose=True`** during development for debugging
2. **Keep `use_random=False`** for consistent voice cloning
3. **Set `emo_alpha` around 0.6** for text-based emotions
4. **Use absolute paths** or set PYTHONPATH correctly
5. **Enable `use_fp16`** for GPU inference (minimal quality loss)
6. **Test with short text** first, then scale up
7. **Check output file** exists and has valid size before using
8. **Use `uv run`** to ensure proper environment activation
