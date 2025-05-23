import unittest

from pdfminer.high_level import extract_pages, extract_text
from pdfminer.layout import LAParams, LTTextContainer
from tests.helpers import absolute_sample_path


def run_with_string(sample_path, laparams=None):
    if laparams is None:
        laparams = {}
    absolute_path = absolute_sample_path(sample_path)
    s = extract_text(absolute_path, laparams=LAParams(**laparams))
    return s


def run_with_file(sample_path):
    absolute_path = absolute_sample_path(sample_path)
    with open(absolute_path, "rb") as in_file:
        s = extract_text(in_file)
    return s


test_strings = {
    "simple1.pdf": "Hello \n\nWorld\n\nHello \n\nWorld\n\n"
    "H e l l o  \n\nW o r l d\n\n"
    "H e l l o  \n\nW o r l d\n\n\f",
    "simple1.pdf_no_boxes_flow": "Hello \n\nWorld\n\nHello \n\nWorld\n\n"
    "H e l l o  \n\nW o r l d\n\n"
    "H e l l o  \n\nW o r l d\n\n\f",
    "simple2.pdf": "\f",
    "simple3.pdf": "Hello\n\nHello\nあ\nい\nう\nえ\nお\nあ\nい\nう\nえ\nお\n"
    "World\n\nWorld\n\n\f",
    "simple4.pdf": "Text1\nText2\nText3\n\n\f",
    "simple5.pdf": "Heading\n\n"
    "Link to heading that is working with vim-pandoc.\n\n"
    "Link to heading “that is” not working with vim-pandoc.\n\n"
    "Subheading\n\nSome “more text”\n\n1\n\n\f",
    "zen_of_python_corrupted.pdf": "Mai 30, 18 13:27\n\nzen_of_python.txt",
    "contrib/issue_495_pdfobjref.pdf": "8\n\n7\n\n6\n\n5\n\n4\n\n3\n\n2\n\n1"
    "\n\n150,00\n\n30,00\n\n(cid:72) 0,05 A\n\n0\n0\n,\n0\n2\n\n0\n0\n,\n8\n\n"
    "(cid:69) 0,05\n\n0\n0\n,\n0\n5\n\nA\n\nF\n\nE\n\nD\n\n20,00\n\n16,00\n\n"
    "+\n0,05\n15,00 - 0,00\n\nC\n\n0\n0\n,\n0\n4\n\n0\n0\n,\n0\n2\n\n"
    "R18,00\n\nM12x1.75 - 6H\n\n0\n0\n,\n5\n4\n\nB\n\nA\n\n"
    "0\n0\n,\n6\n1\n(cid:142)\n\n0\n0\n,\n6\n1\n\n+\n0,50\n15,00 - 0,00\n\n"
    "60,00 (cid:66)0,02\n\n100,00 (cid:66)0,05\n\n132,00\n\n"
    "9\nH\n0\n1\n(cid:142)\n\n9\nH\n0\n1\n(cid:142)\n\n(cid:68) 0,1 A\n\n"
    "+\n0,00\n70,00 - 0,02\n\n50,00\n\n(cid:76) 0,1\n\n(cid:76) 0,1\n\n"
    "0\n0\n,\n5\n3\n\nF\n\nE\n\nD\n\nC\n\nB\n\nAllgemeintoleranzen\n\n"
    "MATERIAL\n\nDIN ISO 2768 - mK\n\nPET BLACK\n\nFINISH\n\n"
    "Eloxieren (natur)\n\nRa 1,6\n\nDate\n29.03.2021\n\n"
    "Name\nLucas Giering\n\nDrawn\n\nChecked\n\nStandard\n\n"
    "Arretierungshilfe\n\nA\n\n1 \n\nA2\n\n8\n\n7\n\n6\n\n5\n\n4\n\nState\n\n"
    "Changes\n\nDate\n\nName\n\n3\n\n2\n\n1",
    "contrib/issue_566_test_1.pdf": "ISSUE Date：2019-4-25 Buyer：黎荣",
    "contrib/issue_566_test_2.pdf": "甲方：中国饮料有限公司（盖章）",
    "contrib/issue-625-identity-cmap.pdf": "Termin płatności: 2021-05-03",
    "contrib/issue-791-non-unicode-cmap.pdf": "Peněžní prostředky na účtech",
    "contrib/issue-886-xref-stream-widths.pdf": "Hello",
}


class TestExtractText(unittest.TestCase):
    def test_simple1_with_string(self):
        test_file = "simple1.pdf"
        s = run_with_string(test_file)
        self.assertEqual(s, test_strings[test_file])

    def test_simple1_no_boxes_flow(self):
        test_file = "simple1.pdf"
        s = run_with_string(test_file, laparams={"boxes_flow": None})
        self.assertEqual(s, test_strings["simple1.pdf_no_boxes_flow"])

    def test_simple2_with_string(self):
        test_file = "simple2.pdf"
        s = run_with_string(test_file)
        self.assertEqual(s, test_strings[test_file])

    def test_simple3_with_string(self):
        test_file = "simple3.pdf"
        s = run_with_string(test_file)
        self.assertEqual(s, test_strings[test_file])

    def test_simple4_with_string(self):
        test_file = "simple4.pdf"
        s = run_with_string(test_file)
        self.assertEqual(s, test_strings[test_file])

    def test_simple5_with_string(self):
        test_file = "simple5.pdf"
        s = run_with_string(test_file)
        self.assertEqual(s, test_strings[test_file])

    def test_simple1_with_file(self):
        test_file = "simple1.pdf"
        s = run_with_file(test_file)
        self.assertEqual(s, test_strings[test_file])

    def test_simple2_with_file(self):
        test_file = "simple2.pdf"
        s = run_with_file(test_file)
        self.assertEqual(s, test_strings[test_file])

    def test_simple3_with_file(self):
        test_file = "simple3.pdf"
        s = run_with_file(test_file)
        self.assertEqual(s, test_strings[test_file])

    def test_simple4_with_file(self):
        test_file = "simple4.pdf"
        s = run_with_file(test_file)
        self.assertEqual(s, test_strings[test_file])

    def test_simple5_with_file(self):
        test_file = "simple5.pdf"
        s = run_with_file(test_file)
        self.assertEqual(s, test_strings[test_file])

    def test_zlib_corrupted(self):
        test_file = "zen_of_python_corrupted.pdf"
        s = run_with_file(test_file)
        expected = test_strings[test_file]
        self.assertEqual(s[: len(expected)], expected)

    def test_issue_495_pdfobjref_iterable(self):
        test_file = "contrib/issue_495_pdfobjref.pdf"
        s = run_with_file(test_file)
        self.assertEqual(s.strip(), test_strings[test_file])

    def test_issue_566_cmap_bytes(self):
        test_file = "contrib/issue_566_test_1.pdf"
        s = run_with_file(test_file)
        self.assertEqual(s.strip(), test_strings[test_file])

    def test_issue_566_cid_range(self):
        test_file = "contrib/issue_566_test_2.pdf"
        s = run_with_file(test_file)
        self.assertEqual(s.strip(), test_strings[test_file])

    def test_issue_625_identity_cmap(self):
        test_file = "contrib/issue-625-identity-cmap.pdf"
        lines = run_with_file(test_file).splitlines()

        self.assertEqual(lines[6], test_strings[test_file])

    def test_issue_791_non_unicode_cmap(self):
        test_file = "contrib/issue-791-non-unicode-cmap.pdf"
        s = run_with_file(test_file)
        self.assertEqual(s.strip(), test_strings[test_file])

    def test_issue_886_xref_stream_widths(self):
        """Ensure that we can support arbitrary width integers in xref streams"""
        test_file = "contrib/issue-886-xref-stream-widths.pdf"
        s = run_with_file(test_file)
        self.assertEqual(s.strip(), test_strings[test_file])


class TestExtractPages(unittest.TestCase):
    def _get_test_file_path(self):
        test_file = "simple4.pdf"
        return absolute_sample_path(test_file)

    def test_line_margin(self):
        # The lines have margin 0.2 relative to the height.
        # Extract with line_margin 0.19 should break into 3 separate textboxes.
        pages = list(
            extract_pages(
                self._get_test_file_path(),
                laparams=LAParams(line_margin=0.19),
            ),
        )
        self.assertEqual(len(pages), 1)
        page = pages[0]

        elements = [element for element in page if isinstance(element, LTTextContainer)]
        self.assertEqual(len(elements), 3)
        self.assertEqual(elements[0].get_text(), "Text1\n")
        self.assertEqual(elements[1].get_text(), "Text2\n")
        self.assertEqual(elements[2].get_text(), "Text3\n")

        # Extract with line_margin 0.21 should merge into one textbox.
        pages = list(
            extract_pages(
                self._get_test_file_path(),
                laparams=LAParams(line_margin=0.21),
            ),
        )
        self.assertEqual(len(pages), 1)
        page = pages[0]

        elements = [element for element in page if isinstance(element, LTTextContainer)]
        self.assertEqual(len(elements), 1)
        self.assertEqual(elements[0].get_text(), "Text1\nText2\nText3\n")

    def test_no_boxes_flow(self):
        pages = list(
            extract_pages(
                self._get_test_file_path(),
                laparams=LAParams(boxes_flow=None),
            ),
        )
        self.assertEqual(len(pages), 1)
        page = pages[0]

        elements = [element for element in page if isinstance(element, LTTextContainer)]
        self.assertEqual(len(elements), 1)
        self.assertEqual(elements[0].get_text(), "Text1\nText2\nText3\n")
