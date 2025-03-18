import argparse
from .papers_fetcher import fetch_papers, filter_papers, save_to_csv

def main():
    parser = argparse.ArgumentParser(description="Fetch research papers from PubMed.")
    parser.add_argument("query", type=str, help="PubMed search query.")
    parser.add_argument("-f", "--file", type=str, help="Output CSV filename.")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode.")
    args = parser.parse_args()

    if args.debug:
        print(f"Debug mode: Fetching papers for query: {args.query}")

    paper_ids = fetch_papers(args.query)
    filtered_papers = filter_papers(paper_ids)

    if args.file:
        save_to_csv(filtered_papers, args.file)
    else:
        for paper in filtered_papers:
            print(paper)

if __name__ == "__main__":
    main()