import requests
import asyncio
import time

from ...utils import format_time


def GoogleYoutubeService(email_list, access_token, included_apps):
   messages = []
   
   async def fetch_todos():
      start_time = time.time()
      
      response = requests.get('https://www.googleapis.com/youtube/v3/activities', params={
            'access_token': access_token,
            'maxResults': 10,
            'mine': True,
            'part': 'snippet',
      })     
      
      
      if response.status_code == 200:
         included_apps.append('YouTube')
         
         for task_list in response.json().get('items', []):         
            activity = task_list.get('snippet', {})
            video_id = task_list['id']
            created_time = activity['publishedAt']
            
            # # Process the tasks for the current list
            messages.append({
               'id':  video_id,
               'type': 'YouTube',
               'title':  activity['title'],
               'sender' : '',
               'link': "",   
               'text': activity['description'],
               'created_time': created_time,
            })
                     
         elapsed_time = time.time() - start_time                  
         print(f'Google YouTube loaded successfully ✅ - {format_time(elapsed_time)}')
         time.sleep(1)
         
         email_list.extend(messages)
                           
   asyncio.run(fetch_todos())
   return messages