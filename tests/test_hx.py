import shlex
import subprocess
import time
from pathlib import Path

import pytest
from playwright.sync_api import Page, expect

PORT = 5002
APP_PATH = Path(__file__).parent.parent.resolve().absolute()
APP_NAME = "main_hx.py"


# https://www.stefsmeets.nl/posts/streamlit-pytest/
@pytest.fixture(scope="function", autouse=True)
def run_webserver(monkeypatch: pytest.MonkeyPatch):
    """Run the app."""

    monkeypatch.chdir(APP_PATH)
    cmd = f"python {APP_NAME}"
    args = shlex.split(cmd)
    p = subprocess.Popen(args)

    time.sleep(10)  # give server some time to start
    yield
    p.kill()


def test_example(page: Page) -> None:
    page.goto(f"http://localhost:{PORT}/")

    expect(page.get_by_role("main")).to_match_aria_snapshot(
        '- main:\n  - heading "DataFrame editor" [level=1]\n  - table:\n    - rowgroup:\n      - row "Name Age City":\n        - columnheader "Name"\n        - columnheader "Age"\n        - columnheader "City"\n    - rowgroup:\n      - row:\n        - cell:\n          - textbox "Alice"\n        - cell:\n          - textbox /\\d+/\n        - cell:\n          - textbox "New York"\n      - row:\n        - cell:\n          - textbox "Bob"\n        - cell:\n          - textbox /\\d+/\n        - cell:\n          - textbox "Los Angeles"\n      - row:\n        - cell:\n          - textbox "Charlie"\n        - cell:\n          - textbox /\\d+/\n        - cell:\n          - textbox "Chicago"\n  - button "save"'
    )

    page.get_by_role("textbox", name="Alice").click()
    page.get_by_role("textbox", name="Alice").fill("a")
    page.get_by_role("textbox", name="25").click()
    page.get_by_role("textbox", name="25").fill("2")
    page.get_by_role("textbox", name="New York").click()
    page.get_by_role("textbox", name="New York").fill("y")
    page.get_by_role("button", name="save").click()

    expect(page.get_by_role("main")).to_match_aria_snapshot(
        '- main:\n  - heading "DataFrame editor" [level=1]\n  - table:\n    - rowgroup:\n      - row "Name Age City":\n        - columnheader "Name"\n        - columnheader "Age"\n        - columnheader "City"\n    - rowgroup:\n      - row:\n        - cell:\n          - textbox "a"\n        - cell:\n          - textbox "2"\n        - cell:\n          - textbox "y"\n      - row:\n        - cell:\n          - textbox "Bob"\n        - cell:\n          - textbox /\\d+/\n        - cell:\n          - textbox "Los Angeles"\n      - row:\n        - cell:\n          - textbox "Charlie"\n        - cell:\n          - textbox /\\d+/\n        - cell:\n          - textbox "Chicago"\n  - button "save"'
    )
