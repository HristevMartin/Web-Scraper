from config import API_KEY


import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def is_valid_image_url(url):
    try:
        response = requests.get(url, headers=headers, stream=True)
        content_type = response.headers.get('content-type')

        # Validate the content type
        if 'image' not in content_type:
            return False
        return True
    except Exception as ex:
        print(ex)
        return False

def translate_text(text, source_language='bg', target_language='en'):
    endpoint = 'https://translation.googleapis.com/language/translate/v2'
    params = {
        'q': text,
        'source': source_language,
        'target': target_language,
        'key': API_KEY
    }

    response = requests.post(endpoint, data=params)

    if response.status_code != 200:
        print("Error:", response.status_code)
        print(response.text)
        raise Exception('Error occurred while calling endpoint')

    result = response.json()

    return result['data']['translations'][0]['translatedText']


def is_complete_sentence(text):
    # Split the text into words
    words = text.split()

    # A simple check: a complete sentence should have at least 3 words
    if len(words) < 3:
        return False

    # Another check: the sentence should end with a punctuation mark
    if not any(text.endswith(punct) for punct in [".", "!", "?"]):
        return False

    return True


def get_image_urls_from_detail_page(url, element, class_element):
    response = requests.get(url, headers=headers)
    page_content = response.content
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(page_content, 'html.parser')
    image_detail_path = soup.find(element, class_=class_element)

    if class_element == 'owl-stage':
        return image_detail_path, soup
    else:
        return image_detail_path


