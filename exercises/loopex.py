import json
with open('Trial.json','r',encoding='utf-8') as trial:
      data=json.load(trial)

videos=[{"id":"a1","title":"intro"},{"id":"a2","title":"transcripts"}]
for i,video in enumerate(videos):
    print(video['id'],'-',video['title'])         
    
print(data)


    