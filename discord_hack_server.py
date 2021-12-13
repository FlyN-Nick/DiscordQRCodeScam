from http.server import BaseHTTPRequestHandler, HTTPServer
import base64

hostName = "localhost"
serverPort = 8080

class DiscordHackServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "image/png")
        self.end_headers()
        with open("discord_login.png", "rb") as login_img:
            img_bytes = login_img.read()
            #img_b64 = str(base64.encodebytes(login_img.read()))[2:-3] # convert image bytes to b64 and remove b' from beginning and \n' from end
            #print(img_b64)
        """
        img_tag = f'<img src="data:image/png;base64,{img_b64}" />'
        print(img_tag)
        self.wfile.write(bytes(f"<html><head><title>Gifted Discord Nitro</title></head>", "utf-8"))
        self.wfile.write(bytes(f'<body>{img_tag}', 'utf-8'))
        self.wfile.write(bytes("</body></html>", "utf-8"))"""
        self.wfile.write(img_bytes)

def main():
    webServer = HTTPServer((hostName, serverPort), DiscordHackServer)
    print("Discord hack server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Discord hack server stopped.")

if __name__ == "__main__":        
    main()