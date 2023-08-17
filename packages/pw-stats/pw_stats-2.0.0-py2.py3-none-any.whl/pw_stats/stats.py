#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""password stats"""

import math
import re
import typing
import unicodedata
from collections import Counter

from async_lru import alru_cache

REPEAT_REGEX: typing.Final[re.Pattern[str]] = re.compile(
    r"((.+?)\2+)", re.UNICODE | re.DOTALL | re.IGNORECASE
)

sequences: str = (
    "abcdefghijklmnopqrstuvwxyz"  # alphabet
    "qwertyuiopasdfghjklzxcvbnm"  # keyboard
    "~!@#$%^&*()_+-="  # keyboard special, top row
    "01234567890"  # numbers
)
sequences += sequences[::-1]  # reversed


class PasswordStats:
    """password statistics"""

    __password: str

    @property
    def password(self) -> str:
        """password"""

        return self.__password

    def __init__(self, password: str) -> None:
        self.__password = password

    async def alphabet(self) -> set[str]:
        """return the password alphabet"""

        return set(self.password)

    async def alphabet_len(self) -> int:
        """return the password alphabet length"""

        return len(await self.alphabet())

    async def charcat_detailed(self) -> Counter[str]:
        """detailed character categories"""

        return Counter(map(unicodedata.category, self.password))

    async def charcat(self) -> Counter[str]:
        """character categories

        - L letter
        - M mark
        - N number
        - P punctuation
        - S symbol
        - Z separator
        - C other"""

        c: Counter[str] = Counter()

        for cat, n in (await self.charcat_detailed()).items():
            c[cat[0]] += n

        return c

    async def length(self) -> int:
        """get password length"""

        return len(self.password)

    async def letters(self) -> int:
        """Count all letters"""

        return (await self.charcat())["L"]

    async def letters_uppercase(self) -> int:
        """count uppercase letters"""

        return (await self.charcat_detailed())["Lu"]

    async def letters_lowercase(self) -> int:
        """count lowercase letters"""

        return (await self.charcat_detailed())["Ll"]

    async def numbers(self) -> int:
        """count numbers"""

        return (await self.charcat_detailed())["N"]

    async def count(self, *categories: str) -> int:
        """count characters of the specified classes only"""

        return sum(
            int(cat in categories) * n for cat, n in (await self.charcat()).items()
        )

    async def count_except(self, *categories: str) -> int:
        """count characters of all classes except the specified ones"""

        return sum(
            int(cat not in categories) * n for cat, n in (await self.charcat()).items()
        )

    async def special_characters(self) -> int:
        """count special characters"""

        return await self.count_except("L", "N")

    async def combinations(self) -> int:
        """the number of possible combinations with the current alphabet"""

        return (await self.alphabet_len()) ** (await self.length())

    async def entropy_bits(self) -> float:
        """get information entropy bits, log2 of the number of possible passwords"""

        return (await self.length()) * math.log(await self.alphabet_len(), 2)

    async def entropy_density(self) -> float:
        """get information entropy density factor, ranged {0 .. 1}"""

        return math.log(await self.alphabet_len(), await self.length())

    async def strength(
        self,
        weak_bits: int = 30,
        weak_max: float = 1 / 3,
        hard_val: float = 0.950,
        hard_k: float = 3,
    ) -> float:
        """get password strength as a number normalized to range {0 .. 1},
        ( use natural_strength for better accuracy )

        <1/3 weak
        <2/3 medium
        >2/3 strong"""

        eb: float

        if (eb := await self.entropy_bits()) <= weak_bits:
            return weak_max * eb / weak_bits

        return 1 - (1 - weak_max) * (
            2
            ** (
                -(-math.log((1 - hard_val) / (1 - weak_max), 2) / (weak_bits * hard_k))
                * (eb - weak_bits)
            )
        )

    async def repeated_patterns_length(self) -> int:
        """detect and return the length of repeated patterns"""

        return sum(
            len(substring) for substring, _ in REPEAT_REGEX.findall(self.password)
        )

    async def sequences_length(self) -> int:
        """detect and return the length of used sequences

        - alphabet letters abcd...
        - keyboard letters qwerty, etc
        - keyboard special characters in the top row ~!@#$%^&*()_+
        - numbers 0123456"""

        # FIXME optimise

        sequences_length: int = 0
        idx: int = 0

        while idx < len(self.password):
            password: str = self.password[idx:]

            jdx: int = -1
            common_length: int = 1

            while True:
                jdx = sequences.find(password[0], jdx + 1)

                if jdx == -1:
                    break

                common_here: str = ""

                for a, b in zip(password, sequences[jdx:]):
                    if a == b:
                        common_here += a
                    else:
                        break

                common_length = max(common_length, len(common_here))

            if common_length > 2:
                sequences_length += common_length

            idx += common_length

        return sequences_length

    async def weakness_factor(self) -> float:
        """get weakness factor as a float in range {0 .. 1}"""

        return min(
            1.0,
            ((await self.repeated_patterns_length()) + (await self.sequences_length()))
            / (await self.length()),
        )

    async def natural_strength(self) -> float:
        """get natural strength of the password

        <100 weak
        <200 medium
        >200 strong"""

        return max(
            0,
            await self.entropy_bits()
            * await self.strength()
            * (1 - await self.weakness_factor())
            * await self.entropy_density()
            + await self.length()
            + await self.alphabet_len()
            + math.log(
                await self.combinations(),
                max(await self.entropy_bits() * await self.entropy_density(), 2),
            )
            + math.log2(await self.entropy_bits() + 1),
        )


for name, value in PasswordStats.__dict__.items():
    if name[0] != "_" and callable(value):
        setattr(PasswordStats, name, alru_cache()(value))
