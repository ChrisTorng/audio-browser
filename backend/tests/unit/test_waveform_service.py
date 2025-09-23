import asyncio
from pathlib import Path
import pytest
from backend.src.services import scan_service, waveform_service

@pytest.mark.asyncio
async def test_waveform_generation_and_reuse(temp_audio_dir, monkeypatch):
    # 建立一個 mp3 檔案
    f = temp_audio_dir / "sample.mp3"
    f.write_bytes(b"DATA")

    await scan_service.start_scan(str(temp_audio_dir))
    files = scan_service.get_scanned_files()
    target = next(x for x in files if x.display_name == "sample.mp3")

    # 第一次生成
    rel_path1 = await waveform_service.get_or_generate_waveform(target.id)
    abs_path1 = Path(temp_audio_dir) / rel_path1
    assert abs_path1.exists()
    first_mtime = abs_path1.stat().st_mtime

    # 第二次應該重用，不改變 mtime
    rel_path2 = await waveform_service.get_or_generate_waveform(target.id)
    abs_path2 = Path(temp_audio_dir) / rel_path2
    assert abs_path2.exists()
    second_mtime = abs_path2.stat().st_mtime
    assert first_mtime == second_mtime

@pytest.mark.asyncio
async def test_waveform_invalid_id():
    with pytest.raises(FileNotFoundError):
        await waveform_service.get_or_generate_waveform("no-such-id")
