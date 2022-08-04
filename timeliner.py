import os,datetime,toml


class TL:
    def __init__(self, db_dir):
        self.root = db_dir
        if not os.path.exists(self.root):
            os.mkdir(self.root)

    def loc_exists(self, code):
        if os.path.exists(self.root + os.sep + code + ".toml"):
            return True
        else:
            return False

    def mk_path(self, code):
        return self.root + os.sep + code + ".toml"

    def get_obj(self, code):
        with open(self.mk_path(code)) as f:
            return toml.load(f)

    def save_obj(self, code, data):
        with open(self.mk_path(code), 'w') as f:
            f.write(toml.dumps(data))

    def new_loc(self, code, long):
        if not self.loc_exists(code):
            with open(self.mk_path(code), "w") as f:
                f.write("desc = '" + long + "'\n")

    def post_time(self, code, time):
        if self.loc_exists(code):
            data = self.get_obj(code)
            if not 'times' in data.keys():
                data['times'] = {}
            data['times'][str(datetime.datetime.now())] = time
            self.save_obj(code, data)

    def get_time(self, code):
        if self.loc_exists(code):
            data = self.get_obj(code)
            if 'times' in data.keys():
                return list(data['times'].items())[-1]

    def list_locations(self):
        stuff = []
        for elem in os.listdir(self.root):
            stuff.append(elem.replace(".toml",""))
        return stuff




if __name__ == "__main__":
    db = TL("data")
    db.new_loc("main", "Town square")
    #db.post_time("main", input("Something funny: "))
    print(db.get_time('main'))