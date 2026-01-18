import socket
import threading
import sys
import time

HOST = "irc.libera.chat"
PORT = 6667
NICK = "Subhro_123"
USER = "subhro 0 * :CS student learning stuffs"
CHANNEL = "#test-channel-123"

CLR_RESET = "\033[0m"
CLR_NICK = "\033[94m"   
CLR_MSG = "\033[92m"    
CLR_SYS = "\033[93m"    
CLR_ERR = "\033[91m" 

class IRC_client:
    def __init__(self,host,port,nick,user,channel):
        self.host = host
        self.port = port
        self.nick = nick
        self.user = user
        self.channel = channel
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.running = True
    
    def get_timestamp(self):
        return time.strftime("[%H:%M:%S]", time.localtime())
        
    def send(self,msg):
        self.sock.send(f"{msg}/r/n".encode("utf-8"))
    
    def connect(self):
        try:
            print(f"{CLR_SYS}Connecting to {self.host}:{self.port}...{CLR_RESET}")
            self.sock.connect((self.host, self.port))
            
            
            self.send(f"NICK {self.nick}")
            self.send(f"USER {self.user}")
            
            threading.Thread(target=self.receive_loop, daemon=True).start()
            
            self.send(f"JOIN {self.channel}")
        
        except Exception as error:
            print(f"{CLR_ERR}Connection error: {error}{CLR_RESET}")
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
        print(f"{CLR_ERR}Disconnected from server.{CLR_RESET}")
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
            print(f"{self.get_timestamp()} {CLR_NICK}<{sender}>{CLR_RESET} : {content}")
        
        elif command == "JOIN":
            print(f"{self.get_timestamp()} {CLR_SYS}*** {sender} joined {self.channel}{CLR_RESET}")

    def run_cli(self):
        print(f"{CLR_SYS}Commands: /join #channel, /quit, or just type to chat.{CLR_RESET}")
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
                        print(f"{CLR_ERR}Unknown command or missing arguments.{CLR_RESET}")
                else:
                    self.send(f"PRIVMSG {self.channel} :{msg}")
                    print(f"{self.get_timestamp()} {CLR_NICK}<{self.nick}>{CLR_RESET} : {msg}")

            except EOFError:
                break

if __name__ == "__main__":
    client = IRC_client(HOST, PORT, NICK, USER, CHANNEL)
    client.connect()
    client.run_cli()