import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

def genFigs():

    conn = sqlite3.connect("vannmagasin.db")

    view_fyllingsgrad_omrnr1 = pd.read_sql("""
        SELECT * FROM view_fyllingsgrad
        -- Litt tilfeldig valgt data for omrnr == 1
        WHERE iso_aar IN (2020,2021, 2022)    
        AND omrnr in (1)     
        ORDER BY iso_uke
                """, conn)


    view_fyllingsgrad_omrnr1["date"] = view_fyllingsgrad_omrnr1["iso_aar"].astype(str) +"-"+ view_fyllingsgrad_omrnr1["iso_uke"].astype(str)
    view_fyllingsgrad_omrnr1["date_day"] = pd.to_datetime(view_fyllingsgrad_omrnr1['date'] + '-1', format='%Y-%W-%w')

    fyllingsgrad_filtrert = view_fyllingsgrad_omrnr1.loc[lambda x: x["omrType"] == "VASS"].loc[lambda x: x["omrnr"] == 1]

    OMRNR_NAVN = fyllingsgrad_filtrert["navn_langt"].values[0]

    #Setter layout 
    fig, (ax1, ax2, ax3) = plt.subplots(nrows = 3, ncols = 1, figsize = (12, 10))

    fyllingsgrad_filtrert.loc[lambda x: x["date_day"] > "2019-12-01"].sort_values("date")\
        .plot(x="date_day", 
            y=["fyllingsgrad", "minFyllingsgrad", "maxFyllingsgrad", "medianFyllingsGrad"], 
            color = ["blue", "grey", "grey", "red"],
            ax=ax1)
    ax1.set_title(f"Fyllingsgrad {OMRNR_NAVN} sammenlignet med historiske tall siste 20 år\n (referanseår 2024)")
    lines1 = ax1.get_lines()
    lines1[1].set_alpha(0.5)
    lines1[2].set_alpha(0.5)


    fyllingsgrad_filtrert.loc[lambda x: x["date_day"] > "2021-12-01"].sort_values("date")\
        .plot(x="date_day", 
            y=["endring_fyllingsgrad", "nedboer_mm"], 
            secondary_y = ["nedboer_mm"],
            ax=ax2)
    ax2.set_title(f"Endring fyllingsgrad og nedbør {OMRNR_NAVN}")


    fyllingsgrad_filtrert.loc[lambda x: x["date_day"] > "2021-12-01"].sort_values("date")\
        .plot(x="date_day", 
            y=["fyllingsgrad", "kumulativ_nedboer"], 
            secondary_y = ["kumulativ_nedboer"],
            ax=ax3)
    ax3.set_title(f"Fyllingsgrad og kumulativ nedbør {OMRNR_NAVN}")

    plt.tight_layout()
    plt.show()

    conn.close()


if __name__ == "__main__":
    genFigs()