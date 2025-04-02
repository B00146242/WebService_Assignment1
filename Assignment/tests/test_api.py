import unittest
import requests
from io import StringIO
from fpdf import FPDF


class ApiTest(unittest.TestCase):
    def test_sample_endpoint(self):
        url = 'http://localhost:8000/getAll' 
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)

    def test_sample_endpoint2(self):
        item_id = 1 
        url = f'http://localhost:8000/getSingleProduct/{item_id}'
        response = requests.get(url) 
        self.assertEqual(response.status_code, 200)
    
    def test_sample_endpoint3(self):
        item_id = 2  
        url = f'http://localhost:8000/addNew/{item_id}' 
        response = requests.get(url)  
        self.assertEqual(response.status_code, 200)  
    
    def test_sample_endpoint4(self):
        item_id = 1  
        url = f'http://localhost:8000/deleteOne/{item_id}'  
        response = requests.get(url) 
        self.assertEqual(response.status_code, 200)  

    def test_sample_endpoint5(self):
        letter = 'A'  
        url = f'http://localhost:8000/startWith/{letter}'  
        response = requests.get(url)  
        self.assertEqual(response.status_code, 200)

    def test_sample_endpoint6(self):
        item_id = 1 
        url = f'http://localhost:8000/convert/{item_id}'  
        response = requests.get(url)  
        self.assertEqual(response.status_code, 200)

def run_tests():
    suite = unittest.TestLoader().loadTestsFromTestCase(ApiTest)
    result_stream = StringIO()
    runner = unittest.TextTestRunner(stream=result_stream)
    runner.run(suite)
    return result_stream.getvalue()

def generate_pdf(test_results):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Unit Test Results", ln=True, align="C")
    pdf.ln(10)
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 10, test_results)  
    pdf.output("test_results.pdf")

test_results = run_tests()
generate_pdf(test_results)


