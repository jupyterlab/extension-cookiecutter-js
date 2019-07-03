# {{ cookiecutter.extension_name }}

{{ cookiecutter.project_short_description }}


## Requirements

* JupyterLab >= 0.30.0 

## Install

```bash
jupyter labextension install {{ cookiecutter.extension_name }}
```

## Contributing

### Install

The `jlpm` command is JupyterLab's pinned version of
[yarn](https://yarnpkg.com/) that is installed with JupyterLab. You may use
`yarn` or `npm` in lieu of `jlpm` below.

```bash
# Clone the repo to your local environment
# Move to {{ cookiecutter.extension_name }} directory
# Install dependencies
jlpm
# Link your development version of the extension with JupyterLab
jupyter labextension link .
# Rebuild JupyterLab after making any changes
jupyter lab build
```

You can run JupyterLab in watch mode to watch for changes in the extension's source and automatically rebuild the application.

```bash
# Run jupyterlab in watch mode in one terminal tab
jupyter lab --watch
```

### Uninstall

```bash
jupyter labextension uninstall {{ cookiecutter.extension_name }}
```

