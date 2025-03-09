# Check-Host Ping & HTTP Tester

[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)](https://www.python.org/downloads/release/python-360/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

A powerful command-line tool for testing host availability and response times from multiple global locations using the Check-Host API. Analyze ping and HTTP performance with detailed statistics by continent.

## 🌟 Features

- **Multi-location Testing**: Check hosts from 40+ global nodes
- **Dual Check Types**: Perform ping or HTTP checks
- **Continental Filtering**: Select nodes by region (EU, NA, AS, SA)
- **Detailed Analytics**: View response statistics globally and by continent
- **Interactive Mode**: User-friendly guided interface
- **Command-line Support**: Quick checks with simple commands
- **Colorized Output**: Intuitive color-coded results with failure highlighting
- **Results Export**: Save findings to JSON or TXT formats
- **Failure Analysis**: Easily identify problematic nodes

## 📋 Requirements

- Python 3.6 or higher
- `requests` library
- `colorama` library

## 🚀 Installation

1. Clone the repository or download the script:

   ```bash
   git clone https://github.com/danielruiterr/check-host.git
   cd check-host
   ```

2. Install the required dependencies:

   ```bash
   pip install requests colorama
   ```

3. Make the script executable (optional, for Unix-like systems):

   ```bash
   chmod +x check_host.py
   ```

## 💻 Usage

### Interactive Mode

Launch the interactive mode for a guided experience:

```bash
python check_host.py
```

The program will prompt you for:
- Host to check (domain or IP)
- Check type (ping or HTTP)
- Node selection by continent
- Output file options

### Command-line Mode

For quick checks from the terminal:

```bash
# Basic ping check with all nodes
python check_host.py 1.1.1.1

# HTTP check for a website
python check_host.py example.com --type http

# Ping test using only European nodes
python check_host.py cloudflare.com --nodes EU

# HTTP check with North American nodes and save to file
python check_host.py github.com --type http --nodes NA --save

# Save results to a specific file in text format
python check_host.py microsoft.com --output results.txt --format txt
```

## 📝 Command-line Arguments

| Argument   | Description                          | Default  |
|------------|--------------------------------------|----------|
| `host`     | Host to check (domain or IP)         | Required |
| `--type`   | Check type (`ping` or `http`)        | `ping`   |
| `--nodes`  | Node selection (`ALL`, `EU`, `NA`, `AS`, `SA`, `EU+NA`) | `ALL` |
| `--save`   | Save results to auto-generated file  | `False`  |
| `--output` | Save results to specific file        | `None`   |
| `--format` | Output format (`json` or `txt`)      | `json`   |

## 📊 Output Example

```
================================================================================
PING RESULTS SUMMARY
================================================================================

Overall Statistics:
  Success Rate: 42/48
  Average RTT: 157.3 ms
  Min/Max RTT: 34.2 ms / 389.5 ms

Statistics by Continent:
  EU:
    Success Rate: 18/21
    Average RTT: 89.4 ms
    Min/Max RTT: 34.2 ms / 176.8 ms
  NA:
    Success Rate: 9/9
    Average RTT: 124.7 ms
    Min/Max RTT: 68.3 ms / 183.5 ms
  AS:
    Success Rate: 12/14
    Average RTT: 247.6 ms
    Min/Max RTT: 143.2 ms / 389.5 ms
  SA:
    Success Rate: 3/4
    Average RTT: 198.3 ms
    Min/Max RTT: 154.1 ms / 256.8 ms

Detailed Results by Node:
Location                       Result     RTT min/avg/max              IP Address     
--------------------------------------------------------------------------------
France, Paris                  4/4        45.3 / 48.7 / 52.4 ms        1.1.1.1        
Germany, Frankfurt             4/4        34.2 / 36.5 / 39.1 ms        1.1.1.1        
Netherlands, Amsterdam         4/4        42.8 / 45.2 / 48.9 ms        1.1.1.1        
UK, London                     4/4        38.6 / 41.3 / 44.7 ms        1.1.1.1        
Spain, Madrid                  2/4        87.4 / 95.2 / 103.6 ms       1.1.1.1        
USA, New York                  4/4        68.3 / 72.9 / 77.4 ms        1.1.1.1        
USA, Los Angeles               4/4        87.2 / 93.5 / 99.8 ms        1.1.1.1        
Japan, Tokyo                   4/4        143.2 / 156.8 / 170.3 ms     1.1.1.1        
Singapore                      4/4        178.5 / 189.2 / 201.7 ms     1.1.1.1        
Brazil, São Paulo              3/4        154.1 / 198.3 / 256.8 ms     1.1.1.1        
```

## 🔍 How It Works

- The program sends requests to the Check-Host API to initiate ping or HTTP checks
- It selects check nodes based on your continent preference
- Results are collected, analyzed, and organized by continent
- Statistics are calculated for response times and success rates
- Results are displayed in a readable format with color-coded indicators
- If requested, results are saved to a file in your preferred format

## 🌎 Available Nodes

The tool includes access to 40+ global nodes across:

- **Europe**: France, Germany, Netherlands, UK, Spain, Switzerland, and more
- **North America**: USA (Los Angeles, Dallas, Atlanta)
- **Asia**: Japan, Singapore, Hong Kong, India, and more
- **South America**: Brazil
- **Eastern Europe**: Russia, Ukraine

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgements

- [Check-Host](https://check-host.net/) for providing the API
- [Requests](https://docs.python-requests.org/) library for HTTP requests
- [Colorama](https://pypi.org/project/colorama/) for cross-platform colored terminal output

---

Created with ❤️ by Daniel
