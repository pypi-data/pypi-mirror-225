from looqbox import CssOption as css, ObjColumn, ObjRow, ObjHTML, ObjText, format
from looqbox.objects.looq_object import LooqObject
from looqbox.render.abstract_render import BaseRender
from numpy import inf


class Tag(LooqObject):
    def __init__(self, tag_value: int | float | str, **template_options):
        """
        This class represents a color tag for displaying values with optional rules for color-coding and formatting.
        :param tag_value: The value to be displayed in the tag. Can be a string, int, or float.
        :param tag_properties:
            tag_rules: list of dictionaries representing rules for color-coding the tag value based on its numerical
            value,
            must follow the constraints:
                    List - tag_rules:
                    [{
                        "symbol": "↓", #String or ObjHTML to be displayed before the tag value (Optional)
                        "color": "#E92C2C",  #Color displayed when the value is within "range"
                        "range": [-inf, 0] #Range in which the parameters above will appear
                    }]
            default_color: The default text color of the tag if no rule is applicable.
            tag_format: The formatting of the tag value.
        """

        self.tag_rules = [
            {
                "symbol": "↓",
                "color": "#E92C2C",
                "range": [-inf, 0]
            },
            {
                "symbol": "↑",
                "color": "#00BA34",
                "range": [0, inf]
            },

        ]

        self.tag_must_have_properties = ["default_color", "tag_format", "tag_rules"]

        self.tag_properties = self._get_tag_properties(template_options)

        self.container_properties = self._get_template_properties(template_options)

        super().__init__(**self.container_properties)

        self.tag_value = tag_value or "-"

        self._text_default_style = [
            css.FontSize("14px")
        ]

        self._container_default_style = [
            css.AlignItems.center,
            css.JustifyContent.center,
            css.BorderRadius("6px"),
            css.Border("4px"),
            css.Height("24px"),
            css.Width("fit-content"),
            css.Padding("0px 5px")
        ]

    def _set_tag_style_values(self):
        self.default_color = self.tag_properties.get("default_color", "#797979")
        self.tag_format = self.tag_properties.get("tag_format", "number:1")
        self.tag_rules = self.tag_properties.get("tag_rules", self.tag_rules)

    def _get_template_properties(self, tag_options) -> dict:
        return {property_key: value for property_key, value in tag_options.items() if
                property_key not in self.tag_must_have_properties}

    def _get_tag_properties(self, tag_options) -> dict:

        return {property_key: value for property_key, value in tag_options.items() if
                property_key in self.tag_must_have_properties}

    def _set_element_style(self, element) -> css:
        for style in self._get_defined_style():
            element.css_options = css.add(element.css_options, style)
        return element

    def _get_defined_style(self):
        if self.css_options is None:
            self.css_options = []
        return list(set(self.css_options).union(set(self._container_default_style)))

    @property
    def invert_default_color(self):
        range_list = [e.get("range") for e in self.tag_rules]
        inverse_range_list = list(reversed(range_list))
        for rule, new_rule in zip(self.tag_rules, inverse_range_list):
            rule["range"] = new_rule
        return self

    def set_font_size(self, font_size: int | str):
        self._text_default_style = css.add(self.css_options, css.FontSize(font_size))
        self._container_default_style = css.clear(self._container_default_style, [css.Height("24px")])
        self._container_default_style = css.add(self._container_default_style, css.Height(10 + font_size))
        return self

    def _is_number(self) -> bool:
        return self.tag_value and not isinstance(self.tag_value, str)

    def _is_in_range(self, rule) -> bool:
        return rule["range"][0] <= self.tag_value <= rule["range"][1]

    def _get_rule_by_range(self) -> dict:
        for rule in self.tag_rules:
            if self._is_number() and self._is_in_range(rule):
                return rule
        return {}

    def _update_container_style(self, color) -> None:
        self._container_default_style += [
            css.BackgroundColor(color + "1a"),
            css.Color(color)
        ]

    def _set_format(self, tag_format: str):
        if self._is_number():
            return format(self.tag_value, tag_format)
        return self.tag_value

    def _get_content(self) -> ObjColumn:

        self._set_tag_style_values()
        rule = self._get_rule_by_range()
        font_size = self._text_default_style[0].value
        symbol = [ObjHTML(f"""<div style="font-size:{font_size}px">{symbol}</div>""")] if (
            symbol := rule.get("symbol")) else []
        self.tag_value = self._set_format(self.tag_format)
        text_obj = ObjText(
            self.tag_value,
            css_options=self._text_default_style
        )
        tag_container = ObjColumn(
            ObjRow(
                symbol + [text_obj],
            ),
            **self.container_properties
        )

        color = rule.get("color") or self.default_color
        self._update_container_style(color)

        tag_container = self._set_element_style(tag_container)
        return tag_container

    def to_json_structure(self, visitor: BaseRender):
        return self._get_content().to_json_structure(visitor)
