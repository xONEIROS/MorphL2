"""
ETH Transfer Bot for MorphL2(TESTNET) 

This script automates the process of creating random wallets and sending ETH transactions
on the MorphL2 network (TESTNET). It creates as many wallets as the number of transactions specified.

Author: 0xOneiros
Twitter: https://x.com/0xOneiros

Disclaimer: Use this script at your own risk. Make sure you understand the implications
of automated transactions on the blockchain.
"""

import time
import random
from web3 import Web3
from colorama import init, Fore, Style

init(autoreset=True)

MORPH_L2_RPC_URL = "https://rpc-holesky.morphl2.io"  

def get_user_input(prompt, input_type=str):
    while True:
        try:
            user_input = input_type(input(prompt))
            return user_input
        except ValueError:
            print(f"{Fore.RED}Invalid input. Please try again.{Style.RESET_ALL}")

def generate_random_address(w3):
    random_address = '0x' + ''.join(random.choices('0123456789abcdef', k=40))
    return w3.to_checksum_address(random_address)
def send_transaction(w3, from_account, to_address, amount):
    nonce = w3.eth.get_transaction_count(from_account.address)
    gas_price = w3.eth.gas_price
    gas_limit = 21000  
    tx = {
        'nonce': nonce,
        'to': to_address,
        'value': w3.to_wei(amount, 'ether'),
        'gas': gas_limit,
        'gasPrice': gas_price,
        'chainId': w3.eth.chain_id
    }
    signed_tx = from_account.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    return tx_hash

def main():
    print(f"{Fore.CYAN}ETH Transfer Bot for MorphL2 Network!{Style.RESET_ALL}")
    print(f"Follow on Twitter: {Fore.BLUE}https://x.com/0xOneiros{Style.RESET_ALL}")
    print("=" * 70)

    w3 = Web3(Web3.HTTPProvider(MORPH_L2_RPC_URL))
    
    if not w3.is_connected():
        print(f"{Fore.RED}Failed to connect to MorphL2 network. Please check your internet connection and RPC URL.{Style.RESET_ALL}")
        return

    private_key = get_user_input("Please enter the sender's private key: ")
    account = w3.eth.account.from_key(private_key)
    balance = w3.eth.get_balance(account.address)
    print(f"{Fore.GREEN}Connected to MorphL2 network.{Style.RESET_ALL}")
    print(f"Account address: {account.address}")
    print(f"Account balance: {w3.from_wei(balance, 'ether')} ETH")

    num_transactions = get_user_input("Number of transactions (This will also be the number of wallets created): ", int)
    transaction_interval = get_user_input("Interval between transactions (in seconds): ", int)
    amount_to_send = get_user_input("Amount of ETH to send in each transaction: ", float)

    if w3.to_wei(amount_to_send, 'ether') * num_transactions > balance:
        print(f"{Fore.RED}Insufficient balance for all transactions. Please reduce the number of transactions or the amount to send.{Style.RESET_ALL}")
        return

    random_wallets = [generate_random_address(w3) for _ in range(num_transactions)]
    print(f"{Fore.YELLOW}{num_transactions} random wallets created.{Style.RESET_ALL}")

    for i, to_address in enumerate(random_wallets):
        try:
            tx_hash = send_transaction(w3, account, to_address, amount_to_send)
            print(f"{Fore.GREEN}Transaction {i+1}/{num_transactions}: Sent {amount_to_send} ETH")
            print(f"Transaction hash: {tx_hash.hex()}{Style.RESET_ALL}")
            w3.eth.wait_for_transaction_receipt(tx_hash)
            print(f"{Fore.GREEN}Transaction confirmed.{Style.RESET_ALL}")
            time.sleep(transaction_interval)
        except Exception as e:
            print(f"{Fore.RED}Error in transaction {i+1}: {str(e)}{Style.RESET_ALL}")
            time.sleep(10)  
    print(f"{Fore.CYAN}All transactions completed.{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Removing created wallets from memory...{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}All {num_transactions} wallets have been removed from memory.{Style.RESET_ALL}")
    print(f"{Fore.GREEN}Operation completed successfully.{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
