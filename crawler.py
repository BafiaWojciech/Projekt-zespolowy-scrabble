import requests
from bs4 import BeautifulSoup


def is_word_correct(word):
    url = "https://sjp.pl/" + word
    response = requests.get(url)
    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, "html.parser")
        if soup.find("body").find("p").text == "dopuszczalne w grach (i) ":
            return True
    return False


print("abecadło:",is_word_correct("abecadło"))
print("echo:",is_word_correct("echo"))
print("szkopuł:",is_word_correct("szkopuł"))
print("przedsięwziął:",is_word_correct("przedsięwziął"))
print("kartkującym:",is_word_correct("kartkującym"))
