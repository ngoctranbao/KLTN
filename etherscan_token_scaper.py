import http.client
from bs4 import BeautifulSoup
import csv


def send_request(page):
    try:
        conn = http.client.HTTPSConnection("etherscan.io")
        payload = ''
        headers = {
            'Cookie': 'ASP.NET_SessionId=zsrvz5qiuqvxnozgkstesgvk; __cflb=02DiuFnsSsHWYH8WqVXaqGvd6BSBaXQLUMoS7YPUxtSn8'
        }
        url = "/tokens?ps=100&p=%d" % page
        conn.request("GET", url, payload, headers)
        res = conn.getresponse()
        
        if res.status != 200:
            raise Exception(f"Request failed with status code {res.status}")
        
        data = res.read()
        body = BeautifulSoup(data.decode("utf-8"), "html.parser")
        html_table = body.find("table")
        
        if not html_table:
            raise Exception("No table found in the response")

        table_rows = html_table.find_all("tr")
        print("success")
        return table_rows
    
    except Exception as e:
        print(f"An error occurred: {e}")
        print("failed")
        return []

def write(table_rows):
    with open("./datasets/tokens.csv", "w", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        
        for index, row in enumerate(table_rows):
            cols = row.find_all(["td", "th"])
            extracted_cols = []
            token_id = "Id"
            for index_col, col in enumerate(cols):
                # Extract the text from the column
                text = col.get_text(strip=True)
                # Check if there is an <a> tag with an href attribute
                a_tag = col.find("a", href=True)
                if a_tag and index_col == 1:
                    # Extract the ID from the href attribute
                    href = a_tag['href']
                    # You can use regular expression to extract the ID if the href format is fixed
                    # Here assuming the ID is the part after "/token/"
                    token_id = href.split('/token/')[-1]
                extracted_cols.append(text)
            # Append the token ID as a separate column
            extracted_cols.append(token_id)
            print(extracted_cols)
            writer.writerow(extracted_cols)
            
table_rows = []
for i in range(0,15):
    table_rows.extend(send_request(i+1))
write(table_rows)