# Coffee Challenge

### Installing and running manuallly

#### Install

(assuming Python >= 3.14 and `venv` module available)

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Run

```bash
gunicorn 'app:app'
```

### Installing and Running in Docker (preferred)

(assuming Docker is available)

#### Build image

```bash
docker build -t coffee-challenge .
```

#### Run

```bash
docker run -it --rm -p 8000:8000 coffee-challenge
```

### Use

With the default run instructions, the app will be available at: http://localhost:8000

TODO
