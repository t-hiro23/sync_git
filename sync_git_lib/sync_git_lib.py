#!/usr/bin/env python
# coding: utf-8

import subprocess
import sys
import os
import datetime



# clone urlにuserとpassを加えたものを作って返す
def make_clone_url_with_user_and_pass(clone_url_, user_, pass_):
    clone_url_prev = clone_url_.split("://")[0]
    clone_url_post = clone_url_.split("://")[-1]
    clone_url_with_user_and_pass = clone_url_prev + "://" + user_ + ":" + pass_ + "@" + clone_url_post
    
    return clone_url_with_user_and_pass



# リポジトリをcloneする
def clone_repository(clone_url_with_user_and_pass_, rep_dir_):
    # リポジトリをclone
    cmd = "git clone --progress " +  clone_url_with_user_and_pass_ + " " + rep_dir_
    cmd_result = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode("utf-8")
    print(cmd_result)



# HEADのhashを取得
def get_head_hash():
    cmd = "git rev-parse HEAD"
    head_hash = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode("utf-8").strip()
    
    return head_hash



# 特定区間のgit logのリストを取得
def get_git_log_list(start_hash_, end_hash_):
    # git log を取得 (必要なhash特定のソースにする)
    cmd = 'git log --pretty=format:"%s ,%H" ' + start_hash_ + ".." + end_hash_
    git_log = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode("utf-8")
    
    # list化
    git_log_list = git_log.split("\n")
    return git_log_list



# git diffからパッチファイルを作る
def make_patch_file(file_path_and_name_, hash_):
    fileobj = open(file_path_and_name_, "wb")
    cmd = "git diff --binary " + hash_ + "~.." + hash_
    fileobj.write(subprocess.check_output(cmd, stderr=subprocess.STDOUT))
    fileobj.close()



# git applyでパッチをあてる
def git_apply_patch(patch_file_path_and_name_):
    cmd = "git apply " + patch_file_path_and_name_
    cmd_result = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode("utf-8")
    print(cmd_result)

# 全ての変更をgit addする
def git_add_all():
    cmd = "git add -A"
    cmd_result = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode("utf-8")
    print(cmd_result)



# git commitする
def git_commit(commit_message_):
    cmd = "git commit " + commit_message_
    cmd_result = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode("utf-8")
    print(cmd_result)



# git_pushする
def git_push(branch_):
    cmd = "git push origin " + branch_
    cmd_result = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode("utf-8")
    print(cmd_result)



# git_addする
def git_add(file_):
    cmd = "git add " + file_
    cmd_result = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode("utf-8")
    print(cmd_result)



# 現在のlocal branchを取得
def get_current_local_branch_name():
    cmd = "git rev-parse --abbrev-ref HEAD"
    cmd_result = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode("utf-8").strip()
    print(cmd_result)
    
    return cmd_result



# localブランチのリストを作成する
def get_local_branch_name_list():
    cmd = "git branch"
    cmd_result = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode("utf-8")
    print(cmd_result)

    local_branch_list = cmd_result.split("\n")
    local_branch_list = [branch.split(" ")[-1].strip() for branch in local_branch_list]
    
    return local_branch_list



# remoteブランチからlocalブランチを作成する
def get_remote_branch_name_list():
    cmd = "git branch --remote"
    cmd_result = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode("utf-8")
    print(cmd_result)

    remote_branch_list = cmd_result.split("\n")
    remote_branch_list = [branch.strip() for branch in remote_branch_list]
    
    return remote_branch_list



# 既存のbranchへ切り替える
def switch_existing_branch(branch_):
        cmd = "git checkout " + branch_
        cmd_result = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode("utf-8")
        print(cmd_result)



# リモートbranchからlocalブランチを作って切り替える
def make_local_branch_from_remote_branch_and_switch(branch_):
    cmd = "git checkout -b " + branch_ + " origin/" + branch_
    cmd_result = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode("utf-8")
    print(cmd_result)



def make_local_and_remote_branch_and_switch(branch_):
    cmd = "git checkout -b " + branch_
    cmd_result = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode("utf-8")
    print(cmd_result)

    cmd = "git push -u origin " + branch_
    cmd_result = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode("utf-8")
    print(cmd_result)



def switch_local_branch_on_src_repository(src_rep_branch_):
    # 現在のlocal branchを取得
    src_rep_current_branch = get_current_local_branch_name()
    print("DEBUG: src_rep_current_branch =", src_rep_current_branch)
    
    # localブランチのリストを作成する
    src_rep_local_branch_list = get_local_branch_name_list()
    print("DEBUG: src_rep_local_branch_list =\n" + "\n".join(src_rep_local_branch_list))
    
    # remoteブランチのリストを作成する
    src_rep_remote_branch_list = get_remote_branch_name_list()
    print("DEBUG: src_rep_remote_branch_list =\n" + "\n".join(src_rep_remote_branch_list))
    
    # local branchが正しいかチェックする
    if not src_rep_branch_ == src_rep_current_branch:
        # local branchを切り替える必要あり
        if src_rep_branch_ in src_rep_local_branch_list:
            # 既にあるlocalブランチに切り替える
            switch_existing_branch(src_rep_branch_)
        elif "origin/" + src_rep_branch_ in src_rep_remote_branch_list:
            # localブランチがない && 既にremoteブランチがある -> remoteブランチからlocalブランチを作る
            make_local_branch_from_remote_branch_and_switch(src_rep_branch_)
        else:
            # localにもremoteにもブランチがない
            print("ERROR: origin/" + src_rep_branch_ + " was not found." )
            sys.exit(1)

    cmd_result = get_current_local_branch_name()
    print("Info: work branch = " + cmd_result)



def switch_local_branch_on_dst_repository(dst_rep_branch_):
    # 現在のlocal branchを取得
    dst_rep_current_branch = get_current_local_branch_name()
    print("DEBUG: dst_rep_current_branch =", dst_rep_current_branch)
    
    # localブランチのリストを作成する
    dst_rep_local_branch_list = get_local_branch_name_list()
    print("DEBUG: dst_rep_local_branch_list =\n" + "\n".join(dst_rep_local_branch_list))
    
    # remoteブランチのリストを作成する
    dst_rep_remote_branch_list = get_remote_branch_name_list()
    print("DEBUG: dst_rep_remote_branch_list =\n" + "\n".join(dst_rep_remote_branch_list))
    
    if not dst_rep_branch_ == dst_rep_current_branch:
        # local branchを切り替える必要あり
        if dst_rep_branch_ in dst_rep_local_branch_list:
            # 既にあるlocalブランチに切り替える
            switch_existing_branch(dst_rep_branch_)
        elif "origin/" + dst_rep_branch_ in dst_rep_remote_branch_list:
            # localブランチがない && 既にremoteブランチがある -> remoteブランチからlocalブランチを作る
            make_local_branch_from_remote_branch_and_switch(dst_rep_branch_)
        else:
            # timestampを取得
            time_stamp = datetime.datetime.today().strftime("%Y%m%d-%H%M%S")
            print("DEBUG: time_stamp = " + time_stamp)

            # localブランチがない && remoteブランチもない -> localブランチとremoteブランチを新規作成
            dst_rep_branch_with_timestamp = dst_rep_branch_ + "-" + time_stamp
            make_local_and_remote_branch_and_switch(dst_rep_branch_with_timestamp)

    # 現在のlocal branchを取得
    cmd_result = get_current_local_branch_name()
    print("Info: work branch = " + cmd_result)
    
    return cmd_result
