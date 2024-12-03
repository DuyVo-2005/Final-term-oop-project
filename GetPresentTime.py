import datetime

def GetPresentTime() -> str:
    datetime_now = datetime.datetime.now()
    formatted_datetime = datetime_now.strftime("%Y-%m-%d")
    return formatted_datetime
