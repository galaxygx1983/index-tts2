#!/usr/bin/env python3
"""
IndexTTS2 Deployment Detection Script

Detects if IndexTTS2 is properly deployed in the current environment.
Checks for:
1. pyproject.toml with indextts dependency
2. uv environment
3. Checkpoint files
4. Example audio files
"""

import subprocess
import sys
import os
from pathlib import Path


def check_pyproject_toml():
    """Check if pyproject.toml exists and contains indextts dependency."""
    print("Checking pyproject.toml...")
    pyproject_path = Path("pyproject.toml")

    if not pyproject_path.exists():
        print("  [FAIL] pyproject.toml not found")
        return False

    content = pyproject_path.read_text()
    if "indextts" in content or "index-tts" in content:
        print("  [OK] IndexTTS dependency found in pyproject.toml")
        return True
    else:
        print("  [FAIL] IndexTTS dependency not found in pyproject.toml")
        return False


def check_uv_environment():
    """Check if uv environment is properly set up."""
    print("Checking uv environment...")

    # Check if uv is available
    try:
        result = subprocess.run(
            ["uv", "--version"], capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            print(f"  [OK] uv is available: {result.stdout.strip()}")
        else:
            print("  [FAIL] uv is not available")
            return False
    except (FileNotFoundError, subprocess.TimeoutExpired):
        print("  [FAIL] uv command not found")
        return False

    # Check if virtual environment exists
    venv_paths = [
        Path(".venv"),
        Path("venv"),
        Path(".tox"),
    ]

    venv_found = False
    for venv_path in venv_paths:
        if venv_path.exists() and venv_path.is_dir():
            print(f"  [OK] Virtual environment found: {venv_path}")
            venv_found = True
            break

    if not venv_found:
        print("  [WARN] No virtual environment found (uv will create one)")

    return True


def check_uv_sync():
    """Check if dependencies are installed with uv sync."""
    print("Checking uv sync --all-extras...")

    # First check if we're in a project directory
    pyproject_path = Path("pyproject.toml")
    if not pyproject_path.exists():
        print("  [INFO] Not in a project directory (pyproject.toml not found)")
        print(
            "  [INFO] Skipping uv sync check - run this script from your IndexTTS2 project directory"
        )
        return None  # Skip this check

    try:
        # Try to run uv sync to verify dependencies are installed
        result = subprocess.run(
            ["uv", "sync", "--all-extras", "--dry-run"],
            capture_output=True,
            text=True,
            timeout=30,
        )

        if result.returncode == 0:
            print("  [OK] uv sync --all-extras is configured correctly")
            return True
        elif (
            "already synced" in result.stderr.lower()
            or "already synced" in result.stdout.lower()
        ):
            print("  [OK] Dependencies are already synced")
            return True
        else:
            print(f"  [WARN] uv sync check: {result.stderr[:150]}")
            return None
    except (FileNotFoundError, subprocess.TimeoutExpired) as e:
        print(f"  [FAIL] uv sync failed: {str(e)}")
        return False


def check_indextts_import():
    """Check if IndexTTS2 can be imported."""
    print("Checking IndexTTS2 import...")

    # First check if we're in a project directory
    pyproject_path = Path("pyproject.toml")
    if not pyproject_path.exists():
        print("  [INFO] Not in a project directory (pyproject.toml not found)")
        print(
            "  [INFO] Skipping import check - run this script from your IndexTTS2 project directory"
        )
        return None  # Skip this check

    try:
        # Try to import using uv run
        result = subprocess.run(
            [
                "uv",
                "run",
                "python",
                "-c",
                "from indextts.infer_v2 import IndexTTS2; print('Import successful')",
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )

        if result.returncode == 0:
            print(f"  [OK] {result.stdout.strip()}")
            return True
        else:
            # Check if it's a project directory issue
            if (
                "not a Python project" in result.stderr
                or "no pyproject.toml found" in result.stderr
            ):
                print("  [INFO] Not in a Python project directory")
                return None
            else:
                print(f"  [FAIL] Import failed: {result.stderr[:200]}")
                return False
    except (FileNotFoundError, subprocess.TimeoutExpired) as e:
        print(f"  [FAIL] Import check failed: {str(e)}")
        return False


def check_checkpoints():
    """Check if checkpoint files exist."""
    print("Checking checkpoint files...")

    checkpoint_path = Path("checkpoints")
    required_files = [
        "config.yaml",
    ]

    if not checkpoint_path.exists():
        print("  [FAIL] checkpoints directory not found")
        return False

    all_found = True
    for file in required_files:
        file_path = checkpoint_path / file
        if file_path.exists():
            print(f"  [OK] {file} found")
        else:
            print(f"  [FAIL] {file} not found")
            all_found = False

    return all_found


def check_local_models():
    """Check if all local model paths are configured correctly."""
    print("Checking local model paths...")

    # Define required local models
    local_models = {
        "INDEXTTS_W2V_DIR": "w2v_bert/",
        "INDEXTTS_MASKGCT_CODEC_PATH": "MaskGCT/semantic_codec/model.safetensors",
        "INDEXTTS_CAMPPLUS_CKPT_PATH": "campplus/campplus_cn_common.bin",
        "INDEXTTS_BIGVGAN_DIR": "bigvgan_v2_22khz_80band_256x/",
    }

    checkpoint_path = Path("checkpoints")
    all_ok = True

    for env_var, model_path in local_models.items():
        env_value = os.environ.get(env_var)

        if env_value:
            # Check if environment variable is set
            model_full_path = Path(env_value)
            if model_full_path.exists():
                # Verify it's a valid path
                if model_full_path.is_dir() or model_full_path.is_file():
                    print(f"  [OK] {env_var}: {model_full_path.name}")
                else:
                    print(f"  [FAIL] {env_var}: Invalid path type")
                    all_ok = False
            else:
                print(
                    f"  [WARN] {env_var}: Path exists but model not found at {env_value}"
                )
        else:
            # Environment variable not set, check if model exists in default location
            default_path = checkpoint_path / model_path
            if default_path.exists():
                print(
                    f"  [WARN] {env_var}: Not set, but model found at default: {model_path}"
                )
                print(f"         [TIP] Set {env_var} for offline use")
            else:
                print(
                    f"  [MISS] {env_var}: Not set and model not found at {model_path}"
                )

    return all_ok


def check_examples():
    """Check if example audio files exist."""
    print("Checking example audio files...")

    examples_path = Path("examples")
    example_files = [
        "voice_01.wav",
        "voice_07.wav",
        "voice_10.wav",
        "voice_12.wav",
    ]

    if not examples_path.exists():
        print("  [WARN] examples directory not found (optional)")
        return True

    found_count = 0
    for file in example_files:
        file_path = examples_path / file
        if file_path.exists():
            found_count += 1
            print(f"  [OK] {file}")
        else:
            print(f"  [MISS] {file} not found")

    if found_count > 0:
        print(f"  [INFO] {found_count}/{len(example_files)} example files found")
        return True
    else:
        print("  [WARN] No example files found (needed for voice cloning)")
        return True  # Not critical


def main():
    """Run all deployment checks."""
    print("=" * 60)
    print("IndexTTS2 Deployment Detection")
    print("=" * 60)
    print()

    checks = [
        ("pyproject.toml", check_pyproject_toml),
        ("uv environment", check_uv_environment),
        ("uv sync", check_uv_sync),
        ("checkpoints", check_checkpoints),
        ("local models", check_local_models),
        ("import test", check_indextts_import),
        ("examples", check_examples),
    ]

    results = {}
    for name, check_func in checks:
        print(f"\n[{name}]")
        try:
            results[name] = check_func()
        except Exception as e:
            print(f"  [FAIL] Check failed with error: {str(e)}")
            import traceback

            traceback.print_exc()
            results[name] = False

    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)

    passed = sum(1 for v in results.values() if v is True)
    skipped = sum(1 for v in results.values() if v is None)
    failed = sum(1 for v in results.values() if v is False)

    for name, result in results.items():
        if result is True:
            status = "[PASS]"
        elif result is False:
            status = "[FAIL]"
        else:
            status = "[SKIP]"
        print(f"{status:8} {name}")

    print()
    print(f"Results: {passed} passed, {failed} failed, {skipped} skipped")

    if failed == 0:
        print("\n[OK] IndexTTS2 deployment check completed!")
        if skipped > 0:
            print(
                "[INFO] Run this script from your IndexTTS2 project directory for complete check"
            )
        return 0
    else:
        print("\n[WARN] Some checks failed. Review the output above.")
        if skipped > 0:
            print(
                "[INFO] Run this script from your IndexTTS2 project directory for complete check"
            )
        return 1


if __name__ == "__main__":
    sys.exit(main())
