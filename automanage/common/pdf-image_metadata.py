#!/usr/bin/env python3
# -*- coding-utf-8 -*-

from io import FileIO as file

import exifread
from PyPDF2 import PdfReader

def pdf_metadata(file_name):
    pdf_file = PdfReader(file(file_name, 'rb'))
    doc_info = pdf_file.metadata
    print(f"[*] PDF MetaData For: {file_name}")
    for key, value in doc_info.items():
        print(f"[+] {key}: {value}")

def image_gps(file_name):
    gps = {}
    date = ''
    tags = exifread.process_file(open(file_name, 'rb').read())

    tag_map = {
        'GPS GPSLatitudeRef': 'GPSLatitudeRef',
        'GPS GPSLongitudeRef': 'GPSLongitudeRef',
        'GPS GPSAltitudeRef': 'GPSAltitudeRef',
        'GPS GPSLatitude': 'GPSLatitude',
        'GPS GPSLongitude': 'GPSLongitude',
        'GPS GPSAltitude': 'GPSAltitude'
    }

    for tag, value in tags.items():
        if tag in tag_map:
            key = tag_map[tag]
            if key in ('GPSLatitude', 'GPSLongitude'):
                try:
                    value = value.values
                    gps[key] = value[0].num, value[1].num, value[2].num / value[2].den
                except:
                    gps[key] = repr(value)
            elif key == 'GPSAltitudeRef':
                gps[key] = value.values[0]
            else:
                gps[key] = repr(value)
        elif tag.endswith('Date'):
            date = repr(value)
    return {"GPS 信息": gps, "时间信息": date}

if __name__ == '__main__':
    pdf_path = '../data/pdf_test.pdf'
    pdf_metadata(pdf_path)



