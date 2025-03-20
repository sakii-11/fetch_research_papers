import requests
import pandas as pd
from typing import List, Dict, Optional
from datetime import datetime
import xml.etree.ElementTree as ET


# Constants
PUBMED_API_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"  #for searching the PubMed database
PUBMED_FETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi" #for fetching detailed records based on PubMed IDs

def fetch_papers(query: str, max_results: int = 100) -> List[Dict]:
    """
    Fetch papers from PubMed based on a query.
    """
    search_params = {
        "db": "pubmed",
        "term": query,
        "retmax": max_results,
        "retmode": "json",
        "sort": "relevance"
    }
    response = requests.get(PUBMED_API_URL, params=search_params)
    response.raise_for_status()
    data = response.json()
    paper_ids = data.get("esearchresult", {}).get("idlist", [])
    return paper_ids

def fetch_paper_details(paper_id: str) -> Optional[Dict]:
    """
    Fetch details for a single paper using its PubMed ID.
    """
    fetch_params = {
        "db": "pubmed",
        "id": paper_id,
        "retmode": "xml"
    }
    response = requests.get(PUBMED_FETCH_URL, params=fetch_params)
    response.raise_for_status()
    return response.text  # Parse XML response for details

def is_non_academic_affiliation(affiliation: str) -> bool:
    """
    Heuristic to identify non-academic affiliations.
    """
    keywords = ["university", "college", "institute", "lab", "hospital"]
    return not any(keyword in affiliation.lower() for keyword in keywords)

def parse_paper_details(xml_content: str) -> Optional[Dict]:
    """
    Parse XML content to extract paper details.
    """
    try:
        root = ET.fromstring(xml_content)
        paper_details = {
            "PubmedID": None,
            "Title": None,
            "Publication Date": None,
            "Authors": [],
            "Affiliations": [],
            "Corresponding Author Email": None
        }

        # Extract PubmedID
        pubmed_id = root.find(".//MedlineCitation/PMID")
        if pubmed_id is not None:
            paper_details["PubmedID"] = pubmed_id.text

        # Extract Title
        title = root.find(".//ArticleTitle")
        if title is not None:
            paper_details["Title"] = title.text

        # Extract Publication Date
        pub_date = root.find(".//PubDate")
        if pub_date is not None:
            year = pub_date.find("Year")
            month = pub_date.find("Month")
            day = pub_date.find("Day")
            if year is not None and month is not None and day is not None:
                paper_details["Publication Date"] = f"{year.text}-{month.text}-{day.text}"

        # Extract Authors and Affiliations
        authors = root.findall(".//Author")
        for author in authors:
            last_name = author.find("LastName")
            fore_name = author.find("ForeName")
            if last_name is not None and fore_name is not None:
                author_name = f"{fore_name.text} {last_name.text}"
                paper_details["Authors"].append(author_name)

            affiliation = author.find("AffiliationInfo/Affiliation")
            if affiliation is not None:
                paper_details["Affiliations"].append(affiliation.text)

        # Extract Corresponding Author Email
        corresponding_author = root.find(".//Author[@ValidYN='Y']")
        if corresponding_author is not None:
            email = corresponding_author.find("Email")
            if email is not None:
                paper_details["Corresponding Author Email"] = email.text

        return paper_details
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
        return None
      
      
def filter_papers(paper_ids: List[str]) -> List[Dict]:
    """
    Filter papers to include only those with non-academic authors.
    """
    filtered_papers = []
    for paper_id in paper_ids:
        details = fetch_paper_details(paper_id)
        if details:
            parsed_details = parse_paper_details(details)
            if parsed_details and "Affiliations" in parsed_details:  
                if any(is_non_academic_affiliation(aff) for aff in parsed_details["Affiliations"]):
                    filtered_papers.append(parsed_details)
    return filtered_papers


def save_to_csv(papers: List[Dict], filename: str) -> None:
    """
    Save the filtered papers to a CSV file.
    If the filename does not end with '.csv', append '.csv' to the filename.
    """
    if not filename.endswith(".csv"):
        filename += ".csv"  

    df = pd.DataFrame(papers)
    df.to_csv(filename, index=False)
    print(f"Results saved to {filename}.")
