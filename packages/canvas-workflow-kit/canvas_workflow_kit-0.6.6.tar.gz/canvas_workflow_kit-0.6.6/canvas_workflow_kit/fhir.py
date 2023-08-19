import requests
from urllib.parse import urlencode
from .internal.attrdict import AttrDict


class FHIRHelper:
    client_id: str
    client_secret: str

    base_url: str
    base_fhir_url: str
    token: str | None
    headers: dict | None

    def __init__(self, settings: AttrDict):
        self.token = None
        self.client_id = settings.get("CLIENT_ID")
        self.client_secret = settings.get("CLIENT_SECRET")
        instance_name = settings.get("INSTANCE_NAME")

        self._set_base_urls(instance_name or "your-instance")

        if not self.client_id or not self.client_secret or not instance_name:
            raise Exception(
                f"Unable to perform FHIR API requests without CLIENT_ID, CLIENT_SECRET, and INSTANCE_NAME Protocol Settings. \n"
                f"Navigate here to manage Protocol Settings: {self.base_url}/admin/api/protocolsetting/"
            )

    def _set_base_urls(self, instance_name: str) -> str:
        self.base_url = f"https://{instance_name}.canvasmedical.com"
        self.base_fhir_url = f"https://fhir-{instance_name}.canvasmedical.com"

    def get_fhir_api_token(self) -> str | None:
        """
        Requests and returns a bearer token for authentication to FHIR.
        """
        grant_type = "client_credentials"

        token_response = requests.post(
            f"{self.base_url}/auth/token/",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data=f"grant_type={grant_type}&client_id={self.client_id}&client_secret={self.client_secret}",
        )

        if token_response.status_code != requests.codes.ok:
            raise Exception(
                "Unable to get a valid FHIR bearer token. \n"
                f"Verify that your CLIENT_ID and CLIENT_SECRET Protocol Settings (found here: {self.base_url}/admin/api/protocolsetting/) \n"
                f"match what is defined for your FHIR API third-party application (found here: {self.base_url}/auth/applications/)"
            )

        token = token_response.json().get("access_token")
        self.token = token
        self.headers = {
            "Authorization": f"Bearer {token}",
            "accept": "application/json",
            "content-type": "application/json",
        }
        return token

    def read(self, resource_type: str, resource_id: str) -> requests.Response:
        """
        Given a resource_type (str) and resource_id (str), returns the requested FHIR resource.
        """
        if not self.token:
            self.get_fhir_api_token()
        return requests.get(
            f"{self.base_fhir_url}/{resource_type}/{resource_id}", headers=self.headers
        )

    def search(
        self, resource_type: str, search_params: dict | None = None
    ) -> requests.Response:
        """
        Given a resource_type (str) and search_params (dict), searches and returns a bundle of FHIR resources.
        """
        if not self.token:
            self.get_fhir_api_token()
        params = urlencode(search_params, doseq=True) if search_params else ""
        return requests.get(
            f"{self.base_fhir_url}/{resource_type}?{params}", headers=self.headers
        )

    def create(self, resource_type: str, payload: dict) -> requests.Response:
        """
        Given a resource_type (str) and FHIR resource payload (dict), creates and returns a FHIR resource.
        """
        if not self.token:
            self.get_fhir_api_token()
        return requests.post(
            f"{self.base_fhir_url}/{resource_type}",
            data=payload,
            headers=self.headers,
        )

    def update(
        self, resource_type: str, resource_id: str, payload: dict
    ) -> requests.Response:
        """
        Given a resource_type (str), resource_id (str), and FHIR resource payload (dict), updates and returns a FHIR resource.
        """
        if not self.token:
            self.get_fhir_api_token()
        return requests.put(
            f"{self.base_fhir_url}/{resource_type}/{resource_id}",
            data=payload,
            headers=self.headers,
        )


class FumageHelper(FHIRHelper):
    def _set_base_urls(self, instance_name: str) -> str:
        self.base_url = f"https://{instance_name}.canvasmedical.com"
        self.base_fhir_url = f"https://fumage-{instance_name}.canvasmedical.com"
