from .input import Input 
from .input_type import InputType
from .unit_converter import UnitConverter
from .page_size import PageSize
from .page_orientation import PageOrientation

class PageInput(Input):
    '''
    Represents a page input.
    '''

    def __init__(self, size = PageSize.Letter, orientation = PageOrientation.Portrait, margins = None):
        '''
        Initializes a new instance of the PageInput class.

        Args:
            size (PageSize | float): The size of the page. | The width of the page.
            oriientation (PageOrientation | float): The orientation of the page. | The height of the page.
            margins (float): The margins of the page.
        '''

        super().__init__()
        self._elements = []
        self._default_page_height = 792.0
        self._default_page_width = 612.0

        # Gets or sets the top margin.
        self.top_margin = margins

        # Gets or sets the bottom margin.
        self.bottom_margin = margins

        # Gets or sets the right margin.
        self.right_margin = margins

        # Gets or sets the left margin.
        self.left_margin = margins

        # Gets or sets the width of the page.
        self.page_width = None

        # Gets or sets the height of the page.
        self.page_height = None
        self._type=InputType.Page
        if type(size) == float or type(size) == int:
            self.page_width = size
            self.page_height = orientation
        else:
            self._page_size = size
            self._page_orientation = orientation
            self.page_size = size
            self.page_orientation = orientation

    @property
    def _width(self):
        return self.page_width or self._default_page_width

    @property
    def _height(self):
        return self.page_height or self._default_page_height

    @property
    def page_size(self):
        '''
        Gets the Page size.
        '''
        return self._page_size

    @page_size.setter
    def page_size(self, value):
        '''
        Sets the Page size.
        '''
        self._page_size = value
        smaller, larger = UnitConverter._get_paper_size(value)
        if self._page_orientation == PageOrientation.Portrait:
            self.page_height = larger
            self.page_width = smaller
        else:
            self.page_height = smaller
            self.page_width = larger

    @property
    def page_orientation(self):
        '''
        Gets page orientation.
        '''
        return self._page_orientation

    @page_orientation.setter
    def page_orientation(self, value):
        '''
        Sets page orientation.
        '''
        self._page_orientation = value
        if self._width > self._height:
            smaller = self._height
            larger = self._width
        else:
            smaller = self._width
            larger = self._height

        if self.page_orientation == PageOrientation.Portrait:
            self.page_height = larger
            self.page_width = smaller
        else:
            self.page_height = smaller
            self.page_width = larger

    @property
    def elements(self):
        '''
        Gets the elements of the page.
        '''
        return self._elements

    def to_json(self): 
        json = {
            "type": self._type,
            "resourceName": self.resource_name,
            "id": self.id,
            "pageHeight": self.page_height,
            "pageWidth": self.page_width
        }
        elements = []
        for i in self.elements:
            elements.append(i.to_json())
        json["elements"] = elements
        if self._template_id:
            json["templateId"] = self._template_id
        if self.top_margin:
            json["topMargin"] = self.top_margin
        if self.left_margin:
            json["leftMargin"] = self.left_margin
        if self.bottom_margin:
            json["bottomMargin"] = self.bottom_margin
        if self.right_margin:
            json["rightMargin"] = self.right_margin
        return json
