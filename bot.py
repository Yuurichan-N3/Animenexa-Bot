import requests
import names
import uuid
import json
import os
from solana.keypair import Keypair
import base58
from colorama import init, Fore, Style

# Initialize colorama for colored output
init()

# Endpoint URL
url = "https://api.getwaitlist.com/api/v1/waiter"

# Banner
def print_banner():
    banner = """
╔══════════════════════════════════════════════╗
║     🌟 Waitlist Automation Animenexa Bot     ║
║ Automate submissions to waitlist endpoints!  ║
║  Developed by: https://t.me/sentineldiscus   ║
╚══════════════════════════════════════════════╝
    """
    print(Fore.CYAN + banner + Style.RESET_ALL)

# Function to generate Solana wallet
def generate_solana_wallet():
    keypair = Keypair.generate()
    address = str(keypair.public_key)
    private_key = base58.b58encode(keypair.secret_key).decode('utf-8')
    return address, private_key

# Function to save wallet and email to wallets.json
def save_wallet(email, address, private_key):
    wallet_data = []
    file_path = "wallets.json"
    
    # Load existing wallets if file exists
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r') as f:
                wallet_data = json.load(f)
        except json.JSONDecodeError:
            print(Fore.RED + "Peringatan: wallets.json rusak, mulai dari nol." + Style.RESET_ALL)
    
    # Add new wallet entry
    wallet_entry = {
        "email": email,
        "address": address,
        "private_key": private_key
    }
    wallet_data.append(wallet_entry)
    
    # Save updated wallets
    try:
        with open(file_path, 'w') as f:
            json.dump(wallet_data, f, indent=4)
    except Exception as e:
        print(Fore.RED + f"Error nyimpen ke wallets.json: {e}" + Style.RESET_ALL)

# Function to get referral code
def get_referral_code():
    ref_code = input("Masukin kode referral (tekan Enter buat random): ").strip()
    return ref_code if ref_code else str(uuid.uuid4())

# Function to send a single POST request
def send_request(referral_code):
    # Generate payload
    random_name = names.get_first_name().lower()
    email = f"{random_name}@gmail.com"
    solana_address, solana_private_key = generate_solana_wallet()
    
    payload = {
        "waitlist_id": 27439,
        "referral_link": f"https://getwaitlist.com/waitlist/27439?ref_id={referral_code}",
        "heartbeat_uuid": "",
        "widget_type": "WIDGET_1",
        "email": email,
        "answers": [
            {
                "question_value": "(Optional)Submit your SOL wallet ",
                "answer_value": solana_address
            }
        ]
    }
    
    # Send POST request
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print(Fore.GREEN + f"Sukses: {email}" + Style.RESET_ALL)
            # Save wallet and email after successful request
            save_wallet(email, solana_address, solana_private_key)
            return True
        else:
            print(Fore.RED + f"Gagal: {email}" + Style.RESET_ALL)
            return False
    except requests.RequestException as e:
        print(Fore.RED + f"Error: {email}" + Style.RESET_ALL)
        return False

# Main function to handle multiple requests
def main():
    print_banner()
    try:
        num_requests = int(input("Masukin jumlah referral: "))
        if num_requests <= 0:
            print(Fore.RED + "Masukin angka positif, bro." + Style.RESET_ALL)
            return
        
        # Get referral code once for all requests
        referral_code = get_referral_code()
        
        success_count = 0
        for i in range(num_requests):
            print(Fore.YELLOW + f"Referral request {i+1}/{num_requests}..." + Style.RESET_ALL)
            if send_request(referral_code):
                success_count += 1
        
        print(Fore.CYAN + f"\nSelesai: {success_count}/{num_requests} request sukses." + Style.RESET_ALL)
    
    except ValueError:
        print(Fore.RED + "Masukin angka yang valid, bro." + Style.RESET_ALL)

if __name__ == "__main__":
    main()
