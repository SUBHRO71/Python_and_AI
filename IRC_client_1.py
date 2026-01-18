import socket
import threading
import sys

HOST = "irc.libera.chat"
PORT = 6667
NICK = "Subhro_123"
USER = "subhro 0 * :CS student learning stuffs"
CHANNEL = "#test-channel-123"

class IRC_client:
    def __init__(self,host,port,nick,user,channel):
        self.host = host
        self.port = port
        self.nick = nick
        self.user = user
        self.channel = channel
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.running = True
        
    def send(self,msg):
        self.sock.send(f"{msg}/r/n".encode("utf-8"))
    
    def connect(self):
        try:
            print(f"Connecting to {self.host}:{self.port}...")
            self.sock.connect((self.host, self.port))
            
            
            self.send(f"NICK {self.nick}")
            self.send(f"USER {self.user}")
            
            threading.Thread(target=self.receive_loop, daemon=True).start()
            
            self.send(f"JOIN {self.channel}")
        
        except Exception as error:
            print(f"Connection error: {error}")
            sys.exit(1)
    
    
    def receive_loop(self):
        buffer = ""
        while self.running:
            try:
                data = self.sock.recv(4096).decode("utf-8", errors="ignore")
                if not data:
                    break
                
                buffer += data
                while "\r\n" in buffer:
                    line, buffer = buffer.split("\r\n", 1)
                    self.parse_line(line)
            except Exception:
                break
        print(f"Disconnected from server.")
        self.running = False
        

    def parse_line(self, line):
        if line.startswith("PING"):
            payload = line.split()[1]
            self.send(f"PONG {payload}")
            return

        parts = line.split()
        if len(parts) < 2: return
        
        if parts[0].startswith(":"):
            sender = parts[0][1:].split("!")[0]  
        else:
            sender = "Server"
            
        command = parts[1]

        if command == "PRIVMSG":
            target = parts[2]
            content = line.split(" :", 1)[1] if " :" in line else ""
            print(f"<{sender}> : {content}")
        
        elif command == "JOIN":
            print(f"*** {sender} joined {self.channel}")

    def run_cli(self):
        print(f"Commands: /join #channel, /quit, or just type to chat.")
        while self.running:
            try:
                msg = input()
                if not msg: continue

                if msg.startswith("/"):
                    cmd_parts = msg.split()
                    cmd = cmd_parts[0].lower()
                    
                    if cmd == "/quit":
                        self.send("QUIT :Later!")
                        self.running = False
                    elif cmd == "/join" and len(cmd_parts) > 1:
                        new_channel = cmd_parts[1]
                        self.send(f"PART {self.channel}")
                        self.channel = new_channel
                        self.send(f"JOIN {self.channel}")
                    else:
                        print(f"Unknown command or missing arguments.")
                else:
                    self.send(f"PRIVMSG {self.channel} :{msg}")
                    print(f"<{self.nick}> : {msg}")

            except EOFError:
                break

if __name__ == "__main__":
    client = IRC_client(HOST, PORT, NICK, USER, CHANNEL)
    client.connect()
    client.run_cli()