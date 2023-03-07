import argparse

import functions

def main(url):
    # Download data
    incident_data =functions.fetchIncidents(url)

    # Extract data
    incidents = functions.extractIncidents(incident_data)
	
    # Create new database
    db = functions.createDB()
	
    # Insert data
    functions.populatedb(db, incidents)
	
    # Print incident counts
    functions.status(db)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--incidents", type=str, required=True, 
                         help="Incident summary url.")
     
    args = parser.parse_args()
    if args.incidents:
        main(args.incidents)
