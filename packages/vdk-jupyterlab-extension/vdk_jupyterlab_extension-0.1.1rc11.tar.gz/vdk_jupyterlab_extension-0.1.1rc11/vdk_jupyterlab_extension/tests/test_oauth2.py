# Copyright 2021-2023 VMware, Inc.
# SPDX-License-Identifier: Apache-2.0
from vdk_jupyterlab_extension.handlers import OAuth2Handler


def test_fix_redirect_uri():
    assert (
        OAuth2Handler._fix_localhost("http://localhost?foo=bar") == "http://127.0.0.1"
    )
    assert (
        OAuth2Handler._fix_localhost("http://localhost:8888?foo=bar")
        == "http://127.0.0.1:8888"
    )
    assert (
        OAuth2Handler._fix_localhost("http://something?foo=bar") == "http://something"
    )
    assert (
        OAuth2Handler._fix_localhost("http://something:9999?foo=bar")
        == "http://something:9999"
    )
    assert (
        OAuth2Handler._fix_localhost("http://something:9999") == "http://something:9999"
    )
