import os
import tempfile
import sys
from unittest.mock import patch
from kube_bench_report_converter_2.command_line import main

def test_main_with_file_paths():
    # Create a sample input file
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as input_file:
        input_file.write('[INFO] 3 Worker Node Security Configuration\n')
        input_file.write('[INFO] 3.1 Worker Node Configuration Files\n')
        input_file.write('[PASS] 3.1.1 Ensure that the kubeconfig file permissions are set to 644 or more restrictive (Automated)\n')
        input_file.write('[WARN] 4.1.1 Ensure that the cluster-admin role is only used where required (Automated)\n')
        input_filename = input_file.name
    
    # Create a temp output file path
    fd, output_filename = tempfile.mkstemp(suffix='.csv')
    os.close(fd)
    os.unlink(output_filename)  # We'll let the command create the file
    
    try:
        # Mock command line arguments
        with patch.object(sys, 'argv', ['kube-bench-report-converter-2', 
                                       '--input_file_path', input_filename,
                                       '--output_file_path', output_filename]):
            # Run the main function
            main()
            
            # Check that the output file was created
            assert os.path.exists(output_filename)
            assert os.path.getsize(output_filename) > 0
            
            # Check that the file only contains PASS entries and not WARN entries
            with open(output_filename, 'r') as f:
                content = f.read()
                assert '3.1.1' in content
                assert '4.1.1' not in content
    finally:
        # Clean up temporary files
        if os.path.exists(input_filename):
            os.unlink(input_filename)
        if os.path.exists(output_filename):
            os.unlink(output_filename)

def test_main_with_warnings():
    # Create a sample input file
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as input_file:
        input_file.write('[INFO] 3 Worker Node Security Configuration\n')
        input_file.write('[INFO] 3.1 Worker Node Configuration Files\n')
        input_file.write('[PASS] 3.1.1 Ensure that the kubeconfig file permissions are set to 644 or more restrictive (Automated)\n')
        input_file.write('[WARN] 4.1.1 Ensure that the cluster-admin role is only used where required (Automated)\n')
        input_filename = input_file.name
    
    # Create a temp output file path
    fd, output_filename = tempfile.mkstemp(suffix='.csv')
    os.close(fd)
    os.unlink(output_filename)  # We'll let the command create the file
    
    try:
        # Mock command line arguments with include_warnings flag
        with patch.object(sys, 'argv', ['kube-bench-report-converter-2', 
                                       '--input_file_path', input_filename,
                                       '--output_file_path', output_filename,
                                       '--include_warnings']):
            # Run the main function
            main()
            
            # Check that the output file was created
            assert os.path.exists(output_filename)
            assert os.path.getsize(output_filename) > 0
            
            # Check that the file contains both PASS and WARN entries
            with open(output_filename, 'r') as f:
                content = f.read()
                assert '3.1.1' in content
                assert '4.1.1' in content
    finally:
        # Clean up temporary files
        if os.path.exists(input_filename):
            os.unlink(input_filename)
        if os.path.exists(output_filename):
            os.unlink(output_filename) 