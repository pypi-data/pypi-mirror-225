#!/usr/bin/env python3
from wikipedia import WikipediaPage, search
from typing import List, Dict
import warnings

warnings.filterwarnings('ignore')

class OdinWiki(object):

    def __init__(self):
        self.related_articles: Dict = {}

    def search_article(self, article: str) -> Dict:

        try:
            results: List[str] = search(article)
            for topic in results:
                try:
                    wiki_subject: 'WikipediaPage' = WikipediaPage(topic)
                    self.related_articles[topic] = {'url': wiki_subject.url,
                                                    'title': wiki_subject.title,
                                                    'images': wiki_subject.images,
                                                    'summary': wiki_subject.summary}
                except:
                    pass

        except ConnectionError as e:
            raise ConnectionError(f"[ERROR] Unable to fetch the following {article}") from e

    def get_html_page(self, article: str, path: str):

        try:
            content: str = WikipediaPage(article).html()
            with open(path, 'wt') as f:
                f.write(content)
            f.close()

        except:
            pass

    @property
    def get_related_articles(self):
        return self.related_articles

