# fyllingsgrad

                        ┌───────────────────────────┐
                        │        fyllingsgrad       │
                        │---------------------------│
                        │ fyllingsgrad              │
                        │ endring_fyllingsgrad      │
                        │ omrnr                     │
                        │ omrType                   │
                        │ iso_aar                   │
                        │ iso_uke                   │
                        └──────────┬────────────────┘
                                   │ LEFT JOIN on omrType, omrnr, iso_uke, iso_aar
               ┌───────────────────┴───────────────────┐
               │                                       │
   ┌───────────────────────┐               ┌────────────────────────┐
   │       omraader        │               │  fyllingsgrad_maxmin   │
   │-----------------------│               │------------------------│
   │ omrType               │               │ omrType                │
   │ omrnr                 │               │ omrnr                  │
   │ navn                  │               │ iso_uke                │
   └─────────────┬─────────┘               │ minFyllingsgrad        │
                 │                         │ medianFyllingsGrad     │
                 │                         │ maxFyllingsgrad        │
                 │                         └────────────┬───────────┘
                 │                                      │ LEFT JOIN on omrType, omrnr, iso_uke
                 │                                      │
                 │                                      │
                 │                            ┌─────────┴─────────────┐
                 │                            │      nedboer          │
                 │                            │-----------------------│
                 │                            │ iso_aar               │
                 │                            │ iso_uke               │
                 │                            │ omrnr                 │
                 │                            │ value                 │
                 │                            │ (filtered:            │
                 │                            │  referenceHour = 0,   │
                 │                            │  iso_dag = 1)         │
                 │                            └────────────┬──────────┘
                 │                                         │ LEFT JOIN on iso_aar, iso_uke, omrnr
                 │                                         │
                 └─────────────────────────────────────────┴───────────────┐
                                                               view_fyllingsgrad
                                               ┌──────────────────────────────┐
                                               │ fyllingsgrad                 │
                                               │ endring_fyllingsgrad         │
                                               │ omrnr                        │
                                               │ omrType                      │
                                               │ iso_aar                      │
                                               │ iso_uke                      │
                                               │ navn (fra omraader)          │
                                               │ minFyllingsgrad              │
                                               │ medianFyllingsGrad           │
                                               │ maxFyllingsgrad              │
                                               │ value (nedbør)               │
                                               └──────────────────────────────┘
