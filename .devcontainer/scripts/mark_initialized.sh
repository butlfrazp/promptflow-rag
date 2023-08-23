#!/bin/env bash

# This file marks the environment as initialized, allowing .bashrc to
# continue with the rest of the terminal setup. This is done to ensure
# that the environment is fully initialized before the terminal is
# available.

echo <<EOF > ~/.env_ready
This file is used to indicate that the environment has finished initializing.
Do not delete this file. If you do by accident, you can recreate it by running
the following command in the terminal:

    touch ~/.env_ready

EOF
