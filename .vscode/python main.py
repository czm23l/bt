import requests
from bitcoinlib.wallets import Wallet

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

def main():
    # Exemplu: lista de chei private WIF din portofelul vechi
    old_wallet_keys = [
        # "L1aW4aubDFB7yfras2S1mN3bqg9w7r5ZQ5Q2...",  # adaugă aici cheile tale WIF
    ]
    for wif in old_wallet_keys:
        w = Wallet.create('scanwallet', keys=wif, network='bitcoin')
        address = w.get_key().address
        balance = get_balance(address)
        print(f"Adresa {address} are {balance} BTC")
        if balance > 0:
            print(f"Trimit {balance} BTC către {MY_ADDRESS}")
            send_btc(wif, MY_ADDRESS, balance)

if __name__ == "__main__":
    main()
    
# pip install bitcoinlib requests
python ".vscode/python main.py"