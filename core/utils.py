#!/usr/bin/env python3
"""
Utility Functions
Helper functions for the system
"""

import os
import sys
import time
from urllib.parse import urlparse

def validate_url(url):
    """Validate URL format"""
    try:
        result = urlparse(url)
        return all([result.scheme in ['http', 'https'], result.netloc])
    except:
        return False

def get_hidden_input(prompt):
    """Get hidden input for passwords"""
    try:
        import getpass
        return getpass.getpass(prompt)
    except:
        # Fallback for environments without getpass
        print(prompt, end='', flush=True)
        
        if os.name == 'nt':  # Windows
            import msvcrt
            password = []
            while True:
                ch = msvcrt.getch()
                if ch == b'\r' or ch == b'\n':
                    print()
                    break
                elif ch == b'\x08':  # Backspace
                    if password:
                        password.pop()
                        print('\b \b', end='', flush=True)
                else:
                    password.append(ch.decode('utf-8', errors='ignore'))
                    print('*', end='', flush=True)
            return ''.join(password)
        else:  # Unix/Linux/Mac
            import termios
            import tty
            
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            
            try:
                tty.setraw(fd)
                password = []
                while True:
                    ch = sys.stdin.read(1)
                    if ch == '\n' or ch == '\r':
                        print()
                        break
                    elif ch == '\x7f' or ch == '\b':  # Backspace
                        if password:
                            password.pop()
                            print('\b \b', end='', flush=True)
                    elif ch == '\x03':  # Ctrl+C
                        raise KeyboardInterrupt
                    else:
                        password.append(ch)
                        print('*', end='', flush=True)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            
            return ''.join(password)

def print_banner():
    """Print system banner"""
    from colorama import Fore, Style
    
    print(f"""{Fore.RED}

    ██╗███╗░░██╗██████╗░░█████╗░
    ██║████╗░██║██╔══██╗██╔══██╗
    ██║██╔██╗██║██║░░██║██║░░██║
    ██║██║╚████║██║░░██║██║░░██║
    ██║██║░╚███║██████╔╝╚█████╔╝
    ╚═╝╚═╝░░╚══╝╚═════╝░░╚════╝░

    ═════════ SERVER DISABLER v2.0 ═════════
{Style.RESET_ALL}""")

def create_directories():
    """Create necessary directories"""
    directories = ['data', 'logs', 'core']
    
    for dir_name in directories:
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
    
    # Create data files if they don't exist
    if not os.path.exists('data/useragents.txt'):
        default_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1'
        ]
        
        with open('data/useragents.txt', 'w') as f:
            for agent in default_agents:
                f.write(f"{agent}\n")
    
    if not os.path.exists('data/config.json'):
        default_config = {
            "max_threads": 99999,
            "request_timeout": 5,
            "proxy_timeout": 10,
            "user_agent_rotation": True,
            "auto_update_proxies": True
        }
        
        import json
        with open('data/config.json', 'w') as f:
            json.dump(default_config, f, indent=2)

def get_timestamp():
    """Get formatted timestamp"""
    return time.strftime("%Y-%m-%d %H:%M:%S")

def format_number(num):
    """Format number with commas"""
    return f"{num:,}"

def log_message(message, level="INFO"):
    """Log message to file"""
    timestamp = get_timestamp()
    log_entry = f"[{timestamp}] [{level}] {message}"
    
    try:
        with open('logs/system.log', 'a') as f:
            f.write(f"{log_entry}\n")
    except:
        pass
    
    # Also print to console
    from colorama import Fore
    colors = {
        'INFO': Fore.CYAN,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'SUCCESS': Fore.GREEN
    }
    
    color = colors.get(level, Fore.WHITE)
    print(f"{color}{log_entry}")
