# 그냥 ROW에서 가져와도됨;;
def get_deadline(soup):
    try:
        deadline = soup.select('.info_period > dd:nth-child(4)') # YYYY.MM.DD tt:mm
        return deadline.split(" ")[0] # YYYY.MM.DD
    except:
        print("ERROR FOR PARSE WORK LOCATION!!")
        return ""