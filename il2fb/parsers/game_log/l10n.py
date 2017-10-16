# coding: utf-8

import os

from verboselib.factory import TranslationsFactory


__here__ = os.path.abspath(os.path.dirname(__file__))

locale_dir = os.path.join(__here__, "locale")
translations = TranslationsFactory("il2fb-game-log-parser", locale_dir)
