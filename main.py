import yaml
from app.scopus_extract import ScopusExtract
from app.scopus_transform import ScopusTransform
from app.scopus_load import ScopusLoad

def main():
    conffile = "conf.json"
    with open(conffile, 'r') as f:
        conf = yaml.safe_load(f)
    
    scopus_extract = ScopusExtract() \
        .build_api_key(conf["api_key"]) \
        .build_author_id(conf["author_id"]) \
        .build()
    scopus_transform = ScopusTransform() \
        .build()
    scopus_load = ScopusLoad() \
        .build()
    
    authors_extracted = scopus_extract.author_name("Lorenzo", "Carnevale")
    authors_transformed = scopus_transform.authors(authors_extracted)
    documents_extracted = scopus_extract.documents('57195963279')
    print(documents_extracted[0])
    documents_transformed = scopus_transform.documents(documents_extracted)
    print(documents_transformed[0])
    scopus_load.load()

if __name__ == "__main__":
    main()