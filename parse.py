# download the HSC timetable page from studentsonline.bostes.nsw.edu.au and run this script and with it as an arg
from bs4 import BeautifulSoup
from sys import argv
import re

soup = None
with open(argv[-1]) as f:
    soup = BeautifulSoup(''.join(f.readlines()), 'html.parser')

# find the table of doom(tm)
tbl = soup.find_all('table')[0]

col_count = len(tbl.thead.tr.find_all('th'))

out = {}
all_subjects = set()

for i in range(col_count):
    out[i] = {}
rows = tbl.tbody.find_all('tr')

cur_days = []
k = 0
for row in rows:
    k+=1
    if row.th: # update cur_days
        cur_days = []
        j = 0
        for i in row.find_all('th'):
            for br in i.find_all('br'):
                br.replace_with('\n')
            cur_days.append(i.get_text().split('\n')[0])
            out[j][cur_days[-1]] = []
            j += 1
    else:
        if len(cur_days) == 0:
            raise Exception("you skipped the header row?")
        cells = row.find_all('td')
        for j in range(len(cells)):
            dl = cells[j].dl
            if dl is None:
                # empty cell
                continue
            for i in dl.find_all('dt'):
                for br in i.find_all('br'):
                    br.replace_with(' ')
                exam_info = {
                        'name': i.get_text(),
                        'times': [], # array of time pairs
                        'comments': [] # text found that's not times
                }
                all_subjects.add(re.sub(r'\s+', ' ', re.sub('[^A-Za-z0-9 ()]', ' ', i.get_text())))
                cur_sibling = i.next_sibling
                while cur_sibling and (cur_sibling.name == 'dd' or cur_sibling.name is None):
                    if cur_sibling.name is None:
                        cur_sibling = cur_sibling.next_sibling
                        continue # empty node
                    # does it look like a time?
                    if "–" in cur_sibling.get_text() and cur_sibling.get_text().strip()[0].isdigit():
                        # it's probably a time.
                        times = cur_sibling.get_text().strip().split(" – ")
                        times[0] = times[0].replace(' noon', 'pm').replace('*', '')
                        if '\n' in times[1]: # comment in same node as time ;_;
                            temp = times[1].split('\n', 1)
                            times[1] = temp[0]
                            exam_info['comments'].append(temp[1])
                        times[1] = times[1].replace(' noon', 'pm').replace('*', '')
                        exam_info['times'].append(times)
                    else:
                        #print("comment: %s"%cur_sibling.get_text())
                        exam_info['comments'].append(cur_sibling.get_text().strip())
                    cur_sibling = cur_sibling.next_sibling
                temp = exam_info['times']
                if len(temp) == 0: # empty subject?
                    continue
                #print(temp)
                exam_info['times'] = [temp[0][0], temp[-1][1]] # first time to last time
                out[j][cur_days[j]].append(exam_info)

import json
print(json.dumps(out))




