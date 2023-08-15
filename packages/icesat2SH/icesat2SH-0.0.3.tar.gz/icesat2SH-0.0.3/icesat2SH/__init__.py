# from pickle import STRING
###################FIND TRACK ID#######################
import requests
import json
from datetime import datetime, timedelta

# miny=52.43
# maxy=52.56
# minx=29.54
# maxx=29.67
def ATL03(photonConfidence,Start_date,End_date,miny,minx,maxy,maxx):
  # Genarate date
  def generate_dates_between(start_date, end_date):
      dates_list = []
      current_date = start_date + timedelta(days=1)  # Start from the day after the start date
      
      while current_date < end_date:
          dates_list.append(current_date)
          current_date += timedelta(days=1)
      
      return dates_list

  start_date_str = Start_date
  end_date_str = End_date

  start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
  end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

  dates_between = generate_dates_between(start_date, end_date)

  Track_list = []
  mainData = []

  # miny=52.43
  # maxy=52.56
  # minx=29.54
  # maxx=29.67
  b = 0
  # photonConfidence = 'buffer'
  if photonConfidence == 'all':
    b = 0
  else:
    b =  photonConfidence


  if b == 0:
    i = 1
    while i <= 1387:
        track_id = i
        p = 0
        while p < len(dates_between):
          date1 = dates_between[p]
          open_altimetry_api ="https://openaltimetry.org/data/api/icesat2/atl03?date="+date1.strftime('%Y-%m-%d')+"&miny="+str(miny)+"&maxy="+str(maxy)+"&minx="+str(minx)+"&maxx="+str(maxx)+"&beamName=gt1l&beamName=gt1r&beamName=gt2l&beamName=gt2r&beamName=gt3l&beamName=gt3r&trackId=" + str(track_id) + "&client=portal&outputFormat=json"
          icesat_2_data = requests.get(open_altimetry_api)
          json_string = json.dumps(icesat_2_data.json())
          if len(json_string) >= 2113:
            print('TrackID = '+str(i)+'\tDate = '+date1.strftime('%Y-%m-%d')+'\tYESSSSSSS')
            mainData.extend(['--------------\n'+'TrackID = '+str(i)+'\tDate = '+date1.strftime('%Y-%m-%d')+'\n'+json_string])
            Track_list.extend(['TrackID = '+str(i)+'\tDate = '+date1.strftime('%Y-%m-%d')+'\tYESSSSSSSSS'])
          a = (i/1387)*100
          print(str(round(a, 3))+' %')
          Track_list.extend(['TrackID = '+str(i)+'\tDate = '+date1.strftime('%Y-%m-%d')+'\tNO'])
          p += 1


        i += 1

  else:
    i = 1
    while i <= 1387:
        track_id = i
        p = 0
        while p < len(dates_between):
          date1 = dates_between[p]
          open_altimetry_api ="https://openaltimetry.org/data/api/icesat2/atl03?date="+date1.strftime('%Y-%m-%d')+"&miny="+str(miny)+"&maxy="+str(maxy)+"&minx="+str(minx)+"&maxx="+str(maxx)+"&beamName=gt1l&beamName=gt1r&beamName=gt2l&beamName=gt2r&beamName=gt3l&beamName=gt3r&trackId=" + str(track_id) + "&client=portal&photonConfidence="+b+"&outputFormat=json"
          icesat_2_data = requests.get(open_altimetry_api)
          json_string = json.dumps(icesat_2_data.json())
          if len(json_string) >= 2113:
            print('TrackID = '+str(i)+'\tDate = '+date1.strftime('%Y-%m-%d')+'\tYESSSSSSS')
            mainData.extend(['--------------\n'+'TrackID = '+str(i)+'\tDate = '+date1.strftime('%Y-%m-%d')+'\n'+json_string])
            Track_list.extend(['TrackID = '+str(i)+'\tDate = '+date1.strftime('%Y-%m-%d')+'\tYESSSSSSSSS'])
          a = (i/1387)*100
          print(str(round(a, 3))+' %')
          Track_list.extend(['TrackID = '+str(i)+'\tDate = '+date1.strftime('%Y-%m-%d')+'\tNO'])
          p += 1


        i += 1


  file_name = "TrackID.txt"

  with open(file_name, "w") as file:
      for item in Track_list:
          file.write("%s\n" % item)

  file_name = "MainData.txt"

  with open(file_name, "w") as file:
      for item in mainData:
          file.write("%s\n" % item)

  return 'Done'





#693