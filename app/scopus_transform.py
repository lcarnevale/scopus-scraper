import logging

class ScopusTransform:
    
    __instance = None

    def __new__(self) -> __instance:
        """Implement Singleton class.
				
        Returns
		    (ScopusTransform) singleton instance of the class.
        """
        if self.__instance is None:
            print('creating the %s object ...' % (self.__name__))
            self.__instance = super(ScopusTransform, self).__new__(self)
        return self.__instance
    
    def build(self) -> __instance:
        """
        Returns:
            (ScopusTransform) the implemented class
        """
        return self.__instance
    

    def documents(self, documents_extracted) -> list:
        documents_transformed = list()
        for document_extracted in documents_extracted:
            document_transformed = {
                "document_type": self.__get_document_type(document_extracted),
                "authors": self.__get_authors(document_extracted),
                "title": self.__get_title(document_extracted),
                "publication_name": self.__get_publication_name(document_extracted),
                "volume": self.__get_volume(document_extracted),
                "pages": self.__get_pages(document_extracted),
                "date": self.__get_publication_date(document_extracted),
                "doi": self.__get_publication_doi(document_extracted),
                "openaccess": self.__get_openaccess(document_extracted),
                "citation": self.__get_citation(document_extracted)
            }
            documents_transformed.append(document_transformed)
        return documents_transformed

    def __get_document_type(self, document_extracted) -> str:
        """ Transform the document type.

        Args:
            document_extracted (dict): the document extracted by Scopus.

        Returns:
            (str) the document type
        """
        return document_extracted['abstracts-retrieval-response']['coredata'].get('prism:aggregationType')
    
    def __get_authors(self, document_extracted) -> str:
        """ Transform the authors.

        Args:
            document_extracted (dict): the document extracted by Scopus.

        Returns:
            (str) a sequence of authors
        """
        authors = ''
        for author in document_extracted['abstracts-retrieval-response']['authors']['author']:
            authors += '%s %s, ' % (author['ce:given-name'], author['ce:surname'])
        return authors[:-2]
    
    def __get_title(self, document_extracted) -> str:
        """ Transform the title.

        Args:
            document_extracted (dict): the document extracted by Scopus.

        Returns:
            (str) the title
        """
        return document_extracted['abstracts-retrieval-response']['coredata'].get('dc:title')
    
    def __get_publication_name(self, document_extracted) -> str:
        """ Transform the publication name.

        Args:
            document_extracted (dict): the document extracted by Scopus.

        Returns:
            (str) the publication name
        """
        return document_extracted['abstracts-retrieval-response']['coredata'].get('prism:publicationName')
    
    def __get_volume(self, document_extracted) -> str:
        """ Transform the volume of publication.

        Args:
            document_extracted (dict): the document extracted by Scopus.

        Returns:
            (str) the volume of publication
        """
        return document_extracted['abstracts-retrieval-response']['coredata'].get('prism:volume')
    
    def __get_pages(self, document_extracted) -> str:
        """ Transform the pages of publication.

        Args:
            document_extracted (dict): the document extracted by Scopus.

        Returns:
            (str) the pages of publication
        """
        return document_extracted['abstracts-retrieval-response']['coredata'].get('prism:pageRange')
    
    def __get_publication_date(self, document_extracted) -> str:
        """ Transform the publication date.

        Args:
            document_extracted (dict): the document extracted by Scopus.

        Returns:
            (str) the publication date
        """
        return document_extracted['abstracts-retrieval-response']['coredata'].get('prism:coverDate')
    
    def __get_publication_doi(self, document_extracted) -> str:
        """ Transform the publication DOI.

        Args:
            document_extracted (dict): the document extracted by Scopus.

        Returns:
            (str) the publication DOI
        """
        return document_extracted['abstracts-retrieval-response']['coredata'].get('prism:doi')
    
    def __get_citation(self, document_extracted) -> str:
        """ Transform the publication citation.

        Args:
            document_extracted (dict): the document extracted by Scopus.

        Returns:
            (str) the publication citation
        """
        return int( document_extracted['abstracts-retrieval-response']['coredata'].get('citedby-count') )
    
    def __get_openaccess(self, document_extracted) -> str:
        """ Transform the open access information.

        Args:
            document_extracted (dict): the document extracted by Scopus.

        Returns:
            (str) the open access information
        """
        return int( document_extracted['abstracts-retrieval-response']['coredata'].get('openaccess') )
    

    def authors(self, authors_extracted) -> list:
        authors_transformed = list()
        for author_extracted in authors_extracted:
            authors_transformed.append({
                "id": author_extracted['dc:identifier'].split(':')[-1],
                "author": self.__get_author_name(author_extracted['preferred-name']),
                "affiliation": self.__get_affiliation(author_extracted['affiliation-current']),
                "subject_area": self.__get_subject_areas(author_extracted['subject-area'])
            })
        return authors_transformed

    def __get_author_name(self, author_name_extracted) -> str:
        """Transform the author name.

        Args:
            author_name_extracted (dict): data structure with the name information.

        Returns:
            (str) the complete name (first and family name)
        """
        return '%s %s' % (
            author_name_extracted['given-name'],
            author_name_extracted['surname']
        )
    
    def __get_affiliation(self, affiliation_extracted) -> dict:
        """Transform the affiliation

        Args:
            affiliation_extracted (dict): data structure with the affiliation information.

        Returns:
            (dict) a data structure with the affiliation information
        """
        return {
            "id": affiliation_extracted['affiliation-id'],
            "institute": affiliation_extracted['affiliation-name'],
            "city": affiliation_extracted['affiliation-city'],
            "country": affiliation_extracted['affiliation-country']
        }

    def __get_subject_areas(self, subject_areas_extracted) -> list:
        """Transform the subject areas

        Args:
            subject_areas_extracted (dict): data structure with the subject areas information.

        Returns:
            (list) a list of subject areas
        """
        subject_area_transformed = list()
        for subject_area_extracted in subject_areas_extracted:
                subject_area_transformed.append( subject_area_extracted["$"] )
        return subject_area_transformed
