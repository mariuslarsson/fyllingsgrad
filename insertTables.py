import sqlite3
import decorators as dec
from datetime import datetime

@dec.connection("vannmagasin.db")
def insertFyllingsgrad(cursor, api_response:list):



    #Lager en teller for å rapportere antall rader som er lagt til
    inserted = 0

    for rowDict in api_response:

        #Skaper unik ID for duplikatsjekk og for fremtidig referanse
        rowDict["ID"] = rowDict["dato_Id"]+rowDict["omrType"]+str(rowDict["omrnr"])

        cursor.execute('''
            INSERT OR IGNORE INTO fyllingsgrad (
                    ID, dato_Id, omrType, omrnr, iso_aar, iso_uke,
                    fyllingsgrad, kapasitet_TWh, fylling_TWh, neste_Publiseringsdato,
                    fyllingsgrad_forrige_uke, endring_fyllingsgrad                   
                    
                ) VALUES (
                    :ID, :dato_Id, :omrType, :omrnr, :iso_aar, :iso_uke,
                    :fyllingsgrad, :kapasitet_TWh, :fylling_TWh, :neste_Publiseringsdato,
                    :fyllingsgrad_forrige_uke, :endring_fyllingsgrad                     
                
                )

        ''', rowDict)

        if cursor.rowcount > 0:
            inserted += 1

    print(f"{inserted} rader ble lagt til")



    

@dec.connection("vannmagasin.db")
def insertMaxMinFyllingsgrad(cursor, api_response:list):



    #Lager en teller for å rapportere antall rader som er lagt til
    inserted = 0

    for rowDict in api_response:

        #Skaper unik ID for duplikatsjekk og for fremtidig referanse
        rowDict["ID"] = str(rowDict["iso_uke"])+rowDict["omrType"]+str(rowDict["omrnr"])

        cursor.execute('''
            INSERT OR IGNORE INTO fyllingsgrad_maxmin (
                    ID, omrType, omrnr, iso_uke,
                    minFyllingsgrad, minFyllingTWH, medianFyllingsGrad,
                    medianFylling_TWH, maxFyllingsgrad, maxFyllingTWH
                    
                ) VALUES (
                    :ID, :omrType, :omrnr, :iso_uke,
                    :minFyllingsgrad, :minFyllingTWH, :medianFyllingsGrad,
                    :medianFylling_TWH, :maxFyllingsgrad, :maxFyllingTWH                  
                
                )

        ''', rowDict)

        if cursor.rowcount > 0:
            inserted += 1
    
    print(f"{inserted} rader ble lagt til")
    



@dec.connection("vannmagasin.db")
def insertOmraader(cursor, api_response:list):



    #Lager en teller for å rapportere antall rader som er lagt til
    inserted = 0

    for key in api_response[0]:
        for rowDict in api_response[0][key]:

            cursor.execute('''
                INSERT INTO omraader (
                        navn, navn_langt, beskrivelse, 
                        omrType, omrnr
                        
                    ) VALUES (
                        :navn, :navn_langt, :beskrivelse, 
                        :omrType, :omrnr               
                    
                    )

            ''', rowDict)

            if cursor.rowcount > 0:
                inserted += 1
    
    print(f"{inserted} rader ble lagt til")


@dec.connection("vannmagasin.db")
def insertNedboer(cursor, api_response:list):



    #Lager en teller for å rapportere antall rader som er lagt til
    inserted = 0

    for rowDict in api_response:

        currentRow = rowDict["observations"][0]
        referenceTime = rowDict["referenceTime"]
        #Henter ut uke, dag, aar og time for å kunne koble på annen data, og for å kunne velge referansetidspunkt for måling senere
        dtObject = datetime.fromisoformat(referenceTime.replace("Z", "+00:00"))
        iso_aar, iso_uke, iso_dag = dtObject.isocalendar()
        referenceHour = dtObject.hour
        
        currentRow["iso_aar"] = iso_aar
        currentRow["iso_uke"] = iso_uke
        currentRow["iso_dag"] = iso_dag
        currentRow["referenceHour"] = referenceHour

        #Bevarer stasjonskode i tilfelle det blir relevant i fremtiden
        currentRow["stajonskode"] = rowDict["sourceId"]
        #Setter kode 0 for prisområde 0
        currentRow["omrnr"] = 1
        #TODO: Legg til omrType=VASS her muligens.

        currentRow["referenceTime"] = referenceTime[0:10]

        cursor.execute('''
            INSERT OR IGNORE INTO nedboer (
                elementId, referenceTime, referenceHour, iso_dag, iso_aar, iso_uke,
                value, omrnr, unit, timeOffset, timeResolution, timeSeriesId,
                performanceCategory, exposureCategory, qualityCode
            ) VALUES (
                :elementId, :referenceTime, :referenceHour, :iso_dag, :iso_aar, :iso_uke,
                :value, :omrnr, :unit, :timeOffset, :timeResolution, :timeSeriesId,
                :performanceCategory, :exposureCategory, :qualityCode
            )

        ''', currentRow)

        if cursor.rowcount > 0:
            inserted += 1
    
    print(f"{inserted} rader ble lagt til")
    