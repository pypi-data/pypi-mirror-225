#   ---------------------------------------------------------------------------------
#   Copyright (c) Railtown AI. All rights reserved.
#   Licensed under the MIT License. See LICENSE in project root for information.
#   ---------------------------------------------------------------------------------
from __future__ import annotations
from dotenv import load_dotenv
import os
import railtownai


def test_integration_log():
    load_dotenv()

    railtownai.init(os.getenv("RAILTOWN_API_KEY"))

    error_message = None
    try:
        continuous_integration_error()

    except Exception as e:
        error_message = str(e)
        railtownai.log(e, environment="continuous_integration")

    assert error_message == "name 'continuous_integration_error' is not defined"
