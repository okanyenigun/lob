import os
import json
import mimetypes
import pandas as pd
from django.http import HttpResponse, HttpRequest
from wsgiref.util import FileWrapper

class Utility:
    
    @staticmethod
    def indexing_1(source_data: pd.DataFrame, new_data: pd.DataFrame, indexed_title: str, map_title: str, new_column: str) -> pd.DataFrame:
        """Excel match-index operation

        Args:
            source_data (pd.DataFrame): the source for the new column
            new_data (pd.DataFrame): target dataframe
            indexed_title (str): common column name from the both dataframes
            map_title (str): target column name in the source
            new_column (str): new column name in the new_data

        Returns:
            pd.DataFrame: returns the new_data with the new column
        """
        source = source_data.copy()
        try:
            source.set_index(indexed_title, inplace=True)
        except:
            pass
        map_dict = source[map_title].to_dict()
        new_data[new_column] = new_data[indexed_title].map(map_dict)
        return new_data

    @staticmethod
    def convert_df_to_html(df: pd.DataFrame) -> tuple([list, list]):
        """converts a dataframe to display in html

        Args:
            df (pd.DataFrame): dataframe

        Returns:
            tuple: arr: data & columns
        """
        columns = df.columns.values.tolist()
        json_records = df.to_json(orient="records")
        arr = json.loads(json_records)
        return arr, columns
    
    @staticmethod
    def download_static_file(path: str) -> HttpResponse:
        """download files in statics

        Args:
            path (str): file path in statics

        Returns:
            HttpResponse: contains the file
        """
        wrapper = FileWrapper(open(path, 'rb'))
        file_mimetype = mimetypes.guess_type(path)
        response = HttpResponse(wrapper, content_type=file_mimetype)
        response['X-Sendfile'] = path
        response['Content-Length'] = os.stat(path).st_size
        response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(path)
        return response

    @staticmethod
    def convert_req_to_dict(req: HttpRequest, tip: str="GET") -> dict:
        """converts a request to dictionary
        just a type conversion

        Args:
            req (HttpRequest): request
            tip (str, optional): request method. Defaults to "GET".

        Returns:
            dict: request parameters in dictionary type
        """
        out = {}
        if tip == "GET":
            for key, value in req.GET.items():
                out[key] = value
        elif tip == "POST":
            for key, value in req.POST.items():
                out[key] = value
        return out