from pathlib import Path

from pmc_toolkit.xml_parse_api import _authors_with_affiliations
from pmc_toolkit.xml_parse_utils import (
    extract_article_data,
    extract_headings,
    extract_references,
    load_xml,
)

SAMPLE_XML = """\
<article article-type="research-article" xml:lang="en" xmlns:xlink="http://www.w3.org/1999/xlink">
  <front>
    <journal-meta>
      <journal-id journal-id-type="nlm-ta">bioRxiv</journal-id>
      <journal-title-group>
        <journal-title>bioRxiv</journal-title>
      </journal-title-group>
      <issn pub-type="epub">2692-8205</issn>
      <publisher>
        <publisher-name>Cold Spring Harbor Laboratory</publisher-name>
        <publisher-loc>US</publisher-loc>
      </publisher>
    </journal-meta>
    <article-meta>
      <article-id pub-id-type="pmcid">PMC11370360</article-id>
      <article-id pub-id-type="pmcid-ver">PMC11370360.2</article-id>
      <article-id pub-id-type="doi">10.1101/example</article-id>
      <title-group>
        <article-title>An Accurate Speech Neuroprosthesis</article-title>
      </title-group>
      <contrib-group>
        <contrib contrib-type="author">
          <name>
            <surname>Doe</surname>
            <given-names>Jane</given-names>
          </name>
          <xref ref-type="aff" rid="aff1" />
        </contrib>
      </contrib-group>
      <aff id="aff1"><label>1</label>Department of Examples</aff>
      <author-notes>
        <fn fn-type="con" id="fn1">
          <label>*</label>
          <p>Equal contribution.</p>
        </fn>
        <corresp id="cor1">Correspondence: <email>jane@example.org</email></corresp>
      </author-notes>
      <abstract>
        <p>This is the abstract.</p>
      </abstract>
      <pub-date pub-type="epub">
        <year>2024</year>
        <month>8</month>
        <day>30</day>
      </pub-date>
      <volume>12</volume>
      <issue>3</issue>
      <fpage>10</fpage>
      <lpage>15</lpage>
      <kwd-group>
        <kwd>brain-computer interface</kwd>
      </kwd-group>
      <permissions>
        <license license-type="cc-by">
          <license-p>Creative Commons</license-p>
          <ext-link xlink:href="https://creativecommons.org/licenses/by/4.0/" />
        </license>
      </permissions>
      <related-article related-article-type="published-article" xlink:href="PMC999">
        <article-title>Published version</article-title>
        <source>Nature</source>
        <volume>1</volume>
        <fpage>20</fpage>
        <lpage>21</lpage>
        <date><year>2025</year><month>6</month><day>12</day></date>
        <pub-id pub-id-type="doi">10.1000/published</pub-id>
      </related-article>
      <custom-meta-group>
        <custom-meta>
          <meta-name>pmc-prop-open-access</meta-name>
          <meta-value>yes</meta-value>
        </custom-meta>
      </custom-meta-group>
    </article-meta>
  </front>
  <body>
    <p id="body-p1">Opening body paragraph.</p>
    <sec id="s1">
      <title>Introduction</title>
      <p id="intro-p1">Text with <xref ref-type="bibr" rid="R1">1</xref>.</p>
      <sec id="s1-1">
        <title>Background</title>
        <p id="background-p1">Nested text.</p>
      </sec>
    </sec>
    <sec id="s2">
      <title>Methods</title>
      <p id="methods-p1">Methods text.</p>
    </sec>
    <fig id="fig1">
      <label>Figure 1</label>
      <caption><p>Example figure.</p></caption>
      <graphic xlink:href="fig1.jpg" />
    </fig>
    <table-wrap id="tbl1">
      <label>Table 1</label>
      <caption><p>Example table.</p></caption>
      <table>
        <thead><tr><th>Measure</th><th>Value</th></tr></thead>
        <tbody><tr><td>Accuracy</td><td>95%</td></tr></tbody>
      </table>
    </table-wrap>
  </body>
  <back>
    <ack id="ack1">
      <title>Acknowledgements</title>
      <p>Thanks to the participant.</p>
    </ack>
    <fn-group>
      <fn fn-type="COI-statement" id="coi1">
        <p><bold>Competing Interests</bold>: None.</p>
      </fn>
      <fn id="supp1">
        <p><bold>Video 1:</bold> Example video.</p>
        <p>Link: <ext-link xlink:href="https://example.org/video" ext-link-type="uri">video</ext-link></p>
      </fn>
    </fn-group>
    <sec sec-type="data-availability" id="data1">
      <title>Data availability</title>
      <p>Data are available.</p>
    </sec>
    <ref-list>
      <ref id="R1">
        <label>1</label>
        <element-citation publication-type="journal">
          <article-title>Prior work</article-title>
          <source>Example Journal</source>
          <year>2020</year>
          <pub-id pub-id-type="doi">10.1000/prior</pub-id>
        </element-citation>
      </ref>
    </ref-list>
  </back>
</article>
"""


def test_extract_article_data_returns_normalized_categories(tmp_path: Path) -> None:
    path = tmp_path / "article.xml"
    path.write_text(SAMPLE_XML, encoding="utf-8")

    data = extract_article_data(load_xml(path))

    assert list(data) == [
        "title",
        "journal",
        "article",
        "affiliations",
        "author_notes",
        "related_articles",
        "custom_metadata",
        "abstract",
        "content",
        "sections",
        "acknowledgements",
        "data_availability",
        "competing_interests",
        "supplementary_media",
        "references",
        "figures",
        "tables",
    ]
    assert data["title"] == "An Accurate Speech Neuroprosthesis"
    assert data["journal"]["title"] == "bioRxiv"
    assert data["journal"]["issn"]["epub"] == "2692-8205"
    assert data["article"]["identifiers"]["pmcid-ver"] == "PMC11370360.2"
    assert data["article"]["title"] == "An Accurate Speech Neuroprosthesis"
    assert data["article"]["type"] == "research-article"
    assert data["article"]["language"] == "en"
    assert data["article"]["authors"][0]["name"] == "Jane Doe"
    assert data["article"]["authors"][0]["affiliation_ids"] == ["aff1"]
    assert data["article"]["publication_dates"] == [
        {"date": "2024-08-30", "type": "epub"}
    ]
    assert data["article"]["pages"] == "10-15"
    assert data["article"]["keywords"] == ["brain-computer interface"]
    assert (
        data["article"]["permissions"]["license"]["url"]
        == "https://creativecommons.org/licenses/by/4.0/"
    )
    assert data["abstract"] == {"text": "This is the abstract.", "sections": []}
    assert data["affiliations"] == [
        {"source_id": "aff1", "label": "1", "text": "Department of Examples"}
    ]
    assert data["author_notes"]["notes"][0]["type"] == "con"
    assert data["author_notes"]["correspondence"][0]["emails"] == ["jane@example.org"]
    assert data["related_articles"][0]["href"] == "PMC999"
    assert data["related_articles"][0]["date"] == "2025-06-12"
    assert data["related_articles"][0]["identifiers"]["doi"] == "10.1000/published"
    assert data["custom_metadata"] == {"pmc-prop-open-access": "yes"}


def test_extract_article_data_returns_content_and_back_matter(tmp_path: Path) -> None:
    path = tmp_path / "article.xml"
    path.write_text(SAMPLE_XML, encoding="utf-8")

    data = extract_article_data(load_xml(path))

    assert data["sections"] == [
        "(1) Introduction",
        "(1.1) Background",
        "(2) Methods",
    ]
    assert "headings" not in data["content"]
    assert data["content"]["paragraphs"][0]["source_id"] == "body-p1"
    assert "content_id" not in data["content"]["paragraphs"][0]
    assert data["content"]["sections"][0]["source_id"] == "s1"
    assert data["content"]["sections"][0]["section_id"] == "1"
    assert "content_id" not in data["content"]["sections"][0]
    assert data["content"]["sections"][0]["paragraphs"][0]["source_id"] == "intro-p1"
    assert "content_id" not in data["content"]["sections"][0]["paragraphs"][0]
    assert data["content"]["sections"][0]["paragraphs"][0]["reference_ids"] == ["R1"]
    assert data["content"]["sections"][0]["sections"][0]["title"] == "Background"
    assert data["content"]["sections"][0]["sections"][0]["section_id"] == "1.1"
    assert "content_id" not in data["content"]["sections"][0]["sections"][0]
    assert (
        "content_id"
        not in data["content"]["sections"][0]["sections"][0]["paragraphs"][0]
    )
    assert data["content"]["sections"][1]["source_id"] == "s2"
    assert data["content"]["sections"][1]["section_id"] == "2"
    assert "content_id" not in data["content"]["sections"][1]
    assert "content_id" not in data["content"]["sections"][1]["paragraphs"][0]
    assert data["references"][0]["source_id"] == "R1"
    assert data["references"][0]["article_title"] == "Prior work"
    assert data["references"][0]["identifiers"]["doi"] == "10.1000/prior"
    assert data["figures"][0]["graphics"] == ["fig1.jpg"]
    assert data["tables"][0]["rows"] == [["Measure", "Value"], ["Accuracy", "95%"]]
    assert data["acknowledgements"][0]["paragraphs"][0]["text"] == (
        "Thanks to the participant."
    )
    assert "content_id" not in data["acknowledgements"][0]["paragraphs"][0]
    assert data["data_availability"][0]["paragraphs"][0]["text"] == (
        "Data are available."
    )
    assert "content_id" not in data["data_availability"][0]
    assert "section_id" not in data["data_availability"][0]
    assert "content_id" not in data["data_availability"][0]["paragraphs"][0]
    assert data["competing_interests"][0]["source_id"] == "coi1"
    assert data["supplementary_media"][0]["source_id"] == "supp1"
    assert data["supplementary_media"][0]["paragraphs"][0]["text"] == (
        "Video 1: Example video."
    )
    assert data["supplementary_media"][0]["links"][0]["href"] == (
        "https://example.org/video"
    )


def test_extract_headings_returns_content_headings(tmp_path: Path) -> None:
    path = tmp_path / "article.xml"
    path.write_text(SAMPLE_XML, encoding="utf-8")

    assert extract_headings(load_xml(path)) == [
        "(1) Introduction",
        "(1.1) Background",
        "(2) Methods",
    ]


def test_extract_content_omits_empty_top_level_paragraphs(tmp_path: Path) -> None:
    path = tmp_path / "article.xml"
    path.write_text(
        """
        <article>
          <body>
            <sec id="S1">
              <title>Introduction</title>
              <p id="P1">Section paragraph.</p>
            </sec>
          </body>
        </article>
        """,
        encoding="utf-8",
    )

    data = extract_article_data(load_xml(path))

    assert "paragraphs" not in data["content"]
    assert data["content"]["sections"][0]["paragraphs"][0]["source_id"] == "P1"


def _references(tmp_path: Path, ref_list: str) -> list[dict]:
    path = tmp_path / "article.xml"
    path.write_text(
        '<article xmlns:xlink="http://www.w3.org/1999/xlink"><back>'
        f"<ref-list>{ref_list}</ref-list></back></article>",
        encoding="utf-8",
    )
    return extract_references(load_xml(path))


def test_extract_references_merges_citation_alternatives(tmp_path: Path) -> None:
    references = _references(
        tmp_path,
        """
        <ref id="CR6"><label>6.</label><citation-alternatives>
          <element-citation id="ec-CR6" publication-type="journal">
            <person-group person-group-type="author">
              <name name-style="western"><surname>Strauss</surname><given-names>P</given-names></name>
              <name name-style="western"><surname>Lin</surname><given-names>A</given-names></name>
            </person-group>
            <article-title>Associations between negative life experiences</article-title>
            <source>Psychol Med</source><year>2020</year><volume>50</volume>
            <issue>5</issue><fpage>808</fpage><lpage>817</lpage>
            <pub-id pub-id-type="doi">10.1017/S0033291719000643</pub-id>
          </element-citation>
          <mixed-citation id="mc-CR6" publication-type="journal">Strauss P, Lin A (2020)
            Associations between negative life experiences. Psychol Med 50(5):808-817
            <pub-id pub-id-type="pmid">31280740</pub-id></mixed-citation>
        </citation-alternatives></ref>
        """,
    )

    assert len(references) == 1
    reference = references[0]
    assert reference["source_id"] == "CR6"
    assert reference["text"].startswith("Strauss P, Lin A (2020)")
    assert reference["identifiers"] == {
        "doi": "10.1017/S0033291719000643",
        "pmid": "31280740",
    }
    assert reference["authors"] == [
        {"given_names": "P", "surname": "Strauss", "full_name": "P Strauss"},
        {"given_names": "A", "surname": "Lin", "full_name": "A Lin"},
    ]
    assert "authors_truncated" not in reference
    assert (
        reference["article_title"] == "Associations between negative life experiences"
    )
    assert reference["source"] == "Psychol Med"
    assert reference["year"] == "2020"
    assert reference["pages"] == "808-817"


def test_extract_references_reads_mixed_citation_authors(tmp_path: Path) -> None:
    references = _references(
        tmp_path,
        """
        <ref id="b31"><mixed-citation publication-type="book">
          <string-name><surname>Kline</surname>, <given-names>R. B.</given-names></string-name>
          (<year>2015</year>). <source>Principles and practice of structural equation
          modeling</source>. <publisher-name>Guilford publications</publisher-name>.
        </mixed-citation></ref>
        <ref id="b32"><mixed-citation publication-type="journal">
          <string-name>Smith J</string-name>, <collab>WHO Study Group</collab>, et al.
          <article-title>Results of the trial</article-title>.
          <pub-id pub-id-type="medline">12345</pub-id>
        </mixed-citation></ref>
        """,
    )

    kline, smith = references
    assert kline["authors"] == [
        {"given_names": "R. B.", "surname": "Kline", "full_name": "R. B. Kline"}
    ]
    assert kline["publisher"] == "Guilford publications"
    assert kline["year"] == "2015"
    assert smith["authors"] == [
        {"full_name": "Smith J"},
        {"full_name": "WHO Study Group", "collaboration": "WHO Study Group"},
    ]
    assert smith["authors_truncated"] is True
    assert smith["identifiers"] == {"pmid": "12345"}


def test_extract_references_detects_truncation_and_skips_editors(
    tmp_path: Path,
) -> None:
    references = _references(
        tmp_path,
        """
        <ref id="R1"><element-citation publication-type="journal">
          <person-group person-group-type="author">
            <name><surname>Radford</surname><given-names>A</given-names></name>
            <etal/>
          </person-group>
          <article-title>Learning transferable visual models</article-title>
        </element-citation></ref>
        <ref id="R2"><element-citation publication-type="book">
          <person-group person-group-type="author">
            <name><surname>Doe</surname><given-names>J</given-names></name>
          </person-group>
          <person-group person-group-type="editor">
            <name><surname>Editor</surname><given-names>E</given-names></name>
            <etal/>
          </person-group>
          <chapter-title>A review of Smith et al. results</chapter-title>
          <source>Handbook</source>
        </element-citation></ref>
        """,
    )

    radford, doe = references
    assert radford["authors_truncated"] is True
    assert [author["surname"] for author in doe["authors"]] == ["Doe"]
    assert "authors_truncated" not in doe
    assert doe["chapter_title"] == "A review of Smith et al. results"


def test_extract_references_splits_refs_citing_several_works(tmp_path: Path) -> None:
    references = _references(
        tmp_path,
        """
        <ref id="R7"><label>7</label>
          <mixed-citation publication-type="journal"><article-title>First</article-title></mixed-citation>
          <mixed-citation publication-type="journal"><article-title>Second</article-title></mixed-citation>
        </ref>
        """,
    )

    assert [
        (ref["source_id"], ref["label"], ref["article_title"]) for ref in references
    ] == [
        ("R7", "7", "First"),
        ("R7", "7", "Second"),
    ]


def _authors(tmp_path: Path, article_meta: str) -> list[dict]:
    path = tmp_path / "article.xml"
    path.write_text(
        f"<article><front><article-meta>{article_meta}</article-meta></front></article>",
        encoding="utf-8",
    )
    data = extract_article_data(load_xml(path))
    return _authors_with_affiliations(data["article"]["authors"], data["affiliations"])


def test_authors_link_affiliations_nested_in_contrib_group(tmp_path: Path) -> None:
    authors = _authors(
        tmp_path,
        """
        <contrib-group>
          <contrib contrib-type="author">
            <name><surname>Sarkar</surname><given-names>F</given-names></name>
            <xref ref-type="aff" rid="Aff1 Aff2"/>
          </contrib>
          <aff id="Aff1"><label>1</label><institution-wrap>
            <institution-id institution-id-type="ROR">https://ror.org/055m2tx54</institution-id>
            <institution>North-Eastern Hill University</institution></institution-wrap>, Shillong, India</aff>
          <aff id="Aff2">Second Institute</aff>
        </contrib-group>
        """,
    )

    assert authors[0]["affiliations"] == [
        "North-Eastern Hill University , Shillong, India",
        "Second Institute",
    ]


def test_authors_share_unreferenced_and_nested_affiliations(tmp_path: Path) -> None:
    authors = _authors(
        tmp_path,
        """
        <contrib-group>
          <contrib contrib-type="author"><name><surname>A</surname></name></contrib>
          <contrib contrib-type="author"><name><surname>B</surname></name>
            <aff>Own Institute</aff></contrib>
        </contrib-group>
        <aff>Shared Hospital</aff>
        """,
    )

    assert [author["affiliations"] for author in authors] == [
        ["Shared Hospital"],
        ["Own Institute"],
    ]
