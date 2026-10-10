import pytest

from malexgen.payloads import PAYLOADS, get_payload, list_payloads


def test_payloads_registry_not_empty():
    assert len(PAYLOADS) > 0


def test_list_payloads():
    ids = list_payloads()
    assert isinstance(ids, list)
    assert len(ids) == len(PAYLOADS)


@pytest.mark.parametrize("payload_id", list(PAYLOADS.keys()))
def test_get_payload(payload_id):
    payload = get_payload(payload_id)
    assert payload is not None


@pytest.mark.parametrize("payload_id", list(PAYLOADS.keys()))
def test_payload_data(payload_id):
    payload = get_payload(payload_id)
    data = payload.get_payload()

    assert data.id == payload_id
    assert data.name
    assert data.description
    assert data.icon
    assert data.risk_level in ("low", "medium", "high", "critical")
    assert isinstance(data.permissions, list)
    assert isinstance(data.targets, list)
    assert data.demo_instructions
    assert isinstance(data.mitigation, list)


@pytest.mark.parametrize("payload_id", list(PAYLOADS.keys()))
def test_payload_background_js(payload_id):
    payload = get_payload(payload_id)
    js = payload.get_background_js()

    assert isinstance(js, str)
    assert len(js) > 0


@pytest.mark.parametrize("payload_id", list(PAYLOADS.keys()))
def test_payload_content_js(payload_id):
    payload = get_payload(payload_id)
    js = payload.get_content_js()

    assert isinstance(js, str)
    assert len(js) > 0


@pytest.mark.parametrize("payload_id", list(PAYLOADS.keys()))
def test_payload_popup_js(payload_id):
    payload = get_payload(payload_id)
    js = payload.get_popup_js()

    assert isinstance(js, str)


@pytest.mark.parametrize("payload_id", list(PAYLOADS.keys()))
def test_payload_risk_emoji(payload_id):
    payload = get_payload(payload_id)
    data = payload.get_payload()

    emoji = data.risk_emoji()
    assert isinstance(emoji, str)
    assert len(emoji) > 0


def test_unknown_payload_raises():
    with pytest.raises(ValueError):
        get_payload("unknown_payload_xyz")


def test_payload_ids_unique():
    ids = list_payloads()
    assert len(ids) == len(set(ids))
