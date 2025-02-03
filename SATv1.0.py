import os
import sys
import logging
import socket
import threading
import ssl
import pyfiglet
import struct
from cryptography.fernet import Fernet
from colorama import Fore, Style

# Configure Logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def displayTitle():
    os.system("clear" if os.name == "posix" else "cls")
    title = pyfiglet.figlet_format("Security Automation Tool")
    print(Fore.CYAN + title + Style.RESET_ALL)
    print(Fore.YELLOW + "Version 1.0" + Style.RESET_ALL)
    print(Fore.MAGENTA + "Author: SA0-XDZ03 / Beyond Beacon\n" + Style.RESET_ALL)

def mainMenu():
    """Main menu for user to select a category."""
    while True:
        displayTitle()
        print(Fore.GREEN + "[1] Defensive Security" + Style.RESET_ALL)
        print(Fore.RED + "[2] Offensive Security" + Style.RESET_ALL)
        print(Fore.BLUE + "[3] Remote Administration & Automation" + Style.RESET_ALL)
        print(Fore.YELLOW + "[4] Exit\n" + Style.RESET_ALL)
        
        try:
            userChoice = input(Fore.CYAN + "Select an option: " + Style.RESET_ALL).strip()
            
            if userChoice == "1":
                defensiveMenu()
            elif userChoice == "2":
                offensiveMenu()
            elif userChoice == "3":
                adminMenu()
            elif userChoice == "4":
                print(Fore.YELLOW + "Exiting..." + Style.RESET_ALL)
                sys.exit(0)
            else:
                print(Fore.RED + "Invalid input! Please select a valid option." + Style.RESET_ALL)
        except KeyboardInterrupt:
            print(Fore.RED + "\nUser terminated program." + Style.RESET_ALL)
            sys.exit(0)

def defensiveMenu():
    """Menu for defensive security options."""
    while True:
        displayTitle()
        print(Fore.GREEN + "[1] Real-Time Secure Chat" + Style.RESET_ALL)
        print(Fore.GREEN + "[2] Intrusion Detection Sensor" + Style.RESET_ALL)
        print(Fore.GREEN + "[3] Automated Security Alerting" + Style.RESET_ALL)
        print(Fore.GREEN + "[4] File Integrity Monitoring" + Style.RESET_ALL)
        print(Fore.GREEN + "[5] Secure Encrypted File Transfer" + Style.RESET_ALL)
        print(Fore.GREEN + "[6] Honeypot Deployment" + Style.RESET_ALL)
        print(Fore.YELLOW + "[7] Back\n" + Style.RESET_ALL)
        
        userChoice = input(Fore.CYAN + "Select an option: " + Style.RESET_ALL).strip()
        
        if userChoice == "1":
            secureChat()
        elif userChoice == "7":
            return
        else:
            print(Fore.RED + "Invalid input! Please select a valid option." + Style.RESET_ALL)


def getLocalIPAddress():
    """Automatically gets the machine's local IP address"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))  # Google DNS to detect local IP dynamically
            return s.getsockname()[0]
    except Exception as e:
        logger.error(f"[ERROR] Could not determine local IP: {e}")
        return "127.0.0.1"

def generateSelfSignedCert():
    """Generate a self-signed SSL certificate if it doesn't exist."""
    if not os.path.exists("server.crt") or not os.path.exists("server.key"):
        logger.info("Generating self-signed SSL certificate...")
        os.system("openssl req -new -x509 -keyout server.key -out server.crt -days 365 -nodes -subj '/CN=localhost'")
        logger.info("SSL Certificate Generated Successfully.")

def icmpListener():
    """Basic ICMP Listener to detect pings from remote machines."""
    print(Fore.YELLOW + "[ICMP] Listening for ICMP Echo Requests..." + Style.RESET_ALL)
    try:
        rawSocket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        rawSocket.bind((getLocalIPAddress(), 0))
    
        while True:
            packet, addr = rawSocket.recvfrom(1024)
            icmpType, icmpCode, checksum, identifier, sequence = struct.unpack('!BBHHH', packet[20:28])
            if icmpType == 8:  # Echo Request (Ping)
                print(Fore.CYAN + f"[ICMP] Ping received from {addr[0]}" + Style.RESET_ALL)
    except PermissionError:
        print(Fore.RED + "[ICMP] Permission Denied! Run as root/admin to capture ICMP packets." + Style.RESET_ALL)
    except Exception as e:
        logger.error(f"[ICMP] Error: {e}")

def secureChat():
    """TLS Encrypted Multi-Client Secure Chat"""
    print(Fore.GREEN + "Initializing Secure Chat..." + Style.RESET_ALL)
    key = Fernet.generate_key()
    cipher = Fernet(key)
    print(Fore.CYAN + "[INFO] Encryption Key Generated" + Style.RESET_ALL)
    
    generateSelfSignedCert()
    
    def chatServer():
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(certfile="server.crt", keyfile="server.key")

        serverIPChoice = input("Use [1] Localhost (127.0.0.1) or [2] LAN IP? ").strip()
        serverIP = "127.0.0.1" if serverIPChoice == "1" else getLocalIPAddress()

        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverSocket.bind((serverIP, 9090))
        serverSocket.listen(5)
        print(Fore.YELLOW + f"[SERVER] Listening on {serverIP}:9090..." + Style.RESET_ALL)
        
        while True:
            try:
                clientSocket, addr = serverSocket.accept()
                secureSocket = context.wrap_socket(clientSocket, server_side=True)
                print(Fore.GREEN + f"[SERVER] Secure Connection established with {addr}" + Style.RESET_ALL)
                
                def handleClient(client):
                    while True:
                        try:
                            encryptedMessage = client.recv(10000)
                            if not encryptedMessage:
                                break
                            decryptedMessage = cipher.decrypt(encryptedMessage).decode()
                            print(Fore.CYAN + f"[Client]: {decryptedMessage}" + Style.RESET_ALL)
                        except Exception as e:
                            logger.error(f"Error in chat: {e}")
                            break
                
                threading.Thread(target=handleClient, args=(secureSocket,)).start()
            except Exception as e:
                logger.error(f"[SERVER] Error accepting connection: {e}")
    
    def chatClient():
        serverIP = input(Fore.CYAN + "Enter Server IP: " + Style.RESET_ALL).strip()

        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        secureSocket = context.wrap_socket(clientSocket, server_hostname=serverIP)

        try:
            secureSocket.connect((serverIP, 9090))
            print(Fore.YELLOW + f"[CLIENT] Connected to Secure Server at {serverIP}:9090." + Style.RESET_ALL)
            
            while True:
                message = input(Fore.GREEN + "[You]: " + Style.RESET_ALL)
                encryptedMessage = cipher.encrypt(message.encode())
                secureSocket.send(encryptedMessage)
        
        except Exception as e:
            logger.error(f"[CLIENT] Connection Error: {e}")
            print(Fore.RED + "[CLIENT] Failed to connect to server. Ensure it's running and reachable." + Style.RESET_ALL)
    
    choice = input("Run as [S]erver, [C]lient or [I]CMP Listener? ").strip().lower()
    if choice == "s":
        chatServer()
    elif choice == "c":
        chatClient()
    elif choice == "i":
        icmpListener()
    else:
        print(Fore.RED + "Invalid input!" + Style.RESET_ALL)
        return

def offensiveMenu():
    """Menu for offensive security options."""
    print(Fore.RED + "Offensive Security Module (To Be Developed)." + Style.RESET_ALL)
    input(Fore.CYAN + "Press Enter to return..." + Style.RESET_ALL)

def adminMenu():
    """Menu for administration & automation options."""
    print(Fore.BLUE + "Remote Administration & Automation Module (To Be Developed)." + Style.RESET_ALL)
    input(Fore.CYAN + "Press Enter to return..." + Style.RESET_ALL)

if __name__ == "__main__":
    mainMenu()
