#!/usr/bin/env python3
"""
Check-Host Ping & HTTP Tester

A Python utility to check host availability and response times using the Check-Host API.
Features:
- Ping and HTTP checks
- Node selection by continent
- Interactive and command-line modes
- Colored output with failure highlighting
- Average response time calculations by continent
- JSON and text output formats
"""

import argparse
import json
import time
import requests
import sys
import os
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple, Set
from collections import defaultdict
import ipaddress
import colorama
from colorama import Fore, Style, Back

# Initialize colorama for cross-platform colored terminal output
colorama.init(autoreset=True)

# Node data organized by continent
NODES_BY_CONTINENT = {
    "EU": [
        "bg1.node.check-host.net", "ch1.node.check-host.net", "cz1.node.check-host.net",
        "de1.node.check-host.net", "de4.node.check-host.net", "es1.node.check-host.net",
        "fi1.node.check-host.net", "fr1.node.check-host.net", "fr2.node.check-host.net",
        "hu1.node.check-host.net", "it2.node.check-host.net", "lt1.node.check-host.net",
        "md1.node.check-host.net", "nl1.node.check-host.net", "nl2.node.check-host.net",
        "pl1.node.check-host.net", "pl2.node.check-host.net", "pt1.node.check-host.net",
        "rs1.node.check-host.net", "se1.node.check-host.net", "uk1.node.check-host.net"
    ],
    "AS": [
        "hk1.node.check-host.net", "il1.node.check-host.net", "il2.node.check-host.net",
        "in1.node.check-host.net", "in2.node.check-host.net", "ir1.node.check-host.net",
        "ir3.node.check-host.net", "ir5.node.check-host.net", "ir6.node.check-host.net",
        "jp1.node.check-host.net", "kz1.node.check-host.net", "tr1.node.check-host.net",
        "tr2.node.check-host.net", "vn1.node.check-host.net"
    ],
    "NA": [
        "us1.node.check-host.net", "us2.node.check-host.net", "us3.node.check-host.net"
    ],
    "SA": [
        "br1.node.check-host.net"
    ],
    "EU-EAST": [
        "ru1.node.check-host.net", "ru2.node.check-host.net", "ru3.node.check-host.net",
        "ru4.node.check-host.net", "ua1.node.check-host.net", "ua2.node.check-host.net",
        "ua3.node.check-host.net"
    ]
}

# All nodes combined
ALL_NODES = []
for nodes in NODES_BY_CONTINENT.values():
    ALL_NODES.extend(nodes)

# Node details mapping
NODE_DETAILS = {
    "bg1.node.check-host.net": {"country": "Bulgaria", "city": "Sofia", "continent": "EU"},
    "br1.node.check-host.net": {"country": "Brazil", "city": "Sao Paulo", "continent": "SA"},
    "ch1.node.check-host.net": {"country": "Switzerland", "city": "Zurich", "continent": "EU"},
    "cz1.node.check-host.net": {"country": "Czechia", "city": "C.Budejovice", "continent": "EU"},
    "de1.node.check-host.net": {"country": "Germany", "city": "Nuremberg", "continent": "EU"},
    "de4.node.check-host.net": {"country": "Germany", "city": "Frankfurt", "continent": "EU"},
    "es1.node.check-host.net": {"country": "Spain", "city": "Barcelona", "continent": "EU"},
    "fi1.node.check-host.net": {"country": "Finland", "city": "Helsinki", "continent": "EU"},
    "fr1.node.check-host.net": {"country": "France", "city": "Roubaix", "continent": "EU"},
    "fr2.node.check-host.net": {"country": "France", "city": "Paris", "continent": "EU"},
    "hk1.node.check-host.net": {"country": "Hong Kong", "city": "Hong Kong", "continent": "AS"},
    "hu1.node.check-host.net": {"country": "Hungary", "city": "Nyiregyhaza", "continent": "EU"},
    "id2.node.check-host.net": {"country": "Indonesia", "city": "Jakarta", "continent": "AS"},
    "il1.node.check-host.net": {"country": "Israel", "city": "Tel Aviv", "continent": "AS"},
    "il2.node.check-host.net": {"country": "Israel", "city": "Netanya", "continent": "AS"},
    "in1.node.check-host.net": {"country": "India", "city": "Mumbai", "continent": "AS"},
    "in2.node.check-host.net": {"country": "India", "city": "Chennai", "continent": "AS"},
    "ir1.node.check-host.net": {"country": "Iran", "city": "Tehran", "continent": "AS"},
    "ir3.node.check-host.net": {"country": "Iran", "city": "Mashhad", "continent": "AS"},
    "ir5.node.check-host.net": {"country": "Iran", "city": "Esfahan", "continent": "AS"},
    "ir6.node.check-host.net": {"country": "Iran", "city": "Karaj", "continent": "AS"},
    "it2.node.check-host.net": {"country": "Italy", "city": "Milan", "continent": "EU"},
    "jp1.node.check-host.net": {"country": "Japan", "city": "Tokyo", "continent": "AS"},
    "kz1.node.check-host.net": {"country": "Kazakhstan", "city": "Karaganda", "continent": "AS"},
    "lt1.node.check-host.net": {"country": "Lithuania", "city": "Vilnius", "continent": "EU"},
    "md1.node.check-host.net": {"country": "Moldova", "city": "Chisinau", "continent": "EU"},
    "nl1.node.check-host.net": {"country": "Netherlands", "city": "Amsterdam", "continent": "EU"},
    "nl2.node.check-host.net": {"country": "Netherlands", "city": "Meppel", "continent": "EU"},
    "pl1.node.check-host.net": {"country": "Poland", "city": "Poznan", "continent": "EU"},
    "pl2.node.check-host.net": {"country": "Poland", "city": "Warsaw", "continent": "EU"},
    "pt1.node.check-host.net": {"country": "Portugal", "city": "Viana", "continent": "EU"},
    "rs1.node.check-host.net": {"country": "Serbia", "city": "Belgrade", "continent": "EU"},
    "ru1.node.check-host.net": {"country": "Russia", "city": "Moscow", "continent": "EU-EAST"},
    "ru2.node.check-host.net": {"country": "Russia", "city": "Moscow", "continent": "EU-EAST"},
    "ru3.node.check-host.net": {"country": "Russia", "city": "Saint Petersburg", "continent": "EU-EAST"},
    "ru4.node.check-host.net": {"country": "Russia", "city": "Ekaterinburg", "continent": "EU-EAST"},
    "se1.node.check-host.net": {"country": "Sweden", "city": "Tallberg", "continent": "EU"},
    "tr1.node.check-host.net": {"country": "Turkey", "city": "Istanbul", "continent": "AS"},
    "tr2.node.check-host.net": {"country": "Turkey", "city": "Gebze", "continent": "AS"},
    "ua1.node.check-host.net": {"country": "Ukraine", "city": "Khmelnytskyi", "continent": "EU-EAST"},
    "ua2.node.check-host.net": {"country": "Ukraine", "city": "Kyiv", "continent": "EU-EAST"},
    "ua3.node.check-host.net": {"country": "Ukraine", "city": "SpaceX Starlink", "continent": "EU-EAST"},
    "uk1.node.check-host.net": {"country": "UK", "city": "Coventry", "continent": "EU"},
    "us1.node.check-host.net": {"country": "USA", "city": "Los Angeles", "continent": "NA"},
    "us2.node.check-host.net": {"country": "USA", "city": "Dallas", "continent": "NA"},
    "us3.node.check-host.net": {"country": "USA", "city": "Atlanta", "continent": "NA"},
    "vn1.node.check-host.net": {"country": "Vietnam", "city": "Ho Chi Minh City", "continent": "AS"}
}

class CheckHostAPI:
    """Client for the Check-Host API, focused on ping and HTTP checks."""
    
    BASE_URL = "https://check-host.net"
    
    def __init__(self):
        """Initialize the API client with proper headers."""
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json"})
    
    def run_check(self, check_type: str, host: str, nodes: List[str]) -> Dict[str, Any]:
        """
        Run a check against a host using specified nodes.
        
        Args:
            check_type: Either 'ping' or 'http'
            host: The host to check (domain or IP)
            nodes: List of node identifiers to use for the check
            
        Returns:
            API response containing request_id and nodes information
        """
        if check_type not in ["ping", "http"]:
            raise ValueError(f"Check type must be either 'ping' or 'http'")
        
        url = f"{self.BASE_URL}/check-{check_type}"
        params = {"host": host}
        
        # Add each node as a separate parameter
        if nodes:
            params["node"] = nodes
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"{Fore.RED}Error making API request: {e}")
            sys.exit(1)
    
    def get_check_result(self, request_id: str, timeout: int = 30) -> Dict[str, Any]:
        """
        Get the results of a check, polling until complete or timeout.
        
        Args:
            request_id: The request ID returned from run_check
            timeout: Maximum time to wait for results in seconds
            
        Returns:
            Check results
        """
        url = f"{self.BASE_URL}/check-result/{request_id}"
        
        # Poll until results are available or timeout
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                response = self.session.get(url)
                response.raise_for_status()
                result = response.json()
                
                # Check if all results are available (not None)
                if not any(v is None for v in result.values()):
                    return result
                    
                # Wait before trying again
                time.sleep(2)
            except requests.exceptions.RequestException as e:
                print(f"{Fore.RED}Error getting results: {e}")
                return {}
        
        print(f"{Fore.YELLOW}Warning: Some nodes did not respond within the timeout period.")
        return result  # Return partial results if timeout


def validate_host(host: str) -> str:
    """
    Validate and format the host input.
    
    Args:
        host: Host to validate (domain or IP)
        
    Returns:
        Properly formatted host string
    """
    # Check if it's an IP address
    try:
        ipaddress.ip_address(host)
        return host  # Valid IP address
    except ValueError:
        pass
    
    # Check if it's an HTTP URL
    if host.startswith(('http://', 'https://')):
        return host
    
    # If it's a domain without protocol, add http:// for HTTP checks
    if '.' in host and not host.startswith(('http://', 'https://')):
        return host  # For ping we don't need protocol
        
    raise ValueError(f"Invalid host format: {host}")


def get_nodes_selection(continent: Optional[str] = None) -> List[str]:
    """
    Get nodes based on continent selection.
    
    Args:
        continent: Continent code or None for all nodes
        
    Returns:
        List of node identifiers
    """
    if not continent:
        return ALL_NODES
    
    continent = continent.upper()
    if continent == "ALL":
        return ALL_NODES
    
    if continent in NODES_BY_CONTINENT:
        return NODES_BY_CONTINENT[continent]
    
    # Special case for combined continents
    if continent == "EU+NA":
        return NODES_BY_CONTINENT["EU"] + NODES_BY_CONTINENT["NA"]
    
    print(f"{Fore.YELLOW}Warning: Unknown continent '{continent}'. Using all nodes.")
    return ALL_NODES


def calculate_ping_stats(ping_results: List[List]) -> Tuple[int, int, float, float, float]:
    """
    Calculate ping statistics from results.
    
    Args:
        ping_results: List of ping results
        
    Returns:
        Tuple of (successful_pings, total_pings, min_rtt, avg_rtt, max_rtt)
    """
    successful = 0
    total = 0
    rtts = []
    
    for result in ping_results:
        total += 1
        if result[0] == "OK":
            successful += 1
            rtts.append(result[1] * 1000)  # Convert to ms
    
    if not rtts:
        return successful, total, 0, 0, 0
    
    min_rtt = min(rtts) if rtts else 0
    max_rtt = max(rtts) if rtts else 0
    avg_rtt = sum(rtts) / len(rtts) if rtts else 0
    
    return successful, total, min_rtt, avg_rtt, max_rtt


def parse_ping_results(results: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and organize ping results by continent.
    
    Args:
        results: Raw ping results from API
        
    Returns:
        Structured results with statistics
    """
    parsed_results = {
        "nodes_results": [],
        "continent_stats": defaultdict(lambda: {"successful": 0, "total": 0, "rtts": []}),
        "overall_stats": {"successful": 0, "total": 0, "rtts": []}
    }
    
    for node, data in results.items():
        if data is None or not data[0] or data[0][0] is None:
            continue
            
        node_detail = NODE_DETAILS.get(node, {"country": "Unknown", "city": "Unknown", "continent": "Unknown"})
        continent = node_detail["continent"]
        ping_data = data[0]
        
        # Calculate ping statistics
        successful, total, min_rtt, avg_rtt, max_rtt = calculate_ping_stats(ping_data)
        
        # Add to node results
        parsed_results["nodes_results"].append({
            "node": node,
            "country": node_detail["country"],
            "city": node_detail["city"],
            "continent": continent,
            "successful": successful,
            "total": total,
            "min_rtt": min_rtt,
            "avg_rtt": avg_rtt,
            "max_rtt": max_rtt,
            "ip": ping_data[0][2] if successful > 0 and len(ping_data[0]) > 2 else "N/A"
        })
        
        # Add to continent stats
        if successful > 0:
            parsed_results["continent_stats"][continent]["successful"] += successful
            parsed_results["continent_stats"][continent]["total"] += total
            parsed_results["continent_stats"][continent]["rtts"].extend([r[1] * 1000 for r in ping_data if r[0] == "OK"])
        else:
            parsed_results["continent_stats"][continent]["total"] += total
            
        # Add to overall stats
        parsed_results["overall_stats"]["successful"] += successful
        parsed_results["overall_stats"]["total"] += total
        if successful > 0:
            parsed_results["overall_stats"]["rtts"].extend([r[1] * 1000 for r in ping_data if r[0] == "OK"])
    
    # Calculate averages for continents
    for continent, stats in parsed_results["continent_stats"].items():
        if stats["rtts"]:
            stats["avg_rtt"] = sum(stats["rtts"]) / len(stats["rtts"])
            stats["min_rtt"] = min(stats["rtts"])
            stats["max_rtt"] = max(stats["rtts"])
        else:
            stats["avg_rtt"] = 0
            stats["min_rtt"] = 0
            stats["max_rtt"] = 0
    
    # Calculate overall average
    if parsed_results["overall_stats"]["rtts"]:
        rtts = parsed_results["overall_stats"]["rtts"]
        parsed_results["overall_stats"]["avg_rtt"] = sum(rtts) / len(rtts)
        parsed_results["overall_stats"]["min_rtt"] = min(rtts)
        parsed_results["overall_stats"]["max_rtt"] = max(rtts)
    else:
        parsed_results["overall_stats"]["avg_rtt"] = 0
        parsed_results["overall_stats"]["min_rtt"] = 0
        parsed_results["overall_stats"]["max_rtt"] = 0
    
    return parsed_results


def parse_http_results(results: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and organize HTTP results by continent.
    
    Args:
        results: Raw HTTP results from API
        
    Returns:
        Structured results with statistics
    """
    parsed_results = {
        "nodes_results": [],
        "continent_stats": defaultdict(lambda: {"successful": 0, "total": 0, "response_times": []}),
        "overall_stats": {"successful": 0, "total": 0, "response_times": []}
    }
    
    for node, data in results.items():
        if data is None or not data[0]:
            continue
            
        node_detail = NODE_DETAILS.get(node, {"country": "Unknown", "city": "Unknown", "continent": "Unknown"})
        continent = node_detail["continent"]
        
        http_data = data[0]
        success = http_data[0] == 1
        response_time = http_data[1] * 1000  # Convert to ms
        status_msg = http_data[2]
        status_code = http_data[3] if len(http_data) > 3 else "N/A"
        ip = http_data[4] if len(http_data) > 4 else "N/A"
        
        # Add to node results
        parsed_results["nodes_results"].append({
            "node": node,
            "country": node_detail["country"],
            "city": node_detail["city"],
            "continent": continent,
            "success": success,
            "response_time": response_time,
            "status_msg": status_msg,
            "status_code": status_code,
            "ip": ip
        })
        
        # Add to continent stats
        parsed_results["continent_stats"][continent]["total"] += 1
        if success:
            parsed_results["continent_stats"][continent]["successful"] += 1
            parsed_results["continent_stats"][continent]["response_times"].append(response_time)
            
        # Add to overall stats
        parsed_results["overall_stats"]["total"] += 1
        if success:
            parsed_results["overall_stats"]["successful"] += 1
            parsed_results["overall_stats"]["response_times"].append(response_time)
    
    # Calculate averages for continents
    for continent, stats in parsed_results["continent_stats"].items():
        if stats["response_times"]:
            stats["avg_response_time"] = sum(stats["response_times"]) / len(stats["response_times"])
        else:
            stats["avg_response_time"] = 0
    
    # Calculate overall average
    if parsed_results["overall_stats"]["response_times"]:
        times = parsed_results["overall_stats"]["response_times"]
        parsed_results["overall_stats"]["avg_response_time"] = sum(times) / len(times)
    else:
        parsed_results["overall_stats"]["avg_response_time"] = 0
    
    return parsed_results


def display_ping_results(parsed_results: Dict[str, Any]) -> None:
    """
    Display ping results in a formatted table.
    
    Args:
        parsed_results: Parsed ping results
    """
    print("\n" + "=" * 80)
    print(f"{Fore.CYAN}PING RESULTS SUMMARY{Style.RESET_ALL}")
    print("=" * 80)
    
    # Overall statistics
    overall = parsed_results["overall_stats"]
    success_ratio = f"{overall['successful']}/{overall['total']}"
    success_color = Fore.GREEN if overall['successful'] == overall['total'] else Fore.RED
    
    print(f"\n{Fore.YELLOW}Overall Statistics:{Style.RESET_ALL}")
    print(f"  Success Rate: {success_color}{success_ratio}{Style.RESET_ALL}")
    if overall['successful'] > 0:
        print(f"  Average RTT: {overall['avg_rtt']:.1f} ms")
        print(f"  Min/Max RTT: {overall['min_rtt']:.1f} ms / {overall['max_rtt']:.1f} ms")
    
    # Continent statistics
    print(f"\n{Fore.YELLOW}Statistics by Continent:{Style.RESET_ALL}")
    for continent, stats in parsed_results["continent_stats"].items():
        success_ratio = f"{stats['successful']}/{stats['total']}"
        success_color = Fore.GREEN if stats['successful'] == stats['total'] else Fore.RED
        
        print(f"  {continent}:")
        print(f"    Success Rate: {success_color}{success_ratio}{Style.RESET_ALL}")
        if stats['successful'] > 0:
            print(f"    Average RTT: {stats['avg_rtt']:.1f} ms")
            print(f"    Min/Max RTT: {stats['min_rtt']:.1f} ms / {stats['max_rtt']:.1f} ms")
    
    # Detailed node results
    print(f"\n{Fore.YELLOW}Detailed Results by Node:{Style.RESET_ALL}")
    print(f"{'Location':<30} {'Result':<10} {'RTT min/avg/max':<25} {'IP Address':<15}")
    print("-" * 80)
    
    # Sort by continent and then by country
    sorted_results = sorted(
        parsed_results["nodes_results"], 
        key=lambda x: (x["continent"], x["country"], x["city"])
    )
    
    for result in sorted_results:
        location = f"{result['country']}, {result['city']}"
        success_ratio = f"{result['successful']}/{result['total']}"
        success_color = Fore.GREEN if result['successful'] == result['total'] else Fore.RED
        
        if result['successful'] > 0:
            rtt_stats = f"{result['min_rtt']:.1f} / {result['avg_rtt']:.1f} / {result['max_rtt']:.1f} ms"
        else:
            rtt_stats = "N/A"
            
        print(f"{location:<30} {success_color}{success_ratio:<10}{Style.RESET_ALL} {rtt_stats:<25} {result['ip']:<15}")


def display_http_results(parsed_results: Dict[str, Any]) -> None:
    """
    Display HTTP results in a formatted table.
    
    Args:
        parsed_results: Parsed HTTP results
    """
    print("\n" + "=" * 80)
    print(f"{Fore.CYAN}HTTP RESULTS SUMMARY{Style.RESET_ALL}")
    print("=" * 80)
    
    # Overall statistics
    overall = parsed_results["overall_stats"]
    success_ratio = f"{overall['successful']}/{overall['total']}"
    success_color = Fore.GREEN if overall['successful'] == overall['total'] else Fore.RED
    
    print(f"\n{Fore.YELLOW}Overall Statistics:{Style.RESET_ALL}")
    print(f"  Success Rate: {success_color}{success_ratio}{Style.RESET_ALL}")
    if overall['successful'] > 0:
        print(f"  Average Response Time: {overall['avg_response_time']:.1f} ms")
    
    # Continent statistics
    print(f"\n{Fore.YELLOW}Statistics by Continent:{Style.RESET_ALL}")
    for continent, stats in parsed_results["continent_stats"].items():
        success_ratio = f"{stats['successful']}/{stats['total']}"
        success_color = Fore.GREEN if stats['successful'] == stats['total'] else Fore.RED
        
        print(f"  {continent}:")
        print(f"    Success Rate: {success_color}{success_ratio}{Style.RESET_ALL}")
        if stats['successful'] > 0:
            print(f"    Average Response Time: {stats['avg_response_time']:.1f} ms")
    
    # Detailed node results
    print(f"\n{Fore.YELLOW}Detailed Results by Node:{Style.RESET_ALL}")
    print(f"{'Location':<30} {'Status':<15} {'Response Time':<15} {'IP Address':<15}")
    print("-" * 80)
    
    # Sort by continent and then by country
    sorted_results = sorted(
        parsed_results["nodes_results"], 
        key=lambda x: (x["continent"], x["country"], x["city"])
    )
    
    for result in sorted_results:
        location = f"{result['country']}, {result['city']}"
        
        status = f"{result['status_code']} {result['status_msg']}"
        status_color = Fore.GREEN if result['success'] else Fore.RED
        
        response_time = f"{result['response_time']:.1f} ms" if result['success'] else "N/A"
        
        print(f"{location:<30} {status_color}{status:<15}{Style.RESET_ALL} {response_time:<15} {result['ip']:<15}")


def save_results_to_file(data: Dict[str, Any], filename: str, format_type: str = "json") -> None:
    """
    Save results to a file in the specified format.
    
    Args:
        data: Results data to save
        filename: Output filename
        format_type: Format to save in ('json' or 'txt')
    """
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        check_type = data.get("check_type", "check")
        filename = f"{check_type}_result_{timestamp}.{format_type}"
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            if format_type == "json":
                json.dump(data, f, indent=2)
            else:
                # Text format
                f.write(f"Check Type: {data.get('check_type', 'unknown')}\n")
                f.write(f"Host: {data.get('host', 'unknown')}\n")
                f.write(f"Timestamp: {data.get('timestamp', datetime.now().isoformat())}\n\n")
                
                # Overall stats
                f.write("Overall Statistics:\n")
                overall = data.get("overall_stats", {})
                f.write(f"  Success Rate: {overall.get('successful', 0)}/{overall.get('total', 0)}\n")
                if data.get("check_type") == "ping":
                    f.write(f"  Average RTT: {overall.get('avg_rtt', 0):.1f} ms\n")
                    f.write(f"  Min/Max RTT: {overall.get('min_rtt', 0):.1f} ms / {overall.get('max_rtt', 0):.1f} ms\n")
                else:
                    f.write(f"  Average Response Time: {overall.get('avg_response_time', 0):.1f} ms\n")
                
                # Continent stats
                f.write("\nStatistics by Continent:\n")
                for continent, stats in data.get("continent_stats", {}).items():
                    f.write(f"  {continent}:\n")
                    f.write(f"    Success Rate: {stats.get('successful', 0)}/{stats.get('total', 0)}\n")
                    if data.get("check_type") == "ping":
                        f.write(f"    Average RTT: {stats.get('avg_rtt', 0):.1f} ms\n")
                        f.write(f"    Min/Max RTT: {stats.get('min_rtt', 0):.1f} ms / {stats.get('max_rtt', 0):.1f} ms\n")
                    else:
                        f.write(f"    Average Response Time: {stats.get('avg_response_time', 0):.1f} ms\n")
                
                # Node results
                f.write("\nDetailed Results by Node:\n")
                if data.get("check_type") == "ping":
                        f.write(f"{location:<30} {success_ratio:<10} {rtt_stats:<25} {result.get('ip', 'N/A'):<15}\n")
                else:
                    f.write(f"{'Location':<30} {'Status':<15} {'Response Time':<15} {'IP Address':<15}\n")
                    f.write("-" * 80 + "\n")
                    
                    for result in data.get("nodes_results", []):
                        location = f"{result.get('country', 'Unknown')}, {result.get('city', 'Unknown')}"
                        status = f"{result.get('status_code', 'N/A')} {result.get('status_msg', 'N/A')}"
                        response_time = f"{result.get('response_time', 0):.1f} ms" if result.get('success', False) else "N/A"
                        
                        f.write(f"{location:<30} {status:<15} {response_time:<15} {result.get('ip', 'N/A'):<15}\n")
        
        print(f"{Fore.GREEN}Results saved to {filename}")
    except Exception as e:
        print(f"{Fore.RED}Error saving results to file: {e}")


def interactive_mode() -> None:
    """Run the program in interactive mode, prompting for inputs."""
    print(f"{Fore.CYAN}=== Check-Host Ping & HTTP Tester - Interactive Mode ==={Style.RESET_ALL}\n")
    
    # Get host to check
    while True:
        host = input(f"{Fore.YELLOW}Enter host to check (domain or IP): {Style.RESET_ALL}")
        try:
            host = validate_host(host)
            break
        except ValueError as e:
            print(f"{Fore.RED}{e}. Please try again.{Style.RESET_ALL}")
    
    # Get check type
    check_type = ""
    while check_type not in ["ping", "http"]:
        check_type = input(f"{Fore.YELLOW}Enter check type (ping/http) [default: ping]: {Style.RESET_ALL}").lower() or "ping"
        if check_type not in ["ping", "http"]:
            print(f"{Fore.RED}Invalid check type. Please enter 'ping' or 'http'.{Style.RESET_ALL}")
    
    # Get nodes selection
    print(f"\n{Fore.CYAN}Available continent options:{Style.RESET_ALL}")
    print("  ALL   - All available nodes")
    print("  EU    - European nodes")
    print("  NA    - North American nodes")
    print("  AS    - Asian nodes")
    print("  SA    - South American nodes")
    print("  EU+NA - European and North American nodes")
    
    continent = input(f"\n{Fore.YELLOW}Select nodes by continent [default: ALL]: {Style.RESET_ALL}").upper() or "ALL"
    nodes = get_nodes_selection(continent)
    
    print(f"\n{Fore.CYAN}Selected {len(nodes)} nodes from {continent or 'ALL'}{Style.RESET_ALL}")
    
    # Ask about saving results
    save_option = input(f"{Fore.YELLOW}Save results to file? (y/n) [default: n]: {Style.RESET_ALL}").lower() or "n"
    save_to_file = save_option in ["y", "yes"]
    
    if save_to_file:
        format_type = input(f"{Fore.YELLOW}Save format (json/txt) [default: json]: {Style.RESET_ALL}").lower() or "json"
        if format_type not in ["json", "txt"]:
            format_type = "json"
            print(f"{Fore.YELLOW}Invalid format. Using json instead.{Style.RESET_ALL}")
        
        filename = input(f"{Fore.YELLOW}Filename [leave empty for auto-generated]: {Style.RESET_ALL}")
    else:
        format_type = "json"
        filename = None
    
    # Run the check
    run_check_and_display(check_type, host, nodes, save_to_file, filename, format_type)


def run_check_and_display(check_type: str, host: str, nodes: List[str], 
                          save_to_file: bool = False, filename: Optional[str] = None,
                          format_type: str = "json") -> None:
    """
    Run a check and display results.
    
    Args:
        check_type: Type of check to run ('ping' or 'http')
        host: Host to check
        nodes: List of nodes to use
        save_to_file: Whether to save results to file
        filename: Filename to save to (or None for auto-generated)
        format_type: Format to save in ('json' or 'txt')
    """
    api = CheckHostAPI()
    
    print(f"\n{Fore.CYAN}Running {check_type} check on {host} using {len(nodes)} nodes...{Style.RESET_ALL}")
    
    try:
        # Run the check
        check_response = api.run_check(check_type, host, nodes)
        
        request_id = check_response.get("request_id")
        print(f"{Fore.GREEN}Check initiated. Request ID: {request_id}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Permanent link: {check_response.get('permanent_link')}{Style.RESET_ALL}")
        
        # Get check results
        print(f"{Fore.CYAN}Fetching results (this may take a few seconds)...{Style.RESET_ALL}")
        results = api.get_check_result(request_id)
        
        # Parse and display results
        if check_type == "ping":
            parsed_results = parse_ping_results(results)
            display_ping_results(parsed_results)
        else:  # http
            parsed_results = parse_http_results(results)
            display_http_results(parsed_results)
        
        # Add metadata
        full_results = {
            "check_type": check_type,
            "host": host,
            "timestamp": datetime.now().isoformat(),
            "permanent_link": check_response.get("permanent_link", ""),
            "request_id": request_id,
            **parsed_results
        }
        
        # Save to file if requested
        if save_to_file:
            save_results_to_file(full_results, filename, format_type)
            
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        sys.exit(1)


def main():
    """Main function to parse command line arguments or start interactive mode."""
    parser = argparse.ArgumentParser(
        description='Check host availability and response times using the Check-Host API.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python check_host.py                             # Start interactive mode
  python check_host.py 1.1.1.1                     # Ping check with all nodes
  python check_host.py google.com --type http      # HTTP check with all nodes
  python check_host.py 1.1.1.1 --nodes EU          # Ping check with European nodes
  python check_host.py example.com --save          # Save results to auto-generated file
  python check_host.py 1.1.1.1 --output ping.json  # Save results to specific file
"""
    )
    
    parser.add_argument('host', nargs='?', help='Host to check (domain or IP)')
    parser.add_argument('--type', choices=['ping', 'http'], default='ping',
                      help='Type of check to perform (default: ping)')
    parser.add_argument('--nodes', default='ALL',
                      help='Nodes to use (ALL, EU, NA, AS, SA, EU+NA)')
    parser.add_argument('--save', action='store_true',
                      help='Save results to file')
    parser.add_argument('--output', help='Output file name')
    parser.add_argument('--format', choices=['json', 'txt'], default='json',
                      help='Output format (default: json)')
    
    args = parser.parse_args()
    
    # If no host provided, run in interactive mode
    if not args.host:
        interactive_mode()
    else:
        try:
            host = validate_host(args.host)
            nodes = get_nodes_selection(args.nodes)
            
            save_to_file = args.save or args.output is not None
            
            run_check_and_display(
                check_type=args.type,
                host=host,
                nodes=nodes,
                save_to_file=save_to_file,
                filename=args.output,
                format_type=args.format
            )
            
        except ValueError as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
            sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Operation cancelled by user{Style.RESET_ALL}")
        sys.exit(0)
