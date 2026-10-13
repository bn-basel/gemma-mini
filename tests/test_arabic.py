from eval.arabic import strip_diacritics


def test_removes_harakat_tanween_and_shadda():
    assert strip_diacritics("مُحَمَّدٌ") == "محمد"


def test_leaves_plain_text_unchanged():
    assert strip_diacritics("السلام عليكم") == "السلام عليكم"
