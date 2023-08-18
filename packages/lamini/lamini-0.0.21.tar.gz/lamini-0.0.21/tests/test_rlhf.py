from llama import Type, Context, LLMEngine

from llama.program.util.run_ai import query_get_models

import unittest
import time
import datetime


class Tweet(Type):
    tweet: str = Context("a viral tweet")
    likes: int = Context("likes the tweet gets")
    retweets: int = Context("retweets the tweet gets")


class User(Type):
    username: str = Context("A user's handle on twitter")


class TestRLHF(unittest.TestCase):
    def test_rlhf(self):
        llm = LLMEngine(id="tweets", model_name="hf-internal-testing/tiny-random-gpt2")

        llm.add_data(get_tweet_data())

        llm.improve(
            on="tweet",
            to="make it shorter",
            good_examples=[
                Tweet(
                    tweet="Solopreneurs, don't chase more clients - it's a beast that'll destroy you. ",
                    likes=45,
                    retweets=10,
                )
            ],
            bad_examples=[
                Tweet(
                    tweet="They tell you to chase more clients. If you're a Solopreneur providing a professional service, you're feeding a beast that will destroy you. Your goal is not MORE clients. Your goal is BETTER clients. 2-3 great clients could set you for life. I'll tell you why and what to do.",
                    likes=5,
                    retweets=1,
                )
            ],
        )

        start_time = datetime.datetime.now()
        usernames = [
            "StarlightDreamer",
            "TechGeekster",
            "WanderlustXplorer",
            "NinjaWarrior21",
            "PixelPerfectionist",
            "LunaGlimmer",
            "ThunderStorm88",
            "HappyDoodleBug",
            "CosmicScribbler",
            "AquaSerenade",
            "SpiritWhisperer",
        ]

        job = llm.submit_inference_job(
            input=[User(username=username) for username in usernames],
            output_type=Tweet,
            random=True,
            rlhf=True,
            generate_finetuning_data=True,
            replace_with_finetune_model=False,
        )

        print("Launched job", job)

        status = llm.get_inference_job_status(job["job_id"])
        assert status["status"] not in ("NOT_SCHEDULED", "ERRORED")

        while status["status"] != "DONE":
            print(f"job not done. waiting... {status}")
            time.sleep(10)
            status = llm.get_inference_job_status(job["job_id"])
            assert status["status"] not in ("ERRORED", "CANCELED")
        status = llm.get_inference_job_status(job["job_id"])
        print(status)
        result = llm.get_inference_job_results(job["job_id"], output_type=Tweet)
        print(result)

        if "generation_job_id" in status:
            generation_job_id = status["generation_job_id"]
            status = llm.get_inference_job_status(generation_job_id)
            while status["status"] != "DONE":
                print(f"generation job not done. waiting... {status}")
                time.sleep(10)
                status = llm.get_inference_job_status(generation_job_id)
                assert status["status"] not in ("ERRORED", "CANCELED")
            status = llm.get_inference_job_status(generation_job_id)
            print(status)

        assert "training_job_id" in status
        training_job_id = status["training_job_id"]
        llm.training_job_id = training_job_id
        while datetime.datetime.now() - start_time < datetime.timedelta(minutes=10):
            status = llm.get_training_job_status(training_job_id)
            assert status["status"] not in ("FAILED", "CANCELLED")
            if status["status"] == "COMPLETED":
                break
            print(f"training job not done. waiting... {status}")
            time.sleep(10)
        trained_model = status["model_name"]

        self.assertTrue(trained_model is not None)

        result = llm(
            input=User(username="lawrencekingyo"),
            output_type=Tweet,
            replace_with_finetune_model=True,
        )


def get_model(type_signature: str):
    models = query_get_models({"type_signature": type_signature})

    if len(models) > 0:
        return models[0]

    return None


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
        [
            User(username="laminiai"),
            Tweet(
                tweet="Taylor Swift is in the Bay!",
                likes=1000,
                retweets=81,
            ),
        ],
        [
            User(username="elonmusk"),
            Tweet(
                tweet="We have liftoff!",
                likes=341,
                retweets=28,
            ),
        ],
        [
            User(username="joerogan"),
            Tweet(
                tweet="New research puts age of universe at 26.7 billion years, nearly twice as old as previously believed",
                likes=1000,
                retweets=59,
            ),
        ],
        [
            User(username="realSharonZhou"),
            Tweet(
                tweet="""A course on finetuning LLMs coming to you!!

So you can build your own private custom LLMs, eg. on 
@MetaAI
 Llama2

🚢 Ship your own LLM
🚢 Get shipped a stuffed llama (maybe)

Sneak peek of us with 🦙s here:""",
                likes=11100,
                retweets=874,
            ),
        ],
        [
            User(username="karpathy"),
            Tweet(
                tweet="The hottest new programming language is English",
                likes=4000,
                retweets=1000,
            ),
        ],
    ]
