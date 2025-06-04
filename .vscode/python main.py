import requests

def get_balance(address):
    url = f"https://blockchain.info/q/addressbalance/{address}"
    r = requests.get(url)
    if r.ok:
        return int(r.text) / 1e8  # BTC
    return 0

# Your Python code goes here, for example:
def main():
	print("Hello, world!")

if __name__ == "__main__":
	main()