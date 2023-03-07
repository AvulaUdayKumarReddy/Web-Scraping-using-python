from pypdf import PdfReader
import re
#import project0.functions
import urllib.request
import sqlite3

def fetchIncidents(url):

    headers = {}
    headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"                          

    data = urllib.request.urlopen(urllib.request.Request(url, headers=headers)).read() 
    datatmp=  open("docs/first.pdf",'wb')
    
    datatmp.write(data) 

    
    reader=PdfReader("docs/first.pdf")
    return reader

def extractIncidents(reader):
    li_all=[]
    for page in reader.pages:

    # extracting incidents
        #page=reader.pages[0]
        demo=page.extract_text()
        #to facilitate regular experession
        demo=demo.replace("<UNKNOWN>","UNKNOWN")
        demo=demo.replace("MVA","Mva")
        demo=demo.replace("COP DDACTS","Cop Ddacts")
        demo=demo.replace("NORMAN POLICE DEPARTMENT\nDaily Incident Summary (Public)","")
        demo=demo.replace("Date / Time Incident Number Location Nature Incident ORI","")
        #replacing the \n values with the # charcter to differenciate the lines.
        demo=demo.replace("EMSSTAT\n","EMSSTAT#")
        demo=demo.replace("OK0140200\n","OK0140200#")
        demo=demo.replace("14005\n","14005#")
        demo=demo.replace("14009\n","14009#")
        #replacing \n with " " to combine the two lines in location field
        demo=demo.replace("\n"," ")
        arr=demo.strip().split('#')
        #arr.replace('\n','')
        for sentence in arr:
            
            li=[]
            #incident_ori
            match_ori=re.search(r'(OK0140200|14005|EMSSTAT|14009)',sentence)
            if match_ori:
                ori=match_ori.group(0)
            else:
                ori=""
            sentence=sentence.replace(ori,"")
            match_dt=re.search(r'\d{1,2}/\d{1,2}/\d{4}\s\d{1,2}:\d{2}',sentence)
            if match_dt:
                dt=match_dt.group(0)
            sentence=sentence.replace(dt,"")
            li.append(dt)
            match_number=re.search(r'\d{4}-\d{8}',sentence)
            if match_number:
                number=match_number.group(0)
            sentence=sentence.replace(number,"")
            li.append(number)
        
            match_loc=re.search(r"[A-Z0-9\s/.;-]*",sentence)
            if match_loc:
                loc=match_loc.group(0)
                
                n=len(loc)
                loc=loc[:n-1]
                #li.append(loc)
            else:
                li.append(" ")
            #replacing to remove all other fileds except nature
            sentence=sentence.replace(loc,"")
            #print(sentence)
            #appending location
            li.append(loc)
            #appending nature
            li.append(sentence)
            #appending ori
            li.append(ori)
            li_all.append(li)
            length=len(li_all)
            #li_all.pop(length-1)
    return li_all

#print(li_all)
#print(li_all)
#print(li_all[length-1][0])

 

def createDB():
    try:
        connection=sqlite3.connect('./normanpd.db')
    except:
        print("An exception Occured")
    return connection

#db=createDB()

def populatedb(db,li_all):
    #li_all=list(li_all)
    length=len(li_all)
    insert="INSERT INTO Incident_data VALUES (?,?,?,?,?);"
    #connection=sqlite3.connect('./normanpd.db')
    p=db.cursor()
    p.execute('''
              DROP TABLE IF EXISTS Incident_data;
              ''')
    p.execute('''
              CREATE TABLE Incident_data(
              incident_time TEXT,
              incident_number TEXT,
              incident_location TEXT,
              nature TEXT,
              incident_ori TEXT
              );
              ''')
    for i in range(length-1):

        #print(li_all[i][0],li_all[i][1],li_all[i][2],li_all[i][3],li_all[i][4])
        try:
            p.execute(insert,li_all[i])  
        except sqlite3.Error as er:
            print(er.args)
             
    #p.execute(''' select * from Incident_data''')
        #p.commit()
#populatedb(db,li_all)

def status(db):
    #connection=sqlite3.connect('./normanpd.db')
    p=db.cursor()
    p.execute('SELECT nature,count(nature) As count from Incident_data group by nature order by count desc, nature asc')
    #p.execute('SELECT * from Incident_data where nature=?'," ")
    data=p.fetchall()
    for item in data:
        print(item[0]+"|",item[1])







