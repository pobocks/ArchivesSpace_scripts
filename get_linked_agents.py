import json
from asnake.aspace import ASpace

import csv

aspace = ASpace(baseurl='http://localhost:8080',
                username = 'admin'
                password = 'admin')

repo = aspace.repositories(2)

records = []
for resource in repo.resources:
    try: 
        # not sure what the ref= is doing in original code
        # operating on the principle that it's intended as a check that first agent exists and is a ref?
        if next(resource.linked_agents).is_ref:
            records.append(resource.json())
    except: 
        continue
        
for accession in repo.accessions:
    try:
        if next(accession.linked_agents).is_ref:
            records.append(accession.json())
    except:
        continue
    
#open a cvs file for output
f=csv.writer(open('new_agents.csv', 'wb'))
f.writerow(['uri']+['name']+['related record'])

selected_records = []
#get all records that are linked to a specific agent
# doing straight transliteration, but I think this would be clearer as:
# for record in records:
#     for agent in record['linked_agents']:
for i in range (0, len (records)):
    for j in range (0, len (records[i]['linked_agents'])):
        uri = records[i]['uri']
        title = records[i]['title']
        needs_review = records[i]['linked_agents'][j].get('ref')
        if needs_review == '/agents/software/2':
            # shows a possible lack in ASnake abstraction layer, should be a way to put in URL get JSONModel obj?
            ag_json = aspace.client.get(uri).json()
            selected_records.append(ag_json)
 
#Now take the records found above and get any related agent and write to csv           
for i in range (0, len (selected_records)):
    for j in range (0, len (selected_records[i]['linked_agents'])):
        uri = selected_records[i]['uri']
        agents = selected_records[i]['linked_agents'][j].get('ref')
        agent_json = aspace.client.get(agents).json()
        title = agent_json['title']
        f.writerow([agents]+[title]+[uri])
