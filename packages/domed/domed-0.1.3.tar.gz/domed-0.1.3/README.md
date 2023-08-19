# domed

The `domed` package provides a Pythonic approach for manipulating the DOM structure of a web document.
It is intended for code running in the browser using [pyodide](https://pyodide.org/en/stable/) or [pyscript](https://pyscript.net/).
A typical usage is for single-page applications with dynamically changing page content.
The name is an abbreviation for DOM editing.

The package provides an API that is greatly inspired by the (dominate)[https://github.com/Knio/dominate] package.
The main difference is that dominate is intended to run on the server.
It creates a datastructure representing the DOM tree.
This datastructure can then be converted to HTML code as a string, which can be sent to a client.

Domed is intended for running in the browser.
It manipulates the DOM tree directly, without producing any HTML text.
This is achieved by wrapping the Javascript DOM structure with Python objects.

The API allows the user to build the hierarchical structure of a DOM tree using context managers.
It allows setting attributes, and adding event handlers.
Through DOM queries, a suitable parent node for the created structure can be selected.
It also allows a clearing children of a DOM node.

## Installation

See the documentation for installing packages from PyPI in pyodide and pyscript, respectively.

## Usage examples

To be added.