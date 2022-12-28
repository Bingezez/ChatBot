from googletrans import Translator, LANGUAGES


class Translate:
    def __init__(self):
        self.translator = Translator()
        self.lang = None
        self.translate_text = None

    def _translate(self, text, dest):
        return self.translator.translate(text, dest=dest).text
    
    def translate(self, text):
        self.lang = self.recognition_lang(text)
        if self.lang != 'en':
            self.translate_text = self._translate(text, 'en')
        elif self.lang != 'uk':
            self.translate_text = self._translate(text, 'uk')
        else:
            self.translate_text = 'This language is not supported yet.'
    
    def recognition_lang(self, text):
        return self.translator.detect(text).lang

    def __str__(self) -> str:
        if self.lang == 'en':
            return f'{LANGUAGES[self.lang]}: {self.translate_text}'
        elif self.lang == 'uk':
            return f'{LANGUAGES[self.lang]}: {self.translate_text}'
        else:
            return 'This language is not supported yet.'


if __name__ == '__main__':
    t = Translate()
    t.translate('Привіт')
    print(t)
    t.translate('Hello')
    print(t)
    t.translate('Привет')
    print(t)
