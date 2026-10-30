#!/bin/sh
exec python3 -m pytest .github/tests -x --tb=short
