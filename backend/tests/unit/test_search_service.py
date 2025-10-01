import pytest
from backend.src.services import search_service
from backend.src.models.audio_file import AudioFile


def make_file(rel: str):
    return AudioFile(
        id=rel.replace('/', '_'),
        relative_path=rel,
        display_name=rel.split('/')[-1],
        format="mp3",
        duration_seconds=None,
        file_size=123,
    )


def setup_index():
    files = [
        make_file("drums/kick.mp3"),
        make_file("drums/snare.mp3"),
        make_file("loops/kick_snare.mp3"),
        make_file("vocals/vox_lead.wav"),
    ]
    search_service.build_index(files)
    return files


def test_search_empty_returns_all():
    files = setup_index()
    res = search_service.search("")
    assert len(res) == len(files)


def test_single_term():
    setup_index()
    res = search_service.search("kick")
    names = [f.display_name for f in res]
    assert set(names) == {"kick.mp3", "kick_snare.mp3"}


def test_multi_term_intersection():
    setup_index()
    res = search_service.search("kick snare")
    names = [f.display_name for f in res]
    assert names == ["kick_snare.mp3"]


def test_min_stars_filter():
    files = setup_index()
    # annotations dict: file_id -> {star_rating}
    ann = {files[0].id: {"star_rating": 2}, files[1].id: {"star_rating": 4}}
    res = search_service.search("drums", min_stars=3, annotations=ann)
    # only snare has 4 stars
    assert [f.display_name for f in res] == ["snare.mp3"]


def test_no_results():
    setup_index()
    assert search_service.search("unknownterm") == []
