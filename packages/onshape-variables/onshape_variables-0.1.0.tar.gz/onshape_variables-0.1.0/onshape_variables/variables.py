from typing import Dict, List, Tuple

import requests

BASE_URL = "https://cad.onshape.com/api/v6"
headers = {
    "Accept": "application/json;charset=UTF-8;qs=0.09",
    "Content-Type": "application/json",
}


# class for interacting with an existing or newly created variable studio
class Variables:
    def __init__(
        self, api_keys: Tuple[str, str], did: str, wid: str, eid: str = ""
    ) -> None:
        self.keys = api_keys
        self.did = did
        self.wid = wid
        self.eid = eid
        self.update_urls()

    def create_varaible_studio(
        self, params: Dict[str, str] = {}, name="my-variable-studio"
    ) -> None:
        request_body = {"name": name}
        response = requests.post(
            self.create_url,
            params=params,
            auth=self.keys,
            json=request_body,
            headers=headers,
        )
        response.raise_for_status()

        self.eid = response.json()["id"]
        self.update_urls()

    def has_duplicates(self, var_list: List[Dict[str, str]]) -> bool:
        names = [item["name"] for item in var_list]
        return len(names) != len(set(names))

    def get_variables(
        self, params={"includeValuesAndReferencedVariables": False}
    ) -> List[Dict[str, any]]:
        self.eid_error_handling()

        response = requests.get(
            self.assign_url,
            params=params,
            auth=self.keys,
            headers=headers,
        )
        response.raise_for_status()

        return response.json()

    def append_variables(self, variables) -> List:
        current_vs = self.get_variables()
        current_variables = current_vs[0]["variables"]
        request_body = current_variables + variables

        if self.has_duplicates(request_body):
            raise ValueError(
                "Variable duplicate found, variables must have unique names!"
            )

        return request_body

    def assign_variables(
        self, variables: List[Dict[str, str]], params: Dict[str, str] = {}, append=True
    ) -> None:
        self.eid_error_handling()

        if append:
            request_body = self.append_variables(variables)
        else:
            if self.has_duplicates(variables):
                raise ValueError(
                    "Variable duplicate found, variables must have unique names!"
                )
            request_body = variables

        response = requests.post(
            self.assign_url,
            params=params,
            auth=self.keys,
            json=request_body,
            headers=headers,
        )
        response.raise_for_status()

    def get_references(self, params: Dict[str, str] = {}) -> Dict:
        self.eid_error_handling()

        response = requests.get(
            self.references_url,
            params=params,
            auth=self.keys,
            headers=headers,
        )
        response.raise_for_status()

        return response.json()

    def append_references(self, references) -> List:
        current_refs = self.get_references()["references"]
        combined_refs = current_refs + references["references"]

        return combined_refs

    def set_references(
        self, references: Dict[str, str], params: Dict[str, str] = {}, append=True
    ) -> None:
        self.eid_error_handling()

        if append:
            references["references"] = self.append_references(references)

        response = requests.post(
            self.references_url,
            params=params,
            auth=self.keys,
            json=references,
            headers=headers,
        )
        response.raise_for_status()

    def set_scope(self, all=True, params: Dict[str, str] = {}) -> None:
        self.eid_error_handling()
        request_body = {"isAutomaticallyInserted": all}
        response = requests.post(
            self.scope_url,
            params=params,
            auth=self.keys,
            json=request_body,
            headers=headers,
        )
        response.raise_for_status()

    def get_scope(self, param: Dict[str, str] = {}) -> Dict:
        self.eid_error_handling()

        # perform api request and handle errors
        response = requests.get(
            self.scope_url,
            params=param,
            auth=self.keys,
            headers=headers,
        )
        response.raise_for_status()

        return response.json()

    def update_urls(self) -> None:
        # UPDATE assign_url and create_url
        self.assign_url = (
            f"{BASE_URL}/variables/d/{self.did}/w/{self.wid}/e/{self.eid}/variables"
        )
        self.create_url = (
            f"{BASE_URL}/variables/d/{self.did}/w/{self.wid}/variablestudio"
        )
        self.references_url = f"{BASE_URL}/variables/d/{self.did}/w/{self.wid}/e/{self.eid}/variablestudioreferences"
        self.scope_url = f"{BASE_URL}/variables/d/{self.did}/w/{self.wid}/e/{self.eid}/variablestudioscope"

    def is_valid_eid(self):
        return isinstance(self.eid, str) and len(self.eid) == 24

    def eid_error_handling(self):
        if self.eid == "":
            raise ValueError(
                "'eid' is missing. Call create_variable_studio() first OR include an existing eid when creating a Variable object."
            )
        if not self.is_valid_eid():
            raise ValueError("Invalid eid. The eid must be a string of 24 characters")
