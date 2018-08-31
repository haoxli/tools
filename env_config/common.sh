#!/usr/bin/env bash
# Automated config script for clean Ubuntu 18.04 LST

SCRIPT_PATH=$(cd `dirname $0`; pwd)
source ${SCRIPT_PATH}/utils/env_const
source ${SCRIPT_PATH}/utils/apt

# Proxy
PROXY="[host]:[port]"

function apt_proxy_set() {
    conf="/etc/apt/apt.conf"
    grep "Acquire::http" ${conf}
    if [ $? -ne 0 ]; then
        # root user
        sudo sh -c "cat >> ${conf} << EOF
# proxy
Acquire::http::proxy \"http://${PROXY}\";
Acquire::https::proxy \"http://${PROXY}\";
Acquire::ftp::proxy \"ftp://${PROXY}\";
EOF"
        echo ">>> apt proxy set succeed"
    else
        echo ">>> apt proxy exists"
    fi
}

function bash_proxy_set() {
    grep "http_proxy" ${BASH_CONF}
    if [ $? -ne 0 ]; then
        cat >> ${BASH_CONF} << EOF

# proxy
export http_proxy="http://${PROXY}"
export https_proxy="http://${PROXY}"
EOF
        source ${BASH_CONF}
        echo ">>> bash proxy set succeed"
    else
        echo ">>> proxy exists"
    fi
}

function git_config() {
    # personal info
    git config --global user.name "Li Hao"
    git config --global user.email "hao.x.li@intel.com"
    # text editor
    git config --global core.editor vim
    # CRLF to LF in end of line
    git config --global core.safecrlf true
    git config --global core.autocrlf input
}

# Set proxy
apt_proxy_set
bash_proxy_set

apt_update

# Install basic dependencies
packages=(\
    net-tools openssh-server\
    gcc g++\
    git curl\
    nodejs npm
)
for pkg in ${packages[@]};
do
    apt_install ${pkg}
done

# Git global config
git_config
