import os
from llama import LLMEngine, setup_config
import unittest

from llama.program.util.config import edit_config, get_config
from llama.program.util.run_ai import get_url_and_key
from llama.program.util.config import reset_config


class TestConfig(unittest.TestCase):
    def test_config(self):
        self.__llm_and_test("test_config")

    def test_setup(self):
        self.__setup_and_test("test_setup")

    def test_edit(self):
        self.__edit_and_test("test_edit")
        self.__edit_and_test("test_edit2")

    def test_config_complex_ordering(self):
        self.__llm_and_test("llm")
        self.__llm_and_test("llm2")
        self.__edit_and_test("edit")
        self.__setup_and_test("setup")
        self.__llm_and_test("llm3")
        self.__llm_and_test("llm4")
        self.__edit_and_test("edit3")

    def test_edit_url(self):
        self.__edit_and_test_url("test_edit", "test_url")
        self.__edit_and_test_url("test_edit2", "test_url2")

    def test_edit_url_local(self):
        self.__edit_and_test_url_local("test_edit", "test_url")
        self.__edit_and_test_url_local("test_edit2", "test_url2")

    def test_get_url_and_key_no_setup(self):
        environment = os.environ.get("LLAMA_ENVIRONMENT")
        del os.environ["LLAMA_ENVIRONMENT"]
        try:
            print(get_config())
            print(get_url_and_key())
            passing = False
        except BaseException:
            passing = True
        finally:
            os.environ["LLAMA_ENVIRONMENT"] = environment
            assert passing

    def test_get_url_and_key(self):
        environment = os.environ.get("LLAMA_ENVIRONMENT")
        del os.environ["LLAMA_ENVIRONMENT"]
        try:
            setup_config({"production.key": "test"})
            edit_config({"production.key": "test2", "production.url": "url2"})
            print(get_config())

            key, url = get_url_and_key()
            print(get_url_and_key())

            assert url == "url2"
            assert key == "test2"
            passing = True
        except BaseException:
            passing = False
        finally:
            os.environ["LLAMA_ENVIRONMENT"] = environment
            assert passing

    def __edit_and_test(self, val: str):
        edit_config({"production.key": val})
        config = get_config()
        assert config["production.key"] == val

    def __edit_and_test_url(self, key: str, url: str):
        edit_config({"production.key": key, "production.url": url})
        config = get_config()
        assert config["production.key"] == key
        assert config["production.url"] == url

    def __edit_and_test_url_local(self, key: str, url: str):
        edit_config({"local.key": key, "local.url": url})
        config = get_config()
        assert config["local.key"] == key
        assert config["local.url"] == url

    def __setup_and_test(self, val: str):
        setup_config({"production.key": val})
        config = get_config()
        assert config["production.key"] == val

    def __llm_and_test(self, val: str):
        LLMEngine(id="test_random", config={"production.key": val})
        config = get_config()
        assert config["production.key"] == val

    def tearDown(self):
        reset_config()
