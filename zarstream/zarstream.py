import requests
import codecs
import lxml
from lxml import html
from lxml import etree
import hashlib
from datetime import datetime
import time
from lxml.html.clean import Cleaner
import os
import http.server
import webbrowser
import getpass
import base64


news = ''


class ZarStream():
    class MyHandler(http.server.SimpleHTTPRequestHandler):
        def do_HEAD(self):
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            title = ''
            header = r'<!DOCTYPE html>'+ '\n' + '<html>' + '\n' + '<head>' + '\n' + \
            '<meta http-equiv="content-type" content="text/html; charset=utf-8" />' + \
            '\n' + '<title>' + title + '</title>' + '\n' + '</head>' + '\n'
            timestamp = datetime.now().strftime("%d.%m.%Y")
            msg = header + '<body>' + '<h1>' + title + '\n' + '</h1>' + news + '\n' + \
                    '<hr/>\n' + timestamp + '\n'+ '</body>' + '\n' + '</html>'
            self.wfile.write(msg.encode('utf-8'))
##            self.wfile.close()


    def view(self):
        server = http.server.HTTPServer(('127.0.0.1', 8080), self.MyHandler)
        webbrowser.open('http://127.0.0.1:%s' % server.server_port)
        server.handle_request()


    cleaner = Cleaner(
        scripts=True, javascript=True, comments=True, style=True, links=True,
        meta=True, page_structure=False, processing_instructions=True,
        embedded=True, frames=True, forms=True, annoying_tags=True,
        remove_tags=[], allow_tags=['font','a'], remove_unknown_tags=False,
        safe_attrs_only=True, add_nofollow=True, host_whitelist=[],
        whitelist_tags = [])


    def __init__(self, url, pattern, extra_protection=False):
        if self.scan(url, pattern):
            self.view()


    def scan(self, url, pattern):
        global news
        try:
            session = requests.session()
            session.proxies = {'http':  'socks5://127.0.0.1:9150',
                               'https': 'socks5://127.0.0.1:9150'}
            base_url = base64.b64decode(url).decode('utf-8')
            r = session.get(base_url)
            data = html.fromstring(r.text)
            data.make_links_absolute(base_url, resolve_base_href=True)
            content = data.xpath(pattern)
            print(f'Found {len(content)} records')
            hash_sum_list = ''
            with codecs.open('dump.txt', 'a+', 'utf-8') as f:
                f.seek(0)
                hash_sum_list = f.read().split()
                content_new_counter = 0
                for item in content:
                    hash_sum = hashlib.sha256(etree.tostring(item)).hexdigest()
                    for action, el in etree.iterwalk(item):
                        if el.tag == 'font' and el.xpath('@size'):
                            del el.attrib['size']
                    text = self.cleaner.clean_html(etree.tostring(item)).decode('utf-8')
                    if not hash_sum in hash_sum_list:
                        f.write(f'{hash_sum}{os.linesep}')
                        news += f'{text}</br>'
                        content_new_counter += 1
        except requests.exceptions.RequestException:
            print(f'Connection error. Check TOR service status {session.proxies}')
            return None
        except Exception as e:
            print(f'ERROR: {e}')
        print(f'Added {content_new_counter} records')
        return content_new_counter


if __name__ == "__main__":
    url = b'aHR0cHM6Ly90ZWxlZ3JhbS5vcmcvYmxvZw=='
    pattern = '//div[@class="dev_blog_card_wrap"]'
    zs = ZarStream(url, pattern)
