# {{ cookiecutter.extension_name }}

{{ cookiecutter.project_short_description }}


## Prerequisites

* JupyterLab

## Installation

To install using pip:

```bash
jupyter labextension install {{ cookiecutter.extension_name }}
```

## Development

For a development install (requires npm version 4 or later), do the following in the repository directory:

```bash
# Clone the repo to your local environment
# Move to {{ cookiecutter.extension_name }} directory
# Install dependencies
npm install
# Install your development version of the extension
jupyter labextension install .
```

You run JupyterLab in watch mode to watch for changes in the extension's source and automatically rebuild.

```bash
# Run jupyterlab in watch mode
jupyter lab --watch
```

Now every change will be built locally and bundled into JupyterLab. Be sure to refresh your browser page after saving file changes to reload the extension (note: you'll need to wait for webpack to finish, which can take 10s+ at times).

### Uninstall

```bash
jupyter labextension uninstall {{ cookiecutter.extension_name }}
```

