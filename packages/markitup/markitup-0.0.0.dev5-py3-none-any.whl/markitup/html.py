"""Dynamically create HTML syntax."""


# Standard libraries
import re
from typing import Literal, Optional, Sequence, Protocol


class HasStr(Protocol):
    def __str__(self) -> str:
        ...


class ElementCollection:
    def __init__(self, elements: list = None, seperator: dict | list | str = "\n"):
        self.elements = [] if not elements else (
            (list(elements) if isinstance(elements, (list, tuple)) else [elements])
        )
        self.seperator = seperator
        return

    def append(self, element):
        self.elements.append(element)
        return

    def extend(self, elements):
        self.elements.extend(elements)
        return

    def __str__(self):
        if not self.elements:
            return ""
        string = ""
        for idx, element in enumerate(self.elements):
            string += str(element)
            if idx == len(self.elements) - 1:
                break
            if isinstance(self.seperator, dict):
                sep = self.seperator.get(idx)
                if not sep:
                    sep = self.seperator.get("default")
                    if not sep:
                        sep = ""
            elif isinstance(self.seperator, (list, tuple)):
                sep = self.seperator[idx % len(self.seperator)]
            else:
                sep = self.seperator
            string += str(sep)
        return string

    def display(self):
        # Non-standard libraries
        from IPython.display import HTML, display

        display(HTML(str(self)))
        return


class Element:
    def __init__(
        self,
        tag: str,
        attrs: Optional[dict] = None,
        content: Optional[list | ElementCollection] = None,
        tag_seperator: Optional[str] = "",
        content_indent: Optional[str] = "",
    ):
        self._tag = tag.lower()
        self.attrs = attrs or dict()
        self.content = (
            content if isinstance(content, ElementCollection) else ElementCollection(content)
        )
        self.tag_seperator = tag_seperator
        self.content_indent = content_indent
        return

    @property
    def tag(self):
        return f"<{self._tag}>"

    @property
    def is_void(self):
        return self._tag in (
            "area",
            "base",
            "br",
            "col",
            "command",
            "embed",
            "hr",
            "img",
            "input",
            "keygen",
            "link",
            "meta",
            "param",
            "source",
            "track",
            "wbr",
        )

    def __str__(self):
        """
        The element in HTML syntax, e.g. for an IMG element:
        '<img alt="My Image" src="https://example.com/image">'.
        """
        attrs = []
        for key, val in self.attrs.items():
            if val is None:
                continue
            if isinstance(val, bool):
                if val:
                    attrs.append(f"{key}")
            else:
                attrs.append(f'{key}="{val}"')
        attrs_str = "" if not attrs else f" {' '.join(attrs)}"
        start_tag = f"<{self._tag}{attrs_str}>"
        if self.is_void:
            return start_tag
        end_tag = f"</{self._tag}>"
        if not self.content:
            return f"{start_tag}{end_tag}"
        content = "\n".join(
            [f"{self.content_indent}{line}" for line in str(self.content).split("\n")]
        )
        return f"{start_tag}{self.tag_seperator}{content}{self.tag_seperator}{end_tag}"

    def display(self):
        # Non-standard libraries
        from IPython.display import HTML, display

        display(HTML(str(self)))
        return


class BR(Element):
    """A <br> element."""

    def __init__(self, **attrs):
        super().__init__(tag="br", attrs=attrs)
        return


def br(**attrs):
    return BR(**attrs)


class HR(Element):
    """An <hr> element."""

    def __init__(self, **attrs):
        super().__init__(tag="hr", attrs=attrs)
        return


def hr(**attrs):
    return HR(**attrs)


class H(Element):
    """A heading element from <h1> to <h6>."""

    def __init__(
        self,
        level: Literal[1, 2, 3, 4, 5, 6],
        content: Optional[Sequence] = None,
        tag_seperator: Optional[str] = "",
        content_indent: Optional[str] = "",
        **attrs,
    ):
        super().__init__(
            tag=f"h{level}",
            attrs=attrs,
            content=content,
            tag_seperator=tag_seperator,
            content_indent=content_indent,
        )
        return


def h(
    level: Literal[1, 2, 3, 4, 5, 6],
    content: Optional[Sequence] = None,
    tag_seperator: Optional[str] = "",
    content_indent: Optional[str] = "",
    **attrs
) -> H:
    return H(level=level, content=content, tag_seperator=tag_seperator, content_indent=content_indent, **attrs)


class IMG(Element):
    """An <img> element."""

    def __init__(self, src: HasStr, **attrs):
        attrs["src"] = src
        super().__init__(tag="img", attrs=attrs)
        return


def img(src: HasStr, **attrs) -> IMG:
    return IMG(src=src, **attrs)


class SOURCE(Element):
    """A <source> element."""

    def __init__(self, **attrs):
        super().__init__(tag="source", attrs=attrs)
        return


def source(**attrs) -> SOURCE:
    return SOURCE(**attrs)


class SUMMARY(Element):
    """A <summary> element."""

    def __init__(
        self,
        content: Optional[Sequence] = None,
        tag_seperator: Optional[str] = "",
        content_indent: Optional[str] = "",
        **attrs,
    ):
        super().__init__(
            tag=f"summary",
            attrs=attrs,
            content=content,
            tag_seperator=tag_seperator,
            content_indent=content_indent,
        )
        return


def summary(
    content: Optional[Sequence] = None,
    tag_seperator: Optional[str] = "",
    content_indent: Optional[str] = "",
    **attrs
) -> SUMMARY:
    return SUMMARY(content=content, tag_seperator=tag_seperator, content_indent=content_indent, **attrs)


class DIV(Element):
    """A <div> element."""

    def __init__(
        self,
        content: Optional[list | ElementCollection] = None,
        tag_seperator: Optional[str] = "",
        content_indent: Optional[str] = "",
        **attrs,
    ):
        super().__init__(
            tag="div",
            attrs=attrs,
            content=content,
            tag_seperator=tag_seperator,
            content_indent=content_indent,
        )
        return


def div(
    content: Optional[list | ElementCollection] = None,
    tag_seperator: Optional[str] = "",
    content_indent: Optional[str] = "",
    **attrs
) -> DIV:
    return DIV(content=content, tag_seperator=tag_seperator, content_indent=content_indent, **attrs)


class P(Element):
    """A <p> element."""

    def __init__(
        self,
        content: Optional[Sequence] = None,
        tag_seperator: Optional[str] = "",
        content_indent: Optional[str] = "",
        **attrs,
    ):
        super().__init__(
            tag="p",
            attrs=attrs,
            content=content,
            tag_seperator=tag_seperator,
            content_indent=content_indent,
        )
        return

    def style(self, words: dict[str, dict[str, str | bool]], ignore_case=False):
        """
        Given a string and a replacement map, it returns the replaced string.
        :param str string: string to execute replacements on
        :param dict words: replacement dictionary {value to find: value to replace}
        :param bool ignore_case: whether the match should be case insensitive
        :rtype: str

        Reference : https://stackoverflow.com/a/6117124/14923024
        """
        if not words:
            return self
        # If case insensitive, we need to normalize the old string so that later a replacement
        # can be found. For instance with {"HEY": "lol"} we should match and find a replacement for "hey",
        # "HEY", "hEy", etc.
        if ignore_case:

            def normalize_old(s):
                return s.lower()

            re_mode = re.IGNORECASE
        else:

            def normalize_old(s):
                return s

            re_mode = 0

        subs = dict()
        for word, config in words.items():
            mod_word = word
            if config.get("italic"):
                mod_word = f"<em>{mod_word}</em>"
            if config.get("bold"):
                mod_word = f"<strong>{mod_word}</strong>"
            if config.get("link"):
                mod_word = str(
                    A(
                        href=config.get("link"),
                        content=[mod_word],
                        tag_seperator="",
                        content_indent="",
                    )
                )
            subs[normalize_old(word)] = mod_word
        # Place longer ones first to keep shorter substrings from matching where the longer ones should take place
        # For instance given the replacements {'ab': 'AB', 'abc': 'ABC'} against the string 'hey abc', it should produce
        # 'hey ABC' and not 'hey ABc'
        rep_sorted = sorted(subs, key=len, reverse=True)
        rep_escaped = map(re.escape, rep_sorted)
        # Create a big OR regex that matches any of the substrings to replace
        pattern = re.compile("|".join(rep_escaped), re_mode)
        # For each match, look up the new string in the replacements, being the key the normalized old string
        string = self.content.elements[0]
        replaced_text = pattern.sub(
            lambda match: subs[normalize_old(match.group(0))], string, count=1
        )
        return P(
            content=[replaced_text],
            tag_seperator=self.tag_seperator,
            content_indent=self.content_indent,
            **self.attrs,
        )


def p(
    content: Optional[Sequence],
    tag_seperator: Optional[str] = "",
    content_indent: Optional[str] = "",
    **attrs
) -> P:
    return P(content=content, tag_seperator=tag_seperator, content_indent=content_indent, **attrs)


class A(Element):
    """An <a> element."""

    def __init__(
        self,
        href: HasStr,
        content: Optional[Sequence] = None,
        tag_seperator: Optional[str] = "",
        content_indent: Optional[str] = "",
        **attrs,
    ):
        """
        Parameters
        ----------
        href : str or pypackit.docs.html.URL
            Anchor reference.
        content : any
            Content of the anchor.
        """
        attrs["href"] = href
        super().__init__(
            tag="a",
            attrs=attrs,
            content=content,
            tag_seperator=tag_seperator,
            content_indent=content_indent,
        )
        return


def a(
    href: HasStr,
    content: Optional[Sequence] = None,
    tag_seperator: Optional[str] = "",
    content_indent: Optional[str] = "",
    **attrs
) -> A:
    return A(href=href, content=content, tag_seperator=tag_seperator, content_indent=content_indent, **attrs)


class PICTURE(Element):
    """A <picture> element."""

    def __init__(
        self,
        img: IMG,
        sources: Sequence[SOURCE],
        tag_seperator: Optional[str] = "",
        content_indent: Optional[str] = "",
        **attrs,
    ):
        super().__init__(
            tag="picture",
            attrs=attrs,
            content=ElementCollection([*sources, img], seperator=tag_seperator),
            tag_seperator=tag_seperator,
            content_indent=content_indent,
        )
        return


def picture(
    img: IMG, sources: Sequence[SOURCE],
    tag_seperator: Optional[str] = "",
    content_indent: Optional[str] = "",
    **attrs
) -> PICTURE:
    return PICTURE(
        img=img, sources=sources, tag_seperator=tag_seperator, content_indent=content_indent, **attrs
    )


class TABLE(Element):
    """A <table> element."""

    def __init__(
        self,
        content: Optional[Sequence] = None,
        tag_seperator: Optional[str] = "",
        content_indent: Optional[str] = "",
        **attrs,
    ):
        super().__init__(
            tag=f"table",
            attrs=attrs,
            content=content,
            tag_seperator=tag_seperator,
            content_indent=content_indent,
        )
        return


def table(
    content: Optional[Sequence] = None,
    tag_seperator: Optional[str] = "",
    content_indent: Optional[str] = "",
    **attrs,
) -> TABLE:
    return TABLE(
        content=content, tag_seperator=tag_seperator, content_indent=content_indent, **attrs
    )


class TR(Element):
    """A table-row <tr> element."""

    def __init__(
        self,
        content: Optional[Sequence] = None,
        tag_seperator: Optional[str] = "",
        content_indent: Optional[str] = "",
        **attrs,
    ):
        super().__init__(
            tag=f"tr",
            attrs=attrs,
            content=content,
            tag_seperator=tag_seperator,
            content_indent=content_indent,
        )
        return


def tr(
    content: Optional[Sequence] = None,
    tag_seperator: Optional[str] = "",
    content_indent: Optional[str] = "",
    **attrs,
) -> TR:
    return TR(content=content, tag_seperator=tag_seperator, content_indent=content_indent, **attrs)


class TD(Element):
    """A table-data <td> element."""

    def __init__(
        self,
        content: Optional[Sequence] = None,
        tag_seperator: Optional[str] = "",
        content_indent: Optional[str] = "",
        **attrs,
    ):
        super().__init__(
            tag=f"td",
            attrs=attrs,
            content=content,
            tag_seperator=tag_seperator,
            content_indent=content_indent,
        )
        return


def td(
    content: Optional[Sequence] = None,
    tag_seperator: Optional[str] = "",
    content_indent: Optional[str] = "",
    **attrs,
) -> TD:
    return TD(content=content, tag_seperator=tag_seperator, content_indent=content_indent, **attrs)


class UL(Element):
    """An unordered list <ul> element."""

    def __init__(
        self,
        content: Optional[Sequence] = None,
        type: Literal["disc", "circle", "square"] = "disc",
        tag_seperator: Optional[str] = "",
        content_indent: Optional[str] = "",
        **attrs,
    ):
        attrs["type"] = type
        if isinstance(content, str):
            content = [LI(content=content, tag_seperator=tag_seperator, content_indent=content_indent)]
        elif isinstance(content, Sequence):
            content = [
                LI(content=li, tag_seperator=tag_seperator, content_indent=content_indent)
                for li in content
            ]
        super().__init__(
            tag=f"ul",
            attrs=attrs,
            content=content,
            tag_seperator=tag_seperator,
            content_indent=content_indent,
        )
        return


def ul(
    content: Optional[Sequence] = None,
    type: Literal["disc", "circle", "square"] = "disc",
    tag_seperator: Optional[str] = "",
    content_indent: Optional[str] = "",
    **attrs,
) -> UL:
    return UL(
        content=content, type=type, tag_seperator=tag_seperator, content_indent=content_indent, **attrs
    )


class OL(Element):
    """An ordered list <ol> element."""

    def __init__(
        self,
        content: Optional[Sequence] = None,
        start: int = 1,
        type: Literal["1", "a", "A", "i", "I"] = "1",
        reversed: bool = False,
        tag_seperator: Optional[str] = "",
        content_indent: Optional[str] = "",
        **attrs,
    ):
        attrs["type"] = type
        attrs["start"] = start
        attrs["reversed"] = reversed
        if isinstance(content, str):
            content = [LI(content=content, tag_seperator=tag_seperator, content_indent=content_indent)]
        elif isinstance(content, Sequence):
            content = [
                LI(content=li, tag_seperator=tag_seperator, content_indent=content_indent)
                for li in content
            ]
        super().__init__(
            tag=f"ol",
            attrs=attrs,
            content=content,
            tag_seperator=tag_seperator,
            content_indent=content_indent,
        )
        return


def ol(
    content: Optional[Sequence] = None,
    start: int = 1,
    type: Literal["1", "a", "A", "i", "I"] = "1",
    reversed: bool = False,
    tag_seperator: Optional[str] = "",
    content_indent: Optional[str] = "",
    **attrs,
) -> OL:
    return OL(
        content=content,
        start=start,
        type=type,
        reversed=reversed,
        tag_seperator=tag_seperator,
        content_indent=content_indent,
        **attrs,
    )


class LI(Element):
    """A list item <li> element."""

    def __init__(
        self,
        content: Optional[Sequence] = None,
        value: Optional[str] = None,
        type: Optional[Literal["1", "a", "A", "i", "I"]] = None,
        tag_seperator: Optional[str] = "",
        content_indent: Optional[str] = "",
        **attrs,
    ):
        attrs["value"] = value
        attrs["type"] = type
        super().__init__(
            tag=f"li",
            attrs=attrs,
            content=content,
            tag_seperator=tag_seperator,
            content_indent=content_indent,
        )
        return


def li(
    content: Optional[Sequence] = None,
    value: Optional[str] = None,
    type: Optional[Literal["1", "a", "A", "i", "I"]] = None,
    tag_seperator: Optional[str] = "",
    content_indent: Optional[str] = "",
    **attrs,
) -> LI:
    return LI(
        content=content,
        value=value,
        type=type,
        tag_seperator=tag_seperator,
        content_indent=content_indent,
        **attrs
    )


class DETAILS(Element):
    """A <details> element."""

    def __init__(
        self,
        content: Optional[Sequence] = None,
        summary: Optional[str | Element] = None,
        open: bool = False,
        tag_seperator: Optional[str] = "",
        content_indent: Optional[str] = "",
        **attrs,
    ):
        attrs["open"] = open
        if summary is not None:
            if not isinstance(summary, SUMMARY):
                summary = SUMMARY(content=summary, content_indent=content_indent, tag_seperator=tag_seperator)
            content = [summary, BR(), content]
        super().__init__(
            tag=f"details",
            attrs=attrs,
            content=content,
            tag_seperator=tag_seperator,
            content_indent=content_indent,
        )
        return


def details(
    content: Optional[Sequence] = None,
    summary: Optional[str | Element] = None,
    open: bool = False,
    tag_seperator: Optional[str] = "",
    content_indent: Optional[str] = "",
    **attrs,
) -> DETAILS:
    return DETAILS(
        content=content,
        summary=summary,
        open=open,
        tag_seperator=tag_seperator,
        content_indent=content_indent,
        **attrs,
    )


class Comment:
    def __init__(self, content: HasStr):
        self.comment = content
        return

    def __str__(self):
        return f"<!-- {self.comment} -->"


def comment(content: HasStr) -> Comment:
    return Comment(content)