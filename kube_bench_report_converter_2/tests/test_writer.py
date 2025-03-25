import os
import tempfile
import csv
from kube_bench_report_converter_2.writer import write_to_file

def test_write_to_file():
    # Create sample findings data
    findings = {
        '1.1.1': {
            'level': 'PASS',
            'anchor': '1.1.1',
            'description': 'Test PASS finding',
            'category': 'Test Category',
            'subcategory': 'Test Subcategory'
        },
        '2.2.2': {
            'level': 'FAIL',
            'anchor': '2.2.2',
            'description': 'Test FAIL finding',
            'category': 'Test Category',
            'subcategory': 'Test Subcategory',
            'remediation': {
                'description': 'Test remediation'
            }
        },
        '3.3.3': {
            'level': 'WARN',
            'anchor': '3.3.3',
            'description': 'Test WARN finding',
            'category': 'Test Category',
            'subcategory': 'Test Subcategory'
        }
    }
    
    # Create a temporary file for output
    fd, temp_filename = tempfile.mkstemp(suffix='.csv')
    os.close(fd)
    
    try:
        # Write findings to the CSV file
        write_to_file(findings, temp_filename)
        
        # Verify the CSV file was created
        assert os.path.exists(temp_filename)
        assert os.path.getsize(temp_filename) > 0
        
        # Read the CSV file and verify its contents
        with open(temp_filename, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            rows = list(reader)
            
            # Check header row
            assert rows[0] == ['Id', 'Category', 'Subcategory', 'Rating', 'Description', 'Remediation']
            
            # Check data rows - we'll have 4 rows including header
            assert len(rows) == 4
            
            # Check for each finding in the CSV
            finding_ids = [row[0] for row in rows[1:]]
            assert '1.1.1' in finding_ids
            assert '2.2.2' in finding_ids
            assert '3.3.3' in finding_ids
            
            # Check that remediation is included for the FAIL finding
            for row in rows:
                if row[0] == '2.2.2':
                    assert row[5] == 'Test remediation'
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_filename):
            os.remove(temp_filename)

def test_write_to_file_empty_findings():
    findings = {}
    
    # Create a temporary file for output
    fd, temp_filename = tempfile.mkstemp(suffix='.csv')
    os.close(fd)
    
    try:
        # Write findings to the CSV file
        write_to_file(findings, temp_filename)
        
        # Verify the CSV file was created with just the header
        assert os.path.exists(temp_filename)
        
        with open(temp_filename, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            rows = list(reader)
            
            # Check header row
            assert len(rows) == 1
            assert rows[0] == ['Id', 'Category', 'Subcategory', 'Rating', 'Description', 'Remediation']
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_filename):
            os.remove(temp_filename) 