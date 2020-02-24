## Installer for PureScript Python

1. Install `nodejs`. `npm` should be bundled.
2. `npm install -g purescript` and `npm install -g spago`.
3. Use `pip` and install repo.

```
npm install -g purescript
npm install -g spago
pip install git+https://github.com/purescript-python/installer
```

NOTE: installing this package sometimes takes a long time, because we will download  the binary files and invoke 2 `setup.py install`.
