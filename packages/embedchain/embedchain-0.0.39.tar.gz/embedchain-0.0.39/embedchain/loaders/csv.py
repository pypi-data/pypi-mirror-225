from langchain.document_loaders import CSVLoader

from embedchain.utils import clean_string


class CsvFileLoader:
    def load_data(self, url):
        """Load data from a PDF file."""
        loader = CSVLoader(file_path=url)
        output = []
        pages = loader.load()
        if not len(pages):
            raise ValueError("No data found")
        for page in pages:
            content = page.page_content
            # content = clean_string(content)
            meta_data = page.metadata
            meta_data["url"] = url
            output.append(
                {
                    "content": content,
                    "meta_data": meta_data,
                }
            )
        print('##', output)
        return output
