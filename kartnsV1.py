import requests
import time
import json
import os

all_reports = {
    "1": {"code": "[\"adult_content-nudity_or_sexual_activity\"]", "name": "عري أو نشاط جنسي"},
    "2": {"code": "[\"violence_hate_or_exploitation-sexual_exploitation-yes\"]", "name": "يبدو كاستغلال جنسي دون 18"},
    "3": {"code": "[\"adult_content-threat_to_share_nude_images-u18-yes\"]", "name": "تهديد بمشاركة صور عارية أو مشاركتها بالفعل دون 18"},
    "4": {"code": "[\"suicide_or_self_harm_concern-suicide_or_self_injury\"]", "name": "انتحار أو إيذاء الذات"},
    "5": {"code": "[\"ig_scam_financial_investment\"]", "name": "خداع بشأن الأموال أو الاستثمار"},
    "6": {"code": "[\"selling_or_promoting_restricted_items-drugs-high-risk\"]", "name": "أدوية شديدة الإدمان، مثل الكوكايين أو الهيروين أو الفينتانيل"},
    "7": {"code": "[\"violent_hateful_or_disturbing-credible_threat\"]", "name": "تهديد جدّي للسلامة"},
    "8": {"code": "[\"suicide_or_self_harm_concern-eating_disorder\"]", "name": "اضطرابات الأكل"},
    "9": {"code": "[\"harrassment_or_abuse-harassment-me-u18-yes\"]", "name": "مضايقة أو اساءة لي (me)"},
    "10": {"code": "[\"violence_hate_or_exploitation-sexual_exploitation-yes\"]", "name": "يبدو كاستغلال جنسي"},
    "11": {"code": "[\"ig_spam_v3\"]", "name": "سبام"},
    "12": {"code": "[\"selling_or_promoting_restricted_items-drugs\"]", "name": "مخدرات"},
    "13": {"code": "[\"violent_hateful_or_disturbing-violence\"]", "name": "عنف"},
    "14": {"code": "[\"violent_hateful_or_disturbing-promotes_hate-hate_speech_or_symbols\"]", "name": "خطاب كراهية أو رموز"},
    "15": {"code": "[\"ig_user_impersonation\"]", "name": "انتحال شخصية"},
    "16": {"code": "[\"ig_its_inappropriate\"]", "name": "غير مناسب/دون سن"},
    "17": {"code": "[\"selling_or_promoting_restricted_items\"]", "name": "بيع أسلحة"}
}

url = "https://www.instagram.com/api/v1/web/reports/get_frx_prompt/"

headers = {
    'User-Agent': "Mozilla/5.0 (Linux; Android 9; SH-M24 Build/PQ3A.190705.09121607; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/124.0.6367.82 Safari/537.36 InstagramLite 1.0.0.0.145 Android (28/9; 240dpi; 900x1600; AQUOS; SH-M24; gracelte; qcom; ar_EG; 115357035)",
    'sec-ch-ua': "\"Chromium\";v=\"124\", \"Android WebView\";v=\"124\", \"Not-A.Brand\";v=\"99\"",
    'x-ig-www-claim': "hmac.AR3_rYnLKeBezIQYHfIUtjIcljl6VzAqGT8JGhQ_M0eCdWOV",
    'x-web-session-id': "m3n2go:suujxi:8c53jj",
    'sec-ch-ua-platform-version': "\"9.0.0\"",
    'x-requested-with': "XMLHttpRequest",
    'sec-ch-ua-full-version-list': "\"Chromium\";v=\"124.0.6367.82\", \"Android WebView\";v=\"124.0.6367.82\", \"Not-A.Brand\";v=\"99.0.0.0\"",
    'sec-ch-prefers-color-scheme': "light",
    'x-csrftoken': "FxCF6jR5tSy3wdcZCfRIZN5viVxZmV1k",
    'sec-ch-ua-platform': "\"Android\"",
    'x-ig-app-id': "936619743392459",
    'sec-ch-ua-model': "\"SH-M24\"",
    'sec-ch-ua-mobile': "?0",
    'x-instagram-ajax': "1028279148",
    'x-asbd-id': "359341",
    'origin': "https://www.instagram.com",
    'sec-fetch-site': "same-origin",
    'sec-fetch-mode': "cors",
    'sec-fetch-dest': "empty",
    'referer': "https://www.instagram.com/dr.mahmoud.91/",
    'accept-language': "ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7",
    'priority': "u=1, i"
}

def show_menu():
    print("\nInstagram Reporting System")
    print("\nChoose option:")
    print("1. Vulnerability Management (create/use vulnerability)")
    
    while True:
        choice = input("\nEnter your choice (1): ").strip()
        if choice == "1":
            return 1
        print("Invalid choice. Please enter 1.")

def show_vuln_management():
    print("\nVulnerability Management")
    print("1. Create new vulnerability")
    print("2. Use saved vulnerability")
    print("3. Show saved vulnerabilities")
    print("4. Delete vulnerability")
    
    while True:
        choice = input("\nEnter your choice: ").strip()
        if choice in ['1', '2', '3', '4']:
            return choice
        print("Invalid choice.")

def get_sleep_time():
    print("\nTime Settings Between Reports")
    print("Enter time in seconds between each report.")
    print("Recommended: 2-5 seconds to avoid detection")
    
    while True:
        try:
            sleep_time = int(input("\nEnter sleep time (seconds): ").strip())
            if sleep_time >= 0:
                return sleep_time
            print("Please enter positive number or 0 for no delay.")
        except ValueError:
            print("Please enter valid number.")

def show_all_reports():
    print("\nAll Available Report Types:")
    for key, report in all_reports.items():
        print(f"{key}. {report['name']}")

def select_report():
    while True:
        choice = input("\nEnter report number (or 0 to finish): ").strip()
        if choice == "0":
            return None
        if choice in all_reports:
            return all_reports[choice]
        print("Invalid report number. Try again.")

def get_repetition_count(report_name):
    while True:
        try:
            count = int(input(f"How many times to repeat '{report_name}'? ").strip())
            if count > 0:
                return count
            print("Please enter number greater than 0.")
        except ValueError:
            print("Please enter valid number.")

def choose_reporting_mode():
    print("\nChoose reporting mode:")
    print("1. Report from single account")
    print("2. Report from multiple accounts")
    
    while True:
        choice = input("\nEnter your choice (1 or 2): ").strip()
        if choice in ['1', '2']:
            return choice
        print("Invalid choice. Please enter 1 or 2.")

def validate_session(session_id):
    test_cookies = {
        'sessionid': session_id,
        'csrftoken': 'FxCF6jR5tSy3wdcZCfRIZN5viVxZmV1k'
    }
    
    try:
        response = requests.get(
            'https://www.instagram.com/api/v1/users/web_profile_info/?username=instagram',
            cookies=test_cookies,
            headers=headers,
            timeout=10
        )
        return response.status_code == 200
    except:
        return False

def create_vulnerability():
    print("\nCreate New Vulnerability")
    
    while True:
        try:
            num_groups = int(input("How many report groups do you need? ").strip())
            if num_groups > 0:
                break
            print("Please enter number greater than 0.")
        except ValueError:
            print("Please enter valid number.")
    
    vulnerability = {"groups": []}
    
    for group_num in range(1, num_groups + 1):
        print(f"\nGroup {group_num}:")
        show_all_reports()
        
        group_reports = []
        print(f"\nSelect reports for Group {group_num}:")
        
        while True:
            report = select_report()
            if report is None:
                if len(group_reports) == 0:
                    print("Must select at least one report for group.")
                    continue
                break
            
            count = get_repetition_count(report['name'])
            
            for i in range(count):
                group_reports.append(report.copy())
            
            print(f"Added: {report['name']} × {count}")
            print(f"Reports in group so far: {len(group_reports)}")
        
        vulnerability["groups"].append(group_reports)
        print(f"Saved Group {group_num} ({len(group_reports)} reports)")
    
    vuln_name = input("\nEnter vulnerability name (no spaces): ").strip()
    
    filename = f"{vuln_name}_vuln.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(vulnerability, f, ensure_ascii=False, indent=2)
    
    print(f"\nVulnerability saved: {filename}")
    print(f"Groups: {len(vulnerability['groups'])}")
    for i, group in enumerate(vulnerability['groups'], 1):
        print(f"  Group {i}: {len(group)} reports")
    
    return filename

def list_vulnerabilities():
    files = [f for f in os.listdir() if f.endswith('_vuln.json')]
    
    if not files:
        print("\nNo saved vulnerabilities.")
        return None
    
    print("\nSaved Vulnerabilities:")
    for i, filename in enumerate(files, 1):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                vuln = json.load(f)
            groups_count = len(vuln['groups'])
            total_reports = sum(len(group) for group in vuln['groups'])
            print(f"{i}. {filename}")
            print(f"   - Groups: {groups_count}")
            print(f"   - Total reports: {total_reports}")
        except:
            print(f"{i}. {filename} (read error)")
    
    return files

def load_vulnerability(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        print(f"Error loading vulnerability: {filename}")
        return None

def delete_vulnerability():
    files = list_vulnerabilities()
    if not files:
        return
    
    while True:
        try:
            choice = int(input("\nEnter vulnerability number to delete (0 to cancel): ").strip())
            if choice == 0:
                return
            if 1 <= choice <= len(files):
                os.remove(files[choice-1])
                print(f"Deleted: {files[choice-1]}")
                return
            print("Invalid number.")
        except ValueError:
            print("Please enter valid number.")

def get_context(user_id, cookies):
    nok = {
        'container_module': 'profilePage',
        'entry_point': '1',
        'location': '2',
        'object_id': user_id,
        'object_type': '5',
        'frx_prompt_request_type': '1',
    }
    
    try:
        response = requests.post(
            'https://www.instagram.com/api/v1/web/reports/get_frx_prompt/',
            cookies=cookies,
            headers=headers,
            data=nok,
            timeout=10
        )
        
        if response.status_code == 200:
            return response.json()['response']['context']
        else:
            return None
    except:
        return None

def send_report(report_data, user_id, cookies, step_num, total_steps, sleep_time):
    report_code = report_data["code"]
    report_name = report_data["name"]
    
    print(f"\nReport {step_num}/{total_steps}: {report_name}")
    
    time.sleep(1)
    
    context = get_context(user_id, cookies)
    
    if not context:
        return "session_expired"
    
    payload = {
        'container_module': "profilePage",
        'entry_point': "1",
        'location': "2",
        'object_id': user_id,
        'object_type': "5",
        'context': context,
        'selected_tag_types': report_code,
        'frx_prompt_request_type': "2",
        'jazoest': "22816"
    }
    
    try:
        response = requests.post(url, data=payload, headers=headers, cookies=cookies, timeout=10)
        
        if response.status_code == 200:
            print("Status: Success")
            return "success"
        else:
            print(f"Status: Failed ({response.status_code})")
            return "failed"
    except Exception as e:
        print(f"Error: {e}")
        return "failed"

def ask_retry():
    print("\nDo you want to retry with the same data?")
    print("1. Yes (return to first group)")
    print("2. No (return to main menu)")
    
    while True:
        choice = input("\nEnter your choice (1 or 2): ").strip()
        if choice in ['1', '2']:
            return choice == '1'
        print("Invalid choice. Please enter 1 or 2.")

def execute_vulnerability_single(vulnerability, user_id, session_id):
    while True:
        sleep_time = get_sleep_time()
        
        print("\nPlease enable VPN now")
        print("Press ENTER when VPN is active")
        input()
        
        cookies = {
            'datr': 't2_paGIejmErDTIjIjwWF7gG',
            'ig_did': 'DD344728-1E3E-4946-AD3E-CAF859846F92',
            'dpr': '1.5',
            'mid': 'aOlvtwABAAEzroEkqUYna_SvGNJS',
            'csrftoken': 'FxCF6jR5tSy3wdcZCfRIZN5viVxZmV1k',
            'ig_nrcb': '1',
            'wd': '600x1043',
            'ds_user_id': '76486059622',
            'ps_l': '1',
            'ps_n': '1',
            'sessionid': session_id,
            'rur': '"RVA\\05476486059622\\0541791670864:01fe3167f0753030cebb866598515e7ba79f9e395da4160195b582c2ab2f4272410b88ee"'
        }
        
        total_success = 0
        total_reports = sum(len(group) for group in vulnerability['groups'])
        session_expired = False
        
        for group_num, group_reports in enumerate(vulnerability['groups'], 1):
            if session_expired:
                break
                
            print(f"\nStarting Group {group_num} of {len(vulnerability['groups'])}")
            print(f"Reports in this group: {len(group_reports)}")
            
            group_success = 0
            for i, report_data in enumerate(group_reports, 1):
                result = send_report(report_data, user_id, cookies, i, len(group_reports), sleep_time)
                
                if result == "session_expired":
                    print("\nSession has expired")
                    print("Press ENTER to restart the tool")
                    input()
                    session_expired = True
                    break
                elif result == "success":
                    group_success += 1
                
                if i < len(group_reports) and sleep_time > 0 and not session_expired:
                    print(f"\nWaiting {sleep_time} seconds before next report...")
                    time.sleep(sleep_time)
            
            if session_expired:
                break
                
            total_success += group_success
            print(f"\nCompleted Group {group_num}: {group_success}/{len(group_reports)} reports")
            
            if group_num < len(vulnerability['groups']):
                print(f"\nVPN change required for next group")
                print("Please change VPN server now")
                print("Press ENTER when VPN is changed")
                input()
        
        if session_expired:
            return False
        
        print(f"\nAll groups completed")
        print(f"Total: {total_success}/{total_reports} successful reports")
        print(f"Sleep time used: {sleep_time} seconds")
        
        if ask_retry():
            print("\nReturning to first group...")
            continue
        else:
            break

def execute_vulnerability_multi(vulnerability, user_id):
    sessions = []
    
    print("\nEnter session IDs (one per line)")
    print("Example:")
    print("23375113665%3AQ5.............")
    print("Press Enter twice when finished")
    
    while True:
        session = input().strip()
        if session == "":
            if sessions:
                break
            else:
                print("Please enter at least one session ID")
                continue
        sessions.append(session)
    
    sleep_time = get_sleep_time()
    
    print("\nValidating sessions...")
    valid_sessions = []
    for i, session in enumerate(sessions, 1):
        print(f"Checking session {i}/{len(sessions)}... ", end="")
        if validate_session(session):
            print("VALID")
            valid_sessions.append(session)
        else:
            print("INVALID")
    
    print(f"\nValid sessions: {len(valid_sessions)}/{len(sessions)}")
    
    if not valid_sessions:
        print("No valid sessions found.")
        print("Press ENTER to restart the tool")
        input()
        return
    
    while True:
        print(f"\nStarting reporting from {len(valid_sessions)} accounts")
        
        total_all_reports = 0
        total_all_success = 0
        all_sessions_expired = True
        
        for account_num, session_id in enumerate(valid_sessions, 1):
            print(f"\nAccount {account_num}/{len(valid_sessions)}")
            
            cookies = {
                'datr': 't2_paGIejmErDTIjIjwWF7gG',
                'ig_did': 'DD344728-1E3E-4946-AD3E-CAF859846F92',
                'dpr': '1.5',
                'mid': 'aOlvtwABAAEzroEkqUYna_SvGNJS',
                'csrftoken': 'FxCF6jR5tSy3wdcZCfRIZN5viVxZmV1k',
                'ig_nrcb': '1',
                'wd': '600x1043',
                'ds_user_id': '76486059622',
                'ps_l': '1',
                'ps_n': '1',
                'sessionid': session_id,
                'rur': '"RVA\\05476486059622\\0541791670864:01fe3167f0753030cebb866598515e7ba79f9e395da4160195b582c2ab2f4272410b88ee"'
            }
            
            print("\nPlease enable VPN now")
            print("Press ENTER when VPN is active")
            input()
            
            account_success = 0
            total_reports = sum(len(group) for group in vulnerability['groups'])
            session_expired = False
            
            for group_num, group_reports in enumerate(vulnerability['groups'], 1):
                if session_expired:
                    break
                    
                print(f"\nAccount {account_num} - Group {group_num} of {len(vulnerability['groups'])}")
                print(f"Reports in this group: {len(group_reports)}")
                
                group_success = 0
                for i, report_data in enumerate(group_reports, 1):
                    result = send_report(report_data, user_id, cookies, i, len(group_reports), sleep_time)
                    
                    if result == "session_expired":
                        print(f"\nSession {account_num} has expired")
                        print(f"Removing session {account_num} from list")
                        valid_sessions.remove(session_id)
                        session_expired = True
                        break
                    elif result == "success":
                        group_success += 1
                    
                    if i < len(group_reports) and sleep_time > 0 and not session_expired:
                        print(f"\nWaiting {sleep_time} seconds before next report...")
                        time.sleep(sleep_time)
                
                if session_expired:
                    break
                    
                account_success += group_success
                print(f"\nCompleted Group {group_num}: {group_success}/{len(group_reports)} reports")
                
                if group_num < len(vulnerability['groups']):
                    print(f"\nVPN change required for next group")
                    print("Please change VPN server now")
                    print("Press ENTER when VPN is changed")
                    input()
            
            if not session_expired:
                all_sessions_expired = False
                total_all_reports += total_reports
                total_all_success += account_success
                
                print(f"\nAccount {account_num} completed: {account_success}/{total_reports} reports")
                
                if account_num < len(valid_sessions):
                    print(f"\nPreparing next account in 5 seconds...")
                    time.sleep(5)
        
        if all_sessions_expired:
            print("\nAll sessions have expired")
            print("Press ENTER to restart the tool")
            input()
            break
        
        print(f"\nMulti-account operation completed")
        print(f"Accounts used: {len(sessions)}")
        print(f"Total reports sent: {total_all_success}")
        max_reports = len(sessions) * sum(len(group) for group in vulnerability['groups'])
        print(f"Maximum possible reports: {max_reports}")
        print(f"Sleep time used: {sleep_time} seconds")
        
        if ask_retry():
            if not valid_sessions:
                print("\nNo valid sessions remaining")
                print("Press ENTER to restart the tool")
                input()
                break
            print("\nReturning to first group...")
            continue
        else:
            break

def use_vulnerability():
    files = list_vulnerabilities()
    if not files:
        return
    
    while True:
        try:
            choice = int(input("\nEnter vulnerability number to use (0 to cancel): ").strip())
            if choice == 0:
                return
            if 1 <= choice <= len(files):
                vuln = load_vulnerability(files[choice-1])
                if vuln:
                    print(f"\nUsing vulnerability: {files[choice-1]}")
                    
                    user_id = input("Enter target user ID: ").strip()
                    
                    mode = choose_reporting_mode()
                    
                    if mode == "1":
                        session_id = input("Enter session ID: ").strip()
                        execute_vulnerability_single(vuln, user_id, session_id)
                    else:
                        execute_vulnerability_multi(vuln, user_id)
                return
            print("Invalid number.")
        except ValueError:
            print("Please enter valid number.")

def main():
    choice = show_menu()
    
    if choice == 1:
        vuln_choice = show_vuln_management()
        
        if vuln_choice == "1":
            create_vulnerability()
        elif vuln_choice == "2":
            use_vulnerability()
        elif vuln_choice == "3":
            list_vulnerabilities()
        elif vuln_choice == "4":
            delete_vulnerability()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
    except Exception as e:
        print(f"\n\nError: {e}")