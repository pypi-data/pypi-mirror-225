import pytest
from unittest.mock import patch
import requests
from types import SimpleNamespace
from urllib.parse import urlencode

from canvas_workflow_kit.fhir import FHIRHelper, FumageHelper
from canvas_workflow_kit.internal.attrdict import AttrDict

init_settings_error_part1 = "Unable to perform FHIR API requests without CLIENT_ID, CLIENT_SECRET, and INSTANCE_NAME Protocol Settings. \nNavigate here to manage Protocol Settings: "
init_settings_error1 = f"{init_settings_error_part1}https://your-instance.canvasmedical.com/admin/api/protocolsetting/"
init_settings_error2 = f"{init_settings_error_part1}https://hello.canvasmedical.com/admin/api/protocolsetting/"


@pytest.fixture
def settings():
    return AttrDict(
        {"INSTANCE_NAME": "hello", "CLIENT_ID": "id", "CLIENT_SECRET": "secret"}
    )


@pytest.fixture
def api_failure():
    return SimpleNamespace(status_code=requests.codes.server_error)


@pytest.fixture
def api_success():
    return SimpleNamespace(
        status_code=requests.codes.ok, json=lambda: {"access_token": "success"}
    )


class TestFHIRHelper:
    @pytest.fixture
    def fhir(self, settings):
        return FHIRHelper(settings)

    @pytest.mark.parametrize(
        argnames="s,err",
        argvalues=[
            (AttrDict(), init_settings_error1),
            (
                AttrDict({"CLIENT_ID": "id", "CLIENT_SECRET": "secret"}),
                init_settings_error1,
            ),
            (
                AttrDict({"INSTANCE_NAME": "hello", "CLIENT_SECRET": "secret"}),
                init_settings_error2,
            ),
            (
                AttrDict({"INSTANCE_NAME": "hello", "CLIENT_ID": "id"}),
                init_settings_error2,
            ),
        ],
        ids=["no settings", "no instance name", "no client id", "no client secret"],
    )
    def test___init(self, s, err):
        with pytest.raises(Exception) as e:
            FHIRHelper(s)
        assert err in str(e.value)

    def test__init__success(self, fhir: FHIRHelper):
        assert fhir.__dict__ == {
            "token": None,
            "client_id": "id",
            "client_secret": "secret",
            "base_url": "https://hello.canvasmedical.com",
            "base_fhir_url": "https://fhir-hello.canvasmedical.com",
        }

    def test_get_fhir_api_token_failure(self, fhir: FHIRHelper, api_failure):
        with patch.object(requests, "post", return_value=api_failure) as mock_method:
            with pytest.raises(Exception) as e:
                fhir.get_fhir_api_token()

        mock_method.assert_called_once_with(
            "https://hello.canvasmedical.com/auth/token/",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data="grant_type=client_credentials&client_id=id&client_secret=secret",
        )
        assert (
            "Unable to get a valid FHIR bearer token. \n"
            f"Verify that your CLIENT_ID and CLIENT_SECRET Protocol Settings (found here: https://hello.canvasmedical.com/admin/api/protocolsetting/) \n"
            f"match what is defined for your FHIR API third-party application (found here: https://hello.canvasmedical.com/auth/applications/)"
        ) in str(e.value)

    def test_get_fhir_api_token_success(self, fhir: FHIRHelper, api_success):
        with patch.object(requests, "post", return_value=api_success) as mock_method:
            fhir.get_fhir_api_token()

        mock_method.assert_called_once_with(
            "https://hello.canvasmedical.com/auth/token/",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data="grant_type=client_credentials&client_id=id&client_secret=secret",
        )
        assert fhir.__dict__ == {
            "token": "success",
            "client_id": "id",
            "client_secret": "secret",
            "base_url": "https://hello.canvasmedical.com",
            "base_fhir_url": "https://fhir-hello.canvasmedical.com",
            "headers": {
                "Authorization": "Bearer success",
                "accept": "application/json",
                "content-type": "application/json",
            },
        }

    def test_read(self, fhir: FHIRHelper, api_success):
        with patch.object(requests, "post", return_value=api_success):
            fhir.get_fhir_api_token()

        with patch.object(requests, "get", return_value="read") as mock_read:
            fhir.read("Appointment", "123")

        mock_read.assert_called_once_with(
            "https://fhir-hello.canvasmedical.com/Appointment/123",
            headers={
                "Authorization": "Bearer success",
                "accept": "application/json",
                "content-type": "application/json",
            },
        )

    @pytest.mark.parametrize(
        argnames="params",
        argvalues=[
            {"patient": "Patient/123", "status": "proposed"},
            {"date": ["ge2020-01-01", "le2020-02-01"]},
        ],
        ids=["patient and status", "date params"],
    )
    def test_search(self, fhir: FHIRHelper, api_success, params):
        with patch.object(requests, "post", return_value=api_success):
            fhir.get_fhir_api_token()

        with patch.object(requests, "get") as mock_search:
            fhir.search("Appointment", params)

        mock_search.assert_called_once_with(
            f"https://fhir-hello.canvasmedical.com/Appointment?{urlencode(params, doseq=True)}",
            headers={
                "Authorization": "Bearer success",
                "accept": "application/json",
                "content-type": "application/json",
            },
        )

    def test_create(self, fhir: FHIRHelper, api_success):
        with patch.object(requests, "post", return_value=api_success):
            fhir.get_fhir_api_token()

        with patch.object(requests, "post") as mock_create:
            fhir.create("Appointment", {"patient": "Patient/123", "status": "proposed"})

        mock_create.assert_called_once_with(
            "https://fhir-hello.canvasmedical.com/Appointment",
            data={"patient": "Patient/123", "status": "proposed"},
            headers={
                "Authorization": "Bearer success",
                "accept": "application/json",
                "content-type": "application/json",
            },
        )

    def test_update(self, fhir: FHIRHelper, api_success):
        with patch.object(requests, "post", return_value=api_success):
            fhir.get_fhir_api_token()

        with patch.object(requests, "put") as mock_update:
            fhir.update(
                "Appointment", "12345", {"patient": "Patient/123", "status": "proposed"}
            )

        mock_update.assert_called_once_with(
            "https://fhir-hello.canvasmedical.com/Appointment/12345",
            data={"patient": "Patient/123", "status": "proposed"},
            headers={
                "Authorization": "Bearer success",
                "accept": "application/json",
                "content-type": "application/json",
            },
        )


class TestFumageHelper:
    @pytest.fixture
    def fumage(self, settings):
        return FumageHelper(settings)

    def test__init__success(self, fumage: FumageHelper):
        assert fumage.__dict__ == {
            "token": None,
            "client_id": "id",
            "client_secret": "secret",
            "base_url": "https://hello.canvasmedical.com",
            "base_fhir_url": "https://fumage-hello.canvasmedical.com",
        }

    def test_get_fhir_api_token_failure(self, fumage: FumageHelper, api_failure):
        with patch.object(requests, "post", return_value=api_failure) as mock_method:
            with pytest.raises(Exception) as e:
                fumage.get_fhir_api_token()

        mock_method.assert_called_once_with(
            "https://hello.canvasmedical.com/auth/token/",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data="grant_type=client_credentials&client_id=id&client_secret=secret",
        )
        assert (
            "Unable to get a valid FHIR bearer token. \n"
            f"Verify that your CLIENT_ID and CLIENT_SECRET Protocol Settings (found here: https://hello.canvasmedical.com/admin/api/protocolsetting/) \n"
            f"match what is defined for your FHIR API third-party application (found here: https://hello.canvasmedical.com/auth/applications/)"
        ) in str(e.value)

    def test_get_fhir_api_token_success(self, fumage: FumageHelper, api_success):
        with patch.object(requests, "post", return_value=api_success) as mock_method:
            fumage.get_fhir_api_token()

        mock_method.assert_called_once_with(
            "https://hello.canvasmedical.com/auth/token/",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data="grant_type=client_credentials&client_id=id&client_secret=secret",
        )
        assert fumage.__dict__ == {
            "token": "success",
            "client_id": "id",
            "client_secret": "secret",
            "base_url": "https://hello.canvasmedical.com",
            "base_fhir_url": "https://fumage-hello.canvasmedical.com",
            "headers": {
                "Authorization": "Bearer success",
                "accept": "application/json",
                "content-type": "application/json",
            },
        }

    def test_read(self, fumage: FumageHelper, api_success):
        with patch.object(requests, "post", return_value=api_success):
            fumage.get_fhir_api_token()

        with patch.object(requests, "get", return_value="read") as mock_read:
            fumage.read("Appointment", "123")

        mock_read.assert_called_once_with(
            "https://fumage-hello.canvasmedical.com/Appointment/123",
            headers={
                "Authorization": "Bearer success",
                "accept": "application/json",
                "content-type": "application/json",
            },
        )

    @pytest.mark.parametrize(
        argnames="params",
        argvalues=[
            {"patient": "Patient/123", "status": "proposed"},
            {"date": ["ge2020-01-01", "le2020-02-01"]},
        ],
        ids=["patient and status", "date params"],
    )
    def test_search(self, fumage: FumageHelper, api_success, params):
        with patch.object(requests, "post", return_value=api_success):
            fumage.get_fhir_api_token()

        with patch.object(requests, "get") as mock_search:
            fumage.search("Appointment", params)

        mock_search.assert_called_once_with(
            f"https://fumage-hello.canvasmedical.com/Appointment?{urlencode(params, doseq=True)}",
            headers={
                "Authorization": "Bearer success",
                "accept": "application/json",
                "content-type": "application/json",
            },
        )

    def test_create(self, fumage: FumageHelper, api_success):
        with patch.object(requests, "post", return_value=api_success):
            fumage.get_fhir_api_token()

        with patch.object(requests, "post") as mock_create:
            fumage.create(
                "Appointment", {"patient": "Patient/123", "status": "proposed"}
            )

        mock_create.assert_called_once_with(
            "https://fumage-hello.canvasmedical.com/Appointment",
            data={"patient": "Patient/123", "status": "proposed"},
            headers={
                "Authorization": "Bearer success",
                "accept": "application/json",
                "content-type": "application/json",
            },
        )

    def test_update(self, fumage: FumageHelper, api_success):
        with patch.object(requests, "post", return_value=api_success):
            fumage.get_fhir_api_token()

        with patch.object(requests, "put") as mock_update:
            fumage.update(
                "Appointment", "12345", {"patient": "Patient/123", "status": "proposed"}
            )

        mock_update.assert_called_once_with(
            "https://fumage-hello.canvasmedical.com/Appointment/12345",
            data={"patient": "Patient/123", "status": "proposed"},
            headers={
                "Authorization": "Bearer success",
                "accept": "application/json",
                "content-type": "application/json",
            },
        )
