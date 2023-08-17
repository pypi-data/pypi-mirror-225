from .endpoint import Endpoint
from .pdf_response import PdfResponse
import asyncio
import json
from concurrent.futures import ThreadPoolExecutor

class DlexLayout(Endpoint):
    '''
    Represents a Dlex layout endpoint.
    '''

    def __init__(self,cloud_dlex_path, layout_data):
        '''
        Initializes a new instance of the <see cref="DlexLayout"/> class using the 
        DLEX file path present in the cloud environment and the JSON data for the PDF report.

        Args:
            cloudDlexPath (string): The DLEX file path present in the resource manager
            layoutData (LayoutDataResource): The LayoutDataResource json data file used to create the PDF report.
        '''

        super().__init__()
        self.dlex_path = cloud_dlex_path
        self._resource = layout_data
        self._endpoint_name = "dlex-layout"

    def process(self):
        '''
        Process the DLEX and layout data to create PDF report.
        '''
        return asyncio.get_event_loop().run_until_complete(self.process_async())

    async def process_async(self):
        '''
        Process  the DLEX and layout data asynchronously to create PDF report.
        '''
        rest_client = self.create_rest_request()
        files = {
            'LayoutData': (
                self._resource.layout_data_resource_name,
                self._resource._data,
                self._resource._mime_type
            )}
        data = {'DlexPath': self.dlex_path}
        with ThreadPoolExecutor() as executor:
            rest_response = executor.submit(rest_client.post, self.url, files=files, data=data).result()
        
        if rest_response.status_code == 200:
            response = PdfResponse(rest_response.content)
            response.is_successful = True
            response.status_code = rest_response.status_code
        else:
            response = PdfResponse()
            error_json = json.loads(rest_response.content)
            response.error_json = error_json
            response.error_id = error_json['traceId']
            response.error_message = error_json['title']
            response.is_successful = False
            response.status_code = rest_response.status_code

        return response
        
        