# KillYon 🛡️

![KillYon Logo](https://img.freepik.com/premium-photo/banner-starry-outer-space-background-texture_78899-4536.jpg?w=2000)

## Overview
KillYon is a Python script designed to enhance your privacy by monitoring and blocking specific ports used by Veyon, a network monitoring and classroom management software. When KillYon detects Veyon connections, it takes action to protect your privacy.

## Usage
Before running KillYon, make sure you run it as an administrator. The script will continuously monitor your network connections and take the following actions:

- If it detects Veyon connections, it will block specific ports used by Veyon.
- It can also stop the VeyonService if it's running to prevent further monitoring.

## Requirements
- Python
- Windows (Administrator privileges required)

## How to Run
1. Run the script as an administrator.

```shell
python killyon.py
