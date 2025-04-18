import subprocess
import os

def separate_vocals(wav_path):
    output_dir = "demucs_output"
    os.makedirs(output_dir, exist_ok=True)

    subprocess.run([
        "python3", "-m", "demucs",
        "-n", "htdemucs",
        "-d", "cpu",
        "--two-stems", "vocals",
        wav_path
    ])

    base = os.path.basename(wav_path)
    stem = os.path.splitext(base)[0]
    vocal_path = os.path.join("separated", "htdemucs", stem, "vocals.wav")
    return vocal_path
