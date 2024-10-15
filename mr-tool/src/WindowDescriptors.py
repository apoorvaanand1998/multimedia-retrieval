from IWindowDBSelector import IWindowDBSelector
from WidgetDescriptors import WidgetDescriptors


class WindowDescriptors(IWindowDBSelector):

    def __init__(self):
        super().__init__(WidgetDescriptors)
