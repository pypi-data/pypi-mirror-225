import subprocess
import argparse
import os

def execute_scripts(script_file, *args):
    scripts_root = os.path.dirname(__file__)
    script_file = os.path.join(scripts_root, 'scripts', script_file)
    # print(script_file)
    cmd_args = ' '.join(args)
    command = "bash {} {}".format(script_file, cmd_args)
    ret = subprocess.run(command, shell=True)
    return ret.returncode, ret.stdout.decode('utf-8'), ret.stderr.decode('utf-8')

def force_kill():
    p = argparse.ArgumentParser(description='force to kill')
    p.add_argument("keyword", help='keyword for match program')
    args = p.parse_args()
    keyword = args.keyword
    execute_scripts('force_kill.sh', keyword)
