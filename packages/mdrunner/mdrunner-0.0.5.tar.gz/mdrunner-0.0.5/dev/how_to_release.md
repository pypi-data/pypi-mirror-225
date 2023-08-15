# How to release this lib
For details see the description in

https://packaging.python.org/en/latest/tutorials/packaging-projects/

## 1. Update the lib version
update the pyproject.toml file
```
version = "x.y.z"
```

## 1. Generate the lib
based on the lib configuration in pyproject.toml
```
py -m pip install --upgrade pip
py -m pip install --upgrade build
python -m build
```

## 2. Publish to PyPi
upload the generated package files from the dist folder
```
py -m pip install --upgrade twine
python -m twine upload dist/*
```

## 3. Installing the latest uploaded package
```
python -m pip install mdrunner
```
