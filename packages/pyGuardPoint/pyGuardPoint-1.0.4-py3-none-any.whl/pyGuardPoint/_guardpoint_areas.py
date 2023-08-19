from .guardpoint_dataclasses import Area
from .guardpoint_error import GuardPointError, GuardPointUnauthorized


class AreasAPI:
    def get_areas(self):
        url = "/odata/API_Areas"
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        code, json_body = self.gp_json_query("GET", headers=headers, url=url)

        if code != 200:
            error_msg = ""
            if isinstance(json_body, dict):
                if 'error' in json_body:
                    error_msg = json_body['error']
                if 'errors' in json_body:
                    if isinstance(json_body['errors'], dict):
                        for key in json_body['errors']:
                            if isinstance(json_body['errors'][key], list):
                                error_msg = error_msg + json_body['errors'][key][0] + '\n';
                            elif isinstance(json_body['errors'][key], str):
                                error_msg = error_msg + json_body['errors'][key][0] + '\n';
            if code == 401:
                raise GuardPointUnauthorized(f"Unauthorized - ({error_msg})")
            else:
                raise GuardPointError(f"No body - ({code})")

        if not isinstance(json_body, dict):
            raise GuardPointError("Badly formatted response.")
        if 'value' not in json_body:
            raise GuardPointError("Badly formatted response.")
        if not isinstance(json_body['value'], list):
            raise GuardPointError("Badly formatted response.")

        areas = []
        for x in json_body['value']:
            areas.append(Area(x))
        return areas