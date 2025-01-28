
# list available commands
default:
    @just --list  

# requirements:
#     source ./.venv/bin/activate
#     pip install -r requirements.txt
#

test:
    #!/usr/bin/env bash
    set -euo pipefail

    export PYTHONPATH=$PYTHONPATH:. 
    export DJANGO_SETTINGS_MODULE=microweb.settings
    pytest tests
