from os import execve
import pandas as pd 
import argparse

event_df = pd.read_csv("event_tracking.csv")
print(event_df)