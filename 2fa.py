import re as ree
import os
import requests
import json
import uuid
import random
import time
import base64

session_vars = {}

def reset_password(username):
    url = "https://i.instagram.com/api/v1/accounts/send_recovery_flow_email/"
    headers={
        "host": "i.instagram.com",
        "x-ig-app-locale": "en_OM",
        "x-ig-device-locale": "en_OM",
        "x-ig-mapped-locale": "en_AR",
        "x-pigeon-session-id": f"UFS-{uuid.uuid4()}-1",
        "x-pigeon-rawclienttime": str(time.time()),
        "x-ig-bandwidth-speed-kbps": str(random.randint(300, 1000)) + ".000",
        "x-ig-bandwidth-totalbytes-b": str(random.randint(1_000_000, 5_000_000)),
        "x-ig-bandwidth-totaltime-ms": str(random.randint(3000, 10000)),
        "x-bloks-version-id": "8ca96ca267e30c02cf90888d91eeff09627f0e3fd2bd9df472278c9a6c022cbb",
        "x-ig-www-claim": "0",
        "x-bloks-is-layout-rtl": "true",
        "x-ig-device-id": str(uuid.uuid4()),
        "x-ig-family-device-id": str(uuid.uuid4()),
        "x-ig-android-id": "android-" + uuid.uuid4().hex[:16],
        "x-ig-timezone-offset": "14400",
        "x-fb-connection-type": "WIFI",
        "x-ig-connection-type": "WIFI",
        "x-ig-capabilities": "3brTv10=",
        "x-ig-app-id": "567067343352427",
        "priority": "u=3",
        "user-agent": "Instagram 275.0.0.27.98 Android (29/10; 443dpi; 1080x2224; HUAWEI; STK-L21; HWSTK-HF; kirin710; ar_OM; 458229237)",
        "accept-language": "en-OM, en-US",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "accept-encoding": "zstd, gzip, deflate",
        "x-fb-http-engine": "Liger",
        "ig-intended-user-id": "0",
    }
    body_json = {
        "adid": str(uuid.uuid4()),
        "guid": str(uuid.uuid4()),
        "device_id": "android-" + uuid.uuid4().hex[:16],
        "query": username,
        "waterfall_id": str(uuid.uuid4())
    }
    signed_body = "SIGNATURE." + json.dumps(body_json, separators=(",", ":"))
    data = {"signed_body": signed_body}
    r = requests.post(url, headers=headers, data=data)
    print(r.text)
    
def check_ban(ssid):#there are some problems in login with ban accounts to check type of ban, we are waiting for next api updates(get message "wrong password" when login with ban accounts)
    url = "https://www.instagram.com/async/wbloks/fetch/?appid=com.bloks.www.checkpoint.disabled.controller&type=app&__bkv=f4e32caf235c4c3198ceb3d7599c397741599ea3447ec2f785d4575aeb99766b"

    headers = {
        "authority": "www.instagram.com",
        "accept": "*/*",
        "cache-control": "no-cache",
        "content-type": "application/x-www-form-urlencoded;charset=UTF-8",
        "origin": "https://www.instagram.com",
        "pragma": "no-cache",
        "referer": "https://www.instagram.com/accounts/disabled/",
        "sec-ch-prefers-color-scheme": "light",
        "sec-ch-ua": '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
        "sec-ch-ua-full-version-list": '"Google Chrome";v="137.0.7151.69", "Chromium";v="137.0.7151.69", "Not/A)Brand";v="24.0.0.0"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-ch-ua-platform-version": '"14.0.0"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
        "cookie": f"sessionid={ssid}",
    }

    data = {
        "__a": "1",
        "fb_dtsg": "NAfupDWSIKv-H-tJ1PQgp1oDTLxdmXuyJehposoQNb-xmeX0EC5LDFw:17843709688147332:1749572507",
    }

    response = requests.post(url, headers=headers, data=data)
    if 'for (;;);{"__ar":1,"rid' in response.text:
        res = response.text.split('for (;;);')[1]
        res = json.loads(res)
        print(res)
    print(response.status_code)

    if "Please try closing and re-opening your browser window." in response.text:
        return True
    elif '(ig.action.challenges.Logout)' in response.text:
        type_ = "logout"
        print(type_)
        #t = ["payload"]["layout"]["bloks_payload"][""]
    else:
        print("err")
        #print(response.text)
    #print(response.text)

def extract_session_from_token(token):
    try:
        if token.startswith('Bearer '):
            token = token.replace('Bearer ', '')
        if token.startswith('IGT:2:'):
            token = token.split(':', 2)[2]
        decoded_bytes = base64.b64decode(token)
        decoded_data = decoded_bytes.decode('utf-8')
        auth_data = json.loads(decoded_data)
        sessionid = auth_data.get('sessionid', '')
        #check_ban(sessionid)
        return sessionid
        
    except Exception as e:
        print(f"Error extracting session: {e}")
        return None
    
def generate_ids():
    return {
        "qe_device_id": str(uuid.uuid4()),
        "family_device_id": str(uuid.uuid4()),
        "device_id": f"android-{uuid.uuid4().hex[:16]}",
        "machine_id": f"a{uuid.uuid4().hex[:12]}",
        "waterfall_id": str(uuid.uuid4()),
        "pigeon_session_id": f"UFS-{uuid.uuid4()}-0",
        "bandwidth_speed": f"{random.uniform(500, 5000):.3f}",
        "bandwidth_totalbytes": str(random.randint(200000, 900000)),
        "bandwidth_totaltime": str(random.randint(100, 800)),
        "rawclienttime": str(time.time()),
        "bloks_version": "e061cacfa956f06869fc2b678270bef1583d2480bf51f508321e64cfb5cc12bd",
        "app_id": "567067343352427",
    }
session_vars = generate_ids()
def login(username, password):
    global session_vars
    session_vars = generate_ids()

    pwd = f"#PWD_INSTAGRAM:0:{int(time.time())}:{password}"

    url = "https://i.instagram.com/api/v1/bloks/apps/com.bloks.www.bloks.caa.login.async.send_login_request/"

    payload = {
        "params": json.dumps({
            "client_input_params": {
                "sim_phones": [],
                "aymh_accounts": [],
                "secure_family_device_id": "",
                "has_granted_read_contacts_permissions": 0,
                "auth_secure_device_id": "",
                "has_whatsapp_installed": 1,
                "password": pwd, 
                "event_flow": "login_manual",
                "password_contains_non_ascii": "false",
                "device_id": session_vars["device_id"],
                "login_attempt_count": 1,
                "machine_id": "",
                "accounts_list": [],
                "family_device_id": session_vars["family_device_id"],
                "fb_ig_device_id": [],
                "device_emails": [],
                "try_num": 1,
                "lois_settings": {"lois_token": ""},
                "event_step": "home_page",
                "contact_point": username
            },
            "server_params": {
                "login_credential_type": "none",
                "server_login_source": "login",
                "waterfall_id": session_vars["waterfall_id"],
                "two_step_login_type": "one_step_login",
                "login_source": "Login",
                "is_platform_login": 0,
                "INTERNALlatency_qpl_marker_id": 36707139,
                "qe_device_id": session_vars["qe_device_id"],
                "username_text_input_id": "lz1ed6:129",
                "password_text_input_id": "lz1ed6:130",
                "device_id": session_vars["device_id"],
                "INTERNALlatency_qpl_instance_id": random.random()*1e14,
                "reg_flow_source": "lid_landing_screen",
                "credential_type": "password",
                "caller": "gslr",
                "family_device_id": session_vars["family_device_id"],
                "access_flow_version": "pre_mt_behavior"
            }
        }),
        "bk_client_context": json.dumps({
            "bloks_version": "e061cacfa956f06869fc2b678270bef1583d2480bf51f508321e64cfb5cc12bd",
            "styles_id": "instagram"
        }),
        "bloks_versioning_id": "e061cacfa956f06869fc2b678270bef1583d2480bf51f508321e64cfb5cc12bd"
    }

    headers = {
        "User-Agent": "Instagram 275.0.0.27.98 Android (29/10; 443dpi; 1080x2224; HUAWEI; STK-L21; HWSTK-HF; kirin710; en_OM; 458229237)",
        #"Accept-Encoding": "zstd, gzip, deflate",
        "x-ig-app-locale": "en_OM",
        "x-ig-device-locale": "en_OM",
        "x-ig-mapped-locale": "en_AR",
        "x-pigeon-session-id": session_vars["pigeon_session_id"],
        "x-pigeon-rawclienttime": session_vars["rawclienttime"],
        "x-ig-bandwidth-speed-kbps": session_vars["bandwidth_speed"],
        "x-ig-bandwidth-totalbytes-b": session_vars["bandwidth_totalbytes"],
        "x-ig-bandwidth-totaltime-ms": session_vars["bandwidth_totaltime"],
        "x-bloks-version-id": "e061cacfa956f06869fc2b678270bef1583d2480bf51f508321e64cfb5cc12bd",
        "x-ig-device-id": session_vars["qe_device_id"],
        "x-ig-family-device-id": session_vars["family_device_id"],
        "x-ig-android-id": session_vars["device_id"],
        "x-ig-timezone-offset": "14400",
        "x-fb-connection-type": "WIFI",
        "x-ig-connection-type": "WIFI",
        "x-ig-capabilities": "3brTv10=",
        "x-ig-app-id": "567067343352427",
        "priority": "u=3",
        "accept-language": "en-OM, en-US",
        "x-mid": session_vars["machine_id"],
        "ig-intended-user-id": "0",
        "x-fb-http-engine": "Liger",
        "x-fb-client-ip": "True",
        "x-fb-server-cluster": "True"
    }
    response = requests.post(url, data=payload, headers=headers)
    return response.text, response.headers.get('ig-set-x-mid')

def choose_verify_method(path, challenge_context, mid):
    guid = session_vars["qe_device_id"]
    device_id = session_vars["device_id"]
    url = f"https://i.instagram.com/api/v1{path}?guid={guid}&device_id={device_id}&challenge_context={challenge_context}"
    headers = {
        'User-Agent': 'Instagram 275.0.0.27.98 Android (29/10; 443dpi; 1080x2224; HUAWEI; STK-L21; HWSTK-HF; kirin710; en_OM; 458229237)',
        'X-Bloks-Version-Id': session_vars["bloks_version"],
        'X-Mid': mid,
    }
    
    re = requests.get(url, headers=headers)
    if 'select_verify_method' in re.text:
        response_json = re.json()
        challenge_context = response_json["challenge_context"]
        nonce_code = response_json["nonce_code"]
        cni = response_json["cni"]
        method = response_json["step_data"]

        if "email" in method and "phone_number" not in method:
            print(f' [{method["choice"]}] {method["email"]}')
        elif "phone_number" in method and "email" not in method:
            print(f' [{method["choice"]}] {method["phone_number"]}')
        elif "email" in method and "phone_number" in method:
            keys = list(method.keys())
            email_index = keys.index("email")
            phone_number_index = keys.index("phone_number")

            if email_index < phone_number_index:
                print(f" [0] {method['email']}")
                print(f" [1] {method['phone_number']}")
            else:
                print(f" [0] {method['phone_number']}")
                print(f" [1] {method['email']}")

        choice = input(f'\n- Choose ---> ')
        print('\n')
        return challenge_context, nonce_code, cni, choice
    else:
        print("Can't open page")
        return 

def take_challenge(challenge_context, nonce_code, cni, choice, mid):
    url = "https://i.instagram.com/api/v1/bloks/apps/com.instagram.challenge.navigation.take_challenge/"
    headers = {
        'User-Agent': 'Instagram 275.0.0.27.98 Android (29/10; 443dpi; 1080x2224; HUAWEI; STK-L21; HWSTK-HF; kirin710; en_OM; 458229237)',
        'X-Bloks-Version-Id': session_vars["bloks_version"],
        'X-Mid': mid,
    }
    fdid = session_vars["family_device_id"]
    data = {
        "cni": str(cni),
        "nonce_code": nonce_code,
        "bk_client_context": '{"bloks_version":"'+session_vars["bloks_version"]+'","styles_id":"instagram"}',
        "fb_family_device_id": fdid,
        "challenge_context": challenge_context,
        "bloks_versioning_id": session_vars["bloks_version"],
        "get_challenge": "true",
    }
    re = requests.post(url, headers=headers, data=data)
    if "select_verification_method" in re.text:
        re = re.text.replace('\\', '').replace('\\\\', '').replace('\\\\\\', '')
        with open('ress.txt', 'w', encoding="utf-8") as f:
            f.write(re)
        perf_logging_id = re.split('(bk.action.array.Make, (bk.action.bloks.GetVariable2, "')[1].split('"),')[0]  
        challenge_context = re.split('n.array.Make, (bk.action.i32.Const, 6), "')[1].split('", (bk.action.bool.Const, fa')[0]
        return perf_logging_id, challenge_context
    else:
        print("bad")
        return 
        
def choice_(challenge_context, choice, mid):
    url = "https://i.instagram.com/api/v1/bloks/apps/com.instagram.challenge.navigation.take_challenge/"
    headers = {
        'User-Agent': 'Instagram 275.0.0.27.98 Android (29/10; 443dpi; 1080x2224; HUAWEI; STK-L21; HWSTK-HF; kirin710; en_OM; 458229237)',
        'X-Bloks-Version-Id': session_vars["bloks_version"],
        'X-Mid': mid,
    }
    data = {
        "choice": choice,
        "has_follow_up_screens": "0",
        "bk_client_context": '{"bloks_version":"'+session_vars["bloks_version"]+'","styles_id":"instagram"}',
        "challenge_context": challenge_context,
        "bloks_versioning_id": session_vars["bloks_version"]}
    re = requests.post(url, headers=headers, data=data)
    if 'Enter the 6-digit code we sent to' in re.text:
        re = re.text.replace('\\', '').replace('\\\\', '').replace('\\\\\\', '')
        with open('resss.txt', 'w', encoding="utf-8") as f:
            f.write(re)
        target = re.split('(bk.action.i32.Const, 0)), (bk.action.i32.Const,')[2].split('", (bk.action.bool.Const, false)))')[0]
        perf_logging_id, challenge_context = target.split('), "')
        return perf_logging_id.strip(), challenge_context
    else:
        print("errror")
        return      
def put_code(challenge_context, perf_logging_id, mid):
    code = input('[Code]: ')
    url = "https://i.instagram.com/api/v1/bloks/apps/com.instagram.challenge.navigation.take_challenge/"
    headers = {
        'User-Agent': 'Instagram 275.0.0.27.98 Android (29/10; 443dpi; 1080x2224; HUAWEI; STK-L21; HWSTK-HF; kirin710; en_OM; 458229237)',
        'X-Bloks-Version-Id': session_vars["bloks_version"],
        'X-Mid': mid,
    }
    data={
        "security_code": code,
        "perf_logging_id": perf_logging_id,
        "has_follow_up_screens": "0",
        "bk_client_context": '{"bloks_version":"'+session_vars["bloks_version"]+'","styles_id":"instagram"}',
        "challenge_context": challenge_context,
        "bloks_versioning_id": session_vars["bloks_version"]
    }
    re = requests.post(url, headers=headers, data=data)
    if 'full_name' in re.text:
        print('[+] Done Login .. ')
        token = re.headers.get('ig-set-authorization', '').split('Bearer IGT:2:')[1]
        print('[+] API SSID:', extract_session_from_token(token))
        print('[+] X-MID:', mid)
    else:
        print("[-] can't login")


#------2f

def entrypoint(two_step_verification_context, mid):
    url = "https://i.instagram.com/api/v1/bloks/apps/com.bloks.www.two_step_verification.entrypoint/"
    headers={
        "User-Agent": 'Instagram 275.0.0.27.98 Android (29/10; 443dpi; 1080x2224; HUAWEI; STK-L21; HWSTK-HF; kirin710; en_OM; 458229237)',
        "X-Mid": mid
    }
    device_id = session_vars["device_id"]
    fdi=session_vars["family_device_id"]
    data = {
        "params": json.dumps({
            "client_input_params": {
            "device_id": device_id,
            "is_whatsapp_installed": 0,
            "machine_id": mid
            },
            "server_params": {
            "family_device_id": fdi,
            "device_id": device_id,
            "two_step_verification_context": two_step_verification_context,
            "flow_source": "two_factor_login",
            "INTERNAL_INFRA_screen_id": "nayrt0:3"
            }
        }),
        "bk_client_context": json.dumps({
            "bloks_version": session_vars["bloks_version"],
            "styles_id": "instagram"
        }),
        "bloks_versioning_id": session_vars["bloks_version"]
        }
    re = requests.post(url, headers=headers, data=data).text
    ch = str(input('\n[1] accept login in another device\n[2] use backup codes\n[3] get sms code\n[4] get whatsapp code\n[5] use authenticat app codes\n\n --> '))#@48i9
    print('\n')
    if ch == "1":
        if 'Check your notifications on another device' in re:
            while True:
                has_been_allowed(two_step_verification_context, mid)
        else:
            print("[Error] can't use this method")
            entrypoint(two_step_verification_context, mid)
    elif ch == "2":
        back_up_codes(two_step_verification_context, mid)
    elif ch == "3":
        sms_code(two_step_verification_context, mid)
    elif ch == "4":
        whatsapp_code(two_step_verification_context, mid)
    elif ch == "5":
        authenticat_app(two_step_verification_context, mid)
def has_been_allowed(two_step_verification_context, mid):
    url = "https://i.instagram.com/api/v1/bloks/apps/com.bloks.www.two_step_verification.has_been_allowed.async/"
    headers={
        "User-Agent": 'Instagram 275.0.0.27.98 Android (29/10; 443dpi; 1080x2224; HUAWEI; STK-L21; HWSTK-HF; kirin710; en_OM; 458229237)',
        "X-Mid": mid
    }
    device_id = session_vars["device_id"]
    fdi=session_vars["family_device_id"]
    data = {
        "params": json.dumps({
            "client_input_params": {
            "auth_secure_device_id": "",
            "machine_id": mid,
            "block_store_machine_id": "",
            "family_device_id": fdi,
            "device_id": device_id,
            "cloud_trust_token": None
            },
            "server_params": {
            "INTERNAL__latency_qpl_marker_id": 36707139,
            "block_store_machine_id": None,
            "device_id": device_id,
            "cloud_trust_token": None,
            "machine_id": None,
            "INTERNAL__latency_qpl_instance_id": 1.59135590600113e14,
            "two_step_verification_context": two_step_verification_context,
            "flow_source": "two_factor_login"
            }
        }),
        "bk_client_context": json.dumps({
            "bloks_version": session_vars["bloks_version"],
            "styles_id": "instagram"
        }),
        "bloks_versioning_id": session_vars["bloks_version"]
        }
    re = requests.post(url, headers=headers, data=data).text
    if len(re)<3000:
        print("[-] still not accept")
        
    elif 'IG-Set-Authorization' in re:
        print('[+] Done Login ..')
        match = ree.search(r'IG-Set-Authorization.*?Bearer ([A-Za-z0-9:_=\-]+)', re.replace('\\', '').replace('\\\\', '').replace('\\\\\\', '')).group(1)#@48i9
        print('[+] API SSID:', extract_session_from_token(match))
        print('[+] X-MID:', mid)
        return 
    else:
        p=''
        return 
    time.sleep(5)

def back_up_codes(two_step_verification_context, mid):
    code=input("[-] Backup_code: ")
    url = "https://i.instagram.com/api/v1/bloks/apps/com.bloks.www.two_step_verification.verify_code.async/"
    headers={
        "User-Agent": 'Instagram 275.0.0.27.98 Android (29/10; 443dpi; 1080x2224; HUAWEI; STK-L21; HWSTK-HF; kirin710; en_OM; 458229237)',
        "X-Mid": mid
    }
    device_id = session_vars["device_id"]
    fdi=session_vars["family_device_id"]
    data={
        "params":json.dumps({
        "client_input_params": {
            "auth_secure_device_id": "",
            "block_store_machine_id": "",
            "code": code,
            "should_trust_device": 1,
            "family_device_id": fdi,
            "device_id": device_id,
            "cloud_trust_token": None,
            "machine_id": mid
        },
        "server_params": {
            "INTERNAL__latency_qpl_marker_id": 36707139,
            "block_store_machine_id": None,
            "device_id": device_id,
            "cloud_trust_token": None,
            "challenge": "backup_codes",
            "machine_id": None,
            "INTERNAL__latency_qpl_instance_id": 166960272200250.0,
            "two_step_verification_context": two_step_verification_context,
            "flow_source": "two_factor_login"
        }
        }),
        "bk_client_context": json.dumps({
            "bloks_version": session_vars["bloks_version"],
            "styles_id": "instagram"
        }),
        "bloks_versioning_id": session_vars["bloks_version"]
        }
    re = requests.post(url, headers=headers, data=data).text.replace('\\', '').replace('\\\\', '').replace('\\\\\\', '')
    if 'IG-Set-Authorization' in re:
        print('[+] Done Login ..')
        match = ree.search(r'IG-Set-Authorization.*?Bearer ([A-Za-z0-9:_=\-]+)', re.replace('\\', '').replace('\\\\', '').replace('\\\\\\', '')).group(1)#@48i9
        print('[+] API SSID:', extract_session_from_token(match))
        print('[+] X-MID:', mid)
        return 
    elif 'Please check the security code and try again.' in re:
        print('[-] Bad code try again ..')
        back_up_codes(two_step_verification_context, mid)
    else:
        print('[-] Error try again')
        with open('else2.txt', 'w', encoding="utf-8") as f:
            f.write(re)
        return 

def whatsapp_code(two_step_verification_context, mid):
    url = "https://i.instagram.com/api/v1/bloks/apps/com.bloks.www.two_step_verification.send_code.async/"
    headers={
        "User-Agent": 'Instagram 275.0.0.27.98 Android (29/10; 443dpi; 1080x2224; HUAWEI; STK-L21; HWSTK-HF; kirin710; en_OM; 458229237)',
        "X-Mid": mid
    }
    device_id = session_vars["device_id"]
    fdi=session_vars["family_device_id"]
    data={"params": json.dumps({
    "client_input_params": {},
    "server_params": {
        "INTERNAL__latency_qpl_marker_id": 36707139,
        "block_store_machine_id": None,
        "device_id": device_id,
        "cloud_trust_token": None,
        "masked_cp": "+",
        "challenge": "whatsapp",
        "machine_id": None,
        "INTERNAL__latency_qpl_instance_id": 1.819340495E14,
        "two_step_verification_context": two_step_verification_context,
        "flow_source": "two_factor_login"
    }
}),
        "bk_client_context": json.dumps({
            "bloks_version": session_vars["bloks_version"],
            "styles_id": "instagram"
        }),
        "bloks_versioning_id": session_vars["bloks_version"]
        }
    re = requests.post(url, headers=headers, data=data).text.replace('\\', '').replace('\\\\', '').replace('\\\\\\', '')
    with open('sent_code.txt', 'w', encoding="utf-8") as f:
            f.write(re)
    code = input('[+] Whatsapp Code: ')
    
    url = "https://i.instagram.com/api/v1/bloks/apps/com.bloks.www.two_step_verification.verify_code.async/"
    data = {
    "params": json.dumps({
        "client_input_params": {
            "auth_secure_device_id": "",
            "block_store_machine_id": "",
            "code": str(code),
            "should_trust_device": 1,
            "family_device_id": fdi,
            "device_id": device_id,
            "cloud_trust_token": None,
            "machine_id": mid
        },
        "server_params": {
            "INTERNAL__latency_qpl_marker_id": 36707139,
            "block_store_machine_id": None,
            "device_id": device_id,
            "cloud_trust_token": None,
            "masked_cp": "+",
            "challenge": "whatsapp",
            "machine_id": None,
            "INTERNAL__latency_qpl_instance_id": 1.81934049500103e14,
            "two_step_verification_context": two_step_verification_context,
            "flow_source": "two_factor_login"
        }
    }),
    "bk_client_context": json.dumps({
        "bloks_version": session_vars["bloks_version"],
        "styles_id": "instagram"
    }),
    "bloks_versioning_id": session_vars["bloks_version"]
}
    re = requests.post(url, headers=headers, data=data).text.replace('\\', '').replace('\\\\', '').replace('\\\\\\', '')
    if 'IG-Set-Authorization' in re:
        print('[+] Done Login ..')
        match = ree.search(r'IG-Set-Authorization.*?Bearer ([A-Za-z0-9:_=\-]+)', re.replace('\\', '').replace('\\\\', '').replace('\\\\\\', '')).group(1)#@48i9
        print('[+] API SSID:', extract_session_from_token(match))
        print('[+] X-MID:', mid)
        return 
    elif 'Please check the security code and try again.' in re:
        print('[-] Bad code try again ..')
        whatsapp_code(two_step_verification_context, mid)
    else:
        print('[-] Error try again')
        with open('else2.txt', 'w', encoding="utf-8") as f:
            f.write(re)
        return 

def sms_code(two_step_verification_context, mid):
    url = "https://i.instagram.com/api/v1/bloks/apps/com.bloks.www.two_step_verification.send_code.async/"
    headers={
        "User-Agent": 'Instagram 275.0.0.27.98 Android (29/10; 443dpi; 1080x2224; HUAWEI; STK-L21; HWSTK-HF; kirin710; en_OM; 458229237)',
        "X-Mid": mid
    }
    device_id = session_vars["device_id"]
    fdi=session_vars["family_device_id"]
    data={"params": json.dumps({
    "client_input_params": {},
    "server_params": {
        "INTERNAL__latency_qpl_marker_id": 36707139,
        "block_store_machine_id": None,
        "device_id": device_id,
        "cloud_trust_token": None,
        "masked_cp": "+",
        "challenge": "sms",
        "machine_id": None,
        "INTERNAL__latency_qpl_instance_id": 1.819340495E14,
        "two_step_verification_context": two_step_verification_context,
        "flow_source": "two_factor_login"
    }
}),
        "bk_client_context": json.dumps({
            "bloks_version": session_vars["bloks_version"],
            "styles_id": "instagram"
        }),
        "bloks_versioning_id": session_vars["bloks_version"]
        }
    re = requests.post(url, headers=headers, data=data).text.replace('\\', '').replace('\\\\', '').replace('\\\\\\', '')
    with open('sent_code.txt', 'w', encoding="utf-8") as f:
            f.write(re)
    code = input('[+] SMS Code: ')
    
    url = "https://i.instagram.com/api/v1/bloks/apps/com.bloks.www.two_step_verification.verify_code.async/"
    data = {
    "params": json.dumps({
        "client_input_params": {
            "auth_secure_device_id": "",
            "block_store_machine_id": "",
            "code": str(code),
            "should_trust_device": 1,
            "family_device_id": fdi,
            "device_id": device_id,
            "cloud_trust_token": None,
            "machine_id": mid
        },
        "server_params": {
            "INTERNAL__latency_qpl_marker_id": 36707139,
            "block_store_machine_id": None,
            "device_id": device_id,
            "cloud_trust_token": None,
            "masked_cp": "+",
            "challenge": "sms",
            "machine_id": None,
            "INTERNAL__latency_qpl_instance_id": 1.81934049500103e14,
            "two_step_verification_context": two_step_verification_context,
            "flow_source": "two_factor_login"
        }
    }),
    "bk_client_context": json.dumps({
        "bloks_version": session_vars["bloks_version"],
        "styles_id": "instagram"
    }),
    "bloks_versioning_id": session_vars["bloks_version"]
}
    re = requests.post(url, headers=headers, data=data).text.replace('\\', '').replace('\\\\', '').replace('\\\\\\', '')
    if 'IG-Set-Authorization' in re:
        print('[+] Done Login ..')
        match = ree.search(r'IG-Set-Authorization.*?Bearer ([A-Za-z0-9:_=\-]+)', re.replace('\\', '').replace('\\\\', '').replace('\\\\\\', '')).group(1)#@48i9
        print('[+] API SSID:', extract_session_from_token(match))
        print('[+] X-MID:', mid)
        return 
    elif 'Please check the security code and try again.' in re:
        print('[-] Bad code try again ..')
        sms_code(two_step_verification_context, mid)
    else:
        print('[-] Error try again')
        with open('else2.txt', 'w', encoding="utf-8") as f:
            f.write(re)
        return 

def authenticat_app(two_step_verification_context, mid):
    code = input("[+] Authenticat code from app: ")
    url = "https://i.instagram.com/api/v1/bloks/apps/com.bloks.www.two_step_verification.verify_code.async/"
    headers={
        "User-Agent": 'Instagram 275.0.0.27.98 Android (29/10; 443dpi; 1080x2224; HUAWEI; STK-L21; HWSTK-HF; kirin710; en_OM; 458229237)',
        "X-Mid": mid
    }
    device_id = session_vars["device_id"]
    fdi=session_vars["family_device_id"]
    data = {
    "params": json.dumps({
        "client_input_params": {
            "auth_secure_device_id": "",
            "block_store_machine_id": "",
            "code": str(code),
            "should_trust_device": 1,
            "family_device_id": fdi,
            "device_id": device_id,
            "cloud_trust_token": None,
            "machine_id": mid
        },
        "server_params": {
            "INTERNAL__latency_qpl_marker_id": 36707139,
            "block_store_machine_id": None,
            "device_id": None,
            "cloud_trust_token": None,
            "challenge": "totp",
            "machine_id": None,
            "INTERNAL__latency_qpl_instance_id": 1.88332788500279e14,
            "two_step_verification_context": two_step_verification_context,
            "flow_source": "two_factor_login"
        }
    }),
    "bk_client_context": json.dumps({
        "bloks_version": session_vars["bloks_version"],
        "styles_id": "instagram"
    }),
    "bloks_versioning_id": session_vars["bloks_version"]
}
    re = requests.post(url, headers=headers, data=data).text.replace('\\', '').replace('\\\\', '').replace('\\\\\\', '')
    if 'IG-Set-Authorization' in re:
        print('[+] Done Login ..')
        match = ree.search(r'IG-Set-Authorization.*?Bearer ([A-Za-z0-9:_=\-]+)', re.replace('\\', '').replace('\\\\', '').replace('\\\\\\', '')).group(1)#@48i9
        print('[+] API SSID:', extract_session_from_token(match))
        print('[+] X-MID:', mid)
        return 
    elif 'Please check the security code and try again.' in re:
        print('[-] Bad code try again ..')
        authenticat_app(two_step_verification_context, mid)
    else:
        print('[-] Error try again')
        return
        
os.system("cls||clr||clear")
username = input("[+] Username: ")
password = input("[+] Password: ")  
#print(f"[+] Password: {'*' * len(password)}", end="\r")

d, mid= login(username, password)
if 'IG-Set-Authorization' in d:
    print("[+] Login Done")
    match = ree.search(r'IG-Set-Authorization.*?Bearer ([A-Za-z0-9:_=\-]+)', d)
    if match:
        token = match.group(1)
        print("[-] API SSID:", extract_session_from_token(token))
        print('[+] X-MID:', mid)
elif 'The password you entered is incorrect.' in d:
    print("[-] The password you entered is incorrect. (maybe its banned) ")
    input('[+] Press Enter To Reset Your Password. ')
    reset_password(username)
    
elif "two_step_verification_context" in d:
    print("[-] two_step_verification(2fa)")
    d=d.replace('\\', '').replace('\\\\', '').replace('\\\\\\', '')
    two_step_verification_context = d.split('"INTERNAL_INFRA_screen_id"), (bk.action.array.Make, "')[1].split('", "two_factor_login')[0]#@48i9 #@suul
    entrypoint(two_step_verification_context, mid)

elif "challenge_context" in d:
    print("[-] Secure found ..")
    match = ree.search(r'"api_path"\s*:\s*"([^"]+)"', d.replace('\\', '').replace('\\\\', '').replace('\\\\\\', '')).group(1)#@48i9
    match2 = ree.search(r'"challenge_context"\s*:\s*"([^"]+)"', d.replace('\\', '').replace('\\\\', '').replace('\\\\\\', '')).group(1)
    challenge_context, nonce_code, cni, choice = choose_verify_method(match, match2, mid)
    perf_logging_id, challenge_context = take_challenge(challenge_context, nonce_code, cni, choice, mid)
    perf_logging_id, challenge_context  = choice_(challenge_context, choice, mid)
    put_code(challenge_context, perf_logging_id, mid)

elif "checkpoint_redirection_login_attempt":
    input('[-] Some Thing is Wrong ..\n[+] Press Enter To Reset Your Password . ')
    reset_password(username)
    #print('[-] Secure2')
    #print(d)
    
    
else:
    input('[-] Some Thing is Wrong ..\n[+] Press Enter To Reset Your Password . ')
    reset_password(username)
