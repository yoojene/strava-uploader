import os, subprocess, requests, shutil

activities = []
# ACCESS_TOKEN = a1195b8e1532140ba73d4e297a0d879ea707910d
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
  print(len(activities))

  url = 'https://www.strava.com/api/v3/uploads'
  payload = {'data_type': 'tcx'}

  i = 0
  for activity in activities:
    print(activity)
    
    files = {'file': open(activity, 'rb')}
    headers = {'Authorization': 'Bearer a1195b8e1532140ba73d4e297a0d879ea707910d'}
    r = requests.post(url, headers=headers, params=payload, files=files)
    print(r.url)
    print(r.json())
    print('processed!')

    shutil.move(activity, "./processed/"+activity)
    print('moved')
    i += 1
    if i == 100: # 100 files per 15 mins rate limit
      break

getFilesAndWriteList()
uploadAndMove()
