import sqlite3
import src.decorators as dec


@dec.connection("vannmagasin.db")
def createFyllingsgrad(cursor):
    


    #Vurder å legge til evaluering om hvorvidt tabell eksisterer eller ikke, og rapporter om den ble opprettet eller eksisterte

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fyllingsgrad (
        ID TEXT PRIMARY KEY, 
        dato_Id TEXT, -- vurdere annet enn tekst pga problemer med datavalidering
        omrType TEXT,
        omrnr INTEGER,
        iso_aar INTEGER,
        iso_uke INTEGER,
        fyllingsgrad REAL,
        kapasitet_TWh REAL,
        fylling_TWh REAL,
        neste_Publiseringsdato TEXT,
        fyllingsgrad_forrige_uke REAL,
        endring_fyllingsgrad REAL

        )
    ''')




@dec.connection("vannmagasin.db")
def createMaxMinFyllingsgrad(cursor):
    


    #Vurder å legge til evaluering om hvorvidt tabell eksisterer eller ikke, og rapporter om den ble opprettet eller eksisterte

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fyllingsgrad_maxmin (
        ID TEXT PRIMARY KEY, 
        omrType TEXT,
        omrnr INTEGER,
        iso_uke INTEGER,
        minFyllingsgrad REAL,
        minFyllingTWH REAL,
        medianFyllingsGrad REAL,
        medianFylling_TWH REAL,
        maxFyllingsgrad REAL,
        maxFyllingTWH REAL

        )
    ''')



@dec.connection("vannmagasin.db")
def createOmraader(cursor):
    


    #Vurder å legge til evaluering om hvorvidt tabell eksisterer eller ikke, og rapporter om den ble opprettet eller eksisterte

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS omraader (
        navn TEXT,
        navn_langt TEXT,
        beskrivelse TEXT,
        omrType TEXT,
        omrnr INTEGER

        )
    ''')

@dec.connection("vannmagasin.db")
def createNedboer(cursor):
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS nedboer (
        elementId TEXT,
        referenceTime TEXT PRIMARY KEY,
        referenceHour INTEGER,
        iso_dag INTEGER,
        iso_aar INTEGER,
        iso_uke INTEGER,
        nedboer_mm REAL,
        omrnr INTEGER,
        unit TEXT,
        timeOffset TEXT,
        timeResolution TEXT,
        timeSeriesId INTEGER,
        performanceCategory TEXT,
        exposureCategory TEXT,
        qualityCode INTEGER
        

        )
    ''')