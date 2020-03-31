from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="standup-notes", 
    version="0.0.1",
    author="Mike Martino",
    author_email="mikemartino86@gmail.com",
    description="This is small tool for managing daily standup notes and getting them ready to be copy/pasted into another platform (i.e. virtual standup in Mattermost)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://www.mikemartino.ca",
    packages=find_packages(),
    install_requires=['python-editor==1.0.4', 'pyperclip==1.8.0'],
    entry_points={
          'console_scripts': [
              'standup-notes = standup_notes.__main__:main'
          ]
      },
    package_data={
        "standup_notes": ["resources/*.template"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)

