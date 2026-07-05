from expect_ime import JapaneseTypoDetector


def test_exact_dictionary_word_is_known():
    result = JapaneseTypoDetector().detect("日本語")

    assert result.is_known is True
    assert result.candidates == ()


def test_particle_confusion_is_ranked_highly():
    detector = JapaneseTypoDetector(["こんにちは", "こんばんは"])

    result = detector.detect("こんにちわ")

    assert result.is_known is False
    assert result.candidates[0].text == "こんにちは"
    assert result.candidates[0].score > 0.9


def test_small_kana_and_prolonged_sound_are_tolerated():
    detector = JapaneseTypoDetector(["ラッキー"])

    result = detector.detect("ラつキ")

    assert result.candidates[0].text == "ラッキー"
    assert result.candidates[0].score >= 0.58


def test_full_width_ascii_is_normalized():
    detector = JapaneseTypoDetector(["ABC入力"])

    result = detector.detect("ＡＢＣ入力")

    assert result.is_known is True
