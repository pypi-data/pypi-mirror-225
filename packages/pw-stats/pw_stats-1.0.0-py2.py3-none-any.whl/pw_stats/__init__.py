#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pw_stats -- statistics for passwords"""

from .stats import PassowrdStats

__version__: str = "1.0.0"
__all__: tuple[str, ...] = "__version__", "PassowrdStats"
