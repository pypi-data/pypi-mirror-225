"""
Checks and tests for the following:
 - Connecting to DGG chat
 - (more to come whenever I think of more)
"""

import threading
import time

from dggbot import DGGChat

import pytest

checks = {"connection": False}


class TestChat(DGGChat):
    def _on_open(self, ws):
        super()._on_open(ws)
        checks["connection"] = True


chat = TestChat()


@pytest.mark.order(0)
def test_connection():
    t = threading.Thread(target=chat.run)
    t.start()
    time.sleep(5)
    assert all(v for v in checks.values())





@pytest.mark.order(after="test_connection")
def test_other():
    chat.ws.close()
    assert "A" in "abefeasfAfaefm"
