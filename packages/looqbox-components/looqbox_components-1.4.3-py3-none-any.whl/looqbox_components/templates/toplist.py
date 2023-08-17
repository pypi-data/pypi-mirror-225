from looqbox.objects.looq_object import LooqObject
from looqbox.objects.visual.looq_table import ObjTable
from looqbox.render.abstract_render import BaseRender
from multimethod import overload
from pandas import DataFrame


class TopList(LooqObject):
    """
    Create and render a TopList template.

    :param data: A pandas DataFrame or looqbox Objtable with the data to be displayed in the TopList.

    :return: A JSON string.

    """

    @overload
    def __init__(self, data: DataFrame, thickness: int = 1, line_color: str = "#D5DFE9", alignment: str = "center"):
        """
        Receives a pandas dataframe and render it as a list.
        :param data: pd.DataFrame or lq.ObjTable
        :param thickness: int - Thickness of the line between rows. Default is 1.
        :param line_color: str - Color of the line between rows. Default is #D5DFE9.
        :param alignment: str - Text-alignment of the list. Default is center. Can be left, right or center.
        """
        super().__init__()
        self.list_content = ObjTable(data)
        self.alignment = alignment
        self.thickness = thickness
        self.line_color = line_color

    @overload
    def __init__(self, data: ObjTable, thickness: int = 1, line_color: str = "#D5DFE9", alignment: str = "center"):
        """
        Receives a looqbox ObjTable and render it as a list.
        :param data: pd.DataFrame or lq.ObjTable
        :param thickness: int - Thickness of the line between rows. Default is 1.
        :param line_color: str - Color of the line between rows. Default is #D5DFE9.
        :param alignment: str - Text-alignment of the list. Default is center. Can be left, right or center.
        """
        super().__init__()
        self.list_content = data
        self.alignment = alignment
        self.thickness = thickness
        self.line_color = line_color

    def _set_list_style(self) -> None:

        for row in range(self.list_content.data.shape[0]):
            self.list_content.row_style[row] = {"background": "white",
                                                "border-bottom": f"{self.thickness}px solid {self.line_color}"}

        self.list_content.show_head = False
        self.list_content.show_option_bar = False
        self.list_content.show_footer = False
        self.list_content.col_style = dict(
            zip(self.list_content.data.columns,
                [{'text-align': self.alignment}] * len(self.list_content.data.columns)))

    def _data_frame_is_empty(self) -> bool:
        return self.list_content.data is None or self.list_content.data.empty

    def to_json_structure(self, visitor: BaseRender):

        if self._data_frame_is_empty():
            raise ValueError("Dataframe is empty")

        self._set_list_style()
        return self.list_content.to_json_structure(visitor)
