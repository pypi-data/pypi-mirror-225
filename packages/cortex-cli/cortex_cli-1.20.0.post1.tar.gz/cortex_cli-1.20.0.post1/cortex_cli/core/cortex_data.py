#!/usr/bin/env python3

import json
import os
import pathlib
import pickle
import pandas as pd
import re
import requests
import yaml
from collections import namedtuple
from markdown import markdown as markdown_reader
from PyPDF2 import PdfFileReader as pdf_reader
from pyth.plugins.rtf15.reader import Rtf15Reader as rtf_reader


class CortexFile(namedtuple('BaseFile', 'local_dir remote_path size etag last_modified')):
    _loaded_data = None

    @property
    def local_path(self):
        return '{}/{}'.format(self.local_dir, self.name)


    @property
    def name(self):
        # File name with file extension
        return os.path.basename(self.remote_path)


    @property
    def type(self):
        return pathlib.Path(self.remote_path).suffix.lower().replace('.', '')


    @property
    def loaded_data(self):
        return self._loaded_data


    @property
    def isPandasLoadable(self):
        return self.type in ['xls', 'xlsx', 'xlsm', 'xlsb', 'odf', 'ods', 'odt', 'csv']


    def load(self, as_polars=False):
        if as_polars:
            try:
                import polars as pl
            except ImportError:
                raise Exception('Polars library is not installed. Please install it using "pip install polars"')
        try:
            # Process doc and docx filetypes
            if self.type in ['doc', 'docx']:
                if self.type=='doc':
                    from doc import Document
                if self.type=='docx':
                    from docx import Document
                
                document = Document(self.local_path)
                paragraphs = [paragraph.text for paragraph in document.paragraphs]
                combined_text = ' '.join(paragraphs)
                self._loaded_data = combined_text
            else:
            
                # Process all other filetypes
                with open(self.local_path, 'rb') as file:
                    if self.type in ['xls', 'xlsx', 'xlsm', 'xlsb', 'odf', 'ods', 'odt']:
                        if as_polars:
                            self._loaded_data = pl.read_excel(file)
                        else:
                            self._loaded_data = pd.read_excel(file)

                    if self.type=='csv':
                        if as_polars:
                            self._loaded_data = pl.read_csv(file)
                        else:
                            self._loaded_data = pd.read_csv(file)

                    if self.type=='json':
                        self._loaded_data = json.load(file)

                    if self.type=='md':
                        text = file.read()
                        html = markdown_reader(text)
                        plain_text = re.sub('<[^<]+?>', '', html)

                        self._loaded_data = plain_text

                    if self.type=='parquet':
                        if as_polars:
                            self._loaded_data = pl.read_parquet(file)
                        else:
                            self._loaded_data = pd.read_parquet(file)

                    if self.type=='pdf':
                        reader = pdf_reader(file)
                        num_pages = reader.numPages

                        text = ''
                        for page_number in range(num_pages):
                            page = reader.getPage(page_number)
                            text += page.extractText()
                        
                        self._loaded_data = text
                        
                    if self.type=='pkl':
                        self._loaded_data = pickle.load(file)
                    
                    if self.type=='rtf':
                        doc = rtf_reader.read(file)
                        text = ''
                        for paragraph in doc.content:
                            text += paragraph.plain_text()
                        
                        self._loaded_data = text
                        
                    if self.type=='txt':
                        self._loaded_data = file.read().decode('utf-8')

                    if self.type=='yml':
                        self._loaded_data = yaml.load(file)
                    
            return self._loaded_data
        except IOError:
            # Throw an exception if there is an unsupported file type
            raise Exception('File {} could not be opened by Cortex File'.format(self.name))
    
    
    def exists(self):
        return os.path.isfile(self.local_path)


class CortexData():
    _api_url = None
    _headers = None
    _local_dir = None
    _files = []


    @property
    def files(self):
        return self._files


    def __init__(self, model_id, api_url, headers, local_dir='data'):
        self._model_id = model_id
        self._api_url = api_url
        self._headers = headers
        self._local_dir = local_dir

        self._files = self._list_remote_files()


    def _list_remote_files(self):
        response = requests.get(
            f'{self._api_url}/models/{self._model_id}/files',
            headers=self._headers
        ).json()

        return [CortexFile(self._local_dir, file['Key'], file['Size'], file['ETag'], file['LastModified'])
                for file in response]


    def download_files(self):
        # Return if there are no files to download
        if len(self._files) == 0:
            return
        
        # Obtain download urls for Cortex data files
        download_urls = requests.get(
            f'{self._api_url}/models/{self._model_id}/files/download',
            headers=self._headers
        )

        download_urls = download_urls.text.replace('[', '').replace(']', '').replace('"', '').split(',')

        for i in range(len(download_urls)):
            response = requests.get(
                download_urls[i]
            )

            file_name = self._files[i].name
            local_path = f'{self._local_dir}/{file_name}'
            
            if not self.find_file(file_name).exists():
                with open(local_path, "wb") as binary_file:
                    # Write bytes to file
                    binary_file.write(response.content)


    def sync_to_cortex(self, file:CortexFile):
        # Syncs an existing file to S3
        if os.path.exists(file.local_path):
            raise Exception('Function not yet implemented!')
        else:
            raise Exception(f'Error syncing file to cortex! File does not exist: {file.local_path}')


    def find_file(self, name:str):
        # Find file with name
        for file in self._files:
            if file.name == name:
                return file
        raise FileNotFoundError(f'File {name} not found in Cortex data.')
