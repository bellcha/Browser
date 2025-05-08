import socket
import sys

class URL:
    def __init__(self, url):
        self.url = url
        try:
            assert self.scheme in ["http", "https"]
        except AssertionError:
            print("http or https is required")
    
    @property
    def scheme(self):
        return self.url.split("://",1)[0]
    
    @property
    def host(self):
        parsed_url = self.url.split("://",1)[1]
        hostname = parsed_url.split("/",1)[0]
        return hostname

    @property
    def path(self):
        parsed_url = self.url.split("://",1)[1]
        path = parsed_url.split("/",1)[1]
        return f"/{path}"
    
    @property
    def request_data(self):
        return f"GET {self.path} HTTP/1.0\r\nHost: {self.host}\r\n\r\n"
    

    def make_request(self):
        s = socket.socket(
            family=socket.AF_INET,
            type=socket.SOCK_STREAM,
            proto=socket.IPPROTO_TCP
        )
        s.connect((self.host, 80))
        s.send(self.request_data.encode("utf8"))
        response = s.makefile("r", encoding="utf8", newline="\r\n")
        return response.read()


def main():

    cli_args = sys.argv

    if len(cli_args) < 2:
        print("Please enter a website as a commandline arg.")

    else:

        url = URL(cli_args[1])

        print(url.make_request())

if __name__ == "__main__":
    main()