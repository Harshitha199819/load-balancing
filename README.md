# Load Balancer Design and Implementation

This repository contains the implementation of various load-balancing strategies using socket programming. The project focuses on distributing client requests across backend servers efficiently, ensuring optimal resource utilization, minimal latency, and high availability.

---

## Table of Contents
- [Repository Structure](#repository-structure)
- [Setup and Execution Instructions](#setup-and-execution-instructions)
  - [Environment Setup](#environment-setup)
  - [Running the XFF Algorithm](#running-the-xff-algorithm)
  - [Executing Other Algorithms](#executing-other-algorithms)
- [Implemented Load Balancing Algorithms](#implemented-load-balancing-algorithms)
- [Key Features](#key-features)
- [System Requirements](#system-requirements)
- [References](#references)

---

## Repository Structure

- **`load-balancer-code/`**: Contains the implementation of load balancer logic for various algorithms.
  - Example: `load-balancer-code/XFF/lb.py` for the XFF load-balancing algorithm.
  
- **`server-code/`**: Contains server-side logic for handling requests.
  - Example: `server-code/XFF/server.py` for the XFF algorithm.

- **`client-code/`**: Contains client-side logic for sending requests to the load balancer.
  - Example: `client-code/XFF/client.py` for the XFF algorithm.

---

## Setup and Execution Instructions

### Environment Setup

1. **Clone the repository** on the respective machines:
   - **Client machine**: Clone `client-code`.
   - **Load Balancer (LB) machine**: Clone `load-balancer-code`.
   - **Server machines**: Clone `server-code`.

2. **Replace IPs and Ports**:
   - Update the IP addresses and ports in the `server.py`, `client.py`, and `lb.py` files as per the deployment setup. Refer to the comments within each file for guidance.

---

## Running the XFF Algorithm

To execute the **XFF load-balancing logic**, follow these steps:

- **Start the Load Balancer**:  
  Run the load balancer script on the load balancer machine:  
  ```bash
  python3 load-balancer-code/XFF/lb.py
- **Start the Server(s)**:  
  Run the server script on the server machine:  
  ```bash
  python3 server-code/XFF/server.py
- **Start the Client**:  
  Run the client script on the client machine:  
  ```bash
  python3 client-code/XFF/client.py
## Executing Other Algorithms

To execute other load-balancing algorithms, follow these steps:

- **Start the Load Balancer**:  
  Run the load balancer script for the desired algorithm on the load balancer machine:  
  ```bash
  python3 server-code/<algorithm-folder>/server.py
- **Start the Server(s)**:  
  Run the server script for the desired algorithm on each server machine:  
  ```bash
  python3 load-balancer-code/<algorithm-folder>/lb.py
- **Start the Client**:  
  Run the client script for the desired algorithm on the client machine: 
  ```bash
  python3 client-code/<algorithm-folder>/client.py
**Note**: Replace `<algorithm-folder>` with the folder name for the desired algorithm, such as:
- `healthcheck`
- `least-response-time`
- `cpu-processing`
- `most-available-bandwidth`

---

## Implemented Load Balancing Algorithms

- **Health-Check-Based Load Balancing**:  
  Ensures requests are routed to healthy and active servers.

- **Least Response Time Load Balancing**:  
  Routes requests to the server with the quickest response time.

- **Least CPU Utilization Load Balancing**:  
  Directs requests to the server with the lowest CPU usage.

- **Most Network Bandwidth Load Balancing**:  
  Routes data-heavy requests to servers with the highest available bandwidth.

- **XFF Logic**:  
  Implements specific load-balancing logic based on IP forwarding.

---

## Key Features

- Multi-threaded request handling.
- Real-time server health checks.
- Dynamic request routing based on server metrics.
- Error handling and logging for debugging.

---

## System Requirements

- **Python 3.8+**
- Required Python libraries:
  - `psutil`
  - `speedtest-cli`

---
## References

- Python socket Documentation
- psutil Library Documentation for resource monitoring
- Linux ping and speedtest-cli for response time and bandwidth checks
- Struct Parsing Techniques for Network Packet Analysis
- AWS EC2 Hosting: [https://aws.amazon.com/](https://aws.amazon.com/)
- [Locust](https://locust.io/)

---
## Other Material  
- [Presentation](https://tinyurl.com/lb-presentation)  

---
For questions or contributions, feel free to **open an issue** or **submit a pull request**!
