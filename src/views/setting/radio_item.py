"""
单个设置选项
"""

from flet_core import Row, Text, CrossAxisAlignment, ControlEvent, RadioGroup, Radio

from src.config.config import config_instance


class RadioItem(Row):

    def __init__(self, label, value, width=None, isExpand=True):
        super().__init__(
            spacing=10,
            vertical_alignment=CrossAxisAlignment.CENTER,
            controls=[
                Text(size=18, value=label),
                RadioGroup(
                    value=value,
                    on_change=self.update_setting,
                    content=Row(
                        controls=[
                            Radio(value="Y", label="是"),
                            Radio(value="N", label="否"),
                        ]
                    )
                )
            ]
        )

    def update_setting(self, e: ControlEvent):
        config_instance.set_contains_sub_directories(e.control.value)