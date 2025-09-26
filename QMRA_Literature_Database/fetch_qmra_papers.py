#!/usr/bin/env python3
"""
QMRA Research Paper Fetcher
Fetches recent peer-reviewed QMRA papers from PubMed and formats them for EndNote
"""

import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import time
import re
import json
from typing import List, Dict, Optional
import argparse

class QMRAPaperFetcher:
    """Fetches QMRA research papers from PubMed"""

    def __init__(self, email: str = "user@example.com"):
        """
        Initialize the fetcher

        Args:
            email: Email for PubMed API (required for large requests)
        """
        self.base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
        self.email = email
        self.papers = []

    def build_search_query(self, years_back: int = 5) -> str:
        """
        Build comprehensive QMRA search query

        Args:
            years_back: Number of years to search back from current date
        """
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365 * years_back)

        # Comprehensive QMRA search terms
        qmra_terms = [
            '"Quantitative Microbial Risk Assessment"',
            '"QMRA"',
            '"Quantitative Microbiological Risk Assessment"',
            '"microbial risk assessment"[MeSH Terms]',
            '("dose response" AND ("pathogen" OR "microbial"))',
            '("exposure assessment" AND ("microbial" OR "pathogen"))',
            '("risk characterization" AND ("microbial" OR "pathogen"))',
            '("hazard identification" AND ("microbial" OR "pathogen"))'
        ]

        # Combine terms with OR
        query = f"({' OR '.join(qmra_terms)})"

        # Add date range
        date_range = f' AND ("{start_date.strftime("%Y/%m/%d")}"[PDAT] : "{end_date.strftime("%Y/%m/%d")}"[PDAT])'

        # Add publication type filters (peer-reviewed)
        pub_type = ' AND (Journal Article[PT] OR Review[PT] OR Systematic Review[PT] OR Meta-Analysis[PT])'

        full_query = query + date_range + pub_type

        return full_query

    def search_pubmed(self, query: str, max_results: int = 500) -> List[str]:
        """
        Search PubMed for papers matching the query

        Args:
            query: Search query
            max_results: Maximum number of results to fetch

        Returns:
            List of PubMed IDs
        """
        search_url = f"{self.base_url}esearch.fcgi"
        params = {
            'db': 'pubmed',
            'term': query,
            'retmax': max_results,
            'retmode': 'xml',
            'email': self.email
        }

        print(f"Searching PubMed with query: {query[:100]}...")
        response = requests.get(search_url, params=params)

        if response.status_code != 200:
            raise Exception(f"PubMed search failed: {response.status_code}")

        root = ET.fromstring(response.content)
        id_list = root.find('IdList')

        if id_list is None:
            return []

        pmids = [id_elem.text for id_elem in id_list.findall('Id')]
        print(f"Found {len(pmids)} papers")

        return pmids

    def fetch_paper_details(self, pmids: List[str]) -> List[Dict]:
        """
        Fetch detailed information for each paper

        Args:
            pmids: List of PubMed IDs

        Returns:
            List of paper details
        """
        papers = []

        # Process in batches to avoid API limits
        batch_size = 200
        for i in range(0, len(pmids), batch_size):
            batch = pmids[i:i+batch_size]
            print(f"Fetching details for papers {i+1} to {min(i+batch_size, len(pmids))}...")

            fetch_url = f"{self.base_url}efetch.fcgi"
            params = {
                'db': 'pubmed',
                'id': ','.join(batch),
                'retmode': 'xml',
                'email': self.email
            }

            response = requests.get(fetch_url, params=params)

            if response.status_code != 200:
                print(f"Warning: Failed to fetch batch {i//batch_size + 1}")
                continue

            root = ET.fromstring(response.content)

            for article in root.findall('.//PubmedArticle'):
                paper = self.parse_article(article)
                if paper:
                    papers.append(paper)

            # Be respectful to the API
            time.sleep(0.5)

        return papers

    def parse_article(self, article_elem: ET.Element) -> Optional[Dict]:
        """
        Parse article XML element to extract paper details

        Args:
            article_elem: XML element containing article data

        Returns:
            Dictionary with paper details or None if parsing fails
        """
        try:
            paper = {}

            # Get PMID
            pmid = article_elem.find('.//PMID')
            paper['pmid'] = pmid.text if pmid is not None else ''

            # Get article details
            article = article_elem.find('.//Article')
            if article is None:
                return None

            # Title
            title = article.find('.//ArticleTitle')
            paper['title'] = title.text if title is not None else ''

            # Authors
            authors = []
            for author in article.findall('.//Author'):
                lastname = author.find('LastName')
                forename = author.find('ForeName')
                if lastname is not None:
                    author_name = lastname.text
                    if forename is not None:
                        author_name = f"{lastname.text}, {forename.text}"
                    authors.append(author_name)
            paper['authors'] = authors

            # Journal
            journal = article.find('.//Journal/Title')
            paper['journal'] = journal.text if journal is not None else ''

            # Publication year
            pub_date = article.find('.//Journal/JournalIssue/PubDate/Year')
            if pub_date is None:
                pub_date = article.find('.//Journal/JournalIssue/PubDate/MedlineDate')
            paper['year'] = pub_date.text[:4] if pub_date is not None else ''

            # Volume and issue
            volume = article.find('.//Journal/JournalIssue/Volume')
            paper['volume'] = volume.text if volume is not None else ''

            issue = article.find('.//Journal/JournalIssue/Issue')
            paper['issue'] = issue.text if issue is not None else ''

            # Pages
            pagination = article.find('.//Pagination/MedlinePgn')
            paper['pages'] = pagination.text if pagination is not None else ''

            # Abstract
            abstract_texts = []
            for abstract in article.findall('.//Abstract/AbstractText'):
                text = abstract.text if abstract.text else ''
                label = abstract.get('Label', '')
                if label:
                    abstract_texts.append(f"{label}: {text}")
                else:
                    abstract_texts.append(text)
            paper['abstract'] = ' '.join(abstract_texts)

            # DOI
            for eloc_id in article.findall('.//ELocationID'):
                if eloc_id.get('EIdType') == 'doi':
                    paper['doi'] = eloc_id.text
                    break
            else:
                paper['doi'] = ''

            # Keywords
            keywords = []
            for keyword in article_elem.findall('.//MeshHeading/DescriptorName'):
                keywords.append(keyword.text)
            paper['keywords'] = keywords

            return paper

        except Exception as e:
            print(f"Error parsing article: {e}")
            return None

    def export_to_ris(self, papers: List[Dict], filename: str = "qmra_papers.ris"):
        """
        Export papers to RIS format (EndNote-friendly)

        Args:
            papers: List of paper dictionaries
            filename: Output filename
        """
        print(f"\nExporting {len(papers)} papers to RIS format...")

        with open(filename, 'w', encoding='utf-8') as f:
            for paper in papers:
                # Record type
                f.write("TY  - JOUR\n")

                # Title
                if paper.get('title'):
                    f.write(f"TI  - {paper['title']}\n")

                # Authors
                for author in paper.get('authors', []):
                    f.write(f"AU  - {author}\n")

                # Journal
                if paper.get('journal'):
                    f.write(f"JO  - {paper['journal']}\n")

                # Year
                if paper.get('year'):
                    f.write(f"PY  - {paper['year']}\n")

                # Volume
                if paper.get('volume'):
                    f.write(f"VL  - {paper['volume']}\n")

                # Issue
                if paper.get('issue'):
                    f.write(f"IS  - {paper['issue']}\n")

                # Pages
                if paper.get('pages'):
                    f.write(f"SP  - {paper['pages']}\n")

                # Abstract
                if paper.get('abstract'):
                    # RIS format requires abstracts to be on one line
                    abstract = paper['abstract'].replace('\n', ' ')
                    f.write(f"AB  - {abstract}\n")

                # Keywords
                for keyword in paper.get('keywords', []):
                    f.write(f"KW  - {keyword}\n")

                # DOI
                if paper.get('doi'):
                    f.write(f"DO  - {paper['doi']}\n")

                # Database provider
                f.write("DP  - PubMed\n")

                # Database ID
                if paper.get('pmid'):
                    f.write(f"AN  - {paper['pmid']}\n")

                # End of record
                f.write("ER  - \n\n")

        print(f"Successfully exported to {filename}")

    def export_to_json(self, papers: List[Dict], filename: str = "qmra_papers.json"):
        """
        Export papers to JSON format for further processing

        Args:
            papers: List of paper dictionaries
            filename: Output filename
        """
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(papers, f, indent=2, ensure_ascii=False)

        print(f"Successfully exported to {filename}")

    def generate_summary_report(self, papers: List[Dict], filename: str = "qmra_papers_summary.txt"):
        """
        Generate a summary report of fetched papers

        Args:
            papers: List of paper dictionaries
            filename: Output filename
        """
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("QMRA Research Papers Summary Report\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Total papers found: {len(papers)}\n")
            f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            # Year distribution
            year_counts = {}
            for paper in papers:
                year = paper.get('year', 'Unknown')
                year_counts[year] = year_counts.get(year, 0) + 1

            f.write("Papers by Year:\n")
            for year in sorted(year_counts.keys(), reverse=True):
                f.write(f"  {year}: {year_counts[year]} papers\n")

            f.write("\n" + "=" * 50 + "\n")
            f.write("Paper List (sorted by year):\n")
            f.write("=" * 50 + "\n\n")

            # Sort papers by year (newest first)
            sorted_papers = sorted(papers,
                                  key=lambda x: x.get('year', '0000'),
                                  reverse=True)

            for i, paper in enumerate(sorted_papers, 1):
                f.write(f"{i}. {paper.get('title', 'No title')}\n")

                # Authors (limit to first 3 for readability)
                authors = paper.get('authors', [])
                if authors:
                    author_str = '; '.join(authors[:3])
                    if len(authors) > 3:
                        author_str += f" et al. ({len(authors)} authors)"
                    f.write(f"   Authors: {author_str}\n")

                f.write(f"   Journal: {paper.get('journal', 'Unknown')}\n")
                f.write(f"   Year: {paper.get('year', 'Unknown')}\n")

                if paper.get('doi'):
                    f.write(f"   DOI: {paper['doi']}\n")

                if paper.get('pmid'):
                    f.write(f"   PubMed ID: {paper['pmid']}\n")
                    f.write(f"   Link: https://pubmed.ncbi.nlm.nih.gov/{paper['pmid']}/\n")

                f.write("\n")

        print(f"Summary report saved to {filename}")

    def fetch_all(self, years_back: int = 5, max_results: int = 500):
        """
        Main method to fetch all QMRA papers

        Args:
            years_back: Number of years to search back
            max_results: Maximum number of results
        """
        print("QMRA Paper Fetcher")
        print("=" * 50)

        # Build and execute search
        query = self.build_search_query(years_back)
        pmids = self.search_pubmed(query, max_results)

        if not pmids:
            print("No papers found!")
            return []

        # Fetch details
        self.papers = self.fetch_paper_details(pmids)

        print(f"\nSuccessfully fetched {len(self.papers)} papers")

        return self.papers


def main():
    """Main function to run the QMRA paper fetcher"""

    parser = argparse.ArgumentParser(description='Fetch QMRA research papers from PubMed')
    parser.add_argument('--years', type=int, default=5,
                       help='Number of years to search back (default: 5)')
    parser.add_argument('--max-results', type=int, default=500,
                       help='Maximum number of results to fetch (default: 500)')
    parser.add_argument('--email', type=str, default='user@example.com',
                       help='Email for PubMed API (recommended for large requests)')
    parser.add_argument('--output-prefix', type=str, default='qmra_papers',
                       help='Prefix for output files (default: qmra_papers)')

    args = parser.parse_args()

    # Initialize fetcher
    fetcher = QMRAPaperFetcher(email=args.email)

    # Fetch papers
    papers = fetcher.fetch_all(years_back=args.years, max_results=args.max_results)

    if papers:
        # Export to different formats
        fetcher.export_to_ris(papers, f"{args.output_prefix}.ris")
        fetcher.export_to_json(papers, f"{args.output_prefix}.json")
        fetcher.generate_summary_report(papers, f"{args.output_prefix}_summary.txt")

        print(f"\nAll files have been saved with prefix '{args.output_prefix}'")
        print("Files generated:")
        print(f"  - {args.output_prefix}.ris (EndNote import)")
        print(f"  - {args.output_prefix}.json (JSON format)")
        print(f"  - {args.output_prefix}_summary.txt (Human-readable summary)")
    else:
        print("No papers were fetched. Please check your search criteria.")


if __name__ == "__main__":
    main()