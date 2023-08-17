#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ==============================================================================
#
#       global_variables.py - Global variables shared by all modules.
#
# ==============================================================================


import os


class Config:
    HOST_URL = os.getenv("HOST_URL", 'http://18.208.75.162:9000')


config = Config()

# from dotenv import load_dotenv
# import os  # provides ways to access the Operating System and allows us to read the environment variables
#
# load_dotenv()
#
#
# def init():
#     """ This should only be called once by the main module
#         Child modules will inherit values. For example if they contain
#
#             import global_variables as g
#
#         Later on they can reference 'g.USER' to get the user ID.
#     """
#     global HOST  # , BASE_PATH
#
#     # HOST
#     HOST = os.getenv("HOST")
#
# # End of global_variables.py
