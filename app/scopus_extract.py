import json
import logging
import requests

class ScopusExtract:

    __instance = None

    def __new__(self) -> __instance:
        """Implement Singleton class.
				
        Returns
		    (ScopusExtract) singleton instance of the class.
        """
        if self.__instance is None:
            print('creating the %s object ...' % (self.__name__))
            self.__instance = super(ScopusExtract, self).__new__(self)
        return self.__instance

    def build_api_key(self, api_key) -> __instance:
        """
        Args:
            api_key (str): Scopus API key

        Returns:
            (ScopusExtract) the implemented class
        """
        self.__api_key = api_key
        return self.__instance
    
    def build_author_id(self, author_id) -> __instance:
        """
        Args:
            author_id (str): Author ID

        Returns:
            (ScopusExtract) the implemented class
        """
        self.__author_id = author_id
        return self.__instance
    
    def build(self) -> __instance:
        """
        Returns:
            (ScopusExtract) the implemented class
        """
        return self.__instance
    

    def __author_id(self) -> dict:
        """
        """
        endpoint = "https://api.elsevier.com/content/search/author?query=AU-ID(%s)" % (self.__author_id)
        headers = {
            "Accept": "application/json",
            "X-ELS-APIKey": self.__api_key
        }

        try:
            response = requests.get(endpoint, headers=headers)
            response.raise_for_status()    
            json_data = json.loads(response.text)
            return json_data

            # return {
            #     "orcid": json_data["search-results"]["entry"][0].get("orcid"),
            #     "scopus_id": self.__author_id,
            #     "author_name": {
            #         "first_name": json_data["search-results"]["entry"][0]["preferred-name"]["given-name"],
            #         "family_name": json_data["search-results"]["entry"][0]["preferred-name"]["surname"]
            #     },
            #     "subject-area": self.__extract_subject_areas(json_data["search-results"]["entry"][0].get("subject-area")),
            #     "affiliation-current": {
            #         "institute": json_data["search-results"]["entry"][0]["affiliation-current"]["affiliation-name"],
            #         "city": json_data["search-results"]["entry"][0]["affiliation-current"]["affiliation-city"],
            #         "country": json_data["search-results"]["entry"][0]["affiliation-current"]["affiliation-country"],
            #     }
            # }
        except Exception as e:
            print("Generic error: %s" % (e))
            return

    def __extract_subject_areas(self, subject_areas) -> list:
        extracted_subject_areas = list()
        for subject_area in subject_areas:
            extracted_subject_areas.append( tuple( (subject_area.get("$"), subject_area.get("@frequency") ) ) )
        return extracted_subject_areas

    def __extract_metrics(self) -> dict:
        """
        """
        endpoint = f"http://api.elsevier.com/content/author?author_id=%s&view=metrics" % (self.__author_id)
        headers = {
            "Accept": "application/json",
            "X-ELS-APIKey": self.__api_key
        }

        try:
            response = requests.get(
                f"http://api.elsevier.com/content/author?author_id={self.__author_id}&view=metrics",
                headers={
                    'Accept': 'application/json',
                    'X-ELS-APIKey': self.__api_key
                }
            )

            # response = requests.get(endpoint, headers)
            response.raise_for_status()    
            json_data = json.loads(response.text)
            #print(json.dumps(json_data, indent=2))

            return {
                "document_count": json_data["author-retrieval-response"][0]["coredata"]["document-count"],
                "cited_by_count": json_data["author-retrieval-response"][0]["coredata"]["cited-by-count"],
                "citation_count": json_data["author-retrieval-response"][0]["coredata"]["citation-count"],
                "h_index": json_data["author-retrieval-response"][0]["h-index"],
                "coauthor-count": json_data["author-retrieval-response"][0]["coauthor-count"]
            }
            print(json.dumps(metrics, indent=2))
        except Exception as e:
            print("Generic error: %s" % (e))
            return   


    def documents(self):
        documents_ids = self.__documents_ids()
        documents = list()

        for document_id in documents_ids:

            endpoint = "http://api.elsevier.com/content/abstract/scopus_id/%s?field=authors,openaccess,title,publicationName,prism:issueIdentifier,prism:pageRange,prism:isbn,prism:issn,coverDate,doi,citedby-count,prism:aggregationType,prism:volume,subject-areas" % (document_id)
            headers = {
                'Accept': 'application/json',
                'X-ELS-APIKey': self.__api_key
            }
            
            try:
                response = requests.get(endpoint, headers=headers)
                response.raise_for_status()    
                json_data = json.loads(response.text.encode('utf-8'))
                documents.append(json_data)
            except Exception as e:
                print("Generic error: %s" % (e))
                return
        return documents

    def __documents_ids(self) -> dict():
        """
        """
        endpoint = f"http://api.elsevier.com/content/search/scopus?query=AU-ID({self.__author_id})&field=dc:identifier&count=100"
        headers = {
            'Accept': 'application/json',
            'X-ELS-APIKey': self.__api_key
        }
        try:
            response = requests.get(endpoint, headers=headers)
            response.raise_for_status()    
            json_data = json.loads(response.text)

            extracted_document_ids = list()
            document_ids = json_data["search-results"]["entry"]
            for document_id in document_ids:
                extracted_document_ids.append( document_id['dc:identifier'] )
            return extracted_document_ids
        except Exception as e:
            print("Generic error: %s" % (e))
            return