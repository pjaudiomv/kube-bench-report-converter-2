from kube_bench_report_converter_2.parser import parse_finding_details, parse_from_file
import tempfile
import os


def test_parse_major_section():
    result = parse_finding_details('[INFO] 4 Worker Node Security Configuration')

    assert result['is_category'] is True
    assert result['anchor'] == '4'
    assert result['level'] == 'INFO'
    assert result['description'] == 'Worker Node Security Configuration'


def test_parse_minor_section():
    result = parse_finding_details('[INFO] 1.1 Master Node Configuration Files')

    assert result['is_category'] is False
    assert result['is_subcategory'] is True
    assert result['anchor'] == '1.1'
    assert result['level'] == 'INFO'
    assert result['description'] == 'Master Node Configuration Files'


def test_parse_finding_details():
    result = parse_finding_details('[PASS] 1.1.1 Ensure that the API server pod specification file permissions are set to 644 '
                           'or more restrictive (Automated)')

    assert result['is_category'] is False
    assert result['is_subcategory'] is False
    assert result['anchor'] == '1.1.1'
    assert result['level'] == 'PASS'
    assert result['description'] == 'Ensure that the API server pod specification file permissions are set to 644 or more ' \
                              'restrictive (Automated)'


def test_parse_warning_finding():
    result = parse_finding_details('[WARN] 4.1.1 Ensure that the cluster-admin role is only used where required (Automated)')
    
    assert result['is_category'] is False
    assert result['is_subcategory'] is False
    assert result['anchor'] == '4.1.1'
    assert result['level'] == 'WARN'
    assert result['description'] == 'Ensure that the cluster-admin role is only used where required (Automated)'


def test_parse_from_file_with_warnings():
    # Create a temporary file with test content
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write('[INFO] 3 Worker Node Security Configuration\n')
        f.write('[INFO] 3.1 Worker Node Configuration Files\n')
        f.write('[PASS] 3.1.1 Ensure that the kubeconfig file permissions are set to 644 or more restrictive (Automated)\n')
        f.write('[WARN] 4.1.1 Ensure that the cluster-admin role is only used where required (Automated)\n')
        f.write('\n== Summary ==\n')
        f.write('1 checks PASS\n')
        f.write('0 checks FAIL\n')
        f.write('1 checks WARN\n')
        temp_filename = f.name
    
    try:
        # Test without warnings
        findings_no_warnings = parse_from_file(temp_filename, include_warnings=False)
        assert len(findings_no_warnings) == 1
        assert '3.1.1' in findings_no_warnings
        assert findings_no_warnings['3.1.1']['level'] == 'PASS'
        
        # Test with warnings
        findings_with_warnings = parse_from_file(temp_filename, include_warnings=True)
        assert len(findings_with_warnings) == 2
        assert '3.1.1' in findings_with_warnings
        assert '4.1.1' in findings_with_warnings
        assert findings_with_warnings['4.1.1']['level'] == 'WARN'
    finally:
        # Clean up the temporary file
        os.unlink(temp_filename)
