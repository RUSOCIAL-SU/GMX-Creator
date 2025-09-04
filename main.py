import base64
import threading
import json
import random
import re
import string
import time
import uuid
import capsolver
import loguru
import curl_cffi.requests.session
import asyncio

file_lock = threading.Lock()

capsolver.api_key = "" # Needed For IMAP

def gen_phone():
    area = random.choice([201, 202, 203, 205, 206, 207, 208, 209, 210, 212, 213, 214, 215, 216, 217, 218, 219, 220, 223, 224, 225, 228, 229, 231, 234, 239, 240, 248, 251, 252, 253, 254, 256, 260, 262, 267, 269, 270, 272, 276, 281, 301, 302, 303, 304, 305, 307, 308, 309, 310, 312, 313, 314, 315, 316, 317, 318, 319, 320, 321, 323, 325, 330, 331, 334, 336, 337, 339, 340, 346, 347, 351, 352, 360, 361, 364, 380, 385, 386, 401, 402, 404, 405, 406, 407, 408, 409, 410, 412, 413, 414, 415, 417, 419, 423, 424, 425, 430, 432, 434, 435, 440, 442, 443, 445, 458, 463, 469, 470, 475, 478, 479, 480, 484, 501, 502, 503, 504, 505, 507, 508, 509, 510, 512, 513, 515, 516, 517, 518, 520, 530, 531, 534, 539, 540, 541, 551, 559, 561, 562, 563, 564, 567, 570, 571, 573, 574, 575, 580, 585, 586, 601, 602, 603, 605, 606, 607, 608, 609, 610, 612, 614, 615, 616, 617, 618, 619, 620, 623, 626, 628, 629, 630, 631, 636, 641, 646, 650, 651, 657, 660, 661, 662, 667, 669, 678, 681, 682, 701, 702, 703, 704, 706, 707, 708, 712, 713, 714, 715, 716, 717, 718, 719, 720, 724, 725, 727, 731, 732, 734, 737, 740, 743, 747, 754, 757, 760, 762, 763, 765, 769, 770, 772, 773, 774, 775, 779, 781, 785, 786, 801, 802, 803, 804, 805, 806, 808, 810, 812, 813, 814, 815, 816, 817, 818, 828, 830, 831, 832, 843, 845, 847, 848, 850, 854, 856, 857, 858, 859, 860, 862, 863, 864, 865, 870, 872, 878, 901, 903, 904, 906, 907, 908, 909, 910, 912, 913, 914, 915, 916, 917, 918, 919, 920, 925, 928, 929, 930, 931, 934, 936, 937, 938, 940, 941, 947, 949, 951, 952, 954, 956, 959, 970, 971, 972, 973, 975, 978, 979, 980, 984, 985, 989])
    return f"{area}-{random.randint(200, 999)}-{random.randint(1000, 9999)}"

class GmxRegister:
    def __init__(self):
        self.session = curl_cffi.requests.Session(impersonate="chrome136")
        self.session.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Sec-GPC': '1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }
        # Thread-safe proxies retrieval
        with file_lock:
            proxies = open('proxies.txt', 'r').readlines()
        proxy = random.choice(proxies).strip()
        self.session.proxies = {
            "http": f"http://{proxy}",
            "https": f"http://{proxy}"
        }
        self.account_passw = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))
        self.account_email = f'{"".join(random.choice(string.ascii_lowercase) for _ in range(13))}@gmx.com'
        self.loop = None

    def get_session(self):
        response = self.session.get('https://signup.gmx.com/')
        try:
            self.accessToken = response.text.split('"accessToken": "')[1].split('"')[0]
            self.clientCredentialGuid = response.text.split('"clientCredentialGuid": "')[1].split('"')[0]
            self.statistics = response.text.split('"statistics": "')[1].split('"')[0]
            loguru.logger.info(f"Access Token: {self.accessToken}")
            loguru.logger.info(f"Client Credential GUID: {self.clientCredentialGuid}")
            loguru.logger.info(f"Statistics: {self.statistics}")
            return bool(self.accessToken and self.clientCredentialGuid) and self.statistics
        except:
            return False

    def register(self):
        self.session.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Authorization': f'Bearer {self.accessToken}',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Type': 'application/vnd.ui.mam.account.creation+json',
            'Origin': 'https://signup.gmx.com',
            'Pragma': 'no-cache',
            'Referer': 'https://signup.gmx.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-GPC': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
            'X-CCGUID': self.clientCredentialGuid,
            'X-REQUEST-ID': str(uuid.uuid4()),
            'X-UI-APP': '@mamdev/umreg.registration-app2/8.16.1',
            'sec-ch-ua': '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }

        start_time = time.time()
        
        if time.time() - start_time < 30:
            time.sleep(30 - (time.time() - start_time)) # or they flag the account
            
        solver = # Use your API key here
        captcha_task = CaptchaTask(
            sitekey="sk_vKdD8WGlPF5FKpRDs1U4qTuu6Jv0w",
            siteurl="https://signup.gmx.com/#.1559516-header-signup1-1",
            proxy=self.session.proxies["http"]
        )
        
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        
        try:
            result = self.loop.run_until_complete(solver.solve_captcha_async(captcha_task, captcha_type="captchafox"))
            self.session.headers['cf-captcha-response'] = result
        finally:
            pass

        data = {
            "user": {
                "givenName": ''.join(random.choice(string.ascii_letters) for _ in range(8)),
                "familyName": ''.join(random.choice(string.ascii_letters) for _ in range(8)),
                "gender": "MALE", # we all straight here
                "birthDate": f"{random.randint(1990, 2000)}-0{random.randint(1, 9)}-{random.randint(10, 30)}",
                "mobileNumber": f"+1{gen_phone()}",
                "address": {
                    "countryCode": "US",
                    "region": "AL",
                    "postalCode": "",
                    "locality": "",
                    "streetAddress": ""
                },
                "credentials": {
                    "password": self.account_passw
                }
            },
            "mailAccount": {
                "email": self.account_email,
            },
            "product": "gmxcomFree"
        }

        response = self.session.post('https://signup.gmx.com/account/email-registration', data=json.dumps(data))
        loguru.logger.info(f"[{self.account_email}] Registration response status: {response.status_code}")
        loguru.logger.info(f"[{self.account_email}] Registration response body: {response.text[:500]}...")
        return response.status_code == 204
        
    def activate_account(self):
        # Safe extraction helper function
        def safe_extract(text, marker, delimiter=None, end_char=None):
            try:
                if marker not in text:
                    loguru.logger.warning(f"[{self.account_email}] Marker '{marker}' not found in response")
                    return None
                    
                parts = text.split(marker)
                if len(parts) < 2:
                    loguru.logger.warning(f"[{self.account_email}] Could not split on '{marker}'")
                    return None
                    
                extracted = parts[1]
                
                if delimiter:
                    extracted_parts = extracted.split(delimiter)
                    if not extracted_parts:
                        loguru.logger.warning(f"[{self.account_email}] Could not split on delimiter '{delimiter}'")
                        return None
                    return extracted_parts[0]
                
                if end_char:
                    end_index = extracted.find(end_char)
                    if end_index == -1:
                        loguru.logger.warning(f"[{self.account_email}] End character '{end_char}' not found")
                        return None
                    return extracted[:end_index]
                    
                return extracted
            except Exception as e:
                loguru.logger.error(f"[{self.account_email}] Error extracting with marker '{marker}': {str(e)}")
                return None
    
        self.session.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'no-cache',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://signup.gmx.com',
            'pragma': 'no-cache',
            'priority': 'u=0, i',
            'referer': 'https://signup.gmx.com/',
            'sec-ch-ua': '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-site',
            'sec-fetch-user': '?1',
            'sec-gpc': '1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
        }
    
        data = {
            'successURL': 'https://interception-bs.gmx.com/logininterceptionfrontend/?interceptiontype=RegistrationWelcomeInterception&tgt=https%3A%2F%2Fnavigator-bs.gmx.com%2Flogin&tsid=mailint',
            'loginErrorURL': 'https://www.gmx.com/int/',
            'loginFailedURL': 'https://www.gmx.com/int/',
            'statistics': self.statistics,
            'service': 'RegistrationWelcomeInterception',
            'username': self.account_email,
            'password': self.account_passw,
            'iid': self.clientCredentialGuid,
            'registrationcountry': 'us',
            'brand': 'gmxcom',
            'contentposition': 'web',
            'source': '',
        }
    
        # Step 1: Login to GMX
        loguru.logger.info(f"[{self.account_email}] Logging in")
        response = self.session.post('https://login.gmx.com/login', data=data)
        
        # Extract necessary tokens from response
        try:
            iid = safe_extract(response.text, 'iid=', '&')
            ott = safe_extract(response.text, 'ott=', '&')
            requestSecurityToken = safe_extract(response.text, 'requestSecurityToken=', '"')
            auth_time = safe_extract(response.text, 'auth_time=', '&')
            
            if None in (iid, ott, requestSecurityToken, auth_time):
                loguru.logger.error(f"[{self.account_email}] Missing tokens in login response")
                return False
                
            loguru.logger.info(f"[{self.account_email}] Successfully extracted login tokens")
        except Exception as e:
            loguru.logger.error(f"[{self.account_email}] Failed to extract tokens: {str(e)}")
            return False
    
        # Step 2: Handle the Welcome Interception
        params = (
            ('0-1.-welcomePanel-continueForm', ''),
            ('interceptiontype', 'RegistrationWelcomeInterception'),
            ('tgt', 'https://navigator-bs.gmx.com/login'),
            ('tsid', 'mailint'),
            ('iid', iid),
            ('registrationcountry', 'us'),
            ('source', ''),
            ('contentposition', 'web'),
            ('auth_time', auth_time),
            ('brand', 'gmxcom'),
            ('ott', ott),
            ('requestSecurityToken', requestSecurityToken),
        )
    
        data = {
            'requestSecurityToken': requestSecurityToken,
            'continueButton': ''
        }
    
        loguru.logger.info(f"[{self.account_email}] Handling welcome interception")
        response = self.session.post('https://interception-bs.gmx.com/logininterceptionfrontend/', params=params, data=data)
        
        ott = safe_extract(response.text, 'ott=', '&')
        if not ott:
            loguru.logger.error(f"[{self.account_email}] Failed to extract OTT token from interception response")
            return False
    
        # Step 3: Navigation to the main interface
        params = (
            ('mobileAction', 'mobile:interception:close'),
            ('ott', ott),
            ('tz', '3'),
        )
    
        loguru.logger.info(f"[{self.account_email}] Navigating to main interface")
        response = self.session.get('https://navigator-bs.gmx.com/halogin', params=params)
        
        if 'sid=' not in response.url:
            loguru.logger.error(f"[{self.account_email}] SID not found in URL: {response.url}")
            return False
            
        sid = safe_extract(response.url, 'sid=')
        if not sid:
            loguru.logger.error(f"[{self.account_email}] Failed to extract SID")
            return False
            
        loguru.logger.info(f"[{self.account_email}] Successfully got SID: {sid[:10]}...")
    
        # Step 4: Access account settings
        params = {'sid': sid}
        
        loguru.logger.info(f"[{self.account_email}] Accessing account settings")
        response = self.session.get('https://navigator-bs.gmx.com/', params=params)
        
        # Step 5: Direct access to email settings since the marker isn't found
        loguru.logger.info(f"[{self.account_email}] Directly accessing email settings")
        
        # From the HTML structure, we need to find mail settings URL
        # First try to find it from the response
        mail_settings_url = None
        
        # Look for mail_settings in the application config
        mail_settings_match = re.search(r'"mail_settings":\s*{[^}]*"url_map":\s*{"default":\s*"([^"]*)"', response.text)
        if mail_settings_match:
            mail_settings_url = mail_settings_match.group(1)
            mail_settings_url = mail_settings_url.replace('\\', '')
            loguru.logger.info(f"[{self.account_email}] Found mail settings URL: {mail_settings_url}")
        
        # If we can't find it, try a direct URL format
        if not mail_settings_url:
            loguru.logger.info(f"[{self.account_email}] Using direct URL to mail settings")
            mail_settings_url = f"/navigator/jump/to/mail_settings?sid={sid}"
        
        # Access mail settings
        loguru.logger.info(f"[{self.account_email}] Accessing mail settings at: {mail_settings_url}")
        
        if mail_settings_url.startswith('/'):
            mail_settings_url = f"https://navigator-bs.gmx.com{mail_settings_url}"
        
        response = self.session.get(mail_settings_url)
        
        # Step 6: Find the POP3/IMAP settings link
        loguru.logger.info(f"[{self.account_email}] Looking for POP3/IMAP settings")
        
        # Try to find the POP3/IMAP settings URL
        pop3_url = None
        
        # Method 1: Look for direct link to popImap settings
        pop3_pattern = r'href="([^"]*popImap[^"]*)"'
        pop3_match = re.search(pop3_pattern, response.text)
        
        if pop3_match:
            pop3_url = pop3_match.group(1)
            loguru.logger.info(f"[{self.account_email}] Found POP3/IMAP settings link: {pop3_url}")
        
        # Method 2: Check if we're redirected to the client interface
        if not pop3_url and "3c-bs.gmx.com" in response.url:
            loguru.logger.info(f"[{self.account_email}] Redirected to client interface, looking for settings")
            # We are in the mail client, need to find settings
            settings_link_pattern = r'href="([^"]*settings[^"]*)"'
            settings_match = re.search(settings_link_pattern, response.text)
            
            if settings_match:
                settings_url = settings_match.group(1)
                if settings_url.startswith('./'):
                    settings_url = settings_url[2:]
                
                base_url = "https://3c-bs.gmx.com/mail/client/"
                settings_url = f"{base_url}{settings_url}"
                
                loguru.logger.info(f"[{self.account_email}] Found settings link: {settings_url}")
                
                # Access settings page
                response = self.session.get(settings_url)
                
                # Now look for POP3/IMAP settings
                pop3_pattern = r'href="([^"]*popImap[^"]*)"'
                pop3_match = re.search(pop3_pattern, response.text)
                
                if pop3_match:
                    pop3_url = pop3_match.group(1)
                    loguru.logger.info(f"[{self.account_email}] Found POP3/IMAP settings link: {pop3_url}")
        
        # Method 3: Direct URL construction
        if not pop3_url:
            loguru.logger.info(f"[{self.account_email}] Using direct URL to POP3/IMAP settings")
            # Extract jsessionid if available
            jsession_match = re.search(r'jsessionid=([^"&;]+)', response.text)
            jsessionid = jsession_match.group(1) if jsession_match else ""
            
            # Try to construct the URL
            if "3c-bs.gmx.com" in response.url:
                base_url = "https://3c-bs.gmx.com/mail/client/settings/"
                if jsessionid:
                    pop3_url = f"{base_url}popImap;jsessionid={jsessionid}"
                else:
                    pop3_url = f"{base_url}popImap"
        
        # Method 4: Last resort - try a set of common URL patterns
        if not pop3_url:
            loguru.logger.warning(f"[{self.account_email}] Could not find POP3/IMAP settings link, trying common patterns")
            common_patterns = [
                f"https://3c-bs.gmx.com/mail/client/settings/popImap?sid={sid}",
                f"https://3c-bs.gmx.com/mail/client/settings/popImap",
                f"https://navigator-bs.gmx.com/navigator/jump/to/mail_settings/popImap?sid={sid}"
            ]
            
            for pattern in common_patterns:
                loguru.logger.info(f"[{self.account_email}] Trying POP3/IMAP URL: {pattern}")
                response = self.session.get(pattern)
                
                if "POP3/IMAP" in response.text or "pop3" in response.text.lower() or "imap" in response.text.lower():
                    pop3_url = pattern
                    loguru.logger.info(f"[{self.account_email}] Found working POP3/IMAP URL: {pattern}")
                    break
        
        if not pop3_url:
            loguru.logger.error(f"[{self.account_email}] Failed to find POP3/IMAP settings link")
            return False
        
        # Step 7: Access POP3/IMAP settings
        loguru.logger.info(f"[{self.account_email}] Accessing POP3/IMAP settings at: {pop3_url}")
        
        # Make sure the URL is absolute
        if not pop3_url.startswith('http'):
            if pop3_url.startswith('/'):
                pop3_url = f"https://3c-bs.gmx.com{pop3_url}"
            else:
                pop3_url = f"https://3c-bs.gmx.com/mail/client/settings/{pop3_url}"
        
        response = self.session.get(pop3_url)
        
        # Step 8: Enable POP3/IMAP
        loguru.logger.info(f"[{self.account_email}] Enabling POP3/IMAP access")
        
        # Update headers for form submission
        self.session.headers.update({
            'Accept': 'application/xml, text/xml, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.9',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'https://3c-bs.gmx.com',
            'Referer': pop3_url,
            'X-Requested-With': 'XMLHttpRequest',
            'Wicket-Ajax': 'true',
            'Wicket-Ajax-BaseURL': 'settings/popImap',
        })
        
        # Look for form submission URL and field names
        form_url = None
        checkbox_name = "popImapChapter%3Apop3ImapSmtpCheckBox"
        submit_name = "popImapChapter%3AsubmitButtons%3Asave"
        
        # Try to find the form URL
        form_pattern = r'action="([^"]*)"[^>]*id="id[^"]*"'
        form_match = re.search(form_pattern, response.text)
        
        if form_match:
            form_action = form_match.group(1)
            if form_action.startswith('./'):
                form_action = form_action[2:]
                
            if "3c-bs.gmx.com" in pop3_url:
                base_url = pop3_url.split('/settings/')[0] + '/settings/'
                form_url = f"{base_url}{form_action}"
            else:
                form_url = f"https://3c-bs.gmx.com/mail/client/settings/{form_action}"
                
            loguru.logger.info(f"[{self.account_email}] Found form submission URL: {form_url}")
        
        # Try to find submit button pattern
        submit_pattern = r'./popImap;jsessionid=[^"]*submitButtons-save'
        submit_match = re.search(submit_pattern, response.text)
        
        if submit_match and not form_url:
            submit_url = submit_match.group(0)
            if submit_url.startswith('./'):
                submit_url = submit_url[2:]
                
            form_url = f"https://3c-bs.gmx.com/mail/client/settings/{submit_url}"
            loguru.logger.info(f"[{self.account_email}] Found submit button URL: {form_url}")
        
        # If we still don't have a form URL, try another approach
        if not form_url:
            # Look for any form with popImap
            alt_form_pattern = r'form[^>]*action="([^"]*popImap[^"]*)"'
            alt_form_match = re.search(alt_form_pattern, response.text)
            
            if alt_form_match:
                form_action = alt_form_match.group(1)
                if form_action.startswith('./'):
                    form_action = form_action[2:]
                    
                form_url = f"https://3c-bs.gmx.com/mail/client/settings/{form_action}"
                loguru.logger.info(f"[{self.account_email}] Found alternative form URL: {form_url}")
        
        # If no form URL is found, use the current URL
        if not form_url:
            form_url = pop3_url
            loguru.logger.warning(f"[{self.account_email}] Using current URL as form URL: {form_url}")
        
        # Look for the correct field names
        checkbox_pattern = r'name="([^"]*checkbox[^"]*)"'
        checkbox_match = re.search(checkbox_pattern, response.text, re.IGNORECASE)
        
        if checkbox_match:
            checkbox_name = checkbox_match.group(1)
            loguru.logger.info(f"[{self.account_email}] Found checkbox name: {checkbox_name}")
        
        submit_pattern = r'name="([^"]*save[^"]*)"'
        submit_match = re.search(submit_pattern, response.text, re.IGNORECASE)
        
        if submit_match:
            submit_name = submit_match.group(1)
            loguru.logger.info(f"[{self.account_email}] Found submit button name: {submit_name}")
        
        # Prepare and submit the form
        form_data = f"{checkbox_name}=on&{submit_name}=1"
        loguru.logger.info(f"[{self.account_email}] Submitting form with data: {form_data}")
        
        try:
            response = self.session.post(form_url, data=form_data)
            loguru.logger.info(f"[{self.account_email}] Form submission status: {response.status_code}")
        except Exception as e:
            loguru.logger.error(f"[{self.account_email}] Error posting form: {str(e)}")
            # Try alternative approach
            try:
                alt_form_data = {
                    checkbox_name: "on",
                    submit_name: "1"
                }
                loguru.logger.info(f"[{self.account_email}] Trying alternative form submission")
                response = self.session.post(form_url, data=alt_form_data)
            except Exception as e:
                loguru.logger.error(f"[{self.account_email}] Error with alternative form submission: {str(e)}")
                return False
        
        # Step 9: Handle captcha if needed
        if "captcha" in response.text.lower():
            loguru.logger.info(f"[{self.account_email}] Captcha challenge detected")
            
            # Find captcha image URL
            captcha_pattern = r'src="([^"]*captcha[^"]*)"'
            captcha_match = re.search(captcha_pattern, response.text)
            
            if not captcha_match:
                # Try alternative patterns
                captcha_pattern = r'src="([^"]*antiCache[^"]*)"'
                captcha_match = re.search(captcha_pattern, response.text)
            
            if not captcha_match:
                captcha_pattern = r'src="(\.\/popImap;jsessionid=[^"]*)"'
                captcha_match = re.search(captcha_pattern, response.text)
            
            if captcha_match:
                captcha_url = captcha_match.group(1)
                if captcha_url.startswith('./'):
                    captcha_url = captcha_url[2:]
                    
                captcha_url = f"https://3c-bs.gmx.com/mail/client/settings/{captcha_url}".replace('&amp;', '&')
                loguru.logger.info(f"[{self.account_email}] Found captcha image URL: {captcha_url}")
                
                # Get captcha image
                response = self.session.get(captcha_url)
                
                # Solve captcha
                b64_captcha = base64.b64encode(response.content).decode()
                
                try:
                    solution = capsolver.solve({
                        "type": "ImageToTextTask",
                        "module": "module_013",
                        "body": b64_captcha
                    })["text"]
                    
                    loguru.logger.info(f"[{self.account_email}] Solved captcha: {solution}")
                except Exception as e:
                    loguru.logger.error(f"[{self.account_email}] Failed to solve captcha: {str(e)}")
                    return False
                
                # Find captcha form submission URL
                captcha_form_url = None
                
                # Try different methods to find the form submission URL
                if '-splitPanel' in form_url:
                    url_parts = form_url.split('-splitPanel')
                    captcha_form_url = url_parts[0] + '-topLevelContainer-dialog-root~container-container-form-chapter-chapter_body-bottomButtons-container-bottomButtons_body-ok'
                    loguru.logger.info(f"[{self.account_email}] Constructed captcha form URL using splitPanel method")
                
                if not captcha_form_url:
                    form_pattern = r'action="([^"]*captcha[^"]*)"'
                    form_match = re.search(form_pattern, response.text)
                    if form_match:
                        form_action = form_match.group(1)
                        if form_action.startswith('./'):
                            form_action = form_action[2:]
                            
                        captcha_form_url = f"https://3c-bs.gmx.com/mail/client/settings/{form_action}"
                        loguru.logger.info(f"[{self.account_email}] Found captcha form URL: {captcha_form_url}")
                
                if not captcha_form_url:
                    # Look for name="ok" button
                    ok_pattern = r'name="([^"]*ok[^"]*)"'
                    ok_match = re.search(ok_pattern, response.text)
                    if ok_match:
                        ok_name = ok_match.group(1)
                        
                        # Try to construct the URL
                        if ';jsessionid=' in form_url:
                            base_url = form_url.split(';jsessionid=')[0]
                            jsession = form_url.split(';jsessionid=')[1]
                            if '?' in jsession:
                                jsession = jsession.split('?')[0]
                            captcha_form_url = f"{base_url};jsessionid={jsession}-form-captchaForm-ok"
                        else:
                            captcha_form_url = form_url
                            
                        loguru.logger.info(f"[{self.account_email}] Constructed captcha form URL using ok button: {captcha_form_url}")
                
                if not captcha_form_url:
                    captcha_form_url = form_url
                    loguru.logger.warning(f"[{self.account_email}] Using current URL as captcha form URL: {captcha_form_url}")
                
                # Find captcha form field names
                captcha_field_name = 'chapter:chapter_body:fieldset:fieldset_body:captchaTextFieldItem:captchaTextFieldItem_body:captchaTextField'
                ok_button_name = 'chapter:chapter_body:bottomButtons:container:bottomButtons_body:ok'
                
                # Look for actual field names
                captcha_field_pattern = r'name="([^"]*captcha[^"]*)"'
                captcha_field_match = re.search(captcha_field_pattern, response.text)
                if captcha_field_match:
                    captcha_field_name = captcha_field_match.group(1)
                    loguru.logger.info(f"[{self.account_email}] Found captcha field name: {captcha_field_name}")
                
                ok_button_pattern = r'name="([^"]*ok[^"]*)"'
                ok_button_match = re.search(ok_button_pattern, response.text)
                if ok_button_match:
                    ok_button_name = ok_button_match.group(1)
                    loguru.logger.info(f"[{self.account_email}] Found ok button name: {ok_button_name}")
                
                # Prepare and submit captcha form
                captcha_data = {
                    captcha_field_name: solution,
                    ok_button_name: '1'
                }
                
                loguru.logger.info(f"[{self.account_email}] Submitting captcha form with solution: {solution}")
                
                try:
                    response = self.session.post(captcha_form_url, data=captcha_data)
                    loguru.logger.info(f"[{self.account_email}] Captcha form submission status: {response.status_code}")
                except Exception as e:
                    loguru.logger.error(f"[{self.account_email}] Error submitting captcha form: {str(e)}")
                    return False
                
            else:
                loguru.logger.error(f"[{self.account_email}] Captcha detected but could not find captcha image URL")
                return False
        
        # Step 10: Check if activation was successful
        if "Settings were saved successfully" in response.text:
            loguru.logger.success(f"[{self.account_email}] POP3/IMAP successfully activated")
            with file_lock:
                with open("account.txt", "a") as f:
                    f.write(f"{self.account_email}:{self.account_passw}\n")
            return True
        else:
            # Check if we need to try an alternative approach
            if "pop3" in response.text.lower() or "imap" in response.text.lower():
                loguru.logger.info(f"[{self.account_email}] POP3/IMAP page found but activation result unclear, checking settings")
                
                # Try to get to settings again to verify
                verify_url = pop3_url
                response = self.session.get(verify_url)
                
                # Check if POP3/IMAP is enabled
                if 'checked="checked"' in response.text and ("pop3" in response.text.lower() or "imap" in response.text.lower()):
                    loguru.logger.success(f"[{self.account_email}] POP3/IMAP appears to be enabled")
                    with file_lock:
                        with open("account.txt", "a") as f:
                            f.write(f"{self.account_email}:{self.account_passw}\n")
                    return True
                else:
                    loguru.logger.error(f"[{self.account_email}] POP3/IMAP activation failed or could not be verified")
                    return False
            else:
                loguru.logger.error(f"[{self.account_email}] POP3/IMAP activation failed")
                return False

    def __del__(self):
        if self.loop:
            self.loop.close()

def handle_thread():
    while True:
        try:
            gmx = GmxRegister()
            csrf_success = gmx.get_session()

            if not csrf_success:
                loguru.logger.error("Failed to get session")
                return False
            else:
                loguru.logger.info(f"[{gmx.account_email}] Successfully got session")
            
            register_success = gmx.register()

            if register_success:
                loguru.logger.success(f"[{gmx.account_email}] Successfully registered {gmx.account_email} with password {gmx.account_passw}")
                gmx.activate_account()
            else:
                loguru.logger.error(f"[{gmx.account_email}] Failed to register {gmx.account_email}")
        except Exception as e:
            loguru.logger.error(f"Error: {e}")

thread_count = int(input("Enter thread count: "))

threads = []
for a in range(thread_count):
    thread = threading.Thread(target=handle_thread)
    thread.daemon = True
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()