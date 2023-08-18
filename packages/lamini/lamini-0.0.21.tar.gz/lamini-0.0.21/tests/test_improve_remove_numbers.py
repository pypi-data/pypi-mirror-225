from statistics import mean

from llama import LLMEngine

from llama import Type, Context

from typing import List, Dict

import unittest

import yaml


class TestImproveRemoveNumbers(unittest.TestCase):
    def test_improve_remove_numbers(self):
        MIN_LENGTH = 50
        MAX_LENGTH = 70

        class KeywordImportanceScores(Type):
            keyword: str = Context(
                "Ranked keywords cluster are the terms and phrases that are most relevant to a given page or website. The most ranked keywords for a given page are those that are most relevant to the content of the page, as determined by search engine algorithms."
            )
            keyword_importance: float = Context(
                "Keyword importance helps weights of each keyword cluster based on how valuable is it to optimize for that cluster.The score range is [0 - 100], where 0 represents the lowest possible score and 100 represents the highest possible score."
            )

        class RankedKeywordData(Type):
            market_share: float = Context(
                """Market share in SEO is the percentage of overall search engine traffic that a website receives compared to other websites. It is an important factor in determining the visibility of a website in search engine results. Market share is a metric that helps identify which websites have the most influence in the search engine landscape.Percent Range:The score range is [0 - 100], where 0 represents the lowest possible score and 100 represents the highest possible score."""
            )
            keyword_importance: float = Context(
                "Keyword importance helps weights of each keyword cluster based on how valuable is it to optimize for that cluster.The score range is [0 - 100], where 0 represents the lowest possible score and 100 represents the highest possible score."
            )
            element_relevance_score: float = Context(
                "Semantic relevance of a keyword to the element on a webpage."
            )

        class KeywordData(Type):
            __root__: Dict[str, RankedKeywordData]

        class RankedKeyword(Type):
            ranked_keywords: KeywordData = Context(
                "List of the higly ranked keyword cluster for given customer page with it's content relevance scores data"
            )

        class Data(Type):
            tag_text: str = Context("HTML page element content")
            ranked_keywords: KeywordData = Context(
                "List of the higly ranked keyword cluster for given customer page with it's content relevance scores data"
            )

        class MetaElements(Type):
            title: Data = Context(
                """Title tag is used to provide a brief description of the page's content"""
            )
            h1: Data = Context(
                "H1 Tag: H1 tag is used to denote the main heading of a webpage"
            )
            meta_description: Data = Context(
                "The meta description tag is used to provide a short summary of the page's content."
            )

        class MetaData(Type):
            type: str = Context("Type of Page i.e Customer URL/ Competitor URL")
            brand: str = Context(
                "Brand Name from the URL that represents customer/ competitor domain"
            )
            meta_elements: MetaElements = Context(
                """Tag Elements in Meta Group are [Title, Meta Description, H1].
                                Title and H1 are two of the most important elements for generating new page titles.
                                H1 Tag: H1 tag is used to denote the main heading of a webpage.
                                Title Tag: Title tag is used to provide a brief description of the page's content.
                                Meta Description Tag: The meta description tag is used to provide a short summary of the page's content."""
            )
            headings: Dict[str, RankedKeyword] = Context(
                """Top 20 List Page headings with the content relevance score, ranked keywords & the market share data"""
            )

        class URLNme(Type):
            __root__: Dict[str, MetaData] = Context(
                "List of [Title, Heading H1, Meta Description] elements for the customer page.A competitor page is a webpage that competes with your customer page for search engine rankings. The customer html elements can be used to get an idea of how the customer page content might look."
            )

        # input (relies on the above)

        class CustomerInfo(Type):
            url: str = Context("Customer URL")
            html_elements: URLNme = Context(
                "List of [Title, Heading H1, Meta Description] elements for the customer page.A competitor page is a webpage that competes with your customer page for search engine rankings. The customer html elements can be used to get an idea of how the customer page content might look."
            )
            ranked_keywords: List[KeywordImportanceScores] = Context(
                "Ranked keywords cluster are the terms and phrases that are most relevant to a given page or website. The most ranked keywords for a given page are those that are most relevant to the content of the page, as determined by search engine algorithms with keyword importance score.The score range is [0 - 100], where 0 represents the lowest possible score and 100 represents the highest possible score."
            )

        # output

        class Recommendations_Meta(Type):
            title: str = Context(
                f"a {MIN_LENGTH}-{MAX_LENGTH} character title tag with high seo without using brand names for competitors"
            )
            score: float = Context("Score for Suggested Page Title")

        class Numbers_Recommendations_Meta(Type):
            title: str = Context(f"Suggested Page Title with numbers")
            h1: str = Context("Suggested Page H1 with numbers")
            meta_description: str = Context(
                "Suggested Page Meta Description with numbers"
            )
            score: float = Context(
                "Combined score for a complete set of (Title, H1, Meta Description)"
            )

        def create_ranked_keyword_data(ranked_keyword_data):
            return RankedKeywordData(
                market_share=ranked_keyword_data["market_share"],
                keyword_importance=ranked_keyword_data["keyword_importance"],
                element_relevance_score=ranked_keyword_data["element_relevance_score"],
            )

        def create_keyword_data(keyword_data):
            keyword_data = (
                keyword_data["ranked_keywords"]
                if "ranked_keywords" in keyword_data
                else {}
            )
            return KeywordData(
                __root__={
                    keyword: create_ranked_keyword_data(ranked_keyword_data)
                    for keyword, ranked_keyword_data in keyword_data.items()
                }
            )

        def create_data(data):
            tag_text = data["tag_text"] if "tag_text" in data else ""
            return Data(tag_text=tag_text, ranked_keywords=create_keyword_data(data))

        def create_meta_elements(meta_elements):
            return MetaElements(
                title=create_data(meta_elements["title"]),
                h1=create_data(meta_elements["h1"]),
                meta_description=create_data(meta_elements["meta_description"]),
            )

        def create_ranked_keyword(ranked_keywords):
            return RankedKeyword(ranked_keywords=create_keyword_data(ranked_keywords))

        def create_headings(headings):
            return {
                heading: create_ranked_keyword(ranked_keywords["ranked_keywords"])
                for heading, ranked_keywords in headings.items()
            }

        def create_metadata(metadata):
            return MetaData(
                type=metadata["type"],
                brand=metadata["brand"],
                meta_elements=create_meta_elements(metadata["meta_elements"]),
                headings=create_headings(metadata["headings"]),
            )

        def create_urlnme_dict(html_elements):
            return {
                url: create_metadata(metadata)
                for url, metadata in html_elements.items()
            }

        def create_ranked_keywords(ranked_keywords):
            ranked_keywords = [
                {key.lower(): value for key, value in ranked_keyword.items()}
                for ranked_keyword in ranked_keywords
            ]
            return [
                KeywordImportanceScores(
                    keyword=ranked_keyword["keyword"],
                    keyword_importance=ranked_keyword["keyword_importance"],
                )
                for ranked_keyword in ranked_keywords
            ]

        def get_metadata(meta_elements):
            title = ""
            score = 0.0
            title_datum = meta_elements["title"]
            if title_datum:
                title = title_datum["tag_text"]
                scores = [
                    keyword_scores["element_relevance_score"]
                    for keyword_scores in title_datum["ranked_keywords"].values()
                ]
                if scores:
                    score = mean(scores) / 100
            metadata = Recommendations_Meta(title=title, score=score)
            return metadata

        def get_datum(customer_info):
            customer_url = customer_info["url"]
            html_elements = {}
            if "html_elements" in customer_info:
                html_elements = create_urlnme_dict(customer_info["html_elements"])
            html_elements = URLNme(__root__=html_elements)
            ranked_keywords = []
            if "ranked_keywords" in customer_info:
                ranked_keywords = create_ranked_keywords(
                    customer_info["ranked_keywords"]
                )
            metadata = get_metadata(
                customer_info["html_elements"][customer_url]["meta_elements"]
            )
            customer_info = CustomerInfo(
                url=customer_url,
                html_elements=html_elements,
                ranked_keywords=ranked_keywords,
            )
            datum = [customer_info, metadata]
            return datum

        def get_data(indices=[], suffix="json"):
            data = []
            for i in indices:
                with open(f"data/quattr/coursera/{i}.{suffix}") as data_file:
                    customer_info = yaml.safe_load(data_file)
                    datum = get_datum(customer_info)
                    data.append(datum)
            return data

        llm = LLMEngine(id="Quattr Feb 20th scored model walkthrough")

        test_indices = [215]
        test_data = get_data(test_indices)
        customer_info = test_data[0][0]

        good_example = Numbers_Recommendations_Meta(
            title="Best Personal Development Courses Online | Coursera",
            h1="Personal Development",
            meta_description="Advance your career in Personal Development with Coursera. We partner with top universities and companies to offer Personal Development courses, certificates and degrees to help you achieve your career goals.",
            score=0.6867798548331712,
        )
        bad_example = Numbers_Recommendations_Meta(
            title="Five Best Personal Development Courses Online [2023] | Coursera",
            h1="5 Personal Development Courses in 2023",
            meta_description="Advance your career in Personal Development with Coursera. We partner with 20 top universities and companies to offer Personal Development courses, certificates and degrees to help you achieve your career goals in 2023.",
            score=0.6867798548331712,
        )

        full_header_metadata = llm(
            input=customer_info,
            output_type=Numbers_Recommendations_Meta,
            random=True,
            score="score",
        )
        print(f"unimproved url={customer_info.url}", full_header_metadata)

        prompt = "avoid numbers and digits, e.g. the number 4 or 7"
        llm.improve(
            on="title",
            to=prompt,
            good_examples=[good_example],
            bad_examples=[bad_example],
        )
        llm.improve(
            on="h1",
            to=prompt,
            good_examples=[good_example],
            bad_examples=[bad_example],
        )
        llm.improve(
            on="meta_description",
            to=prompt,
            good_examples=[good_example],
            bad_examples=[bad_example],
        )
        full_header_metadata_improved = llm(
            input=customer_info,
            output_type=Numbers_Recommendations_Meta,
            random=True,
            score="score",
        )
        print(f"improved url={customer_info.url}", full_header_metadata_improved)

        if any(c.isdigit() for c in full_header_metadata_improved.title):
            assert (
                full_header_metadata_improved.title != full_header_metadata.title
            ), "title fails"
        if any(c.isdigit() for c in full_header_metadata_improved.h1):
            assert (
                full_header_metadata_improved.h1 != full_header_metadata.h1
            ), "h1 fails"
        if any(c.isdigit() for c in full_header_metadata_improved.meta_description):
            assert (
                full_header_metadata_improved.meta_description
                != full_header_metadata.meta_description
            ), "meta fails"
