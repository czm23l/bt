import requests
from bitcoinlib.wallets import Wallet

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

# Your Python code goes here, for example:
def main():
	print("Hello, world!")

if __name__ == "__main__":
	main()