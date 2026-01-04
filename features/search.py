def search_in_pdf(pdf_text, query):
    """
    Return sentences containing the query keyword.
    """
    sentences = pdf_text.split('.')
    results = [s.strip() for s in sentences if query.lower() in s.lower()]
    return results if results else ["No results found."]
