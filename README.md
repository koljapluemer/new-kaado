## Setup

### Adding dependencies

* add the library to `requirements.in`
* run `pip-compile requirements.in > requirements.txt`
* run `pip install -r requirements.txt `

*combined*:
```
pip-compile requirements.in > requirements.txt && pip install -r requirements.txt
```