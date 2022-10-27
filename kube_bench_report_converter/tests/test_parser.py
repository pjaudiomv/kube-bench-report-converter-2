from kube_bench_report_converter.parser import parse_finding_details


def test_parse_major_section():
    result = parse_finding_details('[INFO] 4 Worker Node Security Configuration')

    assert result['section'] is True
    assert result['anchor'] == '4'
    assert result['level'] == 'INFO'
    assert result['title'] == 'Worker Node Security Configuration'


def test_parse_minor_section():
    result = parse_finding_details('[INFO] 1.1 Master Node Configuration Files')

    assert result['section'] is True
    assert result['anchor'] == '1.1'
    assert result['level'] == 'INFO'
    assert result['title'] == 'Master Node Configuration Files'


def test_parse_finding_details():
    result = parse_finding_details('[PASS] 1.1.1 Ensure that the API server pod specification file permissions are set to 644 '
                           'or more restrictive (Automated)')

    assert result['section'] is False
    assert result['anchor'] == '1.1.1'
    assert result['level'] == 'PASS'
    assert result['title'] == 'Ensure that the API server pod specification file permissions are set to 644 or more ' \
                              'restrictive (Automated)'
