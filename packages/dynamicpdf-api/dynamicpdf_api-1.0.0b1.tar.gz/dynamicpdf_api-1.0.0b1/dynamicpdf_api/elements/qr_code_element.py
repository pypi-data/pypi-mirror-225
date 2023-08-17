from .element_type import ElementType
from .text_barcode_element import TextBarcodeElement

class QrCodeElement(TextBarcodeElement):
    '''
    Represents a QR code barcode element.
    '''

    def __init__(self, value, placement, x_offset = 0, y_offset = 0):
        '''
        Initializes a new instance of the QrCodeElement class.

        Args:
            value (string): The value of the barcode.
            placement (ElementPlacement): The placement of the barcode on the page.
            xOffset (integer): The X coordinate of the barcode.
            yOffset (integer): The Y coordinate of the barcode.
        '''
        
        super().__init__(value, placement, x_offset, y_offset)
        self._type = ElementType.QRCode

        # Gets or sets the QR code version.
        self.version = None

        # Gets or sets FNC1 mode.
        self.fnc1 = None
        

    def to_json(self):
        json = {
            "type": self._type,
            "value": self.value,
            "placement": self.placement,
            "xOffset": self.x_offset,
            "yOffset": self.y_offset
        }
        if self._color_name:
            json["color"] = self._color_name
        if self.even_pages is not None:
            json["evenPages"] = self.even_pages
        if self.odd_pages is not None:
            json["oddPages"] = self.odd_pages
        if self.x_dimension:
            json["xDimension"] = self.x_dimension
        if self.font_size:
            json["fontSize"] = self.font_size
        if self.show_text is not None:
            json["showText"] = self.show_text
        if self._font_name:
            json["font"] = self._font_name
        if self._text_color_name:
            json["textColor"] = self._text_color_name
        if self.version:
            json['version'] = self.version
        if self.fnc1:
            json['fnc1'] = self.fnc1
        return json
