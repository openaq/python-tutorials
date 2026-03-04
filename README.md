# OpenAQ Python SDK tutorial

This repo contains the tutorial for using OpenAQ Python SDK for users new to the package. The tutorial is exercises-driven and works as a primer to OpenAQ Python SDK. The SDK is used in this tutorial as the data fetcher for a data exploratory/analysis pipeline in Python.

The tutorial is a .py file made with marimo that is best used in a notebook environment. There are 2 ways you can access the tutorial:
- **Option 1 (recommended):** Fork and run the notebook on molab using this link.
- **Option 2:** Clone this repo and run the notebook locally on your computer using marimo or any Python notebooks of your choice.

Option 1 is straightforward: you only need to create a molab account to access and run the notebook on your own molab session.

If you go with Option 2 and use marimo: 
1. Make sure your Python version is >= 3.10, which is the latest version of Python that OpenAQ Python SDK supports
2. If you haven't, install marimo using `pip install marimo`
3. Clone the repo and from the root directory run `marimo edit openaq-python-tutorials.py`
4. In the terminal, a message will ask if you want to run the notebook in a sandboxed virtual environment with the notebook's dependencies. Type `y` for yes.
5. The notebook will automatically open in your browser with all required dependencies.

For your reference, the notebook makes use of these packages that you'll need to install on a non-marimo deployment:
```
altair==6.0.0
openaq==1.0.0rc2
pandas==3.0.1
wigglystuff==0.2.34
vegafusion>=2.0.3
vl-convert-python>=1.8.0
```
