import pytest
from backend.src.lib.tokenizer import tokenize

@pytest.mark.parametrize(
    "text,expected",
    [
        ("Kick Snare Hat", ["kick", "snare", "hat"]),
        ("kick-kick SNARE", ["kick", "snare"]),  # 去重 + 小寫
        ("  ", []),  # 空字串
        ("Drums/Acoustic/Room.wav", ["drums", "acoustic", "room", "wav"]),
        ("multi__dash--and..dots", ["multi", "dash", "and", "dots"]),
    ],
)
def test_tokenize_cases(text, expected):
    assert tokenize(text) == expected


def test_tokenize_order_preserved():
    # 重複出現後面不再出現
    assert tokenize("a b a c a") == ["a", "b", "c"]
