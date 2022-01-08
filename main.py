import requests
import datetime
import json

headers = {'content-type': 'application/json'}

search = {
  "variables":{
    "q":"",
    "filter":{
      "count":10,
      "page":0
      }
    },
  "query":"""
  query SearchQuery($q: String, $filter: SearchFilterInput, $mediaSize: MediaSize = MEDIUM) {
  search(q: $q, filter: $filter) {
    announcements {
      data {
        ...AnnouncementContent
      }
      paginatorInfo {
        lastPage
        hasMorePages
      }
    }
  }
}

fragment AnnouncementContent on Announcement {
  defaultMedia(size: $mediaSize) {
    mediaUrl
  }
}

"""
}


data = {
  "variables":{
    "q":"",
    "filter":{
      "categorySlug":"",
      "count":1000,
      "page":1
      }
    },
  "query":"""query SearchStore($q: String, $filter: StoreSearchFilterInput!) {
    stores: storeSearch(q: $q, filter: $filter) {
      data {
        id
        name
        categories {
          id
          name
          slug
        }
        mainLocation {
          id
          worktime
          phones
          emails
          socials {
            name
            url
          }
          location {
            id
            address
            lat
            lng
          }
        }
      }
      paginatorInfo {
        count
        lastPage
        hasMorePages
        }
      }
    }
  """
}

stors = []
last_page = 2
current_page = 1
def get_page():
  return requests.post('https://api.ouedkniss.com/graphql',
                            headers=headers,
                            data=json.dumps(data))

has_more_pages = True

while last_page >= current_page:
  response = get_page()
  stors.extend(response.json().get('data').get('stores').get('data'))
  print(response.json()['data']['stores']['paginatorInfo'])
  has_more_pages = response.json().get('data').get('stores').get('paginatorInfo').get('hasMorePages')
  last_page = response.json().get('data').get('stores').get('paginatorInfo').get('lastPage')
  print(len(stors), current_page, last_page)
  data['variables']['filter']['page'] += 1
  current_page = data['variables']['filter']['page']
  
print(len(stors))
# print(response.text)
# print(response.json())
# print(len(response.json().get('data').get('stores').get('data')))
# print(json.loads(response.text))

# print(map(lambda s: s.get('email')))
today = datetime.datetime.now().strftime("%d-%m-%Y %H-%M")
with open(f'data/data {today}.json', 'w') as file:
  file.write(json.dumps(stors))

print(len(stors), ' Done...')
