# Example Package

This is a simple example package. You can use
[Github-flavored Markdown](https://guides.github.com/features/mastering-markdown/)
to write your content.

# How to build package

This is a note for how to packaging a project into Pypi

- Root directory should contain __init__.py file, means it's a library
- Prepare pyporject.toml, project naming convension is like 'short_enough'
- python -m build 產生dist/ will load pyporject.toml
- pip install twine
- Prepare Pypi Account
- save .pypirc 
- twine upload --config-file .pypirc dist/*

package_dir={'mypkg': 'src/mypkg'},