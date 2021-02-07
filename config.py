import configparser

class config:
    # ConfigParser() doesn't work here because if the sessdata string contains '%'
    # it will throw this error: '%' must be followed by '%' or '(', found: "%&'"
    config = configparser.RawConfigParser()

    cookie_sessdata = ""
    cookie_jct = ""

    api_key = ""

    database_host = ""
    database_user = ""
    database_password = ""
    database_name = ""

    setup_time = ""

    bilibili_tid = 0
    bilibili_tag = ""

    @classmethod
    def read(self):
        try:
            self.config.read("config.ini", encoding="utf-8")
            self.cookie_sessdata = self.config.get("cookie", "sessdata")
            self.cookie_jct = self.config.get("cookie", "bili_jct")
            self.api_key = self.config.get("api", "key")
            self.database_host = self.config.get("database", "host")
            self.database_user = self.config.get("database", "user")
            self.database_password = self.config.get("database", "password")
            self.database_name = self.config.get("database", "name")
            self.setup_time = self.config.get("time", "setup_time")
            self.bilibili_tid = self.config.getint("bilibili", "tid")
            self.bilibili_tag = self.config.get("bilibili", "tag")
        except Exception as e:
            print(e.args)