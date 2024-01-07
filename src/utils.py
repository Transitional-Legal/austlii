#!/usr/bin/python3
import http.client
# import requests

# def download(url, filename):
#     r = requests.get(url, allow_redirects=True)
#     open(filename, 'wb').write(r.content)


def crawl(year, start=26, max_page=100):

    conn = http.client.HTTPSConnection("www.austlii.edu.au")
    payload = ''
    headers = {
        'user-agent': 'Mozilla/5.0'
    }

    # for i in range(start, max_page):
    # conn.request(
    #     "GET", f'/cgi-bin/viewdoc/au/cases/cth/FamCA/{year}/{start}.html', payload, headers)

    conn.request(
        "GET", f'/cgi-bin/sign.cgi/au/cases/cth/FamCA/{year}/{start}', payload, headers)

    res = conn.getresponse()
    data = res.read()

    with open(f'/cases/{year}-{start}.pdf', 'wb') as f:
        f.write(data)

    # print(data.decode("utf-8"))

    # A GET request to the API
    # response = requests.get(url)
    # print("Status: {} and reason: {}".format(response.status_code, response.reason))

    # connection = http.client.HTTPSConnection(url)
    # # connection.request("GET", "/cgi-bin/viewtoc/au/cases/cth/FamCA/2021/")
    # connection.request("GET", "/")
    # response = connection.getresponse()
    # print("Status: {} and reason: {}".format(response.status, response.reason))

    # connection.close()


if __name__ == "__main__":
    crawl(2021, 26)
    # crawl("www.google.com")
