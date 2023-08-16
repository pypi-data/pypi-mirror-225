import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    description="tkinter widgets",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=['tkinter', 'widget'],
    python_requires='>=3.11',
)
