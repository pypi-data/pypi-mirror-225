from .input import Input
from .input_type import InputType
from .align import Align
from .v_align import VAlign

class ImageInput(Input):
    '''
    Represents an image input
    '''

    def __init__(self, resource):
        '''
        Initializes a new instance of the ImageInput class. 

        Args:
            resource (ImageResource | string): The object to create ImageInput. | The image file path present in cloud resource manager.
        '''
        
        super().__init__(resource)
        self._type = InputType.Image
       
        # Gets or sets the scaleX of the image.
        self.scale_x  = None

        # Gets or sets the scaleY of the image.
        self.scale_y = None

        # Gets or sets the top margin.
        self.top_margin = None

        # Gets or sets the left margin.
        self.left_margin = None

        # Gets or sets the bottom margin.
        self.bottom_margin = None

        # Gets or sets the right margin.
        self.right_margin = None

        # Gets or sets the page width.
        self.page_width = None

        # Gets or sets the page height.
        self.page_height = None

        # Gets or sets a boolean indicating whether to expand the image.
        self.expand_to_fit = None

        # Gets or sets a boolean indicating whether to shrink the image.
        self.shrink_to_fit = None

        # Gets or sets the horizontal alignment of the image.
        self.align = Align.Center

        # Gets or sets the vertical alignment of the image.
        self.v_align = VAlign.Center

        # Gets or sets the start page.
        self.start_page = None

        # Gets or sets the page count.
        self.page_count = None

    def to_json(self):
        json = {
            "align": self.align,
            "vAlign": self.v_align,
            "type": self._type,
            "resourceName": self.resource_name,
            "id": self.id
        }
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
        if self.page_width:
            json["pageWidth"] = self.page_width
        if self.page_height:
            json["pageHeight"] = self.page_height
        if self.scale_x:
            json["scaleX"] = self.scale_x
        if self.scale_y:
            json["scaleY"] = self.scale_y
        if self.expand_to_fit is not None:
            json["expandToFit"] = self.expand_to_fit
        if self.shrink_to_fit is not None:
            json["shrinkToFit"] = self.shrink_to_fit
        if self.start_page:
            json["startPage"] = self.start_page
        if self.page_count:
            json["pageCount"] = self.page_count
        return json


