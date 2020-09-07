def get_submission_format(soup):
    try:
        soup.select('.template').text