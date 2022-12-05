import requests
import openpyxl 
import concurrent.futures
from openpyxl.styles import Font

wb = openpyxl.Workbook()
# grab the active worksheet
ws = wb.active
header = ['toolName', 'toolDescription', 'features', 'websiteUrl', 'verified', 'favCount', 'type', 'tags']
ws.append(header)
for cell in ws["1:1"]:
    cell.font = Font(bold=True)
wb.save('futurepedia.xlsx')


def scrape_page(url):
    global wb, ws
    res = requests.get(url).json()
    for item in res:
        toolName = item.get('toolName')
        toolDescription = item.get('toolDescription')
        features = item.get('features')
        websiteUrl = item.get('websiteUrl')
        verified = item.get('verified')
        favCount = item.get('favCount')
        itemtype = item.get('_type')
        tags = item['tags']
        tag_list = ''
        feature_list = ''
        if features:
            for feature in features:
                feature_list += f'{feature}, '
        if tags:
            for tag in tags:
                tag_list += f'{tag.get("tagName")}, '

        if toolName:
            toolName = toolName.strip()
        if toolDescription:
            toolDescription = toolDescription.strip()
        if feature_list:
            feature_list = feature_list.strip()[:-1]
        if tag_list:
            tag_list = tag_list.strip()[:-1]
        if websiteUrl:
            websiteUrl = websiteUrl.strip()
        if itemtype:
            itemtype = itemtype.strip()

        row = [toolName, toolDescription, feature_list, websiteUrl, verified, favCount, itemtype, tag_list]
        ws.append(row)
    wb.save('futurepedia.xlsx')


urls = []
page = 1
while page <= 41:
    url = f'https://www.futurepedia.io/api/tools?page={page}&sort=verified'
    urls.append(url)
    page += 1

    
with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(scrape_page, urls)
