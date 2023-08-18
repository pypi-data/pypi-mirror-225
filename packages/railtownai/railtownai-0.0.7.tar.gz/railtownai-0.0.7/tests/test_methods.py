#   ---------------------------------------------------------------------------------
#   Copyright (c) Railtown AI. All rights reserved.
#   Licensed under the MIT License. See LICENSE in project root for information.
#   ---------------------------------------------------------------------------------
from __future__ import annotations

import requests_mock
from railtownai import log, get_config


def test_get_config():
    assert get_config()["u"] == "jaime-dev.railtownlogs.com"


def test_log():
    with requests_mock.Mocker() as m:
        m.post("https://jaime-dev.railtownlogs.com", json={"status": "success"})
        log("Test error", foo="bar")
        assert m.call_count == 1
