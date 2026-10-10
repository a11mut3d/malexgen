import pytest

from malexgen.legends import LEGENDS, get_legend, list_legends


def test_legends_registry_not_empty():
    assert len(LEGENDS) > 0


def test_list_legends():
    ids = list_legends()
    assert isinstance(ids, list)
    assert len(ids) == len(LEGENDS)


@pytest.mark.parametrize("legend_id", list(LEGENDS.keys()))
def test_get_legend(legend_id):
    legend = get_legend(legend_id)
    assert legend is not None


@pytest.mark.parametrize("legend_id", list(LEGENDS.keys()))
def test_legend_data(legend_id):
    legend = get_legend(legend_id)
    data = legend.get_legend()

    assert data.id == legend_id
    assert data.name
    assert data.description
    assert data.icon
    assert isinstance(data.permissions, list)
    assert data.popup_title
    assert data.color_scheme


@pytest.mark.parametrize("legend_id", list(LEGENDS.keys()))
def test_legend_popup_html(legend_id):
    legend = get_legend(legend_id)
    html = legend.get_popup_html()

    assert isinstance(html, str)
    assert len(html) > 0


@pytest.mark.parametrize("legend_id", list(LEGENDS.keys()))
def test_legend_popup_css(legend_id):
    legend = get_legend(legend_id)
    css = legend.get_popup_css()

    assert isinstance(css, str)
    assert len(css) > 0


def test_unknown_legend_raises():
    with pytest.raises(ValueError):
        get_legend("unknown_legend_xyz")


def test_legend_ids_unique():
    ids = list_legends()
    assert len(ids) == len(set(ids))
