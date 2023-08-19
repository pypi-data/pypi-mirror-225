# voila-vuetify-tuwien


## Installation

`voila-vuetify-tuwien-template` can be installed from PyPI

```
pip install voila-vuetify-template-tuwien
```



## Usage

To use the `vuetify` template, just pass `--template=vuetify-default-tuwien` to the `voila` command line.

To open all notebooks in your working folder use:

```
voila . --template=vuetify-default-tuwien
```

To open a specific notebook (for example `Histogram-Sliders.ipynb`) use:

```
voila Histogram-Sliders.ipynb --template=vuetify-default-tuwien
```

## Uploading project to PyPi

1. Delete last locally built version:

```
rm -rf dist/* 
```

2. Build python package:
```
python -m build 
```

3. Upload project to PyPi:
```
twine upload dist/*
```
