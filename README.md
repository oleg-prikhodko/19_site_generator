# Encyclopedia

Collection of useful articles

# Quickstart

Pre rendered documentation lives [here](https://oleg-prikhodko.github.io/19_site_generator/).
Documentation could be easily generated from scratch.
Install required packages by running:
```bash
$ pip install -r requirements.txt
```

Then, launch __main.py__ to create documentation (it will be placed in the __docs__ directory) and serve it via [livereload](https://github.com/lepture/python-livereload). Docs will be available at __http://localhost:5500__

```bash
$ python main.py
```

Or you can download pre rendered docs and view it locally using builtin python http server

```bash
$ python -m http.server -d docs/
```

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
