import importlib
from typing import Dict


class Translator:
    _instances: Dict[str, 'Translator'] = {}

    def __init__(self, locale: str, locale_path: str = 'locale'):
        self.locale = locale
        self.locale_path = locale_path.rstrip('/').replace('/', '.')

    def t(self, key: str, **kwargs) -> str:  # type: ignore
        file_key, *translation_keys = key.split('.')
        locale_module = importlib.import_module(
            f'{self.locale_path}.{self.locale}.{file_key}')

        translation = locale_module.locale
        for translation_key in translation_keys:
            translation = translation.get(translation_key, None)
            if translation is None:
                return f'Key {key} not found in {self.locale} locale'
        if kwargs.keys():
            translation = translation.format(**kwargs)

        return translation  # type: ignore
