import socketio
import threading
import json
import datetime as dt
import pandas as pd
import requests
from colorama import Fore
from colorama import Style
import threading
import time
import pygsheets
import os

f = open("config.json")
config = json.load(f)

c = requests.get(f'https://{config["domain"]}/api/v2/metadata/socket',headers={"Authorization": f"Bearer {config['empireapi']}"})

k = open(f"prices.json")
prices = json.load(k)

items = []

def connect_empire():
    sio = socketio.Client()
    domain = config['domain']
    metadata = c.json()
    user_agent = f'{metadata["user"]["id"]} API Bot'
    @sio.on("connect")
    def connect():
        print("I'm connected!")

    @sio.on("init",namespace="/trade")
    def init(data):
        print(data)
        try:
            if data["authenticated"] == True:
                sio.emit('filters',{'price_max': 9999999},namespace='/trade')
            else:
                identify_data = {
                    'uid': c.json()["user"]["id"],
                    'model': c.json()["user"],
                    'authorizationToken': c.json()['socket_token'],
                    'signature': c.json()['socket_signature']
                }
                sio.emit('identify',identify_data,namespace='/trade')

        except Exception as e:
            print(f"INIT ERROR -> {e}")

    @sio.on("connect_error")
    def connect_error(data):
        print("The connection failed!")
        print(data)
        
        time.sleep(60)
        os.startfile("client.py")
        quit()
    @sio.on("disconnect")
    def disconnect():
        print("I'm disconnected!")

        os.startfile("client.py")
        quit()

    @sio.on('new_item',namespace="/trade")
    def r_new_item(data):
        new_item(data)

    @sio.on('updated_item',namespace="/trade")
    def r_updated_item(data):
        pass

    @sio.on('auction_update',namespace="/trade")
    def r_auction_update(data):
        auction_update(data)

    @sio.on("deleted_item",namespace="/trade")
    def r_deleted_item(data):
        global items
        items = [item for item in items if item["id"] not in data]

    @sio.on('trade_status',namespace="/trade")
    def r_trade_status(data):
        trade_status(data)

    sio.connect(
                url=f"wss://trade.{domain}",
                socketio_path="/s/",
                headers={"User-agent": user_agent},
                transports=["websocket"],
                namespaces=["/trade"]
            )

threading.Thread(target=connect_empire).start()


def new_item(data):
    for item in data:
        try:
            if item["market_value"]/100*0.6135 < prices[item["market_name"]][config["price_compare_source"]]["price"]/100*config["multiplier"] and item["market_value"]/100*0.6135<config["price_range_high"] and item["market_value"]/100*0.6135>config["price_range_low"] and prices[item["market_name"]]["liquidity"]>config["min_liquidity"]:
                skip = False
                if config["price_compare2"]:
                    if item["market_value"]/100*0.6135 > prices[item["market_name"]][config["price_compare_source2"]]["price"]/100*config["multiplier2"]:
                        skip = True
                if config["price_compare_check_profitabilty"]:
                    if (prices[item["market_name"]][config["price_compare_check_profitabilty_source"]]["price"]/100*config["price_compare_check_profitabilty_source_fee"])/(item["market_value"]/100*0.6135)<config["price_compare_check_profitabilty_profit"]:
                        skip = True
                for black in config["blacklist"]:
                    if black in item["market_name"]:
                        skip = True
                if skip == False:
                    item[config["price_compare_source"]] = prices[item["market_name"]][config["price_compare_source"]]["price"]
                    item["liquidity"] = prices[item["market_name"]]["liquidity"]
                    items.append(item)
        except:
            pass

def auction_update(data):
    try:
        global items
        items_to_remove = []
        for item_update in data:
            for item in items:
                if item_update["id"] == item["id"]:
                    item["above_recommended_price"] = item_update["above_recommended_price"]
                    item["auction_highest_bid"] = item_update["auction_highest_bid"]
                    item["auction_highest_bidder"] = item_update["auction_highest_bidder"]
                    item["auction_number_of_bids"] = item_update["auction_number_of_bids"]
                    item["auction_ends_at"] = item_update["auction_ends_at"]
                    delete = False
                    if item["auction_highest_bid"]/100*0.6135 > prices[item["market_name"]][config["price_compare_source"]]["price"]/100*config["multiplier"]:
                        delete = True
                    if config["price_compare2"]:
                        if item["auction_highest_bid"]/100*0.6135 > prices[item["market_name"]][config["price_compare_source2"]]["price"]/100*config["multiplier2"]:
                            delete = True
                    if config["price_compare_check_profitabilty"]:
                        if (prices[item["market_name"]][config["price_compare_check_profitabilty_source"]]["price"]/100*config["price_compare_check_profitabilty_source_fee"])/(item["auction_highest_bid"]/100*0.6135)<config["price_compare_check_profitabilty_profit"]:
                            delete = True
                    if delete:
                        items_to_remove.append(item)
                        print(f"{item['market_name']} is overpriced now.")
        items = [item for item in items if item not in items_to_remove]
    except Exception as e:
        print(f"{Fore.RED}auction_update error: {e}{Style.RESET_ALL}")

def trade_status(data):
    for item in data:
        if item["type"] == "withdrawal" and item["data"]["status"] == 6:
            name = item["data"]["item"]["market_name"]
            market_value = item["data"]["item"]["market_value"]
            bought_price = item["data"]["total_value"]
            bought_date = dt.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            source_price = prices[name][config["price_compare_source"]]["price"] / 100
            price_compare_check_profitabilty_source = prices[name][config["price_compare_check_profitabilty_source"]]["price"] / 100
            source_price2 = prices[name][config["price_compare_source2"]]["price"] / 100
            print(f'{Fore.BLUE}{name} coin = {item["data"]["total_value"]} bought.{Style.RESET_ALL}')

            def create_df():
                df = pd.DataFrame()
                df["market_name"] = name
                df["market_value"] = market_value
                df["total_value"] = bought_price
                df["bought_date"] = bought_date
                df["bought_price"] = df.total_value * 0.6135 / 100
                df["price_compare_source"] = source_price
                if config["price_compare_check_profitabilty"]:
                    df["price_compare_check_profitabilty_source"] = price_compare_check_profitabilty_source
                    df["price_compare_check_profitabilty_source %"] = df.price_compare_check_profitabilty_source * config["price_compare_check_profitabilty_source_fee"] / df.bought_price
                if config["price_compare2"]:
                    df["price_compare_source2"] = source_price2
                return df
            def local_excel():
                df = create_df()
                try:
                    df_read = pd.read_excel(f"items_{c.json()['user']['steam_name']}.xlsx")
                    df = pd.concat([df_read,df],ignore_index=True)
                except:
                    print("No excel found! Creating new.")
                    
                df.to_excel(f"items_{c.json()['user']['steam_name']}.xlsx",index=False)
            def online_excel():
                df = create_df()
                try:
                    file_name = 'client_key.json'
                    gc = pygsheets.authorize(service_file=file_name)
                    sh = gc.open(config['sheet_file_name'])
                    try:
                        a = sh.worksheet_by_title(c.json()['user']['steam_name'])
                    except:
                        sh.add_worksheet(c.json()['user']['steam_name'])

                    url = f"https://docs.google.com/spreadsheets/d/{config['sheet_id']}/gviz/tq?tqx=out:csv&sheet={c.json()['user']['steam_name']}"
                    df_read = pd.read_csv(url)

                    df = pd.concat([df_read,df],ignore_index=True)

                    wks = sh.worksheet('title',c.json()['user']['steam_name'])
                    wks.clear()
                    wks.set_dataframe(df,(1,1))
                except:
                    file_name = 'client_key.json'
                    gc = pygsheets.authorize(service_file=file_name)
                    sh = gc.open(config['sheet_file_name'])
                    try:
                        a = sh.worksheet_by_title(c.json()['user']['steam_name'])
                    except:
                        sh.add_worksheet(c.json()['user']['steam_name'])
                    wks = sh.worksheet('title',c.json()['user']['steam_name'])
                    wks.clear()
                    wks.set_dataframe(df,(1,1))
            if config["local_excel"]:
                local_excel()
            if config["online_excel"]:
                online_excel()

def bid(name,item_id,bid_value):
    try:
        c = requests.post(f"https://{config['domain']}/api/v2/trading/deposit/{item_id}/bid",headers={'Authorization':f'Bearer {config["empireapi"]}'},params={'bid_value':bid_value})
        if c.json()["success"] == True:
            print(f'{Fore.GREEN}{c.json()["success"]} {name} coin = {bid_value} // $ = {round(bid_value/100*0.6135,2)}{Style.RESET_ALL}')
        else:
            print(f'{Fore.LIGHTMAGENTA_EX}{c.json()["success"]} {name} {c.json()["message"]}{Style.RESET_ALL}')
            if c.json()["message"] == "This auction already finished.":
                global items
                items = [item for item in items if item["id"] != item_id]
    except Exception as e:
        print(f"{Fore.RED}bid error: {e}{Style.RESET_ALL}")

threads = {}
t=0
while True:
    completed_threads = [x for x in threads if not threads[x].is_alive()]
    for x in completed_threads:
        del threads[x]
    for item in items:
        if item["auction_highest_bidder"] != c.json()["user"]["id"]:
            fiyat = round(item["auction_highest_bid"]*1.01) if item["auction_highest_bid"] is not None else round(item["market_value"])

            if item["id"] not in threads.keys():
                p = threading.Thread(target=bid, args=(item["market_name"],item["id"],fiyat))
                threads[item["id"]] = p
                p.start()
                print(f'{Fore.YELLOW}BID {item["market_name"]} {fiyat} {round(fiyat*0.6135/100,2)}$ source = {item[config["price_compare_source"]]/100}${Style.RESET_ALL}')

    if t ==1000:
        print("------------------------------------------------------------")
        t=0
    t=t+1
    
    time.sleep(config["bid_timer"])
