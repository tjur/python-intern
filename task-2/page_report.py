import sys
import ipaddress
from urllib.parse import urlparse
from collections import defaultdict as dd


http_methods = ['GET', 'POST', 'HEAD', 'PUT', 'DELETE']


def parse_line(line):
    # many of these variables won't be used, but they can be useful
    # if we'd like to change format of printed results
    # (for instance add some information about ip address or sent bytes)
    ip_addr, rest = parse_ipv4(line)
    datetime, rest = parse_datetime(rest)
    http_method, stripped_url, rest = parse_request(rest)
    response_code, rest = parse_response(rest)
    bytes_sent = parse_bytes(rest)
    return stripped_url


def parse_ipv4(line):
    ipv4_str, rest = line.lstrip().split(' ', 1)
    ipaddress.IPv4Address(ipv4_str)  # validate ipv4 (raises ValueError)
    return ipv4_str, rest


def parse_datetime(line):
    line = line.lstrip()
    start_pos, end_pos = line.index('['), line.index(']')
    if start_pos != 0:
        raise ValueError
    datetime, rest = line[1:end_pos], line[end_pos+1:]
    # I don't validate datetime because there are too many possible formats
    # and the task does not specify one fixed format
    return datetime, rest


def parse_request(line):
    line = line.lstrip()
    start_pos = line.index('"')
    end_pos = line.index('"', start_pos+1)
    if start_pos != 0:
        raise ValueError
    request, rest = line[1:end_pos], line[end_pos+1:]
    http_method, url = request.split(' ', 1)
    if http_method not in http_methods:
        raise ValueError

    stripped_url = strip_url(url)
    return http_method, stripped_url, rest


def strip_url(url):
    url = url.strip()

    # remove everything after the first space (if exists)
    # I assume that there is nothing interesting there (like HTTP/1.1)
    space_index = url.find(' ')
    if space_index != -1:
        url = url[:space_index]

    parse_result = urlparse(url)
    stripped_url = parse_result.netloc + parse_result.path

    # remove ending slash (if exists)
    stripped_url = stripped_url.rstrip('/')

    return stripped_url


def parse_response(line):
    response_code_str, rest = line.lstrip().split(' ', 1)
    response_code = int(response_code_str)
    return response_code, rest


def parse_bytes(line):
    bytes = int(line)
    return bytes


# changes requests_url_count dict to a list of tuples (url, count),
# sorts it in a proper way and prints
def print_result(requests_url_count, invalid_lines_count):
    url_count_list = [
        (url, count) for url, count in requests_url_count.items()
    ]
    # sort - count descending, url lexicographically
    url_count_list.sort(key=lambda p: (-p[1], p[0]))
    for url, count in url_count_list:
        print('"{0}",{1}'.format(url, count))
    if invalid_lines_count > 0:
        print(
            '\nInvalid log lines: {0}'.format(invalid_lines_count),
            file=sys.stderr)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python page_report.py <path-to-log-file>\n')
    else:
        path = sys.argv[1]
        with open(path, 'r') as logs:
            requests_url_count = dd(int)
            invalid_lines_count = 0
            for line in logs:
                try:
                    stripped_url = parse_line(line)
                    requests_url_count[stripped_url] += 1
                except ValueError:
                    invalid_lines_count += 1

            print_result(requests_url_count, invalid_lines_count)
