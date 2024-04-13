from __future__ import annotations

from typing import Any, List

from langchain_text_splitters.base import TextSplitter
import spacy
from spacy.language import Language
from spacy_language_detection import LanguageDetector

class SpacyTextSplitter(TextSplitter):
    def __init__(
        self,
        separator: str = "\n\n",
        max_length: int = 1_000_000,
        language: str = "en",
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self._separator = separator
        self.max_length = max_length
        self.language = language
        # Load the appropriate model for the given language
        self._tokenizer = self._load_spacy_model(language)

    def _load_spacy_model(self, language: str) -> Any:
        # Map the detected language to its full SpaCy model name
        language_model_map = {
            'en': 'en_core_web_sm',
            'fr': 'fr_core_news_sm',
            'es': 'es_core_news_sm',
            'de': 'de_core_news_sm',
            'it': 'it_core_news_sm',
            'uk': 'uk_core_news_sm',
            'ru': 'ru_core_news_sm',
            'zh': 'zh_core_web_sm',
            'ja': 'ja_core_news_sm',
            'xx': 'xx_ent_wiki_sm'
        }
        # Use the full model name if a language code is provided
        if language in language_model_map:
            pipeline = language_model_map[language]
            # Load the appropriate model for the detected language
            tokenizer = spacy.load(pipeline, exclude=["ner", "tagger"])
            tokenizer.max_length = self.max_length # Use self.max_length here
        else:
            # Fallback to English if the language is not supported
            tokenizer = spacy.load("en_core_web_sm", exclude=["ner", "tagger"])
            tokenizer.max_length = self.max_length # Use self.max_length here
        return tokenizer

    def split_text(self, text: str) -> List[str]:
        splits = (s.text for s in self._tokenizer(text).sents)
        return self._merge_splits(splits, self._separator)