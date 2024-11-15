import os
import utils
import yfinance as yf
from tinydb import TinyDB, Query
from datetime import datetime, timedelta
from typing import Optional

def init_tdb() -> TinyDB:
    path = "variables.json"
    db = TinyDB(path)
    return db

def get_last_fetch() -> Optional[datetime]:
    db = init_tdb()
    update_table = db.table("update")
    if not update_table.all():
        return None
    return datetime.strptime(update_table.all()[0]["last_fetch"], '%Y-%m-%d')

def init_folder() -> str:
    cwd = os.getcwd()
    db_path = utils.load_config("config.toml")["db"]["path_"]
    db_path = os.path.join(cwd, db_path)

    if not os.path.exists(db_path):
        os.makedirs(db_path)
    
    return db_path

def generate_data(debug: bool = True):
    path_ = init_folder()
    db = init_tdb()
    update_table = db.table("update")

    if (debug):
        companies = {"Apple Inc.": "AAPL"}
    else:
        companies = utils.load_yaml("company_roster.yaml").get("top_30_sp500")
    
    # don't fetch data if latest fetch is recent
    last_fetch = get_last_fetch()
    if not debug and last_fetch and datetime.today() - last_fetch < timedelta(days=5):
        print("||||| Not fetching new data, latest fetch is less than 5 days old. |||||")
        return
    
    # fetch data in a 5 minute interval over a 60 day period
    for _,v in companies.items():
        symbol = yf.Ticker(v)
        data = symbol.history(interval="2m", start=(datetime.today() - timedelta(days=50)).strftime('%Y-%m-%d'), end=datetime.today().strftime('%Y-%m-%d'))
        store_path = os.path.join(path_, v + ".pickle")
        data.to_pickle(store_path)

    if not debug:
        if not update_table.all():
            update_table.insert({"last_fetch": datetime.today().strftime('%Y-%m-%d')})
        else:
            update_table.update({"last_fetch": datetime.today().strftime('%Y-%m-%d')})
    
    pass