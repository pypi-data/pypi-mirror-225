"""This module is used to parse reference.

Supported source type:
- Web of Science
- CSSCI
- Scopus
"""
import re
from typing import Optional, Literal
from dataclasses import dataclass, asdict


@dataclass
class WosField:
    """@private"""

    First_AU: Optional[str] = None
    PY: Optional[str] = None
    J9: Optional[str] = None
    VL: Optional[str] = None
    BP: Optional[str] = None
    DI: Optional[str] = None


@dataclass
class CssciField:
    """@private"""

    First_AU: Optional[str] = None
    TI: Optional[str] = None
    SO: Optional[str] = None
    PY: Optional[str] = None
    VL: Optional[str] = None


@dataclass
class ScopusField:
    """@private"""

    First_AU: Optional[str] = None
    TI: Optional[str] = None
    SO: Optional[str] = None
    VL: Optional[str] = None
    IS: Optional[str] = None
    BP: Optional[str] = None
    EP: Optional[str] = None
    PY: Optional[str] = None


class ParseReference:
    @staticmethod
    def _parse_wos_ref(
        ref: str, doc_index: Optional[int] = None
    ) -> Optional[dict[str, Optional[str]]]:
        """Parse reference of Web of Science.

        Args:
            ref: A reference string. e.g. `CORTES C, 1995, MACH LEARN, V20, P273, DOI 10.1007/BF00994018`
            doc_index: doc_index to which the reference belongs. Default is None.

        Returns:
            A dict of reference fields.
        """
        # Refs contain another language except english or AU is anonymous
        if re.search(r"[\[\]]", ref):
            return None

        # Don't parse patent
        if "Patent No." in ref:
            return None

        AU, PY, J9, VL, BP, DI = None, None, None, None, None, None

        if ", DOI " in ref:
            # Contain only one DOI
            if "DOI [" not in ref:
                DI_match = re.search(r"DOI (10.*)$", ref)
                DI = DI_match[1] if DI_match else None
            # Contain multi DOIs
            else:
                DI_match = re.search(r"DOI \[(.*)\]", ref)
                DI = DI_match[1] if DI_match else None
            ref = re.sub(r", DOI.*", "", ref)

        BP_match = re.search(r", [Pp]([A-Za-z]?\d+)$", ref)
        if BP_match:
            BP = BP_match[1]
            ref = re.sub(r", [Pp][A-Za-z]?\d+", "", ref)

        ref = re.sub(r"[,\.] PROCEEDINGS(?=, )", "", ref, flags=re.I)
        if VL_match := re.search(r", V([\d-]+)$", ref):
            VL = VL_match[1]
            sub_pattern = r", V[\d-]+$"

        elif re.search(r", VOL[s\.]? ", ref, re.I):
            VL_match = re.search(r", VOL[s\.]? ([\w\- ]+)$", ref, re.I)
            VL = VL_match[1] if VL_match else None
            sub_pattern = r", V[Oo][Ll].*"

        elif VL_match := re.search(r"(?<=[A-Z\.]), V([\w\. ]+)$", ref):
            VL = VL_match[1]
            sub_pattern = r"(?<=[A-Z\.]), V[\w\. ]+$"

        else:
            sub_pattern = None

        if sub_pattern:
            ref = re.sub(sub_pattern, "", ref)

        dot_count = ref.count(", ")
        if dot_count == 2:
            AU, PY, J9 = ref.split(", ")
        elif dot_count > 2:
            PY_pattern = r", (\d{4}), "
            if re.search(PY_pattern, ref):
                AU, PY, J9 = re.split(PY_pattern, ref, 1)
        else:
            return None

        if DI:
            DI = DI.lower()
            if len(re.findall(", ", DI)) == 1:
                try:
                    DI1, DI2 = DI.replace("doi ", "").split(", ")
                except:
                    return None
                if DI1 == DI2:
                    DI = DI1
                else:
                    DI = None

        if PY and not re.match(r"^\d{4}$", PY):
            PY = None

        result = asdict(WosField(AU, PY, J9, VL, BP, DI))
        if doc_index is not None:
            result["doc_index"] = doc_index
        return result

    @staticmethod
    def _parse_cssci_ref(
        ref: str, doc_index: Optional[int] = None
    ) -> Optional[dict[str, Optional[str]]]:
        """Parse reference of CSSCI. Only parse reference in Chinese language.

        Args:
            ref: A reference string. e.g. `1.严栋.基于物联网的智慧图书馆.图书馆学刊.2010.32(7)`
            doc_index: doc_index to which the reference belongs. Default is None.
        
        Returns:
            A dict of reference fields.
        """
        dot_pattern = re.compile(
            r"(?<!\d)\.(?!\d)|(?<=\d)\.(?!\d)|(?<!\d)\.(?=\d)|(?<=\d{4})\.(?=\d)|(?<=\d)\.(?=\d{4})"
        )

        if re.search(r"[\u4e00-\u9fa5]", ref):
            dot_count = len(dot_pattern.findall(ref))

            if re.search(r"[^\d]\.{2,}", ref):
                return None

            # Dissertation
            elif ":学位论文." in ref:
                try:
                    _, AU, TI, other = ref.split(".")
                except:
                    return None
                else:
                    TI = TI.replace(":学位论文", "")
                    SO, PY = other.split(",")
                    PY = PY.split(":")[0]
                    raw_result = CssciField(AU, TI, SO, PY, None)

            # Country standard
            elif "GB/T" in ref:
                if ref[-3:] == "出版社":
                    _, AU, other = ref.split(".", 2)
                    TI, SO = other.rsplit(".", 1)
                    raw_result = CssciField(AU, TI, SO, None, None)
                else:
                    _, AU, TI = ref.split(".", 2)
                    raw_result = CssciField(AU, TI, None, None, None)

            # Standard
            elif re.search(r":DB\d{2}/T", ref):
                _, AU, other = ref.split(".", 2)
                TI, PY = other.rsplit(".", 1)
                raw_result = CssciField(AU, TI, None, PY, None)

            # Newspaper
            elif re.search(r"\.\d{1,2}\.\d{1,2}(?:\(|$)", ref):
                try:
                    _, AU, TI, SO, other = re.split(dot_pattern, ref, 4)
                except:
                    return None
                else:
                    raw_result = CssciField(AU, TI, SO, None, None)

            # Patent1
            elif re.search(r"\.CN\d{9}[A-Z]$", ref):
                TI = ref.split(".", 1)[1]
                raw_result = CssciField(None, TI, None, None, None)
            # Patent2
            elif re.search(r"^\d+\.一种", ref):
                date_pattern = re.compile(r"\d{4}\-\d{1,2}\-\d{1,2}")
                TI = ref.split(".", 1)[1]
                date = date_pattern.search(ref)
                if date:
                    PY = date[0].split("-")[0]
                else:
                    PY = None
                TI = date_pattern.sub("", TI).strip(".()")
                raw_result = CssciField(None, TI, None, PY, None)

            # Network resource
            elif re.search(r"\.\d{4}$", ref):
                if dot_count == 3:
                    _, AU, TI, PY = re.split(dot_pattern, ref)
                elif dot_count == 4:
                    _, AU, TI, SO, PY = re.split(dot_pattern, ref)
                else:
                    return None
                raw_result = CssciField(AU, TI, None, PY, None)

            # Journal1
            elif dot_count == 5:
                _, AU, TI, SO, PY, VL = re.split(dot_pattern, ref)
                raw_result = CssciField(AU, TI, SO, PY, VL)
            # Journal2
            elif dot_count == 4:
                _, AU, TI, SO, _ = re.split(dot_pattern, ref)
                raw_result = CssciField(AU, TI, SO, None, None)

            # Book
            elif dot_count == 3:
                _, AU, TI, SO = re.split(dot_pattern, ref)
                raw_result = CssciField(AU, TI, SO, None, None)

            elif dot_count == 2:
                _, AU, TI = re.split(dot_pattern, ref)
                raw_result = CssciField(AU, TI, None, None, None)

            elif dot_count == 1:
                _, TI = re.split(dot_pattern, ref)
                raw_result = CssciField(None, TI, None, None, None)
            else:
                return None

            result = asdict(raw_result)
            if doc_index is not None:
                result["doc_index"] = doc_index
            return result

    @staticmethod
    def _parse_scopus_ref(
        ref: str, doc_index: Optional[int] = None
    ) -> Optional[dict[str, Optional[str]]]:
        """Parse reference of Scopus.

        Args:
            ref: A reference string. e.g. `Negri E, Fumagalli L, Macchi M., A Review of the Roles of Digital Twin in CPS-based Production Systems, Procedia Manufacturing, 11, pp. 939-948, (2017)`
            doc_index: doc_index to which the reference belongs. Default is None.
        
        Returns:
            A dict of reference fields.
        """
        if re.search(r"^[^A-Z\*\']", ref):
            return None

        if re.search(r"[\[\]]", ref):
            return None

        if ref.count(", ") < 2:
            return None

        # Publication year
        PY_match = re.search(r", \((\d{4})\)$", ref)
        if PY_match:
            PY = PY_match[1]
            ref = ref.rsplit(", ", 1)[0]
        else:
            return None

        First_AU, TI, SO, VL, IS, BP, EP = None, None, None, None, None, None, None

        # remove version info
        ref = re.sub(r", version [\d\.]+(?=,)", "", ref, flags=re.I)

        # remove doi info
        ref = re.sub(r", doi:.*(?=,|$)", "", ref, flags=re.I)

        # remove retrieval info
        ref = re.sub(r"[\.,] Retrieved.*(?=,)", "", ref, flags=re.I)
        ref = re.sub(r", Available from:(?=,)", "", ref, flags=re.I)

        # Page number
        if PP_match := re.search(r"(?:, | \()[Pp]{2}[\.,] ([\w\-]+)\)?", ref):
            PP = PP_match[1]
            try:
                BP, EP = re.split(r"-", PP, 1)
            except:
                BP, EP = None, None
            ref = re.sub(r"(?:, | \()[Pp]{2}.*", "", ref)

        # Volume and Issue
        if VL_IS_match := re.search(r", (\d+\s?[A-Za-z]*, [\w\s\-\.\–]+)$", ref):
            VL, IS = VL_IS_match[1].split(", ")
            ref = ref.rsplit(", ", 2)[0]

        elif IS_match := re.search(r", ([\w-]* ?suppl\.? ?[\w-]*)$", ref, re.I):
            IS = IS_match[1]
            ref = ref.rsplit(", ", 1)[0]

        elif IS_match := re.search(r", (\d* ?PART\.? [A-Z\d]+)$", ref, re.I):
            IS = IS_match[1]
            ref = ref.rsplit(", ", 1)[0]

        elif IS_match := re.search(r", ([Nn]o\. \d+)$", ref):
            IS = IS_match[1]
            ref = ref.rsplit(", ", 1)[0]

        if VL_match := re.search(r", (\d+)$", ref):
            VL = VL_match[1]
            ref = ref.rsplit(", ", 1)[0]

        elif VL_match := re.search(r", ([Vv]ol\. [\w\s\.:]+)$", ref):
            VL = VL_match[1]
            ref = ref.rsplit(", ", 1)[0]

        # Author
        full_name_pattern = r"^(?:[a-zA-Z][a-zA-Z\-\.\']*\s)+[A-Z][a-zA-Z\-\.\']*(, |$)"
        if re.search(r"Et al\.", ref, flags=re.I):
            First_AU = ref.split(", ")[0]
            ref = re.sub(r"^.*Et al\.,?\s?", "", ref, flags=re.I)

        elif "., " in ref:
            AU = ref.rsplit("., ", 1)[0]
            if "," in AU:
                First_AU = AU.split(", ")[0]
            else:
                First_AU = AU + "."
            ref = ref.replace(f"{AU}., ", "")

        elif re.search(r"^(?:[A-Z][a-zA-Z]*\s)+[A-Z][a-zA-Z]*(?=, )", ref):
            First_AU = ref.split(", ", 1)[0]
            ref = ref.replace(f"{First_AU}, ", "")

        elif re.search(r"^[A-Z-]+, (?=[A-Z])", ref):
            First_AU = ref.split(", ", 1)[0]
            ref = ref.replace(f"{First_AU}, ", "")

        elif re.search(full_name_pattern, ref):
            First_AU = re.split(", ", ref, 1)[0]
            while re.search(full_name_pattern, ref):
                ref = re.sub(full_name_pattern, "", ref, 1)

        else:
            return None

        # Title and Source
        if ref != "":
            comma_pattern = r", (?![^\[]*\]|[^(]*\))"
            comma_count = len(re.findall(comma_pattern, ref))
            if comma_count == 0:
                TI = ref
            elif comma_count == 1:
                TI, SO = re.split(comma_pattern, ref)
            else:
                # conference ref
                if re.search(
                    r"[Cc]onference|Conf\.|[Pp]roceeding|Proc\.|[Cc]ommittee|[Ss]ymposium|[Cc]onvention|[Cc]ongress",
                    ref,
                ):
                    TI, SO = ref.split(", ", 1)

                # match source
                elif SO_match := re.search(r", ([A-Z\d][\w\s\.\-&:]+)$", ref):
                    SO = SO_match[1]
                    TI = ref.replace(f", {SO}", "")

                # match title
                elif TI_match := re.search(r"^(([^\.\s]+ ){3,}[^\.\sA-Z]+), [A-Z]", ref):
                    TI = TI_match[1]
                    SO = ref.replace(f"{TI}, ", "")

                elif re.search(r"^[A-Z][^A-Z]+$", ref):
                    TI = ref

                else:
                    return None

        result = asdict(ScopusField(First_AU, TI, SO, VL, IS, BP, EP, PY))
        if doc_index is not None:
            result["doc_index"] = doc_index
        return result

    def parse_one_ref(
        self, ref: str, source_type: Literal["wos", "cssci", "scopus"], doc_index=None
    ):
        """Parse a raw reference string.

        Args:
            ref: A raw reference string.
            source_type: Source type, `wos`, `cssci` or `scopus`.
            doc_index: doc_index to which the reference belongs. Default is None.
        
        Returns:
            Parsed reference as a dict.
        
        Example:
            >>> from histcite.parse_reference import ParseReference
            >>> ref = 'Bengio Y, 2001, ADV NEUR IN, V13, P932'
            >>> parsed_ref = ParseReference().parse_one_ref(ref, 'wos')
            >>> print(parsed_ref)
            {'First_AU': 'Bengio Y', 'PY': '2001', 'J9': 'ADV NEUR IN', 'VL': '13', 'BP': '932'}
        """
        if source_type == "wos":
            return self._parse_wos_ref(ref, doc_index)
        elif source_type == "cssci":
            return self._parse_cssci_ref(ref, doc_index)
        elif source_type == "scopus":
            return self._parse_scopus_ref(ref, doc_index)
        else:
            raise ValueError("Invalid source type")

    def parse_ref_cell(
        self,
        ref_cell: str,
        source_type: Literal["wos", "cssci", "scopus"],
        doc_index=None,
    ) -> Optional[list[dict[str, Optional[str]]]]:
        """Parse a reference cell.

        Args:
            ref_cell: A reference cell.
            source_type: Source type, `wos`, `cssci` or `scopus`.
            doc_index: doc_index to which the reference cell belongs. Default is None.
        
        Returns:
            List of parsed references.
        
        Example:
            >>> from histcite.parse_reference import ParseReference
            >>> ref_cell = 'Bengio Y, 2001, ADV NEUR IN, V13, P932; CORTES C, 1995, MACH LEARN, V20, P273, DOI 10.1007/BF00994018'
            >>> parsed_ref_list = ParseReference().parse_ref_cell(ref_cell, 'wos')
            >>> print(parsed_ref_list)
            [{'First_AU': 'Bengio Y', 'PY': '2001', 'J9': 'ADV NEUR IN', 'VL': '13', 'BP': '932'}, {'First_AU': 'CORTES C', 'PY': '1995', 'J9': 'MACH LEARN', 'VL': '20', 'BP': '273'}]
        """
        sep = "; "
        try:
            ref_list = re.split(sep, ref_cell)
        except:
            return None

        parsed_ref_list: list[Optional[dict[str, Optional[str]]]]
        parsed_ref_list = [
            self.parse_one_ref(ref, source_type, doc_index) for ref in ref_list
        ]
        parse_ref_list = [ref for ref in parsed_ref_list if ref is not None]
        return parse_ref_list
