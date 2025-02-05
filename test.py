from datetime import datetime, date, time, timezone

# Using datetime.combine()
d = date(2005, 7, 14)
t = time(12, 30)

print(type(d))
print(type(t))
# datetime.combine(d, t)
# datetime.datetime(2005, 7, 14, 12, 30)