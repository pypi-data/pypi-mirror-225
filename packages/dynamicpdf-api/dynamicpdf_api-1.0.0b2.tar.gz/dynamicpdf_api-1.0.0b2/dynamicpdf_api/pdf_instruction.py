from .outline_list import OutlineList

class PdfInstructions:
    def __init__(self):
        self._form_fields = []
        self._templates = set()
        self._fonts = set()
        self._outlines = OutlineList()
        self._author = "CeteSoftware"
        self._title = None
        self._subject = None
        self._creator = "DynamicPDF Cloud Api"
        self._keywords = None
        self._security = None
        self._flatten_all_form_fields = None
        self._retain_signature_form_fields = None
        self._inputs = []

    def to_json(self):
        json = {}
        if self._author:
            json["author"] = self._author
        if self._title:
            json["title"] = self._title
        if self._form_fields:
            json["formFields"] = self._form_fields
        if self._subject:
            json["subject"] = self._subject
        if self._creator:
            json["creator"] = self._creator
        if self._keywords:
            json["keywords"] = self._keywords
        if self._security:
            json["security"] = self._security.to_json()
        if self._flatten_all_form_fields is not None:
            json["flattenAllFormFields"] = self._flatten_all_form_fields
        if self._retain_signature_form_fields is not None:
            json["retainSignatureFormFields"] = self._retain_signature_form_fields
        fonts = []
        for i in self._fonts:
            fonts.append(i.to_json())
        json["fonts"] = fonts
        inputs = []
        for i in self._inputs:
            inputs.append(i.to_json())
        json["inputs"] = inputs
        form_field = []
        for i in self._form_fields:
            form_field.append(i.to_json())
        json["formFields"] = form_field
        templates = []
        for i in self._templates:
            templates.append(i.to_json())
        json["templates"] = templates
        json["outlines"] = self._outlines.to_json()
        return json