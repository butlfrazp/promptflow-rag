#####
# Base image - common setup for all targets
#####
FROM mcr.microsoft.com/devcontainers/miniconda:3 AS base
ARG USERNAME=vscode
ARG REPO=askatt_spikes

# Setup user for sudo
USER root
RUN echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME \
    && chown -R $USERNAME:$USERNAME /opt/conda

# Install dependencies
USER $USERNAME
WORKDIR /home/$USERNAME
RUN sudo apt-get update \
    && sudo apt-get install -y gnupg software-properties-common \
    && curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Configure az cli
RUN az config set extension.use_dynamic_install=yes_without_prompt \
    && az extension add -n ml

# Initialize conda
RUN conda init bash

# Force user to wait until initialization is complete
RUN echo "bash /workspaces/$REPO/.devcontainer/scripts/wait_for_initialized.sh" >> /home/$USERNAME/.bashrc

# Temporarily copy source code into the build container
COPY --chown=$USERNAME:$USERNAME . /setup

# Activate conda environment and pre-install pip dependencies
RUN cd /setup \
    && conda env create -f ./conda_environment.yaml \
    && sudo rm -rf /setup

# Activate conda environment on login
RUN echo "conda activate conda-env" >> /home/$USERNAME/.bashrc

#####
# Target for development codespace
#####
FROM base AS development

# Install npm/node + dependencies
ENV NPM_CONFIG_PREFIX=/home/$USERNAME/.npm-global
ENV PATH=/home/$USERNAME/.npm-global/bin:$PATH
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash - \
    && sudo apt-get install -y nodejs \
    && sudo npm install -g npm@latest
RUN npm i -g markdownlint-cli @prantlf/jsonlint markdown-link-check
