import sys
import argparse
""" 
Run from upper directory
	python PTGuruBot
"""
from ptg_main import client

if __name__ == '__main__':
	# //////////////////////////////////
	# Command Line Arguments
	# //////////////////////////////////
	args = argparse.ArgumentParser()
	args.add_argument("--dry-run")


	# //////////////////////////////////
	# Run configure
	# //////////////////////////////////
	import ptg_configure as cfg


	# //////////////////////////////////
	# Overwrite config with cmd args
	# //////////////////////////////////


	# //////////////////////////////////
	# Run Bot
	# //////////////////////////////////
	client.run(cfg.TOKEN)