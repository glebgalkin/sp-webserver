import http.client
import unittest


class TestServer(unittest.TestCase):

    def test_echo(self):
        conn = http.client.HTTPConnection("localhost", 4221)
        conn.request('GET', '/echo/hello')
        response = conn.getresponse()
        body = response.read().decode()
        self.assertEqual(body, 'echohello')
        conn.close()

    def test_user_agent(self):
        conn = http.client.HTTPConnection('localhost', 4221)
        conn.request('GET', '/user-agent', headers={'User-Agent': 'James Bond'})
        response = conn.getresponse()
        body = response.read().decode('utf-8')
        self.assertEqual(body, ' James Bond')