#!/usr/bin/python

import sys, os, time
import simplejson as json
from os.path import *

def exec_cmd(cmd,toprint,toexec):
    if toprint:
        print cmd
    if toexec:
        os.system(cmd)

def gm_argument(switch,argtype,default,message_prefix):

    if switch in sys.argv:
        switch_index = sys.argv.index(switch)
        if argtype in [ 'negative', ]:
            argument = False
        else:
            if len(sys.argv) > switch_index+1:
                argument = sys.argv[switch_index+1]
            else:
                sys.exit(message_prefix + " not defined properly! Exiting.")
    else:
        if argtype in [ 'negative', ]:
            argument = default
        else:
            if default:
                argument = default
            else:
                sys.exit(message_prefix + " not defined and it's mandatory! Exiting.")
        
    if argtype == "dir":
        if not isdir(argument):
           exec_cmd('mkdir -p "' + argument + '"',tp,te)
    elif argtype == "file":
        if not isfile(argument):
            sys.exit(message_prefix + " does not exist! Exiting.")

    return argument

def system_install():
    # create dir
    cmd = "mkdir -p " + odir
    exec_cmd(cmd,tp,te)
    # install the system
    cmd = "debootstrap " + distros[distro][release]['bootstrap release'] + " " + odir
    exec_cmd(cmd,tp,te)

def config_update():
    # fix things inside of the chroot
    cmd = "cp -a " + sysdir_all + "/* " + odir
    exec_cmd(cmd,tp,te)
    cmd = "cp -a " + sysdir_dist + "/* " + odir
    exec_cmd(cmd,tp,te)
    cmd = "chroot " + odir + " apt-get update"
    exec_cmd(cmd,tp,te)
    cmd = "chroot " + odir + " apt-get install -y locales"
    exec_cmd(cmd,tp,te)
    cmd = "echo 'en_us.utf-8 utf-8' > " + odir + "/etc/locale.gen"
    exec_cmd(cmd,tp,te)
    cmd = "chroot " + odir + " locale-gen"
    exec_cmd(cmd,tp,te)

def update_software():
    # update chroot
    cmd = "chroot " + odir + " apt-get update"
    exec_cmd(cmd,tp,te)
    cmd = "chroot " + odir + " apt-get upgrade -y"
    exec_cmd(cmd,tp,te)

def install_software():
    software = [ 
        'vim-nox', 'tcpdump', 'nmap', 'net-tools', 
    ]
    cmd = "chroot " + odir + " apt-get install -y " + " ".join(software)
    exec_cmd(cmd,tp,te)

def create_docker_image():
    # create docker image
    cmd = "tar -C " + odir + " -c . | docker import - " + fullname
    exec_cmd(cmd,tp,te)

def push_to_cloud():
    # tag it
    cmd = "docker full_tag " + fullname + " " + distros[distro][release]['docker repository'] + ":" + full_tag
    exec_cmd(cmd,tp,te)
    # push to the cloud.docker
    cmd = "docker push " + distros[distro][release]['docker repository'] + ":" + full_tag
    exec_cmd(cmd,tp,te)

def run_docker():
    # run docker
    cmd = "docker run -d --name " + name + " " + fullname + " init"
    exec_cmd(cmd,tp,te)

tp = gm_argument("--noprint","negative",True,"Someting is rotten in the state of Denmark! Variable 'tp'. Exiting.")
te = gm_argument("--noexec","negative",True,"Someting is rotten in the state of Denmark! Variable 'te'. Exiting.")
distro = gm_argument("--distro","string",False,"Distribution")
release = gm_argument("--release","string",False,"Release")
tag = gm_argument("--tag","string","default","Tag")
tag_suffix = time.strftime("%Y%m%d%H%M%S")
full_tag = tag + "-" + tag_suffix
simple_name = distro + '-' + release + '-' + tag
name = simple_name + '-' + full_tag
fullname = distro + '-' + release + ':' + full_tag
root_dir = gm_argument("--root","dir",".","Root directory")
chroot_dir = root_dir + "/chroots"
odir = chroot_dir + "/" + simple_name
sysdir = root_dir + "/system"
sysdir_all = sysdir + "/all"
sysdir_dist = sysdir + "/" + distro + "/" + release
distros_config = gm_argument("--distros-config","json file",1,"Distributions config")
if distros_config == 1:
    distros = {
        distro: {
            release: {
                "docker repository": False,
                "bootstrap release": False,
            },
        },
    }
else:
    distros = json.loads(open(distros_config).read())
distros[distro][release]['docker repository'] = gm_argument("--docker-repository","string",distros[distro][release]['docker repository'],"Docker repository")
distros[distro][release]['bootstrap release'] = gm_argument("--bootstrap-release","string",distros[distro][release]['bootstrap release'],"Bootstrap release")

if "--full-init" in sys.argv:
    system_install()
    config_update()
    update_software()
    install_software()
    create_docker_image()
    push_to_cloud()
    run_docker()
elif "--init" in sys.argv:
    system_install()
    config_update()
    update_software()
    install_software()
    create_docker_image()
    run_docker()
elif "--full-update" in sys.argv:
    update_software()
    create_docker_image()
    push_to_cloud()
elif "--update" in sys.argv:
    update_software()
    create_docker_image()

