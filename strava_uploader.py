import os, subprocess, requests, shutil

activities = []
ACCESS_TOKEN = 'token_goes_here'

def getFilesAndWriteList():

  global activities
  process = subprocess.Popen(('ls'),stdout=subprocess.PIPE)
  output = subprocess.check_output(
      ('grep', 'tcx'), stdin=process.stdout, universal_newlines=True)
  process.wait

  f = open('filestoprocess.txt', 'w')
  f.write(output)
  f.close()

  with open('filestoprocess.txt', 'r') as source:
    activities = [line.strip() for line in source]


def uploadAndMove():
  global ACCESS_TOKEN
  print(len(activities))

  url = 'https://www.strava.com/api/v3/uploads'
  payload = {'data_type': 'tcx'}

  i = 0
  for activity in activities:
    print(activity)
    
    files = {'file': open(activity, 'rb')}
    headers = {'Authorization': 'Bearer '+ACCESS_TOKEN}
    r = requests.post(url, headers=headers, params=payload, files=files)
    print(r.url)
    print(r.json())
    print(r.status_code)
    
    if (r.status_code != 201):
      print('error!')
      break

    print('processed!')
    shutil.move(activity, "./processed/"+activity)
    print('moved')
    i += 1
    if i == 100: # 100 files per 15 mins rate limit
      break

getFilesAndWriteList()
uploadAndMove()
