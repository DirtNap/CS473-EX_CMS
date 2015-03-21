import argparse

class ConfigParser(argparse.ArgumentParser):

    def __init__(self, *args, **kwargs):
        super(self, ConfigParser).__init__(*args, **kwargs)
        
