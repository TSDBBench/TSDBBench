#!/usr/bin/env python2
# -*- coding: utf-8 -*-

__author__ = 'Andreas Bader'
__version__ = "0.01"

# db_folders -> List of DB Folder (for space check)
# prerun_once -> list of commands to run local once before ycsb (%%IP%% uses first db vm) (without ycsb, sync or space diff or poweroff commands!)
# postrun_once -> list of commands to run local once after ycsb (%%IP%% uses first db vm) (without ycsb, sync or space diff or poweroff commands!)
# prerun -> list of commands to run before ycsb (all vms or local) (without ycsb, sync or space diff or poweroff commands!)
# postrun -> list of commands to run after ycsb (all vms or local) (without ycsb, sync or space diff or poweroff commands!)
# prerun_master -> list of commands to run before ycsb (only on master(first=ID 0) vm or local)) (without ycsb, sync or space diff or poweroff commands!)
# postrun_master -> list of commands to run after ycsb (only on master(first=ID 0) vm or local)) (without ycsb, sync or space diff or poweroff commands!)
# prerun_slaves -> list of commands to run before ycsb (only on slave (all without master(=ID 0)) vms or local)) (without ycsb, sync or space diff or poweroff commands!)
# postrun_slaves -> list of commands to run after ycsb (only on slave (all without master(=ID 0)) vms or local)) (without ycsb, sync or space diff or poweroff commands!)
# prerun_dict -> list of commands to run before ycsb for each db vm (key=number of vm) (without ycsb, sync or space diff or poweroff commands!) (%%SSH%% not needed)
# postrun_dict -> list of commands to run after ycsb for each db vm (key=number of vm) (without ycsb, sync or space diff or poweroff commands!) (%%SSH%% not needed)
# check -> list of commands to run after prerun (all vms or local) for checking if everything runs correctly (systemctl start xyz oftern returns true even if start failed somehow. Check that here!)
# check_master -> list of commands to run after prerun (all vms or local) for checking if everything runs correctly (only on master(first=ID 0) vm or local))
# check_slaves -> list of commands to run after prerun (all vms or local) for checking if everything runs correctly (all without master(=ID 0)) vms or local))
# check_dict -> list of commands to run after prerun for each db vm (key=number of vm) (without ycsb, sync or space diff or poweroff commands!) (%%SSH%% not needed)
# include -> which base modules should be imported and added to the dictionary (standard functions that are reusable). Warning: infinite import loop possible!
# the following variables are possible in prerun_once, postrun_once, prerun, prerun_master, prerun_slaves, check, check_master, check_slaves, postrun, postrun_master, postrun_slaves, prerun_dict, postrun_dict, check_dict, db_args:
# %%IP%% -> IP of (actual) db vm
# %%IPgen%% -> IP of (actual) generator vm (on which this script runs)
# %%IPn%% -> IP of db vm number n (e.g. %%IP2%%)
# %%IPall%% -> give String with IP of all vms)
# %%HN%% -> Hostname of (actual) db vm
# %%HNgen%% -> Hostname of (actual) generator vm (on which this script runs)
# %%HNn%% -> Hostname of db vm number n (e.g. %%HN2%%)
# %%HNall%% -> give String with Hostname of all vms)
# %%SSH%% -> if SSH should be used (set at the beginning)
# Order of Preruns/Postruns:
# 1. prerun/postrun/check, 2. prerun_master/postrun_master/check_master, 3. preun_skaves/postrun_slaves/check_slaves, 4.prerun_dict/postrun_dict/check_dict
# General Order:
#  prerun -> check -> ycsb -> postrun

# this configures hbase

def getDict():
    baseConfig={}
    baseConfig["db_folders"]=[]
    baseConfig["prerun_once"]= []
    baseConfig["postrun_once"]= []
    baseConfig["prerun"] = [
        "%%SSH%%sudo -s bash -c 'sed -i \"s|#tsd.storage.hbase.zk_quorum = localhost|tsd.storage.hbase.zk_quorum = %%HN0%%,%%HN1%%,%%HN2%%,%%HN3%%,%%HN4%%|\" /etc/opentsdb/opentsdb.conf'",
        "%%SSH%%sudo -s bash -c 'sed -i \"s|<configuration>|<configuration>\\n  <property>\\n    <name>hbase.rootdir</name>\\n    <value>hdfs://%%HN0%%:54310/hbase</value>\\n  </property>\\n  <property>\\n    <name>hbase.cluster.distributed</name>\\n    <value>true</value>\\n  </property>\\n  <property>\\n    <name>hbase.zookeeper.quorum</name>\\n    <value>%%HN0%%,%%HN1%%,%%HN2%%,%%HN3%%,%%HN4%%</value>\\n  </property>\\n  <property>\\n    <name>hbase.zookeeper.property.dataDir</name>\\n    <value>/home/vagrant/zookeeper</value>\\n  </property>|g\" /home/vagrant/hbase/conf/hbase-site.xml'",
        "%%SSH%%sudo -s bash -c 'sed -i \"s|localhost|%%HN1%%\\n%%HN2%%\\n%%HN3%%\\n%%HN4%%|\" /home/vagrant/hbase/conf/regionservers'",
        "%%SSH%%sudo -s bash -c 'echo -e \"%%HN1%%\\n%%HN2%%\" >> /home/vagrant/hbase/conf/backup-masters'"
    ]
    baseConfig["postrun"]= []
    baseConfig["prerun_master"]= []
    baseConfig["postrun_master"]= []
    baseConfig["prerun_slaves"]= []
    baseConfig["postrun_slaves"]= []
    baseConfig["prerun_dict"]= {}
    baseConfig["postrun_dict"]= {}
    baseConfig["check"]= []
    baseConfig["check_master"]= []
    baseConfig["check_slaves"]= []
    baseConfig["check_dict"]= {}
    baseConfig["include"] = []
    return baseConfig