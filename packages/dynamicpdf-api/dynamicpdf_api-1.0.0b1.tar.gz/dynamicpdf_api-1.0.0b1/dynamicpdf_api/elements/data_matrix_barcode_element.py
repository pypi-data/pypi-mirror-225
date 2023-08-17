from .element_type import ElementType
from .dim2_barcode_element import Dim2BarcodeElement
from .data_matrix_encoding_type import DataMatrixEncodingType
from .data_matrix_function_character import DataMatrixFunctionCharacter
from .data_matrix_symbol_size import DataMatrixSymbolSize

class DataMatrixBarcodeElement(Dim2BarcodeElement):
    '''
    Represents a Data Matrix  barcode element.
    '''
    
    def __init__(self, value, placement, x_offset = 0, y_offset = 0, symbol_size = DataMatrixSymbolSize.Auto, encoding_type = DataMatrixEncodingType.Auto, function_character = DataMatrixFunctionCharacter.none):
        '''
        Initializes a new instance of the Code25BarcodeElement class.

        Args:
            value (string): The value of the barcode.
            placement (ElementPlacement): The placement of the barcode on the page.
            xOffset (integer): The X coordinate of the barcode.
            yOffset (integer): The Y coordinate of the barcode.
            symbolSize (DataMatrixSymbolSize): The symbol size of the barcode.
            encodingType (DataMatrixEncodingType): The encoding type of the barcode.
            functionCharacter (DataMatrixFunctionCharacter): The function character of the barcode.
        '''

        super().__init__(value, placement, x_offset, y_offset)
        self._data_matrix_symbol_size = symbol_size
        self._data_matrix_encoding_type = encoding_type
        self._data_matrix_function_character = function_character
        self._type = ElementType.DataMatrixBarcode
        self._text_font = None

        # Gets or sets whether to process tilde character.
        # Setting True will check for ~ character and processes it for FNC1 or ECI characters.
        self.process_tilde = None

    
    def to_json(self):
        json = {
            "type": self._type,
            "value": self.value,
            "placement": self.placement,
            "xOffset": self.x_offset,
            "yOffset": self.y_offset,
            'dataMatrixEncodingType': self._data_matrix_encoding_type,
            'dataMatrixFunctionCharacter': self._data_matrix_function_character,
            'dataMatrixSymbolSize': self._data_matrix_symbol_size,
        }
        if self._color_name:
            json["color"] = self._color_name
        if self.even_pages is not None:
            json["evenPages"] = self.even_pages
        if self.odd_pages is not None:
            json["oddPages"] = self.odd_pages
        if self.x_dimension:
            json["xDimension"] = self.x_dimension
        if self._value_type:
            json["valueType"] = self._value_type
        if self.process_tilde:
            json['processTilde'] = self.process_tilde
        return json
