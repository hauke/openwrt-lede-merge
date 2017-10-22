#!/usr/bin/env python3
import re

def commits_todic(filename):
    file = open(filename)
    commits = {}
    regex = re.compile('([a-f0-9]*) (.*)')
    for line in file:
        m = regex.match(line)
        commits[m.group(2)] = m.group(1)
    return commits


def commits_tolist(filename):
    file = open(filename)
    commits = []
    regex = re.compile('([a-f0-9]*) (.*)')
    for line in file:
        commit = {}
        m = regex.match(line)
        commit["id"] = m.group(1)
        commit["title"] = m.group(2)
        commits.append(commit)
    return commits


# git log 9d61e91d6e6e8eff019e54c48070b5c48e41341c...openwrt/master --no-merges --oneline > openwrt-commits.txt
openwrt_file = "openwrt-commits.txt"
# git log reboot...origin/master --no-merges --oneline > lede-commits.txt
lede_file = "lede-commits.txt"

openwrt_dic = commits_todic(openwrt_file)
lede_dic = commits_todic(lede_file)

openwrt_list = commits_tolist(openwrt_file)

missing_dic = openwrt_dic.keys() - lede_dic.keys()

print('"OpenWrt", "LEDE", "Title";')
for commit in openwrt_list:
    commit["lede"] = lede_dic.get(commit["title"])
    if not commit["lede"]:
        commit["lede"] = "          "

for commit in openwrt_list:
    print('"' + commit["id"] + '", "' + commit["lede"] + '", "' + commit["title"].replace('"', '""') + '";')
