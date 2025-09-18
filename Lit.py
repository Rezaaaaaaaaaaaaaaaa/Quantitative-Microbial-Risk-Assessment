#!/usr/bin/env python3
"""
Quantitative Microbial Risk Assessment (QMRA) Literature and Regulation Scraper
Focuses on New Zealand context and recent research publications.
"""

import requests
import pandas as pd
import json
import time
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re
import logging
from urllib.parse import urlencode, quote_plus, urljoin
import os
from typing import List, Dict, Any
import csv
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
from functools import partial
import asyncio
import aiohttp
import PyPDF2
import pdfplumber
from scholarly import scholarly
import io
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class QMRALiteratureScraper:
    """Scraper for QMRA research literature and NZ regulations."""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.results = []
        self.lock = threading.Lock()
        self.max_workers = 5
        self.driver = None
        self._setup_selenium()

    def _setup_selenium(self):
        """Setup Selenium WebDriver for JavaScript-heavy sites."""
        try:
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")

            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            logger.info("Selenium WebDriver initialized successfully")
        except Exception as e:
            logger.warning(f"Could not initialize Selenium: {e}. Some features may be limited.")

    def search_pubmed(self, keywords: List[str], days_back: int = 365) -> List[Dict]:
        """Search PubMed for QMRA-related publications."""
        logger.info("Searching PubMed for QMRA literature...")

        base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"

        # Combine keywords for QMRA and NZ context
        search_terms = [
            "quantitative microbial risk assessment",
            "QMRA",
            "microbial risk assessment",
            "pathogen risk assessment",
            "waterborne pathogens",
            "foodborne pathogens"
        ]

        nz_terms = [
            "New Zealand",
            "NZ",
            "Aotearoa",
            "New Zealand water",
            "New Zealand food safety"
        ]

        # Create comprehensive search query
        main_query = " OR ".join([f'"{term}"' for term in search_terms])
        nz_query = " OR ".join([f'"{term}"' for term in nz_terms])

        # Date filter for recent publications
        date_filter = f"({(datetime.now() - timedelta(days=days_back)).strftime('%Y/%m/%d')}[PDAT] : 3000[PDAT])"

        final_query = f"(({main_query}) AND ({nz_query})) AND {date_filter}"

        params = {
            'db': 'pubmed',
            'term': final_query,
            'retmax': 100,
            'retmode': 'xml'
        }

        try:
            response = self.session.get(base_url, params=params)
            response.raise_for_status()

            root = ET.fromstring(response.content)
            id_list = [id_elem.text for id_elem in root.findall('.//Id')]

            if not id_list:
                logger.info("No PubMed results found for the specified criteria")
                return []

            # Fetch detailed information for each paper
            return self._fetch_pubmed_details(id_list)

        except Exception as e:
            logger.error(f"Error searching PubMed: {e}")
            return []

    def _fetch_pubmed_details(self, id_list: List[str]) -> List[Dict]:
        """Fetch detailed information for PubMed articles with enhanced data extraction."""
        if not id_list:
            return []

        base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

        params = {
            'db': 'pubmed',
            'id': ','.join(id_list),
            'retmode': 'xml'
        }

        try:
            response = self.session.get(base_url, params=params)
            response.raise_for_status()

            root = ET.fromstring(response.content)
            articles = []

            for article in root.findall('.//PubmedArticle'):
                try:
                    title_elem = article.find('.//ArticleTitle')
                    title = title_elem.text if title_elem is not None else "No title"

                    # Get full abstract with multiple parts if available
                    abstract_parts = []
                    for abstract_elem in article.findall('.//AbstractText'):
                        label = abstract_elem.get('Label', '')
                        text = abstract_elem.text or ""
                        if label:
                            abstract_parts.append(f"{label}: {text}")
                        else:
                            abstract_parts.append(text)

                    full_abstract = "\n\n".join(abstract_parts) if abstract_parts else "No abstract available"

                    # Get authors with affiliations
                    authors = []
                    affiliations = []
                    for author in article.findall('.//Author'):
                        lastname = author.find('.//LastName')
                        forename = author.find('.//ForeName')
                        if lastname is not None and forename is not None:
                            authors.append(f"{forename.text} {lastname.text}")

                        # Get affiliations
                        for affiliation in author.findall('.//Affiliation'):
                            if affiliation.text:
                                affiliations.append(affiliation.text)

                    # Get keywords
                    keywords = []
                    for keyword in article.findall('.//Keyword'):
                        if keyword.text:
                            keywords.append(keyword.text)

                    # Get MeSH terms
                    mesh_terms = []
                    for mesh in article.findall('.//DescriptorName'):
                        if mesh.text:
                            mesh_terms.append(mesh.text)

                    # Get publication date with more detail
                    pub_date = article.find('.//PubDate')
                    year = pub_date.find('.//Year').text if pub_date is not None and pub_date.find('.//Year') is not None else "Unknown"
                    month = pub_date.find('.//Month').text if pub_date is not None and pub_date.find('.//Month') is not None else ""
                    day = pub_date.find('.//Day').text if pub_date is not None and pub_date.find('.//Day') is not None else ""

                    pub_date_full = f"{year}"
                    if month:
                        pub_date_full += f"-{month}"
                    if day:
                        pub_date_full += f"-{day}"

                    # Get journal details
                    journal_elem = article.find('.//Journal/Title')
                    journal = journal_elem.text if journal_elem is not None else "Unknown"

                    iso_abbrev = article.find('.//Journal/ISOAbbreviation')
                    journal_iso = iso_abbrev.text if iso_abbrev is not None else ""

                    # Get volume and issue
                    volume = article.find('.//Volume')
                    volume_text = volume.text if volume is not None else ""

                    issue = article.find('.//Issue')
                    issue_text = issue.text if issue is not None else ""

                    # Get pagination
                    pages = article.find('.//MedlinePgn')
                    pages_text = pages.text if pages is not None else ""

                    # Get all article IDs
                    doi = ""
                    pmc_id = ""
                    pmid = ""

                    for article_id in article.findall('.//ArticleId'):
                        id_type = article_id.get('IdType', '')
                        if id_type == 'doi':
                            doi = article_id.text
                        elif id_type == 'pmc':
                            pmc_id = article_id.text
                        elif id_type == 'pubmed':
                            pmid = article_id.text

                    # Try to get citation count and other metrics
                    citation_count = ""

                    # Try to fetch full text if DOI is available
                    full_text_content = ""
                    if doi:
                        full_text_content = self._try_fetch_full_text(doi)

                    articles.append({
                        'source': 'PubMed',
                        'title': title,
                        'authors': ', '.join(authors),
                        'author_affiliations': '; '.join(list(set(affiliations))),
                        'journal': journal,
                        'journal_iso': journal_iso,
                        'volume': volume_text,
                        'issue': issue_text,
                        'pages': pages_text,
                        'year': year,
                        'publication_date': pub_date_full,
                        'abstract': full_abstract,
                        'keywords': ', '.join(keywords),
                        'mesh_terms': ', '.join(mesh_terms),
                        'doi': doi,
                        'pmid': pmid,
                        'pmc_id': pmc_id,
                        'citation_count': citation_count,
                        'full_text_preview': full_text_content[:1000] + "..." if full_text_content else "",
                        'url': f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/" if pmid else "",
                        'doi_url': f"https://doi.org/{doi}" if doi else "",
                        'pmc_url': f"https://www.ncbi.nlm.nih.gov/pmc/articles/{pmc_id}/" if pmc_id else "",
                        'scraped_date': datetime.now().isoformat()
                    })

                except Exception as e:
                    logger.warning(f"Error parsing PubMed article: {e}")
                    continue

            logger.info(f"Retrieved {len(articles)} detailed articles from PubMed")
            return articles

        except Exception as e:
            logger.error(f"Error fetching PubMed details: {e}")
            return []

    def _try_fetch_full_text(self, doi: str) -> str:
        """Try to fetch full text content from various sources."""
        try:
            # Try PMC first
            pmc_url = f"https://www.ncbi.nlm.nih.gov/pmc/articles/PMC{doi.split('/')[-1]}/"
            response = self.session.get(pmc_url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                # Extract main content
                content_div = soup.find('div', class_='tsec')
                if content_div:
                    return content_div.get_text()[:2000]

            # Try DOI redirect
            doi_url = f"https://doi.org/{doi}"
            response = self.session.get(doi_url, timeout=10, allow_redirects=True)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                # Look for article content
                for content_selector in ['article', '.article-body', '.content', '.main-content']:
                    content = soup.select_one(content_selector)
                    if content:
                        return content.get_text()[:2000]

        except Exception as e:
            logger.debug(f"Could not fetch full text for DOI {doi}: {e}")

        return ""

    def search_google_scholar(self, keywords: List[str], num_results: int = 20) -> List[Dict]:
        """Search Google Scholar for QMRA-related publications."""
        logger.info("Searching Google Scholar for QMRA literature...")

        # Note: Google Scholar has anti-bot measures, so this is a simplified approach
        # For production use, consider using scholarly library or SerpAPI

        search_query = "quantitative microbial risk assessment New Zealand"
        encoded_query = quote_plus(search_query)

        url = f"https://scholar.google.com/scholar?q={encoded_query}&hl=en&as_sdt=0%2C5&as_ylo=2020"

        try:
            time.sleep(2)  # Be respectful to the server
            response = self.session.get(url)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')
            articles = []

            for result in soup.find_all('div', class_='gs_ri')[:num_results]:
                try:
                    title_elem = result.find('h3', class_='gs_rt')
                    if not title_elem:
                        continue

                    title = title_elem.get_text()

                    # Get link
                    link_elem = title_elem.find('a')
                    link = link_elem.get('href') if link_elem else ""

                    # Get authors and publication info
                    info_elem = result.find('div', class_='gs_a')
                    info = info_elem.get_text() if info_elem else ""

                    # Get snippet
                    snippet_elem = result.find('div', class_='gs_rs')
                    snippet = snippet_elem.get_text() if snippet_elem else ""

                    articles.append({
                        'source': 'Google Scholar',
                        'title': title.strip(),
                        'info': info.strip(),
                        'snippet': snippet.strip(),
                        'url': link,
                        'scraped_date': datetime.now().isoformat()
                    })

                except Exception as e:
                    logger.warning(f"Error parsing Google Scholar result: {e}")
                    continue

            logger.info(f"Retrieved {len(articles)} articles from Google Scholar")
            return articles

        except Exception as e:
            logger.error(f"Error searching Google Scholar: {e}")
            return []

    def _scrape_single_url(self, source_name: str, url: str) -> Dict:
        """Scrape a single URL with enhanced content extraction."""
        try:
            # Handle PDF files
            if url.lower().endswith('.pdf'):
                return self._extract_pdf_content(source_name, url)

            response = self.session.get(url, timeout=15)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')
            title = soup.find('title').get_text() if soup.find('title') else url

            # Extract metadata
            meta_description = ""
            meta_keywords = ""
            for meta in soup.find_all('meta'):
                if meta.get('name') == 'description':
                    meta_description = meta.get('content', '')
                elif meta.get('name') == 'keywords':
                    meta_keywords = meta.get('content', '')

            # Get full text content
            full_text = soup.get_text()
            text_content_lower = full_text.lower()

            qmra_keywords = [
                'microbial', 'pathogen', 'risk assessment', 'water quality',
                'food safety', 'contamination', 'qmra', 'dose response',
                'exposure assessment', 'hazard identification', 'risk characterization',
                'drinking water', 'foodborne illness', 'waterborne disease',
                'public health', 'environmental health'
            ]

            # Check relevance
            relevant_keywords_found = [kw for kw in qmra_keywords if kw in text_content_lower]

            if relevant_keywords_found:
                # Extract structured content
                headings = [h.get_text().strip() for h in soup.find_all(['h1', 'h2', 'h3', 'h4'])]

                # Try to find main content area
                main_content = ""
                for content_selector in [
                    'main', '.main-content', '.content', '.body-content',
                    'article', '.article-body', '.text-content', '.page-content'
                ]:
                    content_elem = soup.select_one(content_selector)
                    if content_elem:
                        main_content = content_elem.get_text()[:3000]
                        break

                if not main_content:
                    main_content = full_text[:3000]

                # Extract links to related documents
                related_links = []
                for link in soup.find_all('a', href=True):
                    href = link.get('href')
                    link_text = link.get_text().strip()
                    if href and any(ext in href.lower() for ext in ['.pdf', '.doc', '.docx']) and len(link_text) > 5:
                        full_url = urljoin(url, href)
                        related_links.append(f"{link_text}: {full_url}")

                return {
                    'source': f"NZ Government - {source_name}",
                    'title': title.strip(),
                    'url': url,
                    'meta_description': meta_description,
                    'meta_keywords': meta_keywords,
                    'headings': ' | '.join(headings[:10]),
                    'main_content': main_content,
                    'relevant_keywords': ', '.join(relevant_keywords_found),
                    'related_documents': ' | '.join(related_links[:5]),
                    'content_preview': soup.get_text()[:500] + "...",
                    'full_content_length': len(full_text),
                    'scraped_date': datetime.now().isoformat()
                }
        except Exception as e:
            logger.warning(f"Error accessing {url}: {e}")
            return None

    def _extract_pdf_content(self, source_name: str, pdf_url: str) -> Dict:
        """Extract content from PDF documents."""
        try:
            response = self.session.get(pdf_url, timeout=20)
            response.raise_for_status()

            # Try with pdfplumber first (better for structured PDFs)
            try:
                pdf_file = io.BytesIO(response.content)
                with pdfplumber.open(pdf_file) as pdf:
                    text_content = ""
                    tables = []

                    for page_num, page in enumerate(pdf.pages[:50]):  # Limit to first 50 pages
                        page_text = page.extract_text()
                        if page_text:
                            text_content += f"\n--- Page {page_num + 1} ---\n{page_text}"

                        # Extract tables
                        page_tables = page.extract_tables()
                        if page_tables:
                            for table in page_tables:
                                tables.append(table)

                    # Extract key sections
                    sections = self._extract_pdf_sections(text_content)

                    return {
                        'source': f"NZ Government - {source_name}",
                        'title': f"PDF Document - {pdf_url.split('/')[-1]}",
                        'url': pdf_url,
                        'document_type': 'PDF',
                        'total_pages': len(pdf.pages),
                        'text_content': text_content[:5000] + "..." if len(text_content) > 5000 else text_content,
                        'extracted_sections': sections,
                        'tables_found': len(tables),
                        'table_preview': str(tables[0][:3]) if tables else "",
                        'content_preview': text_content[:500] + "...",
                        'scraped_date': datetime.now().isoformat()
                    }

            except Exception:
                # Fallback to PyPDF2
                pdf_file = io.BytesIO(response.content)
                reader = PyPDF2.PdfReader(pdf_file)
                text_content = ""

                for page_num, page in enumerate(reader.pages[:50]):
                    text_content += f"\n--- Page {page_num + 1} ---\n{page.extract_text()}"

                sections = self._extract_pdf_sections(text_content)

                return {
                    'source': f"NZ Government - {source_name}",
                    'title': f"PDF Document - {pdf_url.split('/')[-1]}",
                    'url': pdf_url,
                    'document_type': 'PDF',
                    'total_pages': len(reader.pages),
                    'text_content': text_content[:5000] + "..." if len(text_content) > 5000 else text_content,
                    'extracted_sections': sections,
                    'content_preview': text_content[:500] + "...",
                    'scraped_date': datetime.now().isoformat()
                }

        except Exception as e:
            logger.warning(f"Error extracting PDF content from {pdf_url}: {e}")
            return None

    def _extract_pdf_sections(self, text_content: str) -> Dict:
        """Extract structured sections from PDF text."""
        sections = {
            'executive_summary': '',
            'introduction': '',
            'methodology': '',
            'results': '',
            'discussion': '',
            'conclusion': '',
            'references': '',
            'regulations': '',
            'standards': ''
        }

        text_lower = text_content.lower()

        # Define section patterns
        section_patterns = {
            'executive_summary': [r'executive summary', r'summary', r'abstract'],
            'introduction': [r'introduction', r'background'],
            'methodology': [r'methodology', r'methods', r'approach'],
            'results': [r'results', r'findings'],
            'discussion': [r'discussion', r'analysis'],
            'conclusion': [r'conclusion', r'recommendations'],
            'references': [r'references', r'bibliography'],
            'regulations': [r'regulation', r'compliance', r'legal framework'],
            'standards': [r'standards', r'guidelines', r'criteria']
        }

        # Extract sections based on patterns
        for section_name, patterns in section_patterns.items():
            for pattern in patterns:
                match = re.search(rf'{pattern}[\s\S]{{0,2000}}', text_lower)
                if match:
                    sections[section_name] = match.group(0)[:1000]
                    break

        return {k: v for k, v in sections.items() if v}

    def search_nz_government_sources(self) -> List[Dict]:
        """Search New Zealand government sources for QMRA regulations and guidelines."""
        logger.info("Searching NZ government sources for QMRA regulations...")

        sources = [
            {
                'name': 'Ministry of Health',
                'search_urls': [
                    'https://www.health.govt.nz/our-work/environmental-health/water-and-wastewater',
                    'https://www.health.govt.nz/publication/drinking-water-standards-new-zealand-2005-revised-2018',
                    'https://www.health.govt.nz/system/files/documents/publications/drinking-water-standards-new-zealand-2005-revised-2018-dec18.pdf',
                    'https://www.health.govt.nz/our-work/environmental-health/food-safety',
                    'https://www.health.govt.nz/publication/food-safety-risk-management-measures-guidance-local-authorities'
                ]
            },
            {
                'name': 'Taumata Arowai',
                'search_urls': [
                    'https://www.taumataarowai.govt.nz/for-suppliers/drinking-water-regulatory-framework/',
                    'https://www.taumataarowai.govt.nz/for-suppliers/drinking-water-standards/',
                    'https://www.taumataarowai.govt.nz/publications/',
                    'https://www.taumataarowai.govt.nz/assets/Uploads/Publications/Drinking-Water-Quality-Assurance-Rules-2022.pdf',
                    'https://www.taumataarowai.govt.nz/assets/Uploads/Publications/Water-Services-Act-Summary.pdf'
                ]
            },
            {
                'name': 'MPI (Food Safety)',
                'search_urls': [
                    'https://www.mpi.govt.nz/food-safety/',
                    'https://www.mpi.govt.nz/dmsdocument/1469-microbiological-reference-criteria-for-food',
                    'https://www.mpi.govt.nz/food-safety/food-safety-for-businesses/food-control-plans/',
                    'https://www.mpi.govt.nz/food-safety/food-safety-for-businesses/haccp/',
                    'https://www.mpi.govt.nz/dmsdocument/45823-microbiological-criteria-for-category-3-animal-products'
                ]
            },
            {
                'name': 'Environment Canterbury (ECan)',
                'search_urls': [
                    'https://www.ecan.govt.nz/your-region/plans-strategies-policies-and-bylaws/canterbury-land-and-water-regional-plan/',
                    'https://www.ecan.govt.nz/data/water-quality-data/'
                ]
            },
            {
                'name': 'Water New Zealand',
                'search_urls': [
                    'https://www.waternz.org.nz/Folder?Action=View%20File&Folder_id=334&File=Water_NZ_Code_of_Practice.pdf',
                    'https://www.waternz.org.nz/Category?Action=View&Category_id=334'
                ]
            }
        ]

        regulations = []

        # Create list of (source_name, url) tuples for parallel processing
        url_tasks = []
        for source in sources:
            for url in source['search_urls']:
                url_tasks.append((source['name'], url))

        # Use ThreadPoolExecutor for parallel processing
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_url = {
                executor.submit(self._scrape_single_url, source_name, url): (source_name, url)
                for source_name, url in url_tasks
            }

            for future in as_completed(future_to_url):
                result = future.result()
                if result:
                    regulations.append(result)

        logger.info(f"Retrieved {len(regulations)} regulatory documents")
        return regulations

    def search_esr_publications(self) -> List[Dict]:
        """Search ESR (Institute of Environmental Science and Research) publications."""
        logger.info("Searching ESR publications...")

        # ESR is a key NZ research institute for microbial risk assessment
        esr_urls = [
            'https://www.esr.cri.nz/our-research/research-areas/public-health/',
            'https://www.esr.cri.nz/our-research/research-areas/environmental-health/'
        ]

        publications = []

        for url in esr_urls:
            try:
                time.sleep(1)
                response = self.session.get(url, timeout=10)
                response.raise_for_status()

                soup = BeautifulSoup(response.content, 'html.parser')

                # Look for publication links and research information
                for link in soup.find_all('a', href=True):
                    href = link.get('href')
                    text = link.get_text().strip()

                    if ('research' in href.lower() or 'publication' in href.lower()) and len(text) > 10:
                        publications.append({
                            'source': 'ESR',
                            'title': text,
                            'url': href if href.startswith('http') else f"https://www.esr.cri.nz{href}",
                            'scraped_date': datetime.now().isoformat()
                        })

            except Exception as e:
                logger.warning(f"Error accessing ESR: {e}")
                continue

        logger.info(f"Retrieved {len(publications)} ESR publications")
        return publications

    def run_comprehensive_search(self) -> None:
        """Run a comprehensive search across all sources with parallel execution."""
        logger.info("Starting comprehensive QMRA literature search...")

        keywords = ['quantitative microbial risk assessment', 'QMRA', 'New Zealand']

        # Run all searches in parallel for speed
        with ThreadPoolExecutor(max_workers=4) as executor:
            # Submit all search tasks
            future_to_search = {
                executor.submit(self.search_pubmed, keywords): "PubMed",
                executor.submit(self.search_google_scholar, keywords, 15): "Google Scholar",
                executor.submit(self.search_nz_government_sources): "NZ Government",
                executor.submit(self.search_esr_publications): "ESR"
            }

            # Collect results as they complete
            for future in as_completed(future_to_search):
                search_type = future_to_search[future]
                try:
                    results = future.result()
                    with self.lock:
                        self.results.extend(results)
                    logger.info(f"Completed {search_type} search: {len(results)} results")
                except Exception as e:
                    logger.error(f"Error in {search_type} search: {e}")

        logger.info(f"Total results collected: {len(self.results)}")

    def save_results(self, filename: str = None) -> None:
        """Save results to CSV, JSON, and EndNote-compatible formats."""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"qmra_literature_search_{timestamp}"

        # Save as CSV
        csv_file = f"{filename}.csv"
        if self.results:
            df = pd.DataFrame(self.results)
            df.to_csv(csv_file, index=False, encoding='utf-8')
            logger.info(f"Results saved to {csv_file}")

        # Save as JSON
        json_file = f"{filename}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        logger.info(f"Results saved to {json_file}")

        # Save as EndNote RIS format
        ris_file = f"{filename}_endnote.ris"
        self._save_as_ris(ris_file)
        logger.info(f"EndNote RIS format saved to {ris_file}")

        # Save as EndNote XML format
        xml_file = f"{filename}_endnote.xml"
        self._save_as_endnote_xml(xml_file)
        logger.info(f"EndNote XML format saved to {xml_file}")

        # Save as BibTeX format (alternative bibliography format)
        bib_file = f"{filename}_bibliography.bib"
        self._save_as_bibtex(bib_file)
        logger.info(f"BibTeX format saved to {bib_file}")

    def _save_as_ris(self, filename: str) -> None:
        """Save results in RIS format for EndNote import."""
        with open(filename, 'w', encoding='utf-8') as f:
            for result in self.results:
                try:
                    # Determine reference type
                    if result.get('source') == 'PubMed' or 'journal' in result.get('journal', '').lower():
                        ref_type = 'JOUR'  # Journal Article
                    elif result.get('document_type') == 'PDF':
                        ref_type = 'RPRT'  # Report
                    elif 'government' in result.get('source', '').lower():
                        ref_type = 'GOVDOC'  # Government Document
                    else:
                        ref_type = 'ELEC'  # Electronic Source

                    f.write(f"TY  - {ref_type}\n")

                    # Title
                    if result.get('title'):
                        f.write(f"TI  - {result['title']}\n")

                    # Authors
                    if result.get('authors'):
                        authors = result['authors'].split(', ')
                        for author in authors:
                            if author.strip():
                                f.write(f"AU  - {author.strip()}\n")

                    # Journal
                    if result.get('journal'):
                        f.write(f"JO  - {result['journal']}\n")

                    # Year
                    if result.get('year'):
                        f.write(f"PY  - {result['year']}\n")

                    # Volume
                    if result.get('volume'):
                        f.write(f"VL  - {result['volume']}\n")

                    # Issue
                    if result.get('issue'):
                        f.write(f"IS  - {result['issue']}\n")

                    # Pages
                    if result.get('pages'):
                        f.write(f"SP  - {result['pages']}\n")

                    # Abstract
                    if result.get('abstract'):
                        abstract = result['abstract'].replace('\n', ' ').strip()
                        f.write(f"AB  - {abstract}\n")

                    # DOI
                    if result.get('doi'):
                        f.write(f"DO  - {result['doi']}\n")

                    # URL
                    if result.get('url'):
                        f.write(f"UR  - {result['url']}\n")

                    # Keywords
                    if result.get('keywords'):
                        keywords = result['keywords'].split(', ')
                        for keyword in keywords:
                            if keyword.strip():
                                f.write(f"KW  - {keyword.strip()}\n")

                    # MeSH terms as additional keywords
                    if result.get('mesh_terms'):
                        mesh_terms = result['mesh_terms'].split(', ')
                        for mesh in mesh_terms:
                            if mesh.strip():
                                f.write(f"KW  - {mesh.strip()}\n")

                    # Publisher/Source
                    if result.get('source'):
                        f.write(f"PB  - {result['source']}\n")

                    # Notes
                    notes = []
                    if result.get('relevant_keywords'):
                        notes.append(f"Relevant keywords: {result['relevant_keywords']}")
                    if result.get('content_preview'):
                        preview = result['content_preview'][:200] + "..." if len(result['content_preview']) > 200 else result['content_preview']
                        notes.append(f"Content preview: {preview}")
                    if result.get('scraped_date'):
                        notes.append(f"Scraped: {result['scraped_date']}")

                    if notes:
                        f.write(f"N1  - {' | '.join(notes)}\n")

                    f.write("ER  -\n\n")

                except Exception as e:
                    logger.warning(f"Error writing RIS entry: {e}")
                    continue

    def _save_as_endnote_xml(self, filename: str) -> None:
        """Save results in EndNote XML format."""
        xml_content = ['<?xml version="1.0" encoding="UTF-8"?>']
        xml_content.append('<xml>')
        xml_content.append('<records>')

        for i, result in enumerate(self.results, 1):
            try:
                xml_content.append(f'<record>')
                xml_content.append(f'<rec-number>{i}</rec-number>')

                # Reference type
                if result.get('source') == 'PubMed':
                    ref_type = '17'  # Journal Article
                elif result.get('document_type') == 'PDF':
                    ref_type = '27'  # Report
                elif 'government' in result.get('source', '').lower():
                    ref_type = '109'  # Government Document
                else:
                    ref_type = '12'  # Electronic Source

                xml_content.append(f'<ref-type name="Journal Article">{ref_type}</ref-type>')

                # Contributors (Authors)
                if result.get('authors'):
                    xml_content.append('<contributors>')
                    xml_content.append('<authors>')
                    authors = result['authors'].split(', ')
                    for author in authors:
                        if author.strip():
                            xml_content.append('<author>')
                            xml_content.append(f'<style face="normal" font="default" size="100%">{author.strip()}</style>')
                            xml_content.append('</author>')
                    xml_content.append('</authors>')
                    xml_content.append('</contributors>')

                # Titles
                xml_content.append('<titles>')
                if result.get('title'):
                    title = result['title'].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                    xml_content.append(f'<title><style face="normal" font="default" size="100%">{title}</style></title>')
                if result.get('journal'):
                    journal = result['journal'].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                    xml_content.append(f'<secondary-title><style face="normal" font="default" size="100%">{journal}</style></secondary-title>')
                xml_content.append('</titles>')

                # Periodical info
                xml_content.append('<periodical>')
                if result.get('volume'):
                    xml_content.append(f'<volume><style face="normal" font="default" size="100%">{result["volume"]}</style></volume>')
                if result.get('issue'):
                    xml_content.append(f'<issue><style face="normal" font="default" size="100%">{result["issue"]}</style></issue>')
                xml_content.append('</periodical>')

                # Pages
                if result.get('pages'):
                    xml_content.append('<pages>')
                    xml_content.append(f'<style face="normal" font="default" size="100%">{result["pages"]}</style>')
                    xml_content.append('</pages>')

                # Date
                if result.get('year'):
                    xml_content.append('<dates>')
                    xml_content.append(f'<year><style face="normal" font="default" size="100%">{result["year"]}</style></year>')
                    xml_content.append('</dates>')

                # Abstract
                if result.get('abstract'):
                    abstract = result['abstract'].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                    xml_content.append('<abstract>')
                    xml_content.append(f'<style face="normal" font="default" size="100%">{abstract}</style>')
                    xml_content.append('</abstract>')

                # Keywords
                keywords_list = []
                if result.get('keywords'):
                    keywords_list.extend(result['keywords'].split(', '))
                if result.get('mesh_terms'):
                    keywords_list.extend(result['mesh_terms'].split(', '))

                if keywords_list:
                    xml_content.append('<keywords>')
                    for keyword in keywords_list:
                        if keyword.strip():
                            kw = keyword.strip().replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                            xml_content.append('<keyword>')
                            xml_content.append(f'<style face="normal" font="default" size="100%">{kw}</style>')
                            xml_content.append('</keyword>')
                    xml_content.append('</keywords>')

                # URLs
                if result.get('url') or result.get('doi_url'):
                    xml_content.append('<urls>')
                    if result.get('url'):
                        xml_content.append('<web-urls>')
                        xml_content.append('<url>')
                        xml_content.append(f'<style face="normal" font="default" size="100%">{result["url"]}</style>')
                        xml_content.append('</url>')
                        xml_content.append('</web-urls>')
                    if result.get('doi_url'):
                        xml_content.append('<pdf-urls>')
                        xml_content.append('<url>')
                        xml_content.append(f'<style face="normal" font="default" size="100%">{result["doi_url"]}</style>')
                        xml_content.append('</url>')
                        xml_content.append('</pdf-urls>')
                    xml_content.append('</urls>')

                # Electronic Resource Number (DOI)
                if result.get('doi'):
                    xml_content.append('<electronic-resource-num>')
                    xml_content.append(f'<style face="normal" font="default" size="100%">{result["doi"]}</style>')
                    xml_content.append('</electronic-resource-num>')

                xml_content.append('</record>')

            except Exception as e:
                logger.warning(f"Error writing XML entry: {e}")
                continue

        xml_content.append('</records>')
        xml_content.append('</xml>')

        with open(filename, 'w', encoding='utf-8') as f:
            f.write('\n'.join(xml_content))

    def _save_as_bibtex(self, filename: str) -> None:
        """Save results in BibTeX format."""
        with open(filename, 'w', encoding='utf-8') as f:
            for i, result in enumerate(self.results, 1):
                try:
                    # Determine entry type
                    if result.get('source') == 'PubMed' or result.get('journal'):
                        entry_type = 'article'
                    elif result.get('document_type') == 'PDF':
                        entry_type = 'techreport'
                    elif 'government' in result.get('source', '').lower():
                        entry_type = 'misc'
                    else:
                        entry_type = 'misc'

                    # Create citation key
                    title_words = result.get('title', 'Unknown').split()[:3]
                    key = ''.join([word.lower().replace(',', '').replace('.', '') for word in title_words])
                    year = result.get('year', datetime.now().year)
                    citation_key = f"{key}{year}"

                    f.write(f"@{entry_type}{{{citation_key},\n")

                    # Title
                    if result.get('title'):
                        title = result['title'].replace('{', '\\{').replace('}', '\\}')
                        f.write(f"  title = {{{title}}},\n")

                    # Authors
                    if result.get('authors'):
                        authors = result['authors'].replace(' and ', ' AND ')
                        f.write(f"  author = {{{authors}}},\n")

                    # Journal
                    if result.get('journal'):
                        f.write(f"  journal = {{{result['journal']}}},\n")

                    # Year
                    if result.get('year'):
                        f.write(f"  year = {{{result['year']}}},\n")

                    # Volume
                    if result.get('volume'):
                        f.write(f"  volume = {{{result['volume']}}},\n")

                    # Number/Issue
                    if result.get('issue'):
                        f.write(f"  number = {{{result['issue']}}},\n")

                    # Pages
                    if result.get('pages'):
                        f.write(f"  pages = {{{result['pages']}}},\n")

                    # DOI
                    if result.get('doi'):
                        f.write(f"  doi = {{{result['doi']}}},\n")

                    # URL
                    if result.get('url'):
                        f.write(f"  url = {{{result['url']}}},\n")

                    # Abstract
                    if result.get('abstract'):
                        abstract = result['abstract'].replace('{', '\\{').replace('}', '\\}')
                        f.write(f"  abstract = {{{abstract}}},\n")

                    # Keywords
                    if result.get('keywords'):
                        f.write(f"  keywords = {{{result['keywords']}}},\n")

                    # Publisher/Institution
                    if result.get('source'):
                        f.write(f"  publisher = {{{result['source']}}},\n")

                    f.write("}\n\n")

                except Exception as e:
                    logger.warning(f"Error writing BibTeX entry: {e}")
                    continue

    def generate_summary_report(self) -> str:
        """Generate a summary report of the search results."""
        if not self.results:
            return "No results found."

        sources = {}
        for result in self.results:
            source = result.get('source', 'Unknown')
            sources[source] = sources.get(source, 0) + 1

        report = f"""
QMRA Literature Search Summary Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Total Results: {len(self.results)}

Results by Source:
"""
        for source, count in sources.items():
            report += f"  {source}: {count} items\n"

        report += f"\nRecent Publications (sample):\n"
        for i, result in enumerate(self.results[:5]):
            report += f"{i+1}. {result.get('title', 'No title')}\n"
            report += f"   Source: {result.get('source', 'Unknown')}\n"
            if result.get('url'):
                report += f"   URL: {result.get('url')}\n"
            report += "\n"

        return report

def main():
    """Main function to run the QMRA literature scraper."""
    print("QMRA Literature and Regulation Scraper for New Zealand")
    print("=" * 60)

    scraper = QMRALiteratureScraper()

    try:
        # Run comprehensive search
        scraper.run_comprehensive_search()

        # Save results
        scraper.save_results()

        # Generate and print summary
        summary = scraper.generate_summary_report()
        print(summary)

        # Save summary report
        with open(f"qmra_search_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt", 'w', encoding='utf-8') as f:
            f.write(summary)

        print("Search completed successfully!")

    except KeyboardInterrupt:
        print("\nSearch interrupted by user.")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

    