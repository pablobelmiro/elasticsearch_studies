#Extract the archive to /dataset directory
#At this script I'm using a simple "way", sending atomic data to the cluster instead of "bulk way"

import pandas as pd
from pathlib import Path
from datetime import datetime
import requests
import json

date_pattern = r'(\d{2})[/.-](\d{2})[/.-](\d{4})'
def to_american_date(date_string):    
    try:
        date_obj = datetime.strptime(date_string.strip(), '%m/%d/%Y').date()
        return date_obj.isoformat()
    except (ValueError, TypeError, AttributeError):
        print(ValueError)
        print(TypeError)
        print(AttributeError)
        return None

def safe_str(value):
    if pd.isna(value) or value is None or str(value).strip() == '':
        return None
    return str(value).strip()

def safe_date(value):
    if pd.isna(value) or value is None or str(value).strip() == '':
        return None
    return to_american_date(str(value))

def safe_float(value):
    if pd.isna(value) or value is None or str(value).strip() == '':
        return None
    try:
        return float(value)
    except (ValueError, TypeError):
        return None

filename = 'Archived_Legally_Operating_Businesses_20240924.csv'
file_path = Path('dataset') / filename

if not file_path.exists():
    raise FileNotFoundError(f"Arquivo {filename} não encontrado em {file_path}")

df = pd.read_csv(file_path, low_memory=False)
df = df.where(pd.notnull(df), None)

sequence = 0
for row in df.iterrows():
    if row is not None:
        print(f'----- actual sequence: {sequence}')
        
        #Formatting data
        dcaLiscenceNumber = safe_str(row[1]['DCA License Number'])
        liscenceType = safe_str(row[1]['License Type'])
        liscenceExpiration = safe_date(row[1]['License Expiration Date'])
        liscenceStatus = safe_str(row[1]['License Status'])
        liscenceCreation = safe_date(row[1]['License Creation Date'])
        industry = safe_str(row[1]['Industry'])
        businessName = safe_str(row[1]['Business Name'])
        businessNameSecundary = safe_str(row[1]['Business Name 2'])
        addressBuilding = safe_str(row[1]['Address Building'])
        addressStreetName = safe_str(row[1]['Address Street Name'])
        addressStreetNameSecundary = safe_str(row[1]['Secondary Address Street Name'])
        addressCity = safe_str(row[1]['Address City'])
        addressState = safe_str(row[1]['Address State'])
        addressZip = safe_str(row[1]['Address ZIP'])
        contactPhone = safe_str(row[1]['Contact Phone Number'])
        addressBorough = safe_str(row[1]['Address Borough'])
        codeBorough = safe_str(row[1]['Borough Code'])
        communityBoard = safe_str(row[1]['Community Board'])
        concilDistrict = safe_str(row[1]['Council District'])
        bin = safe_str(row[1]['BIN'])
        bbl = safe_str(row[1]['BBL'])
        nta = safe_str(row[1]['NTA'])
        censusTract = safe_str(row[1]['Census Tract'])
        detail = safe_str(row[1]['Detail'])
        longitude = safe_float(row[1]['Longitude'])
        latitude = safe_float(row[1]['Latitude'])
        location = safe_str(row[1]['Location'])
        
        #format body
        reqBody = {
            'dcaLiscenceNumber': dcaLiscenceNumber,
            'liscenceType': liscenceType,
            'liscenceExpiration': liscenceExpiration,
            'liscenceStatus': liscenceStatus,
            'liscenceCreation': liscenceCreation,
            'industry': industry,
            'businessName': businessName,
            'businessNameSecundary': businessNameSecundary,
            'addressBuilding': addressBuilding,
            'addressStreetName': addressStreetName,
            'addressStreetNameSecundary': addressStreetNameSecundary,
            'addressCity': addressCity,
            'addressState': addressState,
            'addressZip': addressZip,
            'contactPhone': contactPhone,
            'addressBorough': addressBorough,
            'codeBorough': codeBorough,
            'communityBoard': communityBoard,
            'concilDistrict': concilDistrict,
            'bin': bin,
            'bbl': bbl,
            'nta': nta,
            'censusTract': censusTract,
            'detail': detail,
            'longitude': longitude,
            'latitude': latitude,
            'location': location,
        }
        
        
        
        sequence += 1
        
        elasticResponse = requests.post('http://localhost:9200/nycopendata/_doc', json=reqBody, 
            headers={'Content-Type': 'Application/json'})
        
        #handling response
        data = json.loads(elasticResponse.text)
        print(elasticResponse)
        print(json.dumps(data, indent=2))
        


















#################### DEBUG PURPOSE ONLY
def printData():
    print(f'''
    dcaLiscenceNumber: {dcaLiscenceNumber} - {type(dcaLiscenceNumber)}
    liscenceType: {liscenceType} - {type(liscenceType)}
    liscenceExpiration: {liscenceExpiration} - {type(liscenceExpiration)}
    liscenceStatus: {liscenceStatus} - {type(liscenceStatus)}
    liscenceCreation: {liscenceCreation} - {type(liscenceCreation)}
    industry: {industry} - {type(industry)}
    businessName: {businessName} - {type(businessName)}
    businessNameSecundary: {businessNameSecundary} - {type(businessNameSecundary)}
    addressBuilding: {addressBuilding} - {type(addressBuilding)}
    addressStreetName: {addressStreetName} - {type(addressStreetName)}
    addressStreetNameSecundary: {addressStreetNameSecundary} - {type(addressStreetNameSecundary)}
    addressCity: {addressCity} - {type(addressCity)}
    addressState: {addressState} - {type(addressState)}
    addressZip: {addressZip} - {type(addressZip)}
    contactPhone: {contactPhone} - {type(contactPhone)}
    addressBorough: {addressBorough} - {type(addressBorough)}
    codeBorough: {codeBorough} - {type(codeBorough)}
    communityBoard: {communityBoard} - {type(communityBoard)}
    concilDistrict: {concilDistrict} - {type(concilDistrict)}
    bin: {bin} - {type(bin)}
    bbl: {bbl} - {type(bbl)}
    nta: {nta} - {type(nta)}
    censusTract: {censusTract} - {type(censusTract)}
    detail: {detail} - {type(detail)}
    longitude: {longitude} - {type(longitude)}
    latitude: {latitude} - {type(latitude)}
    location: {location} - {type(location)}
''')