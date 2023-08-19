

## Building

Install build tools
```bash
pip3 install --upgrade build
pip3 install virtualenv
```

Go to project root directory and run build module

```bash
python3 -m build
```

Find the whl file and install it globally (for testing)
```bash
pip3 install --force-reinstall dist/wesync-0.0.1-py3-none-any.whl
```

Test the package:
```bash
wesync --help
python3
>>> import wesync

python3 -m wesync
```
