# IP Analyzer

The IP Analyzer is a Python script that allows you to analyze and provide information about an IP address, including its class, network ID, broadcast address, subnet mask, and more.

## Description

The IP Analyzer classifies IP addresses into different classes (A, B, or C) based on the first octet. It then provides detailed information about the IP address and its corresponding network, including network ID, broadcast address, subnet mask, number of networks, and number of hosts per network.

## Features

- Classifies IP addresses into classes (A, B, C)
- Calculates network ID, broadcast address, and subnet mask
- Determines if the IP address is public or private
- Provides an option to explain the results

## Usage

1. Clone or download the repository.

2. Run the `analyzer.py` script. You will be prompted to enter an IP address (e.g., 192.168.1.1). The script will then analyze the IP address and provide relevant information.

3. The script will display the IP address class and various details about the network associated with the IP address.

4. You can choose to explain the results further, providing insights into the IP address's class, network ID, broadcast address, and subnet mask.

## Dependencies

- Python 3.x
- The `art` library (used for ASCII art text)

## Usage Example

```python
from art import text2art
from analyzer import IPAnalyzer, extract_ip

text = " MR.I"
print('')
print(text2art(text, font="speed"))

user_input = input(">> Enter your IP address (e.g., 192.168.1.1): ")
ip_parts = extract_ip(user_input)

if ip_parts is None:
    print("Invalid IP address format.")
else:
    ip_analyzer = IPAnalyzer(ip_parts)
    ip_analyzer.analyze_ip()
