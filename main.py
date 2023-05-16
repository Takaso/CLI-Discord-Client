import requests; import json; import os; from other.colors import *; from pick import pick; import time;
tok = json.load(open("token/config.json"));
class Sexcord():
    def __init__(self, token) -> None:
        self.api_url:str = "https://discord.com/api/v9/";
        self.token:str = token;
        self.headers = {
            "Authorization": self.token
        };
        pass;
    def load_private_channels(self) -> list:
        _r1 = requests.get("%s/users/@me/channels" % self.api_url, headers=self.headers); z = _r1.json();
        try:
            _r1.raise_for_status();
        except Exception as x:
            print("[%s!%s] Failed to load DMs, an error occured, error message: %s%s%s" % (magenta(), reset(), red(), x, reset())); return 0x1;
        dms = []; 
        for z in _r1.json():
            try:
                dms.append([str(z['name']), " - ", z['id'], z['id']]);
            except KeyError:
                for i in z['recipients']:
                    dms.append([i['username'], i['discriminator'], i['id'], z['id']]);
        dms = dms[::-1];
        def __extract_channel__(lst:list) -> list:
            return ["%s#%s" % (item[0],item[1]) for item in lst];
        choice = pick(__extract_channel__(dms), "Choose the channel > ");
        def __send_message__(dm_id:int, content:str) -> int:
            _r4 = requests.post("%s/channels/%s/messages" % (self.api_url, dm_id), headers=self.headers, json={"content": content}); p = _r4.json();
            os.system("cls" if os.name == "nt" else "clear");
            try:
                _r4.raise_for_status();
            except Exception:
                print("Failed to send message." % p);
            return p;
        def __dm_channel__(dm_id:int, query_parameter:str=""):
            _r3 = requests.get("%s/channels/%s/messages?limit=100%s" % (self.api_url, dm_id, query_parameter), headers=self.headers); l = _r3.json(); l=l[::-1];
            def __extract_messages__(lst:list, n:int=0) -> list:
                return ["%s" % (item[n]) for item in lst];
            messages = [["[+] Exit", "0", "0"]];
            for _ in l:
                messages.append(["%s : %s" % (_['author']['username'], _['content'] if not _['content'] == "" else "[This is an attachment.]"), _['id']]);
            messages.append(["[+] Load more", "0", "0"]); messages.append(["[+] Refresh", "0", "0"]); messages.append(["[+] Send Message", "0", "0"]); messages.append(["[+] Full Chat", "0", "0"]);
            choice_ = pick(__extract_messages__(messages), "Messages with %s" % dms[choice[1]][0]);
            if "[+] Exit" in choice_[0]:
                return self.load_private_channels();
            elif "[+] Load more" in choice_[0]:
                oldest = max(int(___) for ___ in __extract_messages__(messages, 1));
                if oldest == 0:
                    return self.load_private_channels();
                return __dm_channel__(dm_id, "&before=%s" % str(oldest));
            elif "[+] Refresh" in choice_[0]:
                return __dm_channel__(dm_id);
            elif "[+] Send Message" in choice_[0]:
                __send_message__(dm_id, input("   Message > ")); return __dm_channel__(dm_id);
            elif "[+] Full Chat" in choice_[0]:
                os.system("cls" if os.name == "nt" else "clear");
                def dm_chat(_dm_id:str) -> list:
                    b:int = 0; dms = []; xlimit = input("Insert limit > ");
                    x_messages = requests.get("https://discord.com/api/v9/channels/%s/messages/search?min_id=48892162867200000&offset=%s" % (_dm_id, b), headers=self.headers);
                    try:
                        _json = x_messages.json(); tot_res = int(_json['total_results']);
                    except:
                        print(_json); return;
                    if not xlimit.isnumeric(): xlimit = tot_res;
                    if tot_res < 25: return ["%s : %s" % (i[0]['author']['username'], i[0]['content']) for i in _json['messages']][::-1];
                    dms.append(["%s : %s" % (i[0]['author']['username'], i[0]['content']) for i in _json['messages']]); b=25;
                    while b<tot_res and b<int(xlimit):
                        while True:
                            x_messages = requests.get("https://discord.com/api/v9/channels/%s/messages/search?min_id=48892162867200000&offset=%s" % (_dm_id, b), headers=self.headers); _json = x_messages.json();
                            if x_messages.status_code == 429:
                                print("Rate Limited.."); time.sleep(_json['retry_after']);
                            elif x_messages.ok:
                                dms.append(["%s : %s" % (i[0]['author']['username'], i[0]['content']) for i in _json['messages']]); b+=25; break;
                        print("Scraping DMS.. %s/%s messages loaded." % (b, tot_res));
                    return dms;
                def flatten_list(nested_list:list):
                    return [x for sublist in nested_list for x in flatten_list(sublist)] if isinstance(nested_list, list) else [nested_list];
                for _ in flatten_list(dm_chat(dm_id))[::-1]: print(_);
                input(); os.system("cls" if os.name == "nt" else "clear"); return __dm_channel__(dm_id);
            else:
                print(choice_);
        __dm_channel__(dms[choice[1]][3]);
        return [_r1.status_code, _r1.json()];
        
    def login(self) -> int:
        if not "y" in input("User Account? y/n > ").lower():
            self.headers = {"Authorization":"Bot %s" % tok['token']};
        os.system("cls" if os.name == "nt" else "clear");
        _r2 = requests.get("%s/users/@me" % self.api_url, headers=self.headers); y = _r2.json();
        if not _r2.ok:
            print("[%s!%s] Failed to login, an error occured, error message: %s%s%s" % (magenta(), reset(), red(), y, reset())); return 0x1;
        print("""
 Connected to: [%s%s#%s%s] 

""" % (red(), y['username'], y['discriminator'], reset()));
        return y;       
def main() -> int:
    sexcord = Sexcord(tok['token']); sexcord.login();
    sexcord.load_private_channels();
    input(); return 0;
if __name__ == "__main__":
    main();
