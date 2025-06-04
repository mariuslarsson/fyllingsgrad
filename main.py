import src.getApi as getApi
import src.createTables as create
import src.insertTables as insert
import src.decorators as dec
import src.createView as create_v

import json
import os
import sys

def main():

    if not os.path.exists("creds.json"):
        print("Filen creds.json ble ikke funnet i working directory. Se README.md for mer informasjon")
        sys.exit(1)


    #TODO: Legg inn bedre logging og excepts
    with open('creds.json', 'r') as file:
        creds = json.load(file)


    maxMinResponse = getApi.getNveApi("https://biapi.nve.no/magasinstatistikk/api/Magasinstatistikk/HentOffentligDataMinMaxMedian")
    seriesResponse = getApi.getNveApi("https://biapi.nve.no/magasinstatistikk/api/Magasinstatistikk/HentOffentligData")
    omraaderResponse = getApi.getNveApi("https://biapi.nve.no/magasinstatistikk/api/Magasinstatistikk/HentOmråder")
    frostRespons = getApi.getNveApi("https://frost.met.no/observations/v0.jsonld?sources=SN18700&referencetime=2022-01-01%2F2022-12-31&elements=sum(precipitation_amount%20P1D)&timeoffsets=PT6H", creds["ID"])

    create.createNedboer()
    insert.insertNedboer(frostRespons["data"])

    create.createFyllingsgrad()
    insert.insertFyllingsgrad(seriesResponse)

    create.createOmraader()
    insert.insertOmraader(omraaderResponse)

    create.createMaxMinFyllingsgrad()
    insert.insertMaxMinFyllingsgrad(maxMinResponse)

    create_v.createView()
    print("created view")


if __name__ == "__main__":
    main()