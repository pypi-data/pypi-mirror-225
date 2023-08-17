#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pw_stats -- statistics for passwords"""

from .stats import PasswordStats

__version__: str = "2.0.0"
__all__: tuple[str, ...] = "__version__", "PasswordStats"
