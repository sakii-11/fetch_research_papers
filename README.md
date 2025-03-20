# Get Papers List

A Python program to fetch research papers from PubMed based on a user-specified query and filter papers with non-academic authors.

---

## Table of Contents
1. [Installation](#installation)
2. [Clone the Repository](#clone-the-repository)
3. [Install Dependencies](#install-dependencies)
4. [Run the Program](#run-the-program)
5. [Testing](#testing)
6. [Publishing to Test PyPI](#publishing-to-test-pypi)
7. [Dependencies Used](#dependencies)
8. [Tools Used](#tools-used)
9. [License](#license)

---

## Installation

### **1. Install Poetry**
If you don’t have Poetry installed, install it using:
```bash
pip install poetry
```

### **2. Clone the Repository**
Clone the repository to your local machine:

```bash
git clone https://github.com/sakii-11/fetch_research_papers.git
cd get_papers_list
```

### **3. Install Dependencies**
Install the required dependencies using Poetry:

```bash
poetry install
```

---

### **4. Run the Program**
To fetch papers based on a query and save the results to a CSV file, use:

```bash
poetry run python get_papers_list/cli.py "your query here" -f output.csv
```

For example:

```bash
poetry run python get_papers_list/cli.py "cancer treatment" -f papers.csv
```

Command-Line Options
-f or --file: Specify the output CSV file. If not provided, results are printed to the console.

-d or --debug: Enable debug mode for additional information during execution.

---

### **5. Testing **
Run Unit Tests
To run the unit tests, use:

```bash
poetry run python -m unittest discover tests
```

---

### **6. Publishing to Test PyPI**
This module has been published to Test PyPI for testing purposes. You can install it directly from Test PyPI using:

```bash
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ get-papers-list-pubmed
```

---

### **7. Dependencies**
requests: For making HTTP requests to the PubMed API.
pandas: For generating CSV output.
xml.etree.ElementTree: For parsing XML responses.

---

### **8. Tools Used**
Poetry: For dependency management and packaging.
PubMed API: For fetching research papers.
Test PyPI: For testing the package before publishing to the official PyPI.
ChatGPT: For assistance in brainstorming, code optimization, and debugging during development.

---

### **9. License**
This project is licensed under the MIT License. See the LICENSE file for details.

---

