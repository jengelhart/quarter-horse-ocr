from PIL import Image
import pytesseract
from pdf2image import convert_from_path
from dateutil.parser import parse
import datetime
from word2number import w2n
import re
import csv
import sys

#Read Equibase QH race charts and export data to CSV
#PDF to images
pdf = sys.argv[1]
images = convert_from_path(pdf, dpi=450)

#Setup csv
out_name = pdf[:len(pdf) - 4] + '-data.csv'
with open(out_name, 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['date', 'dist', 'ws', 'wt', 'trk', 'name', 'odds', 'time'])
f.close()

#parse each page
for image in images:
    race_raw = pytesseract.image_to_string(image)
    #print(race_raw)
    race_ln = race_raw.split('\n')
    i = 0 #line index

    #race data: date, distance, wind speed, wind type, track
    date = parse((race_ln[i].split(' - '))[1]).date()

    while not 'Track Record:' in race_ln[i]:
        i += 1
    dist_str = (' '.join((race_ln[i].split(' '))[0:4]))
    dist = w2n.word_to_num(dist_str)

    while not 'Wind Speed:' in race_ln[i]:
        i += 1
    w_ln = race_ln[i].split(' ')
    ws = int(w_ln[2])
    wt = w_ln[5].upper()

    while not 'Track:' in race_ln[i]:
        i += 1
    trk = (race_ln[i].split(' '))[3].upper()

    #get to first line of horse data
    while not 'Last' in race_ln[i]:
        i += 1
    i += 1
    while not 'Run-Up:' in race_ln[i]:
        #horse data: name, odds, time
        if not race_ln[i] is '' and not race_ln[i] is '\n':
            horse_record = race_ln[i].split(' ')
            name_end = 3
            while not '(' in horse_record[name_end]:
                name_end += 1
            name = ' '.join(horse_record[3:name_end])

            j = name_end + 3 #+3 skips jockey names w/ '.'
            while not '.' in horse_record[j]:
                j += 1
            odds = float(re.findall('\d+\.\d+', horse_record[j])[0])
            time = float(horse_record[j + 1])

            #append data to csv
            with open(out_name, 'a') as f:
                writer = csv.writer(f)
                writer.writerow([date, dist, ws, wt, trk, name, odds, time])
            f.close()
        i += 1
