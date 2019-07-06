import urllib.request
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import H1Bconfig


def extract_html(url):
    page = urllib.request.urlopen(url)
    page_bytes = page.read()
    html = page_bytes.decode("utf8")
    page.close()
    return html


def format_html(html):
    formatted_html = BeautifulSoup(html, "html.parser")
    return formatted_html


def extract_table_data(url):

    bs_html = format_html(extract_html(url))
    column_names = ["employer", "job title", "base salary", "location", "sub date", "start date", "case status"]
    table_info = {}

    for name in column_names:
        table_info[name] = None

    for row in enumerate(bs_html.find_all("tr")):
        if row[0] == 0:  # title row
            pass
        else:  # data
            for cell in enumerate(row[1].find_all("td")):
                if table_info[column_names[cell[0]]] is None:
                    table_info[column_names[cell[0]]] = [cell[1].text]
                else:
                    table_info[column_names[cell[0]]].append(cell[1].text)

    return table_info


if __name__ == "__main__":

    salaries = []
    for title in H1Bconfig.titles:
        data_dict = extract_table_data("https://h1bdata.info/index.php?em=&job="
                    +title+"&city="+H1Bconfig.location+"&year="+H1Bconfig.year)

        salaries += data_dict["base salary"]

    all_salaries = [int(x.replace(',', ''))*(1-H1Bconfig.offset) for x in salaries]
    all_salaries.sort()
    print(all_salaries)

    # make graph
    plt.plot(all_salaries)
    plt.ylabel('Salary (Los Angeles')
    plt.xlabel("Data Point")
    plt.show()


