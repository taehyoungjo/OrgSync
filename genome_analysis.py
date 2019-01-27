import pandas as pd
import sqlite3

def analyze(file_path):
    return True

def compare(donor, recipients):
    con = sqlite3.connect("database.db")
    donor_df = pd.DataFrame.from_dict(donor)
    recipients_df = pd.read_sql_query("SELECT * FROM recipients", con)
    recipients_gen_df = pd.DataFrame.from_dict(recipients)
    mismatched_df = recipients_gen_df.eq(donor_df.iloc[0], axis='columns')
    mismatched_df = mismatched_df.iloc[:, 0:10]
    counts = mismatched_df.astype(bool).sum(axis=1)
    zeros = 10 - counts
    print(zeros)
    print(zeros[0])
    return zeros
    #results = recipients_df.merge(placeholder_data, left_on='id', right_on='id').to_dict('records')
    #return results