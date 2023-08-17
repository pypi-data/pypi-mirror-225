# jupyterlab_recents

[![Extension status](https://img.shields.io/badge/status-ready-success 'ready to be used')](https://jupyterlab-contrib.github.io/)
[![Github Actions Status](https://github.com/jupyterlab-contrib/jupyterlab-recents/workflows/Build/badge.svg)](https://github.com/jupyterlab-contrib/jupyterlab-recents/actions?query=workflow%3ABuild)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/jupyterlab-contrib/jupyterlab-recents/master?urlpath=lab)
[![npm](https://img.shields.io/npm/v/@jlab-enhanced/recents)](https://www.npmjs.com/package/@jlab-enhanced/recents)
[![PyPI](https://img.shields.io/pypi/v/jupyterlab-recents)](https://pypi.org/project/jupyterlab-recents)
[![conda-forge](https://img.shields.io/conda/vn/conda-forge/jupyterlab-recents)](https://anaconda.org/conda-forge/jupyterlab-recents)

Track recent files and folders.

![JupyterLab Recents extension demonstration](https://raw.githubusercontent.com/jupyterlab-contrib/jupyterlab-recents/master/jupyterlab-recents.gif)

## Requirements

- JupyterLab >= 3.0 and Notebooo >= 7.0

## Install

To install the extension, execute:

```bash
pip install jupyterlab-recents
```

or

```bash
conda install -c conda-forge jupyterlab-recents
```

## Legacy Jupyterlab v1 Support

Via NPM:

```{bash}
jupyter labextension install jupyterlab-recents@1.0.1
```

Or use the tagged 1.0.0 release at:
https://github.com/jupyterlab-contrib/jupyterlab-recents/tree/v1.0.1

## Uninstall

To remove the extension, execute:

```bash
pip uninstall jupyterlab_recents
```

or

```bash
conda remove jupyterlab-recents
```

## Contributing

### Development install

Note: You will need NodeJS to build the extension package.

The `jlpm` command is JupyterLab's pinned version of
[yarn](https://yarnpkg.com/) that is installed with JupyterLab. You may use
`yarn` or `npm` in lieu of `jlpm` below.

```bash
# Clone the repo to your local environment
# Change directory to the jupyterlab_recents directory
# Install package in development mode
pip install -e "."
# Link your development version of the extension with JupyterLab
jupyter labextension develop . --overwrite
# Rebuild extension Typescript source after making changes
jlpm build
```

You can watch the source directory and run JupyterLab at the same time in different terminals to watch for changes in the extension's source and automatically rebuild the extension.

```bash
# Watch the source directory in one terminal, automatically rebuilding when needed
jlpm watch
# Run JupyterLab in another terminal
jupyter lab
```

With the watch command running, every saved change will immediately be built locally and available in your running JupyterLab. Refresh JupyterLab to load the change in your browser (you may need to wait several seconds for the extension to be rebuilt).

By default, the `jlpm build` command generates the source maps for this extension to make it easier to debug using the browser dev tools. To also generate source maps for the JupyterLab core extensions, you can run the following command:

```bash
jupyter lab build --minimize=False
```

### Development uninstall

```bash
pip uninstall jupyterlab_recents
```

In development mode, you will also need to remove the symlink created by `jupyter labextension develop`
command. To find its location, you can run `jupyter labextension list` to figure out where the `labextensions`
folder is located. Then you can remove the symlink named `@jlab-enhanced/recents` within that folder.

### Testing the extension

#### Integration tests

This extension uses [Playwright](https://playwright.dev/docs/intro) for the integration tests (aka user level tests).
More precisely, the JupyterLab helper [Galata](https://github.com/jupyterlab/jupyterlab/tree/master/galata) is used to handle testing the extension in JupyterLab.

More information are provided within the [ui-tests](./ui-tests/README.md) README.

### Packaging the extension

See [RELEASE](RELEASE.md)
