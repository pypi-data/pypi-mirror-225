import typing as t
import random
import string
from enum import Enum
import collections.abc
import io
import urllib3

import pdfplumber


def generate_random_short_code():
    return "".join(
        random.choice(string.ascii_lowercase + string.digits) for _ in range(10)
    )


def string_to_bool(string_in: t.Optional[str] = None) -> bool:
    if string_in is None:
        return False
    if string_in.lower() == "true":
        return True
    return False


def replace_variables_in_html(html_content: str, variable_dict: dict):
    for key, value in variable_dict.items():
        html_content = html_content.replace("{{ " + key + " }}", str(value))
    return html_content


def get_value_from_enum(value: str, enumeration: t.Type[Enum]):
    if value in enumeration.__members__:
        return enumeration.__members__[value]
    if value in enumeration._value2member_map_:
        return enumeration._value2member_map_[value]
    return None


def update_dict(d, u):
    if d is None:
        return u
    for k, v in u.items():
        if isinstance(v, collections.abc.Mapping):
            d[k] = update_dict(d.get(k, {}), v)
        elif isinstance(v, list):
            original_list = d.get(k, [])
            for idx, item in enumerate(v):
                if item is None:
                    if idx < len(original_list):
                        v[idx] = original_list[idx]
            d[k] = v
        else:
            if v is not None:
                d[k] = u[k]
    return d


def extract_pdf_text_by_url(url):
    http = urllib3.PoolManager()
    temp = io.BytesIO()
    temp.write(http.request("GET", url).data)
    all_text = ""
    with pdfplumber.open(temp) as pdf:
        for pdf_page in pdf.pages:
            single_page_text = pdf_page.extract_text()
            all_text = all_text + "\n" + single_page_text
    return all_text
