# css selector for work location value
# #map_0 > div > address > span
# 2020.09.07
def get_work_location(soup):
    try:
        return soup.select('#map_0 > div > address > span')
    except:
        print("ERROR FOR PARSE WORK LOCATION!!")
        return ""