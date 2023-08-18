from llama import Type, Context, LLMEngine

import unittest


class TestFeedback(unittest.TestCase):
    def test_feedback(self):
        class Tweet(Type):
            tweet: str = Context(
                "A viral tweet. Text that really catches the eye of the readers and surprises them, both in terms of format and actual content"
            )
            likes: int = Context("likes the tweet gets")
            retweets: int = Context("retweets the tweet gets")

        class User(Type):
            username: str = Context("a user's handle on twitter")

        def get_tweet_data():
            return [
                [
                    User(username="syswarren"),
                    Tweet(
                        tweet="Tools aren't going to make you great designers. Your way of thinking, attention to detail, and ability to see the bigger picture will.",
                        likes=1000,
                        retweets=81,
                    ),
                ],
                [
                    User(username="TheJackForge"),
                    Tweet(
                        tweet="I don't like telling people how to live their lives, but you should probably learn how to use Figma.",
                        likes=341,
                        retweets=28,
                    ),
                ],
                [
                    User(username="iamharaldur"),
                    Tweet(
                        tweet="Remember when we had the mental energy to hate a new logo?",
                        likes=1000,
                        retweets=59,
                    ),
                ],
                [
                    User(username="lexfridman"),
                    Tweet(
                        tweet="ChatGPT puts a mirror to humanity.",
                        likes=11100,
                        retweets=874,
                    ),
                ],
                [
                    User(username="iamaaronwill"),
                    Tweet(
                        tweet="I had to make you uncomfortable otherwise you would never have moved. - The Universe",
                        likes=4000,
                        retweets=1000,
                    ),
                ],
            ]

        llm = LLMEngine(id="feedback")

        example_tweet = llm(User(username="lawrencekingyo"), output_type=Tweet)

        print("tweet before data", example_tweet)

        llm.add_data(get_tweet_data())

        example_tweet = llm(User(username="lawrencekingyo"), output_type=Tweet)

        print("tweet before feedback", example_tweet)

        llm.improve(on="tweet", to="have more {likes}")
        llm.improve(on="tweet", to="have over 100 {retweets}")

        llm.improve(on="tweet", to="have no hashtags")

        max_retweets = 0
        rounds = 2

        for i in range(rounds):
            tweet_after_feedback = llm(
                User(username="lawrencekingyo"), output_type=Tweet
            )
            if tweet_after_feedback.retweets > max_retweets:
                best_tweet = tweet_after_feedback
                max_retweets = tweet_after_feedback.retweets

        print(f"tweet after {rounds} rounds of feedback", tweet_after_feedback)
