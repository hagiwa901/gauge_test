from getgauge.python import step, before_scenario, Messages
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from getgauge.python import Screenshots
from selenium import webdriver
from selenium.webdriver import ChromeOptions
import chromedriver_binary
import os
from uuid import uuid1
from getgauge.python import custom_screenshot_writer


vowels = ["a", "e", "i", "o", "u"]

options = ChromeOptions()
# options.add_argument("--headless")
options.add_argument("--incognito")
driver = webdriver.Chrome(options=options)


def number_of_vowels(word):
    return len([elem for elem in list(word) if elem in vowels])


# --------------------------
# Gauge step implementations
# --------------------------
@custom_screenshot_writer
def take_screenshot():
    # Use appropriate webdriver instance
    image = driver.get_screenshot_as_png()
    file_name = os.path.join(os.getenv("gauge_screenshots_dir"), "screenshot-{0}.png".format(uuid1().int))
    file = open(file_name, "wb")
    file.write(image)
    return os.path.basename(file_name)

@step("The word <word> has <number> vowels.")
def assert_no_of_vowels_in(word, number):
    assert str(number) == str(number_of_vowels(word))


@step("Vowels in English language are <vowels>.")
def assert_default_vowels(given_vowels):
    Messages.write_message("Given vowels are {0}".format(given_vowels))
    assert given_vowels == "".join(vowels)

@step("Almost all words have vowels <table>")
def assert_words_vowel_count(table):
    actual = [str(number_of_vowels(word)) for word in table.get_column_values_with_name("Word")]
    expected = [str(count) for count in table.get_column_values_with_name("Vowel Count")]
    assert expected == actual

@step("グーグルのサイトを開く")
def assert_words_vowel_count():
    driver.get('https://google.co.jp/')

@step("検索欄に<word>を入力")
def words_input(key_word: str) -> None:
    # Enter "webdriver" text and perform "ENTER" keyboard action
    driver.find_element(By.NAME, "q").send_keys(key_word + Keys.ENTER)

@step("キャプションを撮る")
def take_caption() -> None:
    Screenshots.capture_screenshot()

# ---------------
# Execution Hooks
# ---------------

@before_scenario()
def before_scenario_hook():
    assert "".join(vowels) == "aeiou"
