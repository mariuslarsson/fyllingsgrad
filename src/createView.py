import sqlite3
import src.decorators as dec

@dec.connection("vannmagasin.db")
def createView(cursor):
    cursor.execute('''

        CREATE VIEW view_fyllingsgrad AS
                
        SELECT 
                f.fyllingsgrad, f.endring_fyllingsgrad, f.omrnr, f.omrType, f.iso_aar, f.iso_uke, 
                o.navn, o.navn_langt,
                m.minFyllingsgrad, m.medianFyllingsGrad, m.maxFyllingsgrad,
                n.nedboer_mm,                
                SUM(n.nedboer_mm) OVER (PARTITION BY f.omrnr ORDER BY f.iso_aar, f.iso_uke) AS kumulativ_nedboer
                   
        FROM fyllingsgrad f
                
        LEFT JOIN omraader o 
                ON f.omrType = o.omrType
                AND f.omrnr = o.omrnr
                   
        LEFT JOIN fyllingsgrad_maxmin m
                ON f.omrType = m.omrType 
                AND f.omrnr = m.omrnr 
                AND f.iso_uke = m.iso_uke
                   
        LEFT JOIN (
                   
                SELECT 
                        iso_aar, 
                        iso_uke, 
                        omrnr, 
                        SUM(nedboer_mm) AS nedboer_mm
                FROM nedboer
                GROUP BY iso_aar, iso_uke, omrnr
        ) n
                ON f.iso_aar = n.iso_aar 
                AND f.iso_uke = n.iso_uke 
                AND f.omrnr = n.omrnr;


    ''')