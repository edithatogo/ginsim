from tests.e2e.remote_app_cases import REMOTE_SMOKE_CASES


def test_remote_smoke_cases_have_unique_sidebar_labels() -> None:
    labels = [case.sidebar_label for case in REMOTE_SMOKE_CASES]
    assert len(labels) == len(set(labels))


def test_remote_smoke_cases_with_actions_define_wait_text() -> None:
    for case in REMOTE_SMOKE_CASES:
        if case.action_button is not None:
            assert case.expected_text
