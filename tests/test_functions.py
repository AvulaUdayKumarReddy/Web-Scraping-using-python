from project0 import functions 
import sys

#url="https://www.normanok.gov/sites/default/files/documents/2023-01/2023-01-01_daily_incident_summary.pdf"
url="https://www.normanok.gov/sites/default/files/documents/2023-02/2023-02-01_daily_incident_summary.pdf"
def test_fetch_data():
    
    reader=functions.fetchIncidents(url)
    assert sys.getsizeof(reader)!=0

def test_fetch_incidents():
    reader=functions.fetchIncidents(url)
    li_all=functions.extractIncidents(reader)
    assert len(li_all[0])==5

def test_create_db():
    con=functions.createDB()
    assert con is not None

def test_populate_db():
    db=functions.createDB()
    reader=functions.fetchIncidents(url)
    li_all=functions.extractIncidents(reader)
    functions.populatedb(db,li_all)
    p=db.cursor()
    p.execute("select count(*) from Incident_data")
    assert len(p.fetchall())>0

def test_status():
    db=functions.createDB()
    reader=functions.fetchIncidents(url)
    li_all=functions.extractIncidents(reader)
    functions.populatedb(db,li_all)
    p=db.cursor()
    functions.status(db)
    #testing functionality inside the status
    p.execute("select count(nature) from Incident_data group by nature having nature=?",("Traffic Stop ",))
    data=p.fetchall()
    assert data[0] == (20,)


