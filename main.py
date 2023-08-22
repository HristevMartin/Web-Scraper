from db import mydb
from utils import translate_text, is_complete_sentence, is_valid_image_url, get_image_urls_from_detail_page

base_url = 'https://m.imot.bg/results'

try:
    mycursor = mydb.cursor()

    max_pages = 3

    building_info = []

    for page_num in range(1, max_pages + 1):
        print(f"Scraping page {page_num}...")
        current_url = f"{base_url}?page={page_num}"

        image_detail_path = get_image_urls_from_detail_page(current_url, 'div', 'photo')

        if not image_detail_path:
            continue

        image_str = image_detail_path.find('img')['src']
        digits = image_str.split("/small1/")[1].split("_")[0]
        new_url = f'https://m.imot.bg/details/{digits}'

        detail_images, soup_detail_page = get_image_urls_from_detail_page(new_url, 'div', 'owl-stage')
        if not detail_images:
            continue

        all_images = detail_images.find_all('img')
        res = {
            'title': all_images[0].get('title'),
            'src': list(set([image.get('src') for image in all_images])),
            'second_title': soup_detail_page.find('h1').get_text(strip=True),
            'location': soup_detail_page.find('h2').get_text(strip=True),
            'meta_description': soup_detail_page.find('div', class_='oPanel oOptions ng-star-inserted').find(
                'div').get_text(),
            'meta-info': [div.get_text(strip=True) for div in soup_detail_page.select('.oPanel.oOptions > div[style]')],
            'advert_url': new_url
        }

        building_info.append(res)

    for building in building_info:
        try:
            building['title'] = translate_text(building['title'].split('|')[0])
            building['second_title'] = translate_text(building['second_title'])
            building['location'] = translate_text(building['location'])
            building['meta_description'] = translate_text(building['meta_description'])
            sentences = building['meta_description'].split('.')
            if len(sentences) > 1 and not is_complete_sentence(sentences[-1]):
                building['meta_description'] = '.'.join(sentences[:-1])

            building['src'] = ['https:' + url if not url.startswith(('http:', 'https:')) else url for url in
                               building['src']]
            building['src'] = [url for url in building['src'] if is_valid_image_url(url)]

            sql = "INSERT INTO buildings (title, second_title, location, meta_description, src, advert_url) VALUES (%s, %s, %s, %s, %s, %s)"
            val = (building['title'], building['second_title'], building['location'],
                   building['meta_description'], ','.join(building['src']), building['advert_url'])

            mycursor.execute(sql, val)
            mydb.commit()

            print(f"{mycursor.rowcount} record(s) inserted.")

        except Exception as e:
            print(f"Error processing building: {building}. Error: {e}")

except Exception as e:
    print(f"Error occurred: {e}")

finally:
    mycursor.close()
    mydb.close()
