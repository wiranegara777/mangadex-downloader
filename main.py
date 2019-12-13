import requests
import cloudscraper
import pdb
import os

# sample of manga from mangadex : https://mangadex.org/title/31477/solo-leveling

def get_manga_id( chapter_url ):
  try:
    id = int(''.join(filter(str.isdigit, chapter_url)))
  except:
    print('Please input correct link of manga')
    exit(0)
  return id

manga_url = raw_input("Please input manga url : ")
manga_id = get_manga_id(manga_url)

# get manga info

scraper = cloudscraper.create_scraper()

r = scraper.get('https://mangadex.org/api/manga/{}'.format(manga_id))

if r.status_code == 404:
  print("Manga Not Found ! Please check availability on mangadex manually..")
  exit(0)

manga = r.json()
title = manga['manga']['title'].encode('utf-8')
author = manga['manga']['author'].encode('utf-8')
artist = manga['manga']['artist'].encode('utf-8')

print('manga found!\ntitle : {}'.format(title))
print('author : {}'.format(author))
print('artist : {}'.format(artist))

# check available chapters

chapters = []
for chap in manga['chapter']:
  if manga['chapter'][str(chap)]['lang_code'] == 'gb': # check if the chapters was english
    chapters.append( int(manga['chapter'][str(chap)]['chapter']) )

print('Available Chapters :')
count = 0
chapters.sort()
for chap in chapters:
  if count == 10:
    count = 0
    print("{} ".format(chap))
  else:
    print("{} ".format(chap)),
  count+=1

print
# requested chapters

requested_chapters = []
req = str(raw_input("Input Chapter to download. ex: (1-7 for multiple chapters or 2 for single chapter) : "))
if '-' in req:
  arr = req.split('-')
  lower_bound = int(arr[0])
  upper_bound = int(arr[1])

  for x in range(lower_bound, upper_bound+1):
    if x not in chapters:
      print('chapter {} doesnt exist, please input correct chapter'.format(x))
      exit(0)
    else:
      requested_chapters.append(x)
else:
    if req not in chapters:
      print('chapter {} doesnt exist, please input correct chapter'.format(req))
      exit(0)
    else:
      requested_chapters.append(int(req))

# downloading chapters
# for x in requested_chapters

print(requested_chapters)
exit(0)



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
print('response', response)
exit(0)
response_json = response.json()
# pdb.set_trace()

server = response_json['server']
hash_value = response_json['hash']
page_array = response_json['page_array']

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