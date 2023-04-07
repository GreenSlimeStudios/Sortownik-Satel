import datetime
import math

lokalizacja_pliku_wejsciowego = './test_Max.txt'
lokalizacja_pliku_wyjsciowege = './output.txt'

osoby = []
okres = ""
poczatek = ""

class Osoba:
    def __init__(self, nazwa,aktywnosc,data):
        self.nazwa = nazwa
        self.aktywnosci = {data: [aktywnosc]}

with open(lokalizacja_pliku_wejsciowego,encoding='latin-1',mode='r') as file:
    for line in file:
        
        if "w okresie:" in line:
            okres = line.split("okresie: ")[1].split(';')[0]
            poczatek = okres.split(' ÷ ')[0]
            zmiana = poczatek.split('.');
            poczatek = zmiana[2]+'-'+zmiana[1]+'-'+zmiana[0]
        
        # Odfiltrowanie niewłaściwych linijek
        if ("U:" in line) == False: continue

        nazwisko = line.split("U:")[1].split('\n')[0].strip()
        split = line.split("-")
        rok = split[0].split(' ')[len(split[0].split(' '))-1]
        miesiac = split[1]
        dzien = split[2].split(' ')[0]
        godzina = split[2].split(' ')[len(split[2].split(' '))-2]
        data = rok + '-' + miesiac + '-' + dzien

        # print(rok,miesiac,dzien,godzina,nazwisko)
        
        jest_juz = False
        for i in range(0,len(osoby)):
            if osoby[i].nazwa == nazwisko:
                jest_juz = True
                break
        
        if jest_juz:
            if data in osoby[i].aktywnosci.keys():
                osoby[i].aktywnosci[data].append(godzina)
            else:
                osoby[i].aktywnosci[data] = [godzina]
        else:
            osoby.append(Osoba(nazwisko,godzina,data))


for osoba in osoby:
    # print(osoba.nazwa+':')
    for data in osoba.aktywnosci.keys():
        # print('*'+data)
        sorted(osoba.aktywnosci[data])
    #     for godzina in osoba.aktywnosci[data]:
    #         print('  -'+godzina)
    # print()

time1 = datetime.date.fromisoformat(poczatek)
end = ','

with open(lokalizacja_pliku_wyjsciowege,encoding='latin-1',mode="w") as file:
    print('osoba',end=',')
    file.write('osoba,')
    for i in range(0,5):
        if i == 4: end=''
        print(time1 + datetime.timedelta(days=i),'wejscie',end=',') 
        print(time1 + datetime.timedelta(days=i),'wyjscie',end=',') 
        print(str(time1 + datetime.timedelta(days=i)),'roznica',end=end) 
        file.write(str(time1 + datetime.timedelta(days=i))+' wejscie' + ',') 
        file.write(str(time1 + datetime.timedelta(days=i))+' wyjscie' + ',') 
        file.write(str(time1 + datetime.timedelta(days=i))+' roznica'+end) 
    print()
    file.write('\n')
    for osoba in osoby:
        end = ','
        print(osoba.nazwa,end=',')
        file.write(osoba.nazwa + ',')
        for i in range(0,5):
            if i == 4: end=''
            czas = str(time1 + datetime.timedelta(days=i)) 
            if str(czas) in osoba.aktywnosci.keys():
                wejscie = datetime.datetime.strptime(str(osoba.aktywnosci[czas][len(osoba.aktywnosci[czas])-1]),'%H:%M');
                wyjscie = datetime.datetime.strptime(str(osoba.aktywnosci[czas][0]),'%H:%M');
                czas_p = wyjscie-wejscie;
                h = str(czas_p.seconds // 3600)
                s = czas_p.seconds % 3600
                m = str(s // 60)
                if len(m) == 1: m = '0' + m
                if len(h) == 1: h = '0' + h
                print(wejscie.strftime("%H:%M"),end=',');
                print(wyjscie.strftime("%H:%M"),end=',');
                print(h+":"+m,end=end);
                file.write(str(wejscie.strftime("%H:%M"))+',')
                file.write(str(wyjscie.strftime("%H:%M"))+',')
                file.write(h+":"+m+end)
            else:
                print('brak,brak,brak',end=end)
                file.write('brak,brak,brak'+end)
        print()
        file.write('\n')