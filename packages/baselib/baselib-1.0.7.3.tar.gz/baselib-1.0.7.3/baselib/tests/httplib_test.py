from baselib.py import httplib



class TestHttplib(object):

    def test_request(self):
        import ssl
        ssl._create_default_https_context = ssl._create_unverified_context
        conn = httplib.HTTPSConnection("www.python.org")
        conn.request("GET", "/index.html")
        r1 = conn.getresponse()
        print(r1.status, r1.reason)
        # data1 = r1.read()
        # print('data', data1)
        conn.close()


if __name__ == "__main__":
    TestHttplib().test_request()
