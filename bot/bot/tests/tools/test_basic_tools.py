from twitter_bot.tools import basic_tools


def test_get_timestamp_utc():
    assert isinstance(basic_tools.get_timestamp_utc(), int)
    assert basic_tools.get_timestamp_utc() > 1640995200  # 2022/01/01 00:00:00


def test_clean_text_NO_REMOVE():
    assert basic_tools.clean_text("je tranlfd lfdfd") == "je tranlfd lfdfd"


def test_clean_text_ONE_LEADING_AT():
    assert basic_tools.clean_text("@ldsl je tranlfd lfdfd") == "je tranlfd lfdfd"


def test_clean_text_TWO_LEADING_AT():
    assert basic_tools.clean_text("@dllfd @ldsl je tranlfd lfdfd") == "je tranlfd lfdfd"


def test_clean_text_LEADING_AT_AND_IN_THE_MIDDLE():
    assert (
        basic_tools.clean_text("@dllfd @ldsl je @tkfdl tranlfd lfdfd")
        == "je @tkfdl tranlfd lfdfd"
    )


def test_clean_text_SPACES():
    assert (
        basic_tools.clean_text(
            "           @dllfd @ldsl         je @tkfdl tranlfd lfdfd        "
        )
        == "je @tkfdl tranlfd lfdfd"
    )


def test_clean_text_LINKS():
    assert (
        basic_tools.clean_text(
            "@dllfd @ldsl  http://lfdl je @tkfdl tranlfd lfdfd http://lfdl   "
        )
        == "je @tkfdl tranlfd lfdfd"
    )


def test_clean_text_LEADING_LINK():
    assert basic_tools.clean_text("http://lfdl loi") == "loi"


def test_clean_text_LEADING_LINK_AND_AT():
    assert basic_tools.clean_text("http://lfdl @ldld loi") == "loi"


def test_clean_text_LEADING_LINK_AND_AT_IN_THE_END():
    assert basic_tools.clean_text("http://lfdl @ldld loi @ldsl") == "loi @ldsl"


def test_clean_text_EMPTY_STRING_RESULT():
    assert basic_tools.clean_text("@dllfd http://kkf") == ""
