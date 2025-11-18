import json
def filename(fname):
    with open(fname,'r') as f:
        return json.load(f)
    
data= filename('Movie.json')
print("titles of each movie :")
for movie in data:
 print(movie['title'])
for movie in data:
  if movie['year']>2010:
      print(movie['title'])

print(len(data))