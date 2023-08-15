import datetime

def is_birthday_coming(obj):
  today = datetime.datetime.now()
  tomorrow = today + datetime.timedelta(days=1)
  if today.month == obj.dob.month and today.day == obj.dob.day:
    return obj
  elif tomorrow.month == obj.dob.month and tomorrow.day == obj.dob.day:
    return obj