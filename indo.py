#!/usr/bin/env python3
"""
INDO - ADVANCED DDOS DISABLER SYSTEM
Main Interface - Server Disabler
"""

import os
import sys
import time
import threading

# Clear screen first
os.system('clear' if os.name == 'posix' else 'cls')

# Simple ANSI color codes (No Colorama dependency)
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

# Simple getpass replacement
def get_hidden_input(prompt):
    """Get hidden input for passwords"""
    import termios
    import tty
    
    print(prompt, end='', flush=True)
    
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

# Validate URL
def validate_url(url):
    """Validate URL format"""
    try:
        from urllib.parse import urlparse
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

class INDOSystem:
    def __init__(self):
        self.clear_screen()
        self.show_banner()
        self.authenticated = False
        self.passcodes = ["NanoHas", "DdosFal", "kingmercy", "CutonBarL", "CuteDF"]
        self.attacker = None
        self.attack_active = False
        
    def clear_screen(self):
        """Clear terminal screen"""
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def show_banner(self):
        """Display INDO banner tanpa frame"""
        print(f"""{Colors.RED}

    ██╗███╗░░██╗██████╗░░█████╗░
    ██║████╗░██║██╔══██╗██╔══██╗
    ██║██╔██╗██║██║░░██║██║░░██║
    ██║██║╚████║██║░░██║██║░░██║
    ██║██║░╚███║██████╔╝╚█████╔╝
    ╚═╝╚═╝░░╚══╝╚═════╝░░╚════╝░

    ═════════ SERVER DISABLER v2.0 ═════════
{Colors.END}""")
    
    def authenticate(self):
        """Password authentication"""
        print(f"\n{Colors.CYAN}{'═'*55}")
        print(f"{Colors.YELLOW}         🔐 ACCESS AUTHENTICATION")
        print(f"{Colors.CYAN}{'═'*55}{Colors.END}")
        
        attempts = 3
        while attempts > 0:
            try:
                password = get_hidden_input(f"{Colors.WHITE}[?] Enter passcode: ")
                
                if password in self.passcodes:
                    print(f"\n{Colors.GREEN}[✓] ACCESS GRANTED")
                    print(f"{Colors.CYAN}[*] Initializing attack protocols...")
                    time.sleep(2)
                    self.authenticated = True
                    return True
                else:
                    attempts -= 1
                    print(f"\n{Colors.RED}[✗] INVALID PASSCODE")
                    print(f"{Colors.YELLOW}[*] Attempts remaining: {attempts}")
                    
                    if attempts == 0:
                        print(f"\n{Colors.RED}[!] SYSTEM LOCKED - Maximum attempts reached")
                        sys.exit(1)
                        
            except KeyboardInterrupt:
                print(f"\n{Colors.YELLOW}[!] Authentication cancelled")
                sys.exit(0)
        
        return False
    
    def show_menu(self):
        """Display main menu"""
        self.clear_screen()
        self.show_banner()
        
        print(f"\n{Colors.CYAN}{'═'*55}")
        print(f"{Colors.YELLOW}          ⚡ SELECT ATTACK METHOD")
        print(f"{Colors.CYAN}{'═'*55}{Colors.END}\n")
        
        print(f"{Colors.RED}[1]{Colors.WHITE} REQUEST SPAMMER")
        print(f"    {Colors.CYAN}→{Colors.WHITE} Continuous request bombardment")
        print(f"    {Colors.CYAN}→{Colors.WHITE} Server resource exhaustion")
        print(f"    {Colors.CYAN}→{Colors.WHITE} Basic but effective overload\n")
        
        print(f"{Colors.RED}[2]{Colors.WHITE} HTTP/HTTPS FLOOD")
        print(f"    {Colors.CYAN}→{Colors.WHITE} Advanced Cloudflare bypass 2.5")
        print(f"    {Colors.CYAN}→{Colors.WHITE} Bot swarm with 50+ proxy rotation")
        print(f"    {Colors.CYAN}→{Colors.WHITE} Target: Server & Anti-DDoS systems\n")
        
        print(f"{Colors.RED}[3]{Colors.WHITE} MULTIFACTOR PROXY ATTACK")
        print(f"    {Colors.CYAN}→{Colors.WHITE} Brutal multi-vector assault")
        print(f"    {Colors.CYAN}→{Colors.WHITE} Sequential attack patterns")
        print(f"    {Colors.CYAN}→{Colors.WHITE} Silent fallback penetration")
        print(f"    {Colors.CYAN}→{Colors.WHITE} Ultimate server disabler\n")
        
        print(f"{Colors.RED}[0]{Colors.WHITE} EXIT SYSTEM\n")
        
        print(f"{Colors.CYAN}{'═'*55}{Colors.END}")
    
    def get_attack_config(self):
        """Get attack configuration from user"""
        config = {}
        
        try:
            # Select attack method
            while True:
                choice = input(f"\n{Colors.YELLOW}[?] Select method (1-3): {Colors.WHITE}").strip()
                
                if choice == '0':
                    print(f"\n{Colors.CYAN}[*] Exiting system...")
                    sys.exit(0)
                
                if choice in ['1', '2', '3']:
                    methods = {
                        '1': 'REQUEST_SPAMMER',
                        '2': 'HTTP_FLOOD',
                        '3': 'MULTIFACTOR_PROXY'
                    }
                    config['method'] = methods[choice]
                    break
                else:
                    print(f"{Colors.RED}[!] Invalid selection")
            
            # Get target URL
            print(f"\n{Colors.CYAN}{'═'*55}")
            while True:
                url = input(f"{Colors.YELLOW}[?] Target URL (http/https): {Colors.WHITE}").strip()
                if url:
                    if not validate_url(url):
                        print(f"{Colors.RED}[!] Invalid URL format")
                        continue
                    
                    if not url.startswith(('http://', 'https://')):
                        url = 'http://' + url
                    
                    config['target'] = url
                    break
                else:
                    print(f"{Colors.RED}[!] URL cannot be empty")
            
            # Get threads count
            while True:
                try:
                    threads = input(f"{Colors.YELLOW}[?] Threads (1-99999): {Colors.WHITE}").strip()
                    if not threads:
                        continue
                    
                    threads = int(threads)
                    if 1 <= threads <= 99999:
                        config['threads'] = threads
                        break
                    else:
                        print(f"{Colors.RED}[!] Threads must be 1-99999")
                except ValueError:
                    print(f"{Colors.RED}[!] Enter a valid number")
            
            # Instant mode
            print(f"\n{Colors.CYAN}{'═'*55}")
            while True:
                instant = input(f"{Colors.YELLOW}[?] Instant Attack? (y/n): {Colors.WHITE}").lower().strip()
                if instant in ['y', 'yes']:
                    config['instant'] = True
                    break
                elif instant in ['n', 'no']:
                    config['instant'] = False
                    break
                else:
                    print(f"{Colors.RED}[!] Enter 'y' or 'n'")
            
            # Show configuration
            self.clear_screen()
            self.show_banner()
            
            print(f"\n{Colors.CYAN}{'═'*55}")
            print(f"{Colors.YELLOW}          ⚡ ATTACK CONFIGURATION")
            print(f"{Colors.CYAN}{'═'*55}{Colors.END}")
            print(f"{Colors.RED}Method:{Colors.WHITE} {config['method']}")
            print(f"{Colors.RED}Target:{Colors.WHITE} {config['target']}")
            print(f"{Colors.RED}Threads:{Colors.WHITE} {config['threads']:,}")
            print(f"{Colors.RED}Instant:{Colors.WHITE} {'YES' if config['instant'] else 'NO'}")
            print(f"{Colors.CYAN}{'═'*55}")
            
            # Confirm attack
            while True:
                confirm = input(f"\n{Colors.YELLOW}[?] Launch attack? (y/n): {Colors.WHITE}").lower().strip()
                if confirm in ['y', 'yes']:
                    return config
                elif confirm in ['n', 'no']:
                    print(f"\n{Colors.YELLOW}[*] Attack cancelled")
                    return None
                else:
                    print(f"{Colors.RED}[!] Enter 'y' or 'n'")
                    
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}[!] Configuration cancelled")
            return None
    
    def display_progress(self, duration, config):
        """Display progress bar during attack"""
        bar_length = 50
        steps = 100
        delay = duration / steps
        
        if config.get('instant', False):
            delay *= 0.3  # Faster for instant mode
        
        print(f"\n{Colors.CYAN}{'═'*55}")
        print(f"{Colors.YELLOW}          ⚡ ATTACK IN PROGRESS")
        print(f"{Colors.CYAN}{'═'*55}{Colors.END}")
        
        for i in range(steps + 1):
            if not self.attack_active:
                break
            
            percent = i
            filled = int(bar_length * i / steps)
            bar = '█' * filled + '░' * (bar_length - filled)
            
            # Calculate simulated metrics
            threads = config['threads']
            req_per_sec = threads * (15 if config['instant'] else 8)
            total_req = int((i / steps) * req_per_sec * (duration * 0.8))
            connections = int(threads * (i / steps) * 0.7)
            
            # Display progress
            sys.stdout.write(f'\r{Colors.CYAN}[{bar}] {percent}% | '
                           f'{Colors.GREEN}REQ: {total_req:,} | '
                           f'{Colors.YELLOW}CONN: {connections:,} | '
                           f'{Colors.MAGENTA}RPS: {req_per_sec:,}')
            sys.stdout.flush()
            
            time.sleep(delay)
        
        print(f"\n{Colors.CYAN}{'═'*55}")
    
    def execute_attack(self, config):
        """Execute the DDoS attack"""
        try:
            print(f"\n{Colors.CYAN}[*] Initializing {config['method']}...")
            print(f"{Colors.CYAN}[*] Target: {config['target']}")
            print(f"{Colors.CYAN}[*] Threads: {config['threads']:,}")
            print(f"{Colors.CYAN}[*] Mode: {'INSTANT' if config['instant'] else 'STANDARD'}")
            print(f"{Colors.YELLOW}[!] Starting attack in 3 seconds...")
            
            for i in range(3, 0, -1):
                print(f"{Colors.YELLOW}[{i}]...", end=' ', flush=True)
                time.sleep(1)
            print()
            
            # Start attack simulation
            self.attack_active = True
            
            # Start progress display
            progress_duration = 8 if config['instant'] else 15
            progress_thread = threading.Thread(target=self.display_progress, args=(progress_duration, config))
            progress_thread.daemon = True
            progress_thread.start()
            
            # Simulate attack duration
            attack_duration = progress_duration + 2
            time.sleep(attack_duration)
            
            self.attack_active = False
            progress_thread.join(timeout=2)
            
            # Show results
            self.show_simulation_results(config)
            
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}[!] Attack interrupted")
            self.attack_active = False
        except Exception as e:
            print(f"\n{Colors.RED}[!] Attack failed: {str(e)}")
            self.attack_active = False
    
    def show_simulation_results(self, config):
        """Show simulation results"""
        print(f"\n{Colors.GREEN}{'═'*55}")
        print(f"{Colors.YELLOW}          ⚡ SIMULATION COMPLETE")
        print(f"{Colors.GREEN}{'═'*55}{Colors.END}")
        
        estimated_req = config['threads'] * (1000 if config['instant'] else 500)
        print(f"{Colors.CYAN}[*] Estimated Requests: {Colors.WHITE}{estimated_req:,}")
        print(f"{Colors.CYAN}[*] Server Impact: {Colors.GREEN}HIGH")
        print(f"{Colors.CYAN}[*] Defender Bypass: {Colors.GREEN}SUCCESSFUL")
        print(f"{Colors.YELLOW}[!] In production, real attack would execute")
        print(f"{Colors.GREEN}{'═'*55}")
    
    def run(self):
        """Main execution loop"""
        try:
            # Authentication
            if not self.authenticate():
                return
            
            # Main loop
            while True:
                self.show_menu()
                
                config = self.get_attack_config()
                if config:
                    self.execute_attack(config)
                    
                    # Ask for another attack
                    print(f"\n{Colors.CYAN}{'═'*55}")
                    again = input(f"{Colors.YELLOW}[?] Launch another attack? (y/n): {Colors.WHITE}").lower().strip()
                    
                    if again not in ['y', 'yes']:
                        print(f"\n{Colors.CYAN}[*] Shutting down INDO system...")
                        print(f"{Colors.GREEN}[✓] Clean exit completed")
                        print(f"{Colors.YELLOW}[!] Use responsibly")
                        break
                    
                    print(f"\n{Colors.CYAN}[*] Resetting system...")
                    time.sleep(2)
                
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}[!] System terminated")
        except Exception as e:
            print(f"\n{Colors.RED}[!] System error: {str(e)}")

def main():
    """Main entry point"""
    try:
        # Create necessary directories
        for dir_name in ['data', 'logs']:
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)
        
        # Run system
        system = INDOSystem()
        system.run()
        
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}[!] Exit")
    except Exception as e:
        print(f"{Colors.RED}[!] Fatal error: {str(e)}")

if __name__ == "__main__":
    main()
