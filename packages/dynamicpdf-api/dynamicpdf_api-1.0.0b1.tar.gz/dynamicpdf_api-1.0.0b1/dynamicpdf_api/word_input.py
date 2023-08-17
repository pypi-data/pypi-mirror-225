from .input_type import InputType
from .page_size import PageSize
from .page_orientation import PageOrientation
from .unit_converter import UnitConverter
from .input import Input

class WordInput(Input):
    '''
    Represents a Word input.
    '''

    def __init__(self, resource, size = PageSize.Letter, orientation = PageOrientation.Portrait, margins = None):
        '''
        Initializes a new instance of the WordInput class.

        Args:
            resource (WordResource): The resource of type WordResource.
            size (PageSize): The page size of the output PDF.
            orientation (PageOrientation): The page orientation of the output PDF.
            margins (float): The page margins of the output PDF.
        '''
        
        super().__init__(resource)
        self._page_size = size
        self._page_orientation = orientation
        self._type = InputType.Word

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

        # Gets or sets the TextReplace object List
        self.text_replace = []

    @property
    def _get_text_replace(self):
        if self.text_replace and len(self.text_replace) > 0:
            return self.text_replace
        return None
    
    @property
    def page_size(self):
        '''
        Gets the page size.
        '''
        return self._page_size

    @page_size.setter
    def page_size(self, value):
        '''
        Sets the page size.
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
        smaller, larger = UnitConverter._get_paper_size(self.page_size)
        if self.page_width > self.page_height:
            smaller, larger = self.page_height, self.page_width
        if self._page_orientation == PageOrientation.Portrait:
            self.page_height = larger
            self.page_width = smaller
        else:
            self.page_height = smaller
            self.page_width = larger

    def to_json(self):
        json = {
            "id":self.id,
            "resourceName": self.resource_name,
            "templateId": self._template_id,
            "type": self._type,
            "pageWidth": self.page_width,
            "pageHeight": self.page_height,
        }
        if self.top_margin:
            json["topMargin"] = self.top_margin
        if self.left_margin:
            json["leftMargin"] = self.left_margin
        if self.bottom_margin:
            json["bottomMargin"] = self.bottom_margin
        if self.right_margin:
            json["rightMargin"] = self.right_margin
        if self._get_text_replace:
            text_replace=[]
            for i in self._get_text_replace:
                text_replace.append(i.to_json())
            json["textReplace"] = text_replace
        return json