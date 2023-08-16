import json
import requests


class ScopusExtract:

    def __init__(self, conffile) -> None:
        """
        """
        with open(conffile, 'r') as f:
            conf = json.load(f)
        self.__author_id = conf["author_id"]
        self.__api_key = conf["api_key"]

    def extract_author(self) -> dict:
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
            #print(json.dumps(json_data, indent=2))

            return {
                "orcid": json_data["search-results"]["entry"][0].get("orcid"),
                "scopus_id": self.__author_id,
                "author_name": {
                    "first_name": json_data["search-results"]["entry"][0]["preferred-name"]["given-name"],
                    "family_name": json_data["search-results"]["entry"][0]["preferred-name"]["surname"]
                },
                "subject-area": self.__extract_subject_areas(json_data["search-results"]["entry"][0].get("subject-area")),
                "affiliation-current": {
                    "institute": json_data["search-results"]["entry"][0]["affiliation-current"]["affiliation-name"],
                    "city": json_data["search-results"]["entry"][0]["affiliation-current"]["affiliation-city"],
                    "country": json_data["search-results"]["entry"][0]["affiliation-current"]["affiliation-country"],
                }
            }
        except Exception as e:
            print("Generic error: %s" % (e))
            return

    def __extract_subject_areas(self, subject_areas) -> list:
        extracted_subject_areas = list()
        for subject_area in subject_areas:
            extracted_subject_areas.append( tuple( (subject_area.get("$"), subject_area.get("@frequency") ) ) )
        return extracted_subject_areas

    def extract_metrics(self) -> dict:
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

    def extract_documents_ids(self) -> dict():
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
            #print(json.dumps(json_data, indent=2))

            extracted_document_ids = list()
            document_ids = json_data["search-results"]["entry"]
            for document_id in document_ids:
                extracted_document_ids.append( document_id['dc:identifier'] )
            return extracted_document_ids
        except Exception as e:
            print("Generic error: %s" % (e))
            return
        
    def extract_documents(self, document_ids):
        documents = list()

        for document_id in document_ids:

            endpoint = "http://api.elsevier.com/content/abstract/scopus_id/%s?field=authors,title,publicationName,volume,issueIdentifier,prism:pageRange,coverDate,article-number,doi,citedby-count,prism:aggregationType" % (document_id)
            headers = {
                'Accept': 'application/json',
                'X-ELS-APIKey': self.__api_key
            }
            
            try:
                response = requests.get(endpoint, headers=headers)
                response.raise_for_status()    
                json_data = json.loads(response.text.encode('utf-8'))
                #print(json.dumps(json_data, indent=2, ensure_ascii=False))
                
                document = {
                    "type": json_data['abstracts-retrieval-response']['coredata'].get('prism:aggregationType'),
                    "authors": ', '.join([author['ce:indexed-name'] for author in json_data['abstracts-retrieval-response']['authors']['author']]),
                    "title": json_data['abstracts-retrieval-response']['coredata'].get('dc:title'),
                    "publication_name": json_data['abstracts-retrieval-response']['coredata'].get('prism:publicationName'),
                    "volume": json_data['abstracts-retrieval-response']['coredata'].get('prism:volume'),
                    "articlenum": ( json_data['abstracts-retrieval-response']['coredata'].get('prism:pageRange') or json_data['abstracts-retrieval-response']['coredata'].get('article-number')),
                    "date": json_data['abstracts-retrieval-response']['coredata'].get('prism:coverDate'),
                    "doi": json_data['abstracts-retrieval-response']['coredata'].get('prism:doi'),
                    "cites": int( json_data['abstracts-retrieval-response']['coredata'].get('citedby-count') )
                }
                documents.append(document)
            except Exception as e:
                print("Generic error: %s" % (e))
                return
        return documents


def main():
    conffile = "conf.json"
    scopus_extract = ScopusExtract(conffile)

    author_info = scopus_extract.extract_author()
    author_info['metrics'] = scopus_extract.extract_metrics()
    documents_ids = scopus_extract.extract_documents_ids()
    author_info['documents'] = scopus_extract.extract_documents(documents_ids)
    #print(json.dumps(author_info, indent=2, ensure_ascii=False))

    with open('result.json', 'w') as f:
        json.dump(author_info, f)

if __name__ == "__main__":
    main()