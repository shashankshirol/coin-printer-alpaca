import yfinance as yf

import os

import utils

def init_folder() -> str:
    cwd = os.getcwd()
    db_path = utils.load_config("config.toml")["db"]["path_"]
    db_path = os.path.join(cwd, db_path)

    if not os.path.exists(db_path):
        os.makedirs(db_path)
    
    return db_path

def generate_data(debug: bool = True):
    path_ = init_folder()
    companies = utils.load_yaml("company_roster.yaml").get("top_30_sp500")
    for _,v in companies.items():
        data = yf.download(tickers= "AAPL" if debug else v, period="1d" if debug else "5d")
        store_path = os.path.join(path_, v + ".pickle")
        data.to_pickle(store_path)
    
    pass