from typing import Union

from looqbox import ObjText, ObjRow, ObjColumn
from looqbox.objects.container.positional.abstract_positional_container import AbstractPositionalContainer
from looqbox.render.abstract_render import BaseRender

from looqbox_components.templates.container import Container
from looqbox_components.templates.tag import Tag
from looqbox_components.utils.parent_parameters import include_extra_parent_params


class SimpleCard(AbstractPositionalContainer):
    """
    Create and render a simple card template.

    :return: A JSON string.

    """

    def __init__(self, title: Union[ObjText, str], value: Union[ObjText, float, int],
                 tag_value: Union[int, float] = None, tooltip: str = None, line: bool = False,
                 line_color: str = "#40db62", tag_properties=None, children=None, **parent_params) -> None:
        """
        Default template for simple card
        :param title: str or lq.ObjText - title of the card
        :param value: lq.ObjText or int or float - value of the card
        :param tag_value: int or float - value of the tag in card
        :param tooltip: str - text to display in tooltip
        :param line: boolean - add a line on the left side of the card
        :param line_color: str - set color of the line
        :param tag_properties: properties for tag customization
        """
        super().__init__(value)

        self.title = title
        self.value = value
        self.tag_value = tag_value
        self.tooltip = tooltip
        self.line = line
        self.line_color = line_color
        self.tag_properties = tag_properties or {}
        self.parent_params = parent_params
        self._set_value_as_text()
        self.children = children or self.get_children()

    @include_extra_parent_params
    def _build_card(self):
        return Container(
            self.children,
            title=self.title,
            tooltip=self.tooltip,
            line=self.line,
            line_color=self.line_color,
            **self.parent_params
        )

    def get_children(self):
        return ObjRow(
            [ObjColumn(self.value, render_condition=self.value).set_main_alignment_center],
            ObjRow(
                Tag(self.tag_value, tag_format="percent:1", **self.tag_properties),
                render_condition=self.tag_value).set_main_alignment_end
        ).set_main_alignment_space_between.set_cross_alignment_center

    def _set_value_as_text(self):
        if not isinstance(self.value, ObjText):
            self.value = ObjText(self.value)

    def to_json_structure(self, visitor: BaseRender):
        return self._build_card().to_json_structure(visitor)
