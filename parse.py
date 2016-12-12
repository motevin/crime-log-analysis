import json
import csv
from collections import OrderedDict
from datetime import datetime

DATETIME_FORMAT_IN = "%m/%d/%y - %a at %H:%M"
DATETIME_FORMAT_OUT = "%y-%m-%d %H:%M"


def parse(report):
    """
    Get report attributes with the fucked 4 element list
        report[0] -> date, location, location, event #
        report[1] -> from/to attr, from/to, X, X
        report[2] -> incident, X, X, report #
        report[3] -> disposition, X, X, X
    :param report: 4-element list
    :return: parsed list
    """

    incident_no = get_incident_no(report[0][-1]['text'])
    date = get_date(report[0][0]['text'])

    if len(report[0]) <= 3:
        location = get_location(report[0][1]['text'])
    else:
        l1 = get_location(report[0][1]['text'])
        l2 = get_location(report[0][2]['text'])
        location = l1 if len(l1) > len(l2) else l2

    start_time, end_time = get_start_end_times(report[1][1]['text'])
    incident = get_incident(report[2][0]['text'])
    disposition = get_disposition(report[3][0]['text'])

    return [date, incident, location, disposition, start_time, end_time]


def get_incident_no(raw):
    return raw.replace("event #: ", "")


def get_date(raw):
    raw = raw.replace("date reported: ", "")
    try:
        raw = raw.replace("date reported: ", "")
        date = datetime.strptime(raw, DATETIME_FORMAT_IN)
        return date.strftime(DATETIME_FORMAT_OUT)
    except ValueError as e:
        print(e)
        return ""


def get_location(raw):
    if "event #" in raw:
        raw = raw[:raw.find("event #")-1]
    return raw.replace("location :", "").strip()


def get_start_end_times(raw):
    if len(raw) > 0:
        return get_date(raw[0:23]), get_date(raw[-23:])
    else:
        return "", ""


def get_incident(raw):
    return raw.replace("incident : ", "")


def get_disposition(raw):
    return raw.replace("disposition: :", "").strip()


def get_report_chunks(data):
    """
    Split data array into reports. Reports are every 4 elements
    """
    for i in range(0, len(data), 4):
        yield data[i: i+4]

if __name__ == "__main__":
    pages = {}
    with open("/home/tevin/Downloads/tabula-NUPD Daily Log 01.16 - 12.16.json", "r") as tabula_json_file:
        pages = json.load(tabula_json_file, object_pairs_hook=OrderedDict)

    with open('parsedlogfull.csv', 'w') as csvfile:
        report_writer = csv.writer(csvfile, delimiter=';')
        report_writer.writerow(['DATE', 'INCIDENT', 'LOCATION', 'DISPOSITION', 'FROM', 'TO'])
        for page in pages:
            for report in get_report_chunks(page['data']):
                report_writer.writerow(parse(report))

