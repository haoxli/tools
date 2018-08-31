#!/usr/bin/env bash

SCRIPT_PATH=$(cd `dirname $0`; pwd)
source ${SCRIPT_PATH}/utils/env_const
source ${SCRIPT_PATH}/utils/apt

function depot_tools_install() {
    tool_path="${DEV_TOOLS}/depot_tools"
    if [ ! -d  ${tool_path} ]; then
        git clone https://chromium.googlesource.com/chromium/tools/depot_tools.git ${tool_path}
    fi
    grep 'depot_tools' ${BASH_CONF}
    if [ $? -ne 0 ]; then
        cat >> ${BASH_CONF} << EOF

# chromium depot_tools
export PATH=\$PATH:${tool_path}
EOF
        source ${BASH_CONF}
        echo ">>> depot tools install succeed"
    else
        echo ">>> depot tools exists"
    fi
}

function yarn_install() {
    # configure yarn repository
    curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -
    echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list
    sudo apt update
    apt_install yarn
}

function rust_install() {
    curl https://sh.rustup.rs -sSf | sh
    grep '.cargo/bin' ${BASH_CONF}
    if [ $? -ne 0 ]; then
        cat >> ${BASH_CONF} << EOF

# Rust
export PATH=\$PATH:\$HOME/.cargo/bin
EOF
        source ${BASH_CONF}
        echo ">>> rust install succeed"
    else
        echo ">>> rust exists"
    fi
}

# depo_tools
depot_tools_install

# yarn
yarn_install

# Rust
rust_install

# ccache
apt_install ccache
