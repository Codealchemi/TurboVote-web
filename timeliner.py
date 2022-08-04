import os,datetime,toml,json

from jServ_api.jServ import jServ

class TL:
    def __init__(self, url, port, key):
        self.db = jServ(url, port, key)

    def loc_exists(self, code):
        resp = self.db.send_query("locations", code)
        if resp['status'] == "error":
            return False
        else:
            return True

    def get_obj(self, code):
        return self.db.send_query("locations", code)

    def get_js_id(self):
        res = self.db.send_query_newId("locations")
        if res['status'] == 'ok':
            return int(res['data']['value'])

    def new_loc(self, long):
        nid = self.get_js_id()
        obj = {
            "id": nid,
            "data": {
                "desc": long,
                "times": []
            }
        }
        resp = self.db.send_add_object("locations", json.dumps(obj))
        if resp['status'] == 'ok':
            return "New location made with code: " + str(nid)

    def post_time(self, code, time):
        if self.loc_exists(code):
            obj = self.get_obj(code)
            if obj['status'] == 'ok':
                times = obj['data']['data']['times']
                times.append(time)
                times_obj = {"times": times}
                print(str(json.dumps(times_obj)))
                resp = self.db.send_mod_attribute("locations", code, "times", json.dumps(times_obj))
                if resp['status'] == 'ok':
                    return "Added new time of " + str(time) + " to object " + str(code)
                else:
                    return str(resp)

    def get_time(self, code):
        if self.loc_exists(code):
            obj = self.get_obj(code)
            if obj['status'] == 'ok':
                times = obj['data']['times']
                return str(times[-1])
            else:
                return "n/a"


    def list_locations(self):
        res = self.db.send_query_allAttributes("locations", "desc")
        print(str(res))




if __name__ == "__main__":
    db = TL("localhost", 4040, "7dd30892-a7a9-4343-bab0-1cdf6575a201")
    db.new_loc("Town square")
    db.post_time("main", input("Something funny: "))
    db.list_locations()