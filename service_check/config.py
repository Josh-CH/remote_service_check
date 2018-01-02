#!/usr/bin/env python
import sys, os
PACKAGE_ROOT = os.path.abspath(os.path.dirname(__name__))
sys.path.append(PACKAGE_ROOT)

# Your current problem is that you cannot reference the correct package location
# once you have built the package
