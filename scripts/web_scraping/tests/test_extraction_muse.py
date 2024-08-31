import unittest
from unittest.mock import patch, Mock
from scripts.web_scraping.extraction_muse import load_api_key, build_url, fetch_jobs_data, parse_job_details, save_to_csv

class TestExtractionMuse(unittest.TestCase):

    @patch('scripts.web_scraping.extraction_muse.os.getenv')
    def test_load_api_key(self, mock_getenv):
        mock_getenv.return_value = "dummy_api_key"
        api_key = load_api_key("API_KEY1")
        self.assertEqual(api_key, "dummy_api_key")
    
    def test_build_url(self):
        url = build_url(1)
        self.assertIn("page=1", url)
        self.assertTrue(url.startswith("https://www.themuse.com/api/public/jobs"))

    @patch('scripts.web_scraping.extraction_muse.requests.get')
    def test_fetch_jobs_data(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"results": []}
        mock_get.return_value = mock_response
        
        url = build_url(1)
        headers = {'Authorization': 'dummy_api_key'}
        data = fetch_jobs_data(url, headers)
        
        self.assertIsInstance(data, dict)
        self.assertIn('results', data)

    def test_parse_job_details(self):
        job = {
            'name': 'Data Scientist',
            'company': {'name': 'Tech Corp'},
            'locations': [{'name': 'Berlin, Germany'}],
            'publication_date': '2024-01-01',
            'categories': [{'name': 'Data Science'}],
            'levels': [{'name': 'Mid Level'}],
            'refs': {'landing_page': 'https://example.com/job'}
        }
        
        job_info = parse_job_details(job)
        
        self.assertEqual(job_info['Job Title'], 'Data Scientist')
        self.assertEqual(job_info['Company Name'], 'Tech Corp')
        self.assertEqual(job_info['Location'], 'Berlin, Germany')
        self.assertEqual(job_info['Categories'], 'Data Science')
        self.assertEqual(job_info['Experience Level'], 'Mid Level')
        self.assertEqual(job_info['Job Link'], 'https://example.com/job')
        self.assertIsNone(job_info['Full/Part Time'])

    @patch('scripts.web_scraping.extraction_muse.pd.DataFrame.to_csv')
    def test_save_to_csv(self, mock_to_csv):
        data = [{'Job Title': 'Data Scientist'}]
        save_to_csv(data, 'dummy_path.csv')
        mock_to_csv.assert_called_once()

if __name__ == '__main__':
    unittest.main()
