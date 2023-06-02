from license_expression import ExpressionError
import pytest

from ..constellations.data import ImageContentPermissions


@pytest.fixture
def valid_permissions_data():
    return {
        "copyright": "Some copyright information",
        "credits": "<strong>Image Credit:</strong> Someone",
        "license": "BSD-2-Clause",
    }


def test_valid_image_permissions(valid_permissions_data):
    permissions = ImageContentPermissions(**valid_permissions_data)

    assert permissions.copyright == valid_permissions_data["copyright"]
    assert permissions.credits == valid_permissions_data["credits"]
    assert permissions.license == valid_permissions_data["license"]


def test_invalid_permissions_license(valid_permissions_data):
    with pytest.raises(ExpressionError):
        permissions_data = valid_permissions_data.copy()
        permissions_data["license"] = "NO SUCH LICENSE"
        ImageContentPermissions(**permissions_data)


def test_sanitize_permissions_html(valid_permissions_data):
    permissions_data = valid_permissions_data.copy()
    permissions_data["credits"] = "<script>Some JS here</script><a>Credits Link</a>"
    permissions = ImageContentPermissions(**permissions_data)

    assert permissions.copyright == permissions_data["copyright"]
    assert permissions.license == permissions_data["license"]
    assert permissions.credits == "<a>Credits Link</a>"
