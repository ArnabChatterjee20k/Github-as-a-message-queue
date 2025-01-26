#!/bin/bash

# Update system packages
sudo apt-get update

# Install Playwright and its dependencies
pip install playwright
playwright install chromium