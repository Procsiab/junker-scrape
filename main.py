#!/usr/bin/env python3

import sys
import json
import re
import unicodedata
from datetime import datetime
import requests
from collection import Collection, AreaNotFound, AreaRequired

EVENTS_REGEX = re.compile(r"var\s+events\s*=\s*(\[.*?\])\s*;")
ZONE_REGEX = re.compile(r"var\s+zone\s*=\s*(\[.*?\])\s*;")

# From Iconify: https://icon-sets.iconify.design/
ICON_MAP = {
    "organic": "cbi:garbage-organic",
    "paper": "healthicons:toilet-paper",
    "light": "mdi:package-variant",
    "general": "mdi:trash-can",
    "bulky": "mdi:sofa",
    "plastic": "mdi:recycle",
    "glass": "mdi:bottle-wine",
    "napkins": "mdi:diaper-outline",
}


def replace_accents(text: str) -> str:
    # Normalize the text to NFD (Normalization Form Decomposition)
    normalized_text = unicodedata.normalize("NFD", text)

    # Filter out combining diacritical marks
    filtered_text = "".join(
        char for char in normalized_text if unicodedata.category(char) != "Mn"
    )

    # Normalize back to NFC (Normalization Form Composition)
    return unicodedata.normalize("NFC", filtered_text)


def fetch(municipality: str, area: str, collect_date: str) -> list[Collection]:
    _municipality = municipality
    _area = area
    _area_name = _area
    _municipalities_with_area = {"municipality": _municipality,  "area": _area}
    _url = "https://differenziata.junkerapp.it/{municipality}/calendario".format(
            municipality=_municipality)
    _area_url = "https://differenziata.junkerapp.it/{municipality}/{area}/calendario".format(
            municipality=_municipality,
            area=_area)

    mun_str = replace_accents(
        _municipality.lower().strip().replace(" ", "-").replace("'", "-")
    )
    if _area:
        url = _area_url.format(municipality=mun_str,
                               area=_area)
    else:
        url = _url.format(municipality=mun_str)

    r = requests.get(url)
    r.raise_for_status()

    zone_match = ZONE_REGEX.search(r.text)

    if zone_match:
        zone_string = zone_match.group(1)
        zones = json.loads(zone_string)
        areas = [(zone["NOME"], zone["ID"]) for zone in zones]
        if not areas:
            raise ValueError("No areas found")

        if _area_name:
            for area in areas:
                if replace_accents(area[0]).lower().strip().replace(
                    " ", ""
                ).replace(",", "").replace("'", "") == replace_accents(
                    _area_name
                ).lower().strip().replace(
                    " ", ""
                ).replace(
                    ",", ""
                ).replace(
                    "'", ""
                ):
                    if _area in (str(area[1]), area[1]):
                        raise ValueError("Something went wrong with the area")
                    _area = area[1]
                    return fetch()

            raise AreaNotFound(areas)
        raise AreaRequired(areas)

    envents_match = EVENTS_REGEX.search(r.text)
    if not envents_match:
        raise ValueError("No events found maybe wrong/not supported municipality")
    events_string = envents_match.group(1)
    data = json.loads(events_string)

    entries = []
    _collect_date = datetime.strptime(collect_date, "%Y-%m-%d").date()
    for d in data:
        date = datetime.strptime(d["date"], "%Y-%m-%d").date()
        if date == _collect_date:
            bin_type = d["vbin_desc"]
            icon = ICON_MAP.get(bin_type.lower().split()[0])  # Collection icon
            entries.append(Collection(date=date,
                                      t=bin_type,
                                      icon=icon))

    if not entries:
        muns = [
            m
            for m in _municipalities_with_area
            if m.lower().replace(" ", "")
            == _municipality.lower().replace(" ", "")
        ]
        mun = muns[0] if muns else _municipality
        if (
            not _area
            and mun in _municipalities_with_area
            and len(_municipalities_with_area[mun]) == 1
        ):
            # If municipality needs region but only one region is available use it
            _area = _municipalities_with_area[_municipality][0]
            return fetch()
        raise ValueError("No collections found maybe you need to specify an area")

    return entries


def main():
    if len(sys.argv) != 3:
        raise ValueError("Wrong number of arguments passed!")
    if sys.argv[1] is None:
        raise ValueError("The 'municipality' argument should be a string!")
    else:
        provided_mun = sys.argv[1]
    if sys.argv[2] is None:
        raise ValueError("The 'area' argument should be a string!")
    else:
        provided_area = sys.argv[2]
    if sys.argv[3] is None:
        raise ValueError("The 'date' argument should be a string!")
    else:
        provided_date = sys.argv[3]

    collection_list = fetch(municipality=provided_mun,
                            area=provided_area,
                            collect_date=provided_date)
    print(json.dumps(collection_list))


if __name__ == "__main__":
    main()
