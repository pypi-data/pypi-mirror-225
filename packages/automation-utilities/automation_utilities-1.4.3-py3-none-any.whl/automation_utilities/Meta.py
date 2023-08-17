import json
import re
from json import JSONDecodeError
import URLs
from playwright.sync_api import Page


def get_script_contents(page: Page):
    return page.evaluate('''() => {
                const scriptTags = Array.from(document.querySelectorAll('script'));
                return scriptTags.map(tag => tag.innerText);
            }''')


def get_av(scripts: list):
    for script in scripts:
        try:
            return URLs.get_parameters(json.loads(script)["u"])['__user']
        except (KeyError, TypeError, IndexError, JSONDecodeError):
            pass


def get_hsi(scripts: list):
    for script in scripts:
        try:
            return json.loads(script)["e"]
        except (KeyError, TypeError, IndexError, JSONDecodeError):
            pass


def get_rev(scripts: list):
    for script in scripts:
        try:
            return json.loads(script)["consistency"]["rev"]
        except (KeyError, TypeError, IndexError, JSONDecodeError):
            pass


def get_jazoest(scripts: list):
    for script in scripts:
        try:
            return json.loads(script)["u"].split('&')[-1].split('=')[-1]
        except (KeyError, TypeError, IndexError, JSONDecodeError):
            pass


def get_fb_dtsg(scripts: list):
    for script in scripts:
        try:
            return json.loads(script)["f"]
        except (KeyError, TypeError, IndexError, JSONDecodeError):
            pass


def get_spin_t(scripts: list):
    for script in scripts:
        match = re.search(r'"__spin_t":(\d+)', script)
        if match:
            return match.group(1)


def get_ids(scripts: list):
    for script in scripts:
        try:
            ids = []
            main_list0 = json.loads(script)["require"][0][3][0]["__bbox"]["require"][0][3][1]["__bbox"]["result"]
            main_list = main_list0["data"]["fxcal_settings"]["node"]["all_contact_points"][0]["contact_point_info"]
            for dictionary in main_list:
                ids.append(dictionary["owner_profile"]["id"])
            return ids
        except (KeyError, TypeError, IndexError, JSONDecodeError):
            pass
