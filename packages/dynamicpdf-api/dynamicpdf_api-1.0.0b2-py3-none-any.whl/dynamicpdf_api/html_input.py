from .input import Input
from .input_type import InputType
from .page_size import PageSize
from .page_orientation import PageOrientation
from .unit_converter import UnitConverter

class HtmlInput(Input):
    ''' 
    Represents a html input
    '''
    
    def __init__(self, resource, base_path = None, size = PageSize.Letter, orientation = PageOrientation.Portrait, margins = None):
        '''
        Initializes a new instance of the HtmlInput class.
        
        Args:
            resource (HtmlResource): The resource of type HtmlResource.
            basepath (string): The basepath options for the url.
            size (PageSize): The page size of the output PDF.
            orientation (PageOrientation): The page orientation of the output PDF.
            margins (integer): The page margins of the output PDF.
        '''

        super().__init__(resource)

        # Gets or sets the base path option.
        self.base_path = base_path

        # Gets or sets the top margin.
        self.top_margin = margins

        # Gets or sets the bottom margin.
        self.bottom_margin = margins

        # Gets or sets the right margin.
        self.right_margin = margins

        # Gets or sets the left margin.
        self.left_margin = margins

        self.page_width = None
        self.page_height = None
        self._page_size = None
        self._page_orientation = None
        self.page_size = size
        self.page_orientation = orientation
        self.html_string = ''
        self._type = InputType.Html
        
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
        if self.page_orientation == PageOrientation.Portrait:
            self.page_height = larger
            self.page_width = smaller
        else:
            self.page_height = smaller
            self.page_width = larger
    
    @property
    def page_orientation(self):
        '''
        Gets the page orientation.
        '''
        return self._page_orientation

    @page_orientation.setter
    def page_orientation(self, value):
        '''
        Sets the page orientation.
        '''
        self._page_orientation = value
        if self.page_width > self.page_height:
            smaller = self.page_height
            larger = self.page_width
        else:
            smaller = self.page_width
            larger = self.page_height
        if self._page_orientation == PageOrientation.Portrait:
            self.page_height = larger
            self.page_width = smaller
        else:
            self.page_height = smaller
            self.page_width = larger

    
    def to_json(self):
        json = {
            "type": self._type,
            "resourceName": self.resource_name,
            "id": self.id,
            "pageHeight": self.page_height,
            "pageWidth": self.page_width
        }
        if self._template_id:
            json["templateId"] = self._template_id
        if self.base_path:
            json["basePath"] = self.base_path
        if self.top_margin:
            json["topMargin"] = self.top_margin
        if self.left_margin:
            json["leftMargin"] = self.left_margin
        if self.bottom_margin:
            json["bottomMargin"] = self.bottom_margin
        if self.right_margin:
            json["rightMargin"] = self.right_margin
        return json