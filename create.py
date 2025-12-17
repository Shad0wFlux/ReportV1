import requests
import time
import uuid
import random
import string
import re
import logging
import argparse
import os
import imaplib
import email
from datetime import datetime
from tqdm import tqdm
from email.header import decode_header
from email.utils import getaddresses

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("instagram_creator.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    ORANGE = '\033[38;5;208m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_banner():
    banner = f"""
{Colors.CYAN}{Colors.BOLD}╔══════════════════════════════════════════════╗
║  {Colors.MAGENTA}▪ INSTAGRAM ACCOUNT CREATOR TOOL ▪{Colors.CYAN}         ║
╠══════════════════════════════════════════════╣
║  {Colors.GREEN}➤ Author   : {Colors.WHITE}EK6Q{Colors.CYAN}                     ║
║  {Colors.GREEN}➤ Version  : {Colors.WHITE}3.0 (Gmail Edition){Colors.CYAN}       ║
║  {Colors.GREEN}➤ Email    : {Colors.WHITE}Gmail with App Password{Colors.CYAN}   ║
╚══════════════════════════════════════════════╝{Colors.RESET}
"""
    print(banner)

def generate_random_string(length):
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))

def generate_user_agent():
    mobile_agents = [
        "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Instagram 243.0.0.12.111",
        "Mozilla/5.0 (Linux; Android 13; SM-S901B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 12; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36"
    ]
    return random.choice(mobile_agents)

def load_gmail_credentials():
    """Load Gmail credentials from credentials.txt file"""
    try:
        credentials = []
        if os.path.exists('credentials.txt'):
            with open('credentials.txt', 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and ':' in line:
                        email, app_password = line.split(':', 1)
                        credentials.append({
                            'email': email.strip(),
                            'app_password': app_password.strip()
                        })
            return credentials
        else:
            print(f"{Colors.YELLOW}[!] Creating credentials.txt file...{Colors.RESET}")
            with open('credentials.txt', 'w') as f:
                f.write("# Format: email:app_password\n")
                f.write("# Example: yourgmail@gmail.com:your_app_password\n")
            return []
    except Exception as e:
        print(f"{Colors.RED}[!] Error loading credentials: {e}{Colors.RESET}")
        return []

def verify_gmail_auth(email, app_password):
    """Verify Gmail authentication"""
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
        mail.login(email, app_password)
        mail.logout()
        print(f"{Colors.GREEN}[+] Gmail authentication successful for {email}{Colors.RESET}")
        return True
    except imaplib.IMAP4.error as e:
        print(f"{Colors.RED}[!] Gmail authentication failed (IMAP error): {e}{Colors.RESET}")
        return False
    except Exception as e:
        print(f"{Colors.RED}[!] Gmail authentication failed (Other error): {e}{Colors.RESET}")
        return False

def get_gmail_verification_code(email, app_password, target_email, max_retries=20, delay=5):
    """Get verification code from Gmail inbox"""
    print(f"\n{Colors.CYAN}[*] Waiting for verification code from Instagram...{Colors.RESET}")
    pbar = tqdm(total=max_retries, desc="Searching for code", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} attempts")
    
    for retry in range(max_retries):
        try:
            pbar.update(1)
            
            mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
            mail.login(email, app_password)
            mail.select("inbox")
            
            # Search for emails from Instagram
            status, data = mail.search(None, 'FROM', '"no-reply@mail.instagram.com"')
            mail_ids = data[0].split()
            
            if mail_ids:
                # Get the latest email
                latest_id = mail_ids[-1]
                status, msg_data = mail.fetch(latest_id, "(RFC822)")
                
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        
                        # Decode subject
                        subject, encoding = decode_header(msg["subject"])[0]
                        if isinstance(subject, bytes):
                            subject = subject.decode(encoding if encoding else "utf-8", errors="ignore")
                        
                        # Extract recipient emails
                        to_emails = [addr[1] for addr in getaddresses([msg["to"]])]
                        
                        # Check if email is for target email
                        if target_email in to_emails:
                            # Search for verification code in subject
                            code_match = re.search(r'\b\d{4,6}\b', subject)
                            if code_match:
                                pbar.close()
                                mail.logout()
                                print(f"{Colors.GREEN}[+] Verification code found!{Colors.RESET}")
                                return code_match.group(0)
                            
                            # If not in subject, check in body
                            if msg.is_multipart():
                                for part in msg.walk():
                                    if part.get_content_type() == "text/plain":
                                        body = part.get_payload(decode=True).decode(errors='ignore')
                                        code_match = re.search(r'\b\d{4,6}\b', body)
                                        if code_match:
                                            pbar.close()
                                            mail.logout()
                                            print(f"{Colors.GREEN}[+] Verification code found in body!{Colors.RESET}")
                                            return code_match.group(0)
                            else:
                                body = msg.get_payload(decode=True).decode(errors='ignore')
                                code_match = re.search(r'\b\d{4,6}\b', body)
                                if code_match:
                                    pbar.close()
                                    mail.logout()
                                    print(f"{Colors.GREEN}[+] Verification code found in body!{Colors.RESET}")
                                    return code_match.group(0)
                
                mail.logout()
            
            time.sleep(delay)
            
        except Exception as e:
            print(f"{Colors.YELLOW}[!] Error while searching for verification code: {e}{Colors.RESET}")
            time.sleep(delay)
            try:
                mail.logout()
            except:
                pass
    
    pbar.close()
    print(f"{Colors.RED}[!] Timeout waiting for verification code{Colors.RESET}")
    logger.error("Timeout waiting for verification code")
    return None

def generate_random_name():
    first_names = ["أحمد", "محمد", "سارة", "فاطمة", "نور", "علي", "عمر", "مريم", "حسن", "ليلى", 
                  "Alex", "Emma", "Noah", "Sophia", "Liam", "Olivia", "John", "Zoe", "Ryan", "Lily"]
    return random.choice(first_names)

def generate_random_birthday():
    current_year = datetime.now().year
    year = random.randint(current_year - 45, current_year - 18)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    return day, month, year

def create_dot_emails(base_email):
    """Create dot variations of email address"""
    email_parts = base_email.split('@')
    if len(email_parts) != 2:
        return []
    
    username = email_parts[0].replace('.', '')
    domain = email_parts[1]
    
    positions = len(username) - 1
    all_combinations = []
    
    # Generate all possible dot combinations
    for i in range(2 ** positions):
        comb = format(i, f'0{positions}b')
        s = username[0]
        for j in range(positions):
            if comb[j] == '1':
                s += '.'
            s += username[j + 1]
        all_combinations.append(f"{s}@{domain}")
    
    return all_combinations

class GmailManager:
    def __init__(self):
        self.credentials = load_gmail_credentials()
        self.current_index = 0
        self.dot_emails_cache = {}
        
    def get_next_credential(self):
        """Get next available Gmail credential"""
        if not self.credentials:
            return None
        
        credential = self.credentials[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.credentials)
        return credential
    
    def get_dot_emails(self, base_email):
        """Get or create dot emails for a base email"""
        if base_email not in self.dot_emails_cache:
            self.dot_emails_cache[base_email] = create_dot_emails(base_email)
        return self.dot_emails_cache[base_email]
    
    def get_random_dot_email(self, base_email):
        """Get random dot email variation"""
        dot_emails = self.get_dot_emails(base_email)
        if not dot_emails:
            return base_email
        return random.choice(dot_emails)
    
    def remove_dot_email(self, base_email, dot_email):
        """Remove used dot email from cache"""
        if base_email in self.dot_emails_cache and dot_email in self.dot_emails_cache[base_email]:
            self.dot_emails_cache[base_email].remove(dot_email)

class InstagramAccountCreator:
    def __init__(self, save_to_file=True):
        self.save_to_file = save_to_file
        self.success_count = 0
        self.fail_count = 0
        self.gmail_manager = GmailManager()
        
    def create_account(self):
        logger.info("Starting account creation process...")
        
        # Get Gmail credential
        credential = self.gmail_manager.get_next_credential()
        if not credential:
            print(f"{Colors.RED}[!] No Gmail credentials found in credentials.txt{Colors.RESET}")
            print(f"{Colors.YELLOW}[!] Please add credentials in format: email:app_password{Colors.RESET}")
            self.fail_count += 1
            return False
        
        base_email = credential['email']
        app_password = credential['app_password']
        
        # Verify Gmail authentication
        print(f"{Colors.YELLOW}[*] Verifying Gmail authentication...{Colors.RESET}")
        if not verify_gmail_auth(base_email, app_password):
            self.fail_count += 1
            return False
        
        # Get random dot email
        email = self.gmail_manager.get_random_dot_email(base_email)
        print(f"{Colors.GREEN}[+] Using email: {Colors.CYAN}{email}{Colors.RESET}")
        logger.info(f"Using email: {email}")
        
        device_id = f"android-{generate_random_string(16)}"
        st4_user_agent = generate_user_agent()
        st4_time = str(time.time()).split('.')[1]
        
        print(f"{Colors.YELLOW}[*] Checking email availability...{Colors.RESET}")
        url = "https://www.instagram.com/api/v1/web/accounts/check_email/"
        payload = {
            'email': email,
        }
        headers = {
            'User-Agent': st4_user_agent, 
            'sec-ch-ua': "\"Not A(Brand\";v=\"8\", \"Chromium\";v=\"132\"",
            'x-ig-www-claim': "0",
            'x-web-session-id': "o7brq2:ihhkws:b833kp",
            'sec-ch-ua-platform-version': "\"14.0.0\"",
            'x-requested-with': "XMLHttpRequest",
            'sec-ch-ua-full-version-list': "\"Not A(Brand\";v=\"8.0.0.0\", \"Chromium\";v=\"132.0.6961.0\"",
            'sec-ch-prefers-color-scheme': "dark",
            'x-csrftoken': "8D26VZbnpmxsokorogKvshOiKojeTii5",
            'sec-ch-ua-platform': "\"Android\"",
            'x-ig-app-id': "1217981644879628",
            'sec-ch-ua-model': "\"RMX3941\"",
            'sec-ch-ua-mobile': "?1",
            'x-instagram-ajax': "1021370996",
            'x-asbd-id': "359341",
            'origin': "https://www.instagram.com",
            'sec-fetch-site': "same-origin",
            'sec-fetch-mode': "cors",
            'sec-fetch-dest': "empty",
            'referer': "https://www.instagram.com/accounts/signup/email/",
            'accept-language': "en",
        }
        
        try:
            st4_session = requests.Session()
            response = st4_session.post(url, data=payload, headers=headers).text
            if '"available":true' not in response:
                print(f"{Colors.RED}[!] Email not available{Colors.RESET}")
                logger.error(f"Email not available: {response}")
                
                # Try another dot email
                self.gmail_manager.remove_dot_email(base_email, email)
                dot_emails = self.gmail_manager.get_dot_emails(base_email)
                if dot_emails:
                    email = random.choice(dot_emails)
                    print(f"{Colors.YELLOW}[*] Trying alternative email: {email}{Colors.RESET}")
                    return self.create_account()
                else:
                    self.fail_count += 1
                    return False
                    
            print(f"{Colors.GREEN}[+] Email availability check passed{Colors.RESET}")
            logger.info("Email availability check passed")
        except requests.exceptions.RequestException as e:
            print(f"{Colors.RED}[!] Error during email check: {e}{Colors.RESET}")
            logger.error(f"Error during email check: {e}")
            self.fail_count += 1
            return False

        print(f"{Colors.YELLOW}[*] Sending verification email...{Colors.RESET}")
        url = "https://www.instagram.com/api/v1/accounts/send_verify_email/"
        payload = {
            'device_id': device_id,
            'email': email,  
        }
        
        try:
            response = st4_session.post(url, data=payload, headers=headers).text
            if '"email_sent":true' not in response:
                print(f"{Colors.RED}[!] Failed to send verification email{Colors.RESET}")
                logger.error(f"Failed to send verification email: {response}")
                self.fail_count += 1
                return False
                
            print(f"{Colors.GREEN}[+] Verification email sent successfully{Colors.RESET}")
            logger.info("Verification email sent successfully")
        except requests.exceptions.RequestException as e:
            print(f"{Colors.RED}[!] Error sending verification email: {e}{Colors.RESET}")
            logger.error(f"Error sending verification email: {e}")
            self.fail_count += 1
            return False

        # Get verification code from Gmail
        st4_code = get_gmail_verification_code(base_email, app_password, email)
        if not st4_code:
            print(f"{Colors.RED}[!] Failed to get verification code{Colors.RESET}")
            logger.error("Failed to get verification code")
            self.fail_count += 1
            return False
            
        print(f"{Colors.GREEN}[+] Received verification code: {Colors.CYAN}{st4_code}{Colors.RESET}")
        logger.info(f"Received verification code: {st4_code}")

        print(f"{Colors.YELLOW}[*] Validating confirmation code...{Colors.RESET}")
        url = "https://www.instagram.com/api/v1/accounts/check_confirmation_code/"
        payload = {
            'code': st4_code,
            'device_id': device_id,
            'email': email,
        }
        
        try:
            response = st4_session.post(url, data=payload, headers=headers)
            try:
                st4_newCode = response.json()['signup_code']
                print(f"{Colors.GREEN}[+] Confirmation code validated successfully{Colors.RESET}")
                logger.info("Confirmation code validated successfully")
            except Exception as e:
                print(f"{Colors.RED}[!] Failed to get signup code: {e}{Colors.RESET}")
                logger.error(f"Failed to get signup code: {e}")
                self.fail_count += 1
                return False
        except requests.exceptions.RequestException as e:
            print(f"{Colors.RED}[!] Error checking confirmation code: {e}{Colors.RESET}")
            logger.error(f"Error checking confirmation code: {e}")
            self.fail_count += 1
            return False

        print(f"{Colors.YELLOW}[*] Generating account details...{Colors.RESET}")
        st4_password = ''.join(random.choice(string.ascii_letters + string.digits + '!@#$%^&*()') for _ in range(12))
        username = f"user_{generate_random_string(8).lower()}"
        st4_first_name = generate_random_name()
        st4_day, st4_month, st4_year = generate_random_birthday()

        print(f"{Colors.YELLOW}[*] Creating Instagram account...{Colors.RESET}")
        url = "https://www.instagram.com/api/v1/web/accounts/web_create_ajax/"
        payload = {
            'enc_password': f"#PWD_INSTAGRAM_BROWSER:0:{st4_time}:{st4_password}",
            'day': st4_day,
            'email': email,
            'failed_birthday_year_count': "{}",
            'first_name': st4_first_name,
            'month': st4_month,
            'username': username,
            'year': st4_year,
            'client_id': device_id,
            'seamless_login_enabled': "1",
            'tos_version': "row",
            'force_sign_up_code': st4_newCode,  
        }
        headers = {
            'User-Agent': st4_user_agent, 
            'sec-ch-ua': "\"Not A(Brand\";v=\"8\", \"Chromium\";v=\"132\"",
            'x-ig-www-claim': "0",
            'x-web-session-id': "v3s3xo:8vy7v8:i14b7i",
            'sec-ch-ua-platform-version': "\"14.0.0\"",
            'x-requested-with': "XMLHttpRequest",
            'sec-ch-ua-full-version-list': "\"Not A(Brand\";v=\"8.0.0.0\", \"Chromium\";v=\"132.0.6961.0\"",
            'sec-ch-prefers-color-scheme': "dark",
            'x-csrftoken': "B6yOLYbJgFWFh2e0rNe2wZHXbnPZw9LP",
            'sec-ch-ua-platform': "\"Android\"",
            'x-ig-app-id': "1217981644879628",
            'sec-ch-ua-model': "\"RMX3941\"",
            'sec-ch-ua-mobile': "?1",
            'x-instagram-ajax': "1021374421",
            'x-asbd-id': "359341",
            'origin': "https://www.instagram.com",
            'sec-fetch-site': "same-origin",
            'sec-fetch-mode': "cors",
            'sec-fetch-dest': "empty",
            'referer': "https://www.instagram.com/accounts/signup/username/",
            'accept-language': "en",
        }
        
        try:
            response = requests.post(url, data=payload, headers=headers)
            
            if '"account_created":true' not in response.text:
                print(f"{Colors.RED}[!] Account creation failed{Colors.RESET}")
                logger.error(f"Account creation failed: {response.text}")
                self.fail_count += 1
                return False
                
            ST4_SESSION = response.cookies.get_dict().get('sessionid')
            if not ST4_SESSION:
                print(f"{Colors.RED}[!] Failed to get session ID{Colors.RESET}")
                logger.error("Failed to get session ID")
                self.fail_count += 1
                return False
                
            print(f"\n{Colors.GREEN}{Colors.BOLD}✅ ACCOUNT CREATED SUCCESSFULLY! ✅{Colors.RESET}\n")
            
            account_info = [
                f"{Colors.CYAN}╔{'═' * 50}╗",
                f"║ {Colors.GREEN}INSTAGRAM ACCOUNT DETAILS{Colors.CYAN}{' ' * 28}║",
                f"╠{'═' * 50}╣",
                f"║ {Colors.YELLOW}• Username:{Colors.WHITE}{' ' * (41 - len(username))}{username}{Colors.CYAN} ║",
                f"║ {Colors.YELLOW}• Password:{Colors.WHITE}{' ' * (41 - len(st4_password))}{st4_password}{Colors.CYAN} ║",
                f"║ {Colors.YELLOW}• Email:{Colors.WHITE}{' ' * (44 - len(email))}{email}{Colors.CYAN} ║",
                f"║ {Colors.YELLOW}• Base Email:{Colors.WHITE}{' ' * (40 - len(base_email))}{base_email}{Colors.CYAN} ║",
                f"║ {Colors.YELLOW}• First Name:{Colors.WHITE}{' ' * (39 - len(st4_first_name))}{st4_first_name}{Colors.CYAN} ║",
                f"║ {Colors.YELLOW}• Birthday:{Colors.WHITE}{' ' * (33)}{st4_year}-{st4_month}-{st4_day}{Colors.CYAN} ║",
                f"║ {Colors.YELLOW}• Session ID:{Colors.WHITE}{' ' * (40 - len(ST4_SESSION[:10]))}{ST4_SESSION[:10]}...{Colors.CYAN} ║",
                f"║ {Colors.YELLOW}• Created At:{Colors.WHITE}{' ' * (30)}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.CYAN} ║",
                f"╚{'═' * 50}╝{Colors.RESET}"
            ]
            
            for line in account_info:
                print(line)
            
            logger.info("Account created successfully!")
            
            # Remove used dot email
            self.gmail_manager.remove_dot_email(base_email, email)
            
            if self.save_to_file:
                with open("ACC_SESSIONS_IG.txt", "a") as f:
                    f.write(f"{ST4_SESSION}\n")
                    
                with open("instagram_accounts.txt", "a", encoding="utf-8") as f:
                    f.write(f"Username: {username}\n")
                    f.write(f"Password: {st4_password}\n")
                    f.write(f"Email: {email}\n")
                    f.write(f"Base Email: {base_email}\n")
                    f.write(f"First Name: {st4_first_name}\n")
                    f.write(f"Birthday: {st4_year}-{st4_month}-{st4_day}\n")
                    f.write(f"Session ID: {ST4_SESSION}\n")
                    f.write(f"Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write("=" * 50 + "\n")
                
                print(f"\n{Colors.GREEN}[+] Account details saved to 'instagram_accounts.txt'{Colors.RESET}")
                print(f"{Colors.GREEN}[+] Session ID saved to 'ACC_SESSIONS_IG.txt'{Colors.RESET}")
                
            self.success_count += 1
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"{Colors.RED}[!] Error during account creation: {e}{Colors.RESET}")
            logger.error(f"Error during account creation: {e}")
            self.fail_count += 1
            return False

def get_user_input():
    try:
        print(f"\n{Colors.YELLOW}{Colors.BOLD}How many Instagram accounts do you want to create?{Colors.RESET}")
        while True:
            try:
                count = int(input(f"{Colors.CYAN}Enter number (1-100): {Colors.RESET}"))
                if 1 <= count <= 100:
                    break
                print(f"{Colors.RED}Please enter a number between 1 and 100.{Colors.RESET}")
            except ValueError:
                print(f"{Colors.RED}Please enter a valid number.{Colors.RESET}")
        
        print(f"\n{Colors.YELLOW}{Colors.BOLD}Delay between account creations (seconds):{Colors.RESET}")
        while True:
            try:
                delay = int(input(f"{Colors.CYAN}Enter delay (5-120): {Colors.RESET}"))
                if 5 <= delay <= 120:
                    break
                print(f"{Colors.RED}Please enter a number between 5 and 120.{Colors.RESET}")
            except ValueError:
                print(f"{Colors.RED}Please enter a valid number.{Colors.RESET}")
        
        print(f"\n{Colors.YELLOW}{Colors.BOLD}Save accounts to file?{Colors.RESET}")
        while True:
            save = input(f"{Colors.CYAN}Save to file? (Y/n): {Colors.RESET}").lower()
            if save in ['', 'y', 'yes', 'n', 'no']:
                save_to_file = save != 'n' and save != 'no'
                break
            print(f"{Colors.RED}Please enter Y or N.{Colors.RESET}")
            
        return count, delay, save_to_file
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}Operation cancelled by user.{Colors.RESET}")
        exit(0)

def main():
    try:
        clear_screen()
        display_banner()
        
        # Check if credentials.txt exists
        if not os.path.exists('credentials.txt'):
            print(f"{Colors.YELLOW}[!] Creating credentials.txt file...{Colors.RESET}")
            print(f"{Colors.CYAN}Please add your Gmail credentials in this format:{Colors.RESET}")
            print(f"{Colors.WHITE}yourgmail@gmail.com:your_app_password{Colors.RESET}\n")
            with open('credentials.txt', 'w') as f:
                f.write("# Format: email:app_password\n")
                f.write("# Example: yourgmail@gmail.com:your_app_password\n")
                f.write("# Note: You need to enable 2FA and create App Password in Google Account\n")
        
        count, delay, save_to_file = get_user_input()
        
        print("\n" + "=" * 60)
        print(f"{Colors.GREEN}Starting Instagram Account Creator (Gmail Edition){Colors.RESET}")
        print(f"{Colors.CYAN}• Creating {Colors.WHITE}{count}{Colors.CYAN} account(s){Colors.RESET}")
        print(f"{Colors.CYAN}• Delay between accounts: {Colors.WHITE}{delay}{Colors.CYAN} seconds{Colors.RESET}")
        print(f"{Colors.CYAN}• Save to file: {Colors.WHITE}{'Yes' if save_to_file else 'No'}{Colors.RESET}")
        print(f"{Colors.YELLOW}• Using: Gmail with App Passwords{Colors.RESET}")
        print("=" * 60)
        
        creator = InstagramAccountCreator(save_to_file=save_to_file)
        
        for i in range(count):
            print(f"\n{Colors.CYAN}{Colors.BOLD}[{i+1}/{count}] Creating Instagram account...{Colors.RESET}\n")
            result = creator.create_account()
            
            if i < count - 1:
                print(f"\n{Colors.YELLOW}Waiting {delay} seconds before next attempt...{Colors.RESET}")
                for remaining in range(delay, 0, -1):
                    print(f"\r{Colors.CYAN}Next account in: {Colors.WHITE}{remaining}{Colors.CYAN} seconds{Colors.RESET}", end="")
                    time.sleep(1)
                print("\n")
    
    except KeyboardInterrupt:
        print(f"\n\n{Colors.RED}Program stopped by user.{Colors.RESET}")
    
    finally:
        print("\n" + "=" * 60)
        print(f"{Colors.MAGENTA}{Colors.BOLD}SUMMARY:{Colors.RESET}")
        print(f"{Colors.GREEN}✓ Successful accounts: {Colors.WHITE}{creator.success_count}{Colors.RESET}")
        print(f"{Colors.RED}✗ Failed accounts: {Colors.WHITE}{creator.fail_count}{Colors.RESET}")
        print("=" * 60)
        
        if creator.success_count > 0 and save_to_file:
            print(f"{Colors.GREEN}Successful accounts saved to instagram_accounts.txt{Colors.RESET}")
            print(f"{Colors.GREEN}Session IDs saved to ACC_SESSIONS_IG.txt{Colors.RESET}")
        
        print(f"\n{Colors.CYAN}Thank you for using Enhanced Instagram Account Creator!{Colors.RESET}")

if __name__ == "__main__":
    main()