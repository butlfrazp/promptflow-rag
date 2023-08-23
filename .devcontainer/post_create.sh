#!/bin/bash

# Setup conda environment

# Install the ffmodel package
conda run -n conda-env pip install promptflow promptflow-tools --extra-index-url https://azuremlsdktestpypi.azureedge.net/promptflow/

# Add CORS fix config for jupyter-notebook
cp ~/.jupyter/jupyter_server_config.py ~/.jupyter/jupyter_notebook_config.py

# Mark environment as initialized
bash /workspaces/askatt_spikes/.devcontainer/scripts/mark_initialized.sh
