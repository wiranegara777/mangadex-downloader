import requests
import cloudscraper
import pdb
import os

def get_chapter_id( chapter_url ):
  string_to_remove = "https://" if "https://" in chapter_url else "" 
  substring = chapter_url.replace(string_to_remove+"mangadex.org/chapter/","")
  id = substring[:-2]
  return id

chapter_url = raw_input("Please input chapter url : ")
chapter_id = get_chapter_id(chapter_url)

request_url = "https://mangadex.org/api/"

headers = {
    'Accept': 'application/json, text/plain, */*',
    'DNT': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/73.0.3683.86 Safari/537.36'
}

params = (
  ('id', chapter_id),
  ('server', 'null'),
  ('type', 'chapter')
)

response = requests.get(request_url, headers=headers, params=params)

response_json = response.json()
# pdb.set_trace()

server = response_json['server']
hash_value = response_json['hash']
page_array = response_json['page_array']

scraper = cloudscraper.create_scraper()

for image_id in page_array:
  print(server+hash_value+'/'+image_id)
  img_url = server+hash_value+'/'+image_id
  img_response = scraper.get(img_url)
  if img_response.status_code == 200:
    with open('download/'+image_id, 'wb') as f:
		f.write(img_response.content)
  else:
    print("ecountered error {}".format(image_id) )

print("img_url", img_url)