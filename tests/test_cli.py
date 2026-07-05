import json

from expect_ime.__main__ import main


def test_cli_outputs_json_lines(capsys):
    exit_code = main(["こんにちわ", "--json"])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)

    assert exit_code == 0
    assert payload["original"] == "こんにちわ"
    assert payload["candidates"][0]["text"] == "こんにちは"


def test_cli_accepts_custom_dictionary(tmp_path, capsys):
    dictionary = tmp_path / "words.txt"
    dictionary.write_text("期待入力\n", encoding="utf-8")

    exit_code = main(["--dictionary", str(dictionary), "期待人力"])

    captured = capsys.readouterr()

    assert exit_code == 0
    assert "期待入力" in captured.out
