# Coffee Challenge

### Installing prereqs

(assuming Python >= 3.14 and `venv` module available)

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Running

```bash
gunicorn 'app:app'
```
