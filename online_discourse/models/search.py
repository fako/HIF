import os
from collections import OrderedDict

import spacy
from spacy_arguing_lexicon import ArguingLexiconParser
from sklearn.feature_extraction.text import CountVectorizer

from core.models.organisms import Community, Collective, Individual
from core.models.organisms.states import CommunityState
from core.utils.helpers import cross_combine
from online_discourse.discourse import configurations


class DiscourseSearchCommunity(Community):

    COMMUNITY_SPIRIT = OrderedDict([
        ("search", {
            "process": "HttpResourceProcessor.fetch_mass",
            "input": None,
            "contribute": "Append:ExtractProcessor.extract_from_resource",
            "output": "Collective#url",
            "config": {
                "_args": ["$.query", "$.quantity"],
                "_kwargs": {},
                "_resource": "GoogleText",
                "_objective": {
                    "@": "$.items",
                    "#term": "$.queries.request.0.searchTerms",
                    "title": "$.title",
                    "url": "$.link"
                },
                "_continuation_limit": 10,
                "_interval_duration": 1000
            },
            "schema": {},
            "errors": {},
        }),
        ("download", {
            "process": "HttpResourceProcessor.fetch_mass",
            "input": "@search",
            "contribute": "Update:ExtractProcessor.extract_from_resource",
            "output": "@search",
            "config": {
                "_args": ["$.url"],
                "_kwargs": {},
                "_resource": "WebTextResource",
                "_objective": {  # objective uses properties added to the soup by WebTextResource
                    "#url": "soup.source",
                    "#paragraph_groups": "soup.paragraph_groups",
                    "#author": "soup.find('meta', attrs={'name':'author'}).get('content') if soup.find('meta', attrs={'name':'author'}) else None"
                },
                "_update_key": "url",
                "$language": "en"
            },
            "schema": {},
            "errors": {},
        })
    ])

    COMMUNITY_BODY = [
        {
            "process": "FilterProcessor.distinct",
            "config": {
                "distinct_key": "url"
            }
        },
        {
            "name": "rank",
            "process": "OnlineDiscourseRankProcessor.default_ranking",
            "config": {
                "$result_size": 60,
                "ranking_feature": "argument_score",
                "identifier_key": "url",
                "feature_frame_path": None,
                "$keywords": []
            }
        }
    ]

    SPACY_PACKAGES = {
        "en": "en_core_web_md",
        "nl": "nl_core_news_sm"
    }

    def initial_input(self, *args):
        configuration = getattr(configurations, args[0])
        combinations = cross_combine(
            configuration.singular_subjects + configuration.plural_subjects,
            configuration.descriptive_adjectives
        )
        collective = Collective.objects.create(community=self, schema={})
        for terms in combinations:
            Individual.objects.create(
                community=self,
                collective=collective,
                properties={
                    "terms": "+".join(terms),
                    "query": " AND ".join(
                        [
                            '"{}"'.format(term) if not term.startswith("~") else term
                            for term in terms
                        ]
                    ),
                    "quantity": 10
                }
            )
        return collective

    def begin_download(self, inp):
        for individual in inp.individual_set.all():
            if individual.properties.get("url", "").endswith("pdf"):
                individual.delete()

    def finish_download(self, out, err):

        nlp = spacy.load(self.SPACY_PACKAGES[self.config.language])
        nlp.add_pipe(ArguingLexiconParser(lang=nlp.lang))

        for individual in out.individual_set.iterator():

            argument_count = 0
            sents_count = 0
            paragraph_groups = individual.properties.get("paragraph_groups", [])
            if not paragraph_groups:
                continue
            text = ""
            for paragraph_group in paragraph_groups:
                for doc in nlp.pipe(paragraph_group):
                    sents_count += len(list(doc.sents))
                    argument_spans = list(doc._.arguments.get_argument_spans())
                    argument_count += len(argument_spans)
                text += " ".join(paragraph_group) + " "
            if not text.trim():
                continue
            if sents_count:
                individual.properties["argument_score"] = argument_count / sents_count
            vectorizer = CountVectorizer()
            text_vector = vectorizer.fit_transform([text])[0].toarray().tolist()[0]
            individual.properties["word_count"] = {
                word: count
                for word, count in zip(vectorizer.get_feature_names(), text_vector) if count >= 3
            }
            individual.clean()
            individual.save()

    def set_kernel(self):
        self.kernel = self.current_growth.output

    def get_feature_frame_file(self):
        return os.path.join(self._meta.app_label, "data", "feature_frames", self.signature + ".pkl")

    def before_rank_manifestation(self, manifestation_part):
        manifestation_part["config"]["feature_frame_path"] = self.get_feature_frame_file()

    def store_feature_frame(self):
        assert self.state == CommunityState.READY, "Can't store a frame for a Community that is not ready"
        path, file_name = os.path.split(self.get_feature_frame_file())
        if not os.path.exists(path):
            os.makedirs(path)

        part = next((part for part in self.COMMUNITY_BODY if part.get("name") == "rank"), None)
        if part is None:
            raise TypeError("No RankProcessor part found in COMMUNITY_BODY")
        rank_processor, method, args_type = self.prepare_process(part["process"], class_config=part.get("config"))
        rank_processor.feature_frame.load_content(lambda: self.kernel.content)
        rank_processor.feature_frame.to_disk(self.get_feature_frame_file())

    class Meta:
        verbose_name = "Discourse search community"
        verbose_name_plural = "Discourse search communities"
