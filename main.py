import httpx; import json; import os; from other.colors import *; from pick import pick;
tok = json.load(open("token/config.json"));
class Sexcord():
    def __init__(self, token) -> None:
        self.api_url:str = "https://discord.com/api/v10/";
        self.token:str = token;
        self.headers = {
            "Authorization": self.token
        };
        pass;
    def load_private_channels(self) -> list:
        _r1 = httpx.get("%s/users/@me/channels" % self.api_url, headers=self.headers); z = _r1.json();
        try:
            _r1.raise_for_status();
        except Exception as x:
            print("An error occured: %s" % z);
            return 1;
        # Test
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
            _r4 = httpx.post("%s/channels/%s/messages" % (self.api_url, dm_id), headers=self.headers, json={"content": content}); p = _r4.json();
            os.system("cls" if os.name == "nt" else "clear");
            try:
                _r4.raise_for_status();
            except Exception:
                print("Failed to send message." % p);
            return p;
        def __dm_channel__(dm_id:int, query_parameter:str=""):
            _r3 = httpx.get("%s/channels/%s/messages?limit=100%s" % (self.api_url, dm_id, query_parameter), headers=self.headers); l = _r3.json(); l=l[::-1];
            def __extract_messages__(lst:list, n:int=0) -> list:
                return ["%s" % (item[n]) for item in lst];
            messages = [["[+] Exit", "0", "0"]];
            for _ in l:
                messages.append(["%s : %s" % (_['author']['username'], _['content'] if not _['content'] == "" else "[This is an attachment.]"), _['id']]);
            messages.append(["[+] Load more", "0", "0"]); messages.append(["[+] Refresh", "0", "0"]); messages.append(["[+] Send Message", "0", "0"]);
            choice_ = pick(__extract_messages__(messages), "Messages with %s" % dms[choice[1]][0]);
            if choice_[0] == "[+] Exit":
                return self.load_private_channels();
            elif choice_[0] == "[+] Load more":
                oldest = max(int(___) for ___ in __extract_messages__(messages, 1));
                if oldest == 0:
                    return self.load_private_channels();
                return __dm_channel__(dm_id, "&before=%s" % str(oldest));
            elif choice_[0] == "[+] Refresh":
                return __dm_channel__(dm_id);
            elif choice_[0] == "[+] Send Message":
                __send_message__(dm_id, input("   Message > ")); return __dm_channel__(dm_id);
            else:
                print(choice_);
        __dm_channel__(dms[choice[1]][3]);
        return [_r1.status_code, _r1.json()];
        
    def login(self) -> int:
        if not "y" in input("User Account? y/n > ").lower():
            self.headers = {"Authorization":"Bot %s" % tok['token']};
        os.system("cls" if os.name == "nt" else "clear");
        _r2 = httpx.get("%s/users/@me" % self.api_url, headers=self.headers); y = _r2.json();
        try:
            _r2.raise_for_status();
        except Exception:
            print("An error occured: %s" % y)
            return 1;
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
