from opyml import __version__, Body, Head, OPML, Outline
from defusedxml import ElementTree

import pytest


def __read_sample(file_name: str) -> str:
    with open(f"tests/samples/{file_name}.opml", mode="r") as file:
        return file.read()


def test_version():
    assert len(__version__) > 0


def test_to_json():
    opml = OPML("1.1")
    assert '"version": "1.1"' in opml.to_json()
    assert '"outlines": []' in opml.body.to_json()

    opml.head = Head(title="Title")
    assert '"title": "Title"' in opml.head.to_json()

    opml.body.outlines.append(Outline("Outline"))
    assert '"text": "Outline"' in opml.body.outlines[0].to_json()
    assert "null" not in opml.to_json()


def test_valid_samples(snapshot):
    snapshot.snapshot_dir = "tests/samples"
    samples = [
        "minimum_valid_opml",
        "valid_opml_1_0",
        "valid_opml_with_everything",
    ]

    for file_name in samples:
        opml = OPML.from_xml(__read_sample(file_name))
        snapshot.assert_match(f"{opml.to_json()}\n", f"{file_name}.json")


def test_invalid_samples():
    with pytest.raises(ElementTree.ParseError):
        OPML.from_xml(__read_sample("invalid_xml"))

    samples = [
        "invalid_opml_no_body",
        "invalid_opml_no_outlines",
        "invalid_opml_no_version",
        "invalid_opml_not_opml",
        "invalid_opml_version",
    ]

    for file_name in samples:
        with pytest.raises(ValueError):
            OPML.from_xml(__read_sample(file_name))

    with pytest.raises(ValueError):
        OPML(version="unsupported")


def test_construction_1(snapshot):
    opml = OPML(
        version="2.0",
        head=Head(title="Rust Feeds"),
        body=Body(
            outlines=[
                Outline(
                    text="Rust Blog", xml_url="https://blog.rust-lang.org/feed.xml"
                ),
                Outline(
                    text="Inside Rust",
                    xml_url="https://blog.rust-lang.org/inside-rust/feed.xml",
                ),
            ]
        ),
    )

    xml = f"{opml.to_xml()}\n"
    snapshot.snapshot_dir = "tests/samples"
    snapshot.assert_match(xml, "construction_1.opml")


def test_construction_2(snapshot):
    opml = OPML(
        head=Head(title="Rust & Mozilla Feeds"),
        body=Body(
            outlines=[
                Outline(
                    text="Rust Feeds",
                    outlines=[
                        Outline(
                            text="Rust Blog",
                            xml_url="https://blog.rust-lang.org/feed.xml",
                        ),
                        Outline(
                            text="Inside Rust",
                            xml_url="https://blog.rust-lang.org/inside-rust/feed.xml",
                        ),
                    ],
                ),
                Outline(
                    text="Mozilla Feeds",
                    outlines=[
                        Outline(
                            text="Mozilla Blog",
                            xml_url="https://blog.mozilla.org/feed",
                        ),
                        Outline(
                            text="Mozilla Hacks",
                            xml_url="https://hacks.mozilla.org/feed",
                        ),
                    ],
                ),
            ]
        ),
    )

    xml = f"{opml.to_xml()}\n"
    snapshot.snapshot_dir = "tests/samples"
    snapshot.assert_match(xml, "construction_2.opml")


def test_construction_3(snapshot):
    opml = OPML(
        version="2.0",
        head=Head(
            title="Title",
            date_created="Date Created",
            date_modified="Date Modified",
            owner_name="Owner Name",
            owner_email="Owner Email",
            owner_id="Owner ID",
            docs="http://dev.opml.org/spec2.html",
            expansion_state="0,1",
            vert_scroll_state=0,
            window_top=1,
            window_left=2,
            window_bottom=3,
            window_right=4,
        ),
        body=Body(
            outlines=[
                Outline(
                    text="Outline Text",
                    type="Outline Type",
                    is_breakpoint=True,
                    is_comment=True,
                    created="Outline Date",
                    category="Outline Category",
                    xml_url="Outline XML URL",
                    description="Outline Description",
                    html_url="Outline HTML URL",
                    language="Outline Language",
                    title="Outline Title",
                    version="Outline Version",
                    url="Outline URL",
                )
            ]
        ),
    )

    xml = f"{opml.to_xml()}\n"
    snapshot.snapshot_dir = "tests/samples"
    snapshot.assert_match(xml, "construction_3.opml")
