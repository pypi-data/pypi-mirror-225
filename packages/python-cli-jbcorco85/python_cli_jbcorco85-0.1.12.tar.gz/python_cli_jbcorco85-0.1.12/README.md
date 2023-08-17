# Start virtual environment
python3 -m venv env
source env/bin/activate

Increment version in pyproject.toml
poetry build
poetry publish -r testpypi

# pip install
pip3 install -i https://test.pypi.org/simple/ python-cli
pip3 list

# test build
python3 -m pyton_cli
python python_cli

# uninstall
pip3 uninstall python_cli
pip3 list

