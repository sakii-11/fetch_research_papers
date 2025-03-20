import unittest
from get_papers_list.papers_fetcher import parse_paper_details

class TestPapersFetcher(unittest.TestCase):
    def test_parse_paper_details(self):
        """
        Test parsing XML content into paper details.
        """
        xml_content = """
        <PubmedArticle>
            <MedlineCitation>
                <PMID>12345678</PMID>
                <Article>
                    <ArticleTitle>Example Paper Title</ArticleTitle>
                    <AuthorList>
                        <Author>
                            <LastName>Doe</LastName>
                            <ForeName>John</ForeName>
                            <AffiliationInfo>
                                <Affiliation>Pharma Company</Affiliation>
                            </AffiliationInfo>
                        </Author>
                        <Author>
                            <LastName>Smith</LastName>
                            <ForeName>Jane</ForeName>
                            <AffiliationInfo>
                                <Affiliation>University of Example</Affiliation>
                            </AffiliationInfo>
                        </Author>
                    </AuthorList>
                    <Journal>
                        <PubDate>
                            <Year>2023</Year>
                            <Month>Oct</Month>
                            <Day>15</Day>
                        </PubDate>
                    </Journal>
                </Article>
            </MedlineCitation>
        </PubmedArticle>
        """

        expected_result = {
            "PubmedID": "12345678",
            "Title": "Example Paper Title",
            "Publication Date": "2023-Oct-15",
            "Authors": ["John Doe", "Jane Smith"],
            "Affiliations": ["Pharma Company", "University of Example"],
            "Corresponding Author Email": None,
        }

        result = parse_paper_details(xml_content)
        self.assertEqual(result, expected_result)

if __name__ == "__main__":
    unittest.main()