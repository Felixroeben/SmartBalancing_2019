import pandas as pd
import numpy as np
import datetime

WC_Generation1 = pd.read_csv("WC_Generation_1.csv",sep=";",decimal=".")
WC_Generation2 = pd.read_csv("WC_Generation_2.csv",sep=";",decimal=".")
WC_Generation = pd.concat([WC_Generation1, WC_Generation2], axis=1, sort=False)
WC_Generation.to_csv("WC_Generation.csv",sep=";",decimal=".",index=False)