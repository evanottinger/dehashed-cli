# dehashed-cli
An CLI tool to query DeHashed's API

## Installation

### With Pipenv
```
git clone git@github.com:evanottinger/dehashed-cli.git
cd dehashed-cli
pipenv install
./dehashed.py --email <dehashed-email> --api_key <dehashed-api-key> --query <dehashed-query> --size <results-to-return>
```

### With Pip
```
git clone git@github.com:evanottinger/dehashed-cli.git
cd dehashed-cli
pip install -r requirements.txt
./dehashed.py --email <dehashed-email> --api_key <dehashed-api-key> --query <dehashed-query> --size <results-to-return>
```