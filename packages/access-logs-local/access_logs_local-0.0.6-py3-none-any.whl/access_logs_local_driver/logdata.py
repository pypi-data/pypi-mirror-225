from datetime import date, datetime, timedelta
import gzip
import logging
import os
import re
import socket
import sys

from typing import Iterator
import urllib.error
import urllib.parse


class Request:
    """Represent the data in a single line of the Apache log file."""

    def __init__(
            self,
            ip_address: str,
            url_prefix: str,
            url: str,
            response_code: int,
            content_length: int,
            timestamp: datetime,
            user_agent: str,
    ):
        self.ip_address = ip_address
        self.timestamp = timestamp
        self.user_agent = user_agent or ""
        self.url = self.parse_url(url, url_prefix)
        self.response_code = response_code
        self.content_length = content_length

    def parse_url(self, url: str, url_prefix: str) -> str:
        try:
            if url.startswith("http"):
                return url_prefix + urllib.parse.urlparse(url).path.lower()
            return self.normalise_url(url_prefix + url.lower())
        except ValueError:
            raise ValueError(f"Error parsing: {url}, {sys.stderr}")

    @staticmethod
    def normalise_url(url: str) -> str:
        try:
            return url[:-1] if url[-1] == "/" else url
        except IndexError as err:
            raise IndexError(f"Error parsing: {url}, {err}")

    def fmttime(self) -> str:
        return self.timestamp.strftime("%Y-%m-%d %H:%M:%S")

    def __str__(self) -> str:
        return f"Request {self.fmttime()}, {self.ip_address}, {self.url}"

    def __iter__(self):
        for _item in self.as_tuple():
            yield _item

    def as_tuple(self) -> tuple[str, str, str, str]:
        return self.fmttime(), self.ip_address, self.url, self.user_agent

    def sanitise_url(self, regexes: str) -> None:
        for regex in regexes:
            matched = re.search(re.compile(regex), self.url)
            if matched is not None:
                self.url = matched.group(0)
                break


class LogStream:
    def __init__(
            self,
            log_dir: str,
            filter_groups: list,
            url_prefix: str,
            start_date: str,
            end_date: str,
    ) -> None:
        self.log_dir = log_dir
        self.filter_groups = filter_groups
        self.url_prefix = url_prefix
        self.start_date = date.fromisoformat(start_date)
        self.end_date = date.fromisoformat(end_date)

        self.access_logs_re = re.compile(
            r"(?P<ip_address>\d+\.\d+\.\d+\.\d+) "
            r"(?P<users>.+ .+) "
            r"\[(?P<timestamp>.+)\] "
            r'"(?P<request>.+)" '
            r"(?P<status_and_size>\d+ \d+) "
            r'(?P<referer>".+") '
            r'"(?P<user_agent>.+)"'
        )

    def regex_match_line(self, line: str) -> Request | None:
        """Use regex to convert the line to a dict identifying all parts, if
        not, just log it and skip the line, then, call the Request class. Also,
        if the line doesn't match (strict) the timestamp requested, ignore it.
        """
        if re_match_dict := self.access_logs_re.search(line):
            re_match_dict = re_match_dict.groupdict()
        else:
            return logging.info(f"Skipping invalid request log entry: {line}")

        timestamp = datetime.strptime(
            re_match_dict.pop("timestamp"),
            "%d/%b/%Y:%H:%M:%S %z",
        )
        timestamp_date = timestamp.date()
        if not self.start_date <= timestamp_date <= self.end_date:
            return

        ip_address = re_match_dict.pop("ip_address")
        if not self.validate_ip_address(ip_address):
            return logging.info(f"Skipping invalid request log entry: {line}")

        status_and_size = re_match_dict.pop("status_and_size")
        response_code, content_length = map(int, status_and_size.split(" "))

        request = re_match_dict.pop('request')
        url = self.validate_request(request)
        if not url:
            return logging.info(f"Skipping invalid request log entry: {line}")

        return Request(
            ip_address=ip_address,
            url_prefix=self.url_prefix,
            url=url,
            response_code=response_code,
            content_length=content_length,
            timestamp=timestamp,
            user_agent=re_match_dict['user_agent'],
        )

    @staticmethod
    def validate_request(request):
        """Make sure the request and url are correct.
        Sample: 'GET /test/books/e/10.5334/bbc HTTP/1.0'
        """
        if re.match(r"^(GET|POST|PUT)\s+(/\S+)\s+HTTP/1\.\d$", request):
            _, url, _ = request.split()
            return url

    @staticmethod
    def validate_ip_address(ip_adrress):
        """Validate the ip_address using socket,
        Better approach than REGEX since would validate
        999.999.999.999"""
        try:
            socket.inet_aton(ip_adrress)
            return True
        except OSError:
            return False

    def logfile_names(self) -> Iterator[str]:
        """Generate a list of matching logfile names in the directory.
        Includes files within the range of a day before and a day after of
        the search_date requested to account for time zone differences.
        """
        for path in sorted(os.listdir(self.log_dir)):
            if "access.log" not in path or not path.endswith(".gz"):
                continue
            match_pattern = re.compile(
                r"(?P<year>\d{4})-?(?P<month>\d{2})-?(?P<day>\d{2})"
            )
            match = match_pattern.search(path)
            if match is None:
                raise AttributeError(
                    "Your file has to have a date at the end of its name"
                )
            date_dict = match.groupdict()
            file_datestamp = (
                f"{date_dict['year']}-{date_dict['month']}-{date_dict['day']}"
            )
            file_date = date.fromisoformat(file_datestamp)
            min_date = self.start_date - timedelta(days=1)
            max_date = self.end_date + timedelta(days=1)
            if not min_date <= file_date <= max_date:
                continue

            yield os.path.join(self.log_dir, path)

    def lines(self) -> Request:
        """Reads relevant logfiles and yields each line."""
        for logfile in self.logfile_names():
            with gzip.open(logfile, "r") as f:
                for line in f:
                    if line := self.regex_match_line(line.decode("utf-8")):
                        yield line

    def relevant_requests(self) -> Iterator[tuple]:
        """Generate a filtered stream of requests; apply the predicate list
        `self.filters' to these requests; if any predicate fails, ignore
        the request and do not generate it for downstream processing."""
        for line_request in self.lines():
            for filter_group in self.filter_groups:
                measure_uri, filters, regex = filter_group
                if not self.filter_in_line_request(filters, line_request):
                    continue
                line_request.sanitise_url(regex)
                yield measure_uri, line_request
                break  # only allow one measure to match per line

    @staticmethod
    def filter_in_line_request(filters: list, line_request: str) -> bool:  # TODO: Rename to something more understandable
        """If the filter from make_filters doesn't align with the line_request
        ignore the next iteration in the parent loop."""
        for f in filters:
            if not f(line_request):
                return False
        return True

    def __iter__(self):
        return self.relevant_requests()

    def return_output(self) -> list[tuple]:
        """Return the results from the filters."""
        return list(self)
