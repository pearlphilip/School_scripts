import os
import unittest
from pronto_utils import download_if_needed, remove_data, plot_daily_totals, get_pronto_data

class TestDownload_if_needed(unittest.TestCase):
    
    # Test for present file.
    def test_file_present(self):
        remove_data('open_data_year_one.zip')
        get_pronto_data()
        result = download_if_needed('https://s3.amazonaws.com/pronto-data/open_data_year_one.zip', 'open_data_year_one.zip')
        self.assertEqual('open_data_year_one.zip already exists', result)  
    
    # Test for existent url and download.
    def test_url_existent(self):
        remove_data('open_data_year_one.zip')
        result = download_if_needed('https://s3.amazonaws.com/pronto-data/open_data_year_one.zip', 'open_data_year_one.zip')
        self.assertEqual('downloading', result)
        
    # Test for nonexistent url.
    def test_url_nonexistent(self):
        remove_data('open_data_year_one.zip')
        result = download_if_needed('https://s3.amazonaws.com/pronto-data/open_data_year_ne.zip', 'open_data_year_one.zip')
        self.assertEqual('Url does not exist', result) 
        
    
class TestRemove_data(unittest.TestCase):

    # Test for file removal.
    def test_file_removal(self):
        download_if_needed('https://s3.amazonaws.com/pronto-data/open_data_year_one.zip', 'open_data_year_one.zip')
        result = remove_data('open_data_year_one.zip')
        self.assertEqual(result, 'Data file removed')
    
    # Test for no such file in directory.
    def test_file_notpresent(self):
        os.remove('open_data_year_one.zip')
        result = remove_data('open_data_year_one')
        self.assertEqual(result, 'No such data file exists that can be removed')


class TestPlot_daily_totals(unittest.TestCase):

    # Test for plot file.
    def test_plot_daily_totals(self):
        result = plot_daily_totals()
        self.assertEqual(None, result)

if __name__ == '__main__':
    unittest.main()