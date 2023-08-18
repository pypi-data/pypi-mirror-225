#
#    socksimap : Connect to IMAP through Socks
#    Copyright (c) 2023 Vitaly (Optinsoft)
#
#    Permission is hereby granted, free of charge, to any person obtaining a copy
#    of this software and associated documentation files (the "Software"), to deal
#    in the Software without restriction, including without limitation the rights
#    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#    copies of the Software, and to permit persons to whom the Software is
#    furnished to do so, subject to the following conditions:
#
#    The above copyright notice and this permission notice shall be included in all
#    copies or substantial portions of the Software.
#
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#    SOFTWARE.

from imaplib import IMAP4, IMAP4_PORT, IMAP4_SSL_PORT
from socks import create_connection, PROXY_TYPE_SOCKS4, PROXY_TYPE_SOCKS5
import ssl

__version__ = "1.0.1"

class SocksIMAP4(IMAP4):

    SOCKS_PROXY_TYPES = {"socks4": PROXY_TYPE_SOCKS4, "socks5": PROXY_TYPE_SOCKS5}

    def __init__(self, host='', port=IMAP4_PORT, timeout=None, proxy_addr=None, proxy_port=None,
                 rdns=True, username=None, password=None, proxy_type=None):

        self.proxy_addr = proxy_addr
        self.proxy_port = proxy_port
        self.rdns = rdns
        self.username = username
        self.password = password
        self.proxy_type = SocksIMAP4.SOCKS_PROXY_TYPES[proxy_type.lower()] if not proxy_type is None else None

        IMAP4.__init__(self, host, port, timeout)

    def _create_socket(self, timeout):
        if self.proxy_type is None:
            return IMAP4._create_socket(self, timeout)
        else:
            return create_connection((self.host, self.port), timeout, proxy_type=self.proxy_type, proxy_addr=self.proxy_addr,
                                    proxy_port=self.proxy_port, proxy_rdns=self.rdns, proxy_username=self.username,
                                    proxy_password=self.password)

class SocksIMAP4_SSL(SocksIMAP4):

    def __init__(self,
                host: str = "",
                port: int = IMAP4_SSL_PORT,
                keyfile: str | None = None,
                certfile: str | None = None,
                ssl_context: ssl.SSLContext | None = None,
                timeout: float | None = None,                 
                proxy_addr=None, 
                proxy_port=None,
                rdns=True, 
                username=None, 
                password=None, 
                proxy_type=None):

        if ssl_context is not None and keyfile is not None:
                raise ValueError("ssl_context and keyfile arguments are mutually "
                                 "exclusive")
        if ssl_context is not None and certfile is not None:
            raise ValueError("ssl_context and certfile arguments are mutually "
                             "exclusive")

        self.keyfile = keyfile
        self.certfile = certfile
        if ssl_context is None:
            ssl_context = ssl._create_stdlib_context(certfile=certfile,
                                                     keyfile=keyfile)
        self.ssl_context = ssl_context

        SocksIMAP4.__init__(self, host, port, timeout, proxy_addr, proxy_port, rdns, username, password, proxy_type)

    def _create_socket(self, timeout):
        sock = SocksIMAP4._create_socket(self, timeout)
        server_hostname = self.host if ssl.HAS_SNI else None
        return self.ssl_context.wrap_socket(sock, 
                                            server_hostname=server_hostname)

    def open(self, host='', port=IMAP4_PORT, timeout=None):
        SocksIMAP4.open(self, host, port, timeout)
