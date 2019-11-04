
import requests
res = requests.get('https://www.goodreads.com/review/list?key=IzTRndFKRignOkxxlNn0ng&v=2&id=101556262&per_page=infinite&shelf=read&sort=date_read')
writer = open("bla1.xml", "w")
cur = res.text
print(type(cur))
writer.write(str(cur))

exit(0)


