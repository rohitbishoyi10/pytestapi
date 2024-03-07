import sys
import os
from bs4 import BeautifulSoup
import re

dir_path = os.path.dirname(os.path.realpath(__file__))
framework_path = os.path.split(dir_path)[0]
framework_path = os.path.split(framework_path)[0]
print(framework_path)
sys.path.append(framework_path)

def html_get_attr_value(html, attr_name):

    parsed_html = BeautifulSoup(html, 'lxml')
    input_tag = parsed_html.find_all(attrs={"name": attr_name})
    val = input_tag[0]['value']
    print(val)
    return val

def html_find_href(html, search_txt):
    #html = open('/Users/trilokesh.b/Desktop/error_pay2.html', 'r').read()
    parsed_html = BeautifulSoup(html, 'lxml')
    for a in parsed_html.find_all('a', href=True):
        if search_txt in a['href']:
            return a['href']

def find_token(s):
    pattern = "token=(.*?)&"
    token = re.search(pattern, s).group(1)
    print(token)
    return token

def check_for_text_by_div_class(class_name, html, text_to_check):
#def check_for_text():
    #html = open('/Users/trilokesh.b/Desktop/error_pay2.html', 'r').read()
    #text_to_check = 'Your purchase was a success!'
    #class_name = 'center'
    # html = open('/Users/trilokesh.b/Desktop/domain1_error.html', 'r').read()
    # text_to_check = '.com is available!'
    # class_name = 'domain_success'
    try:
        parsed_html = BeautifulSoup(html, 'lxml')
        result = parsed_html.find("div", {"class": class_name})
        if result is not None:
            txt = result.text
            print('DIV TEXT' + txt)
            print('Exp TEXT' + text_to_check)
            if text_to_check in txt:
                print('MATCH FOUND')
                return True
            else:
                print('MATCH NOT FOUND')
                return False
        else:
            return False
    except Exception as e:
        print(e)
        return False

def get_text_by_p_class(class_name, html):
    # html = open('/Users/trilokesh.b/Documents/aa_payment_error_.html')
    # class_name = 'error'
    try:
        parsed_html = BeautifulSoup(html, 'lxml')
        result = parsed_html.find("p", {"class": class_name})
        if result is not None:
            txt = result.text
            print('DIV TEXT' + txt)
            return txt
    except Exception as e:
        print(e)
        return ''

#print(get_text_by_p_class('',''))

# def check_for_text(html, text_to_check):
# #def check_for_text():
#     #html = open('/Users/trilokesh.b/Desktop/error_pay2.html', 'r').read()
#     #html = open('/Users/trilokesh.b/Desktop/domain1_error.html', 'r').read()
#     #text_to_check = 'The domain test-api-06112020120258-pwstqo7s.com is available!'
#     parsed_html = BeautifulSoup(html,'lxml')
#     print(parsed_html)
#     print('**********')
#     if parsed_html.find(text=text_to_check):
#         print('Able to find text ' + text_to_check)
#         return True
#     else:
#         print('Unable to find text ' + text_to_check)
#         return False

def check_for_text(html, text_to_check):
    parsed_html = BeautifulSoup(html, 'lxml')
    return parsed_html.find(text=text_to_check)




def write_to_a_file(file, html):
    file = open(file, 'w')
    file.write(html)
    file.close()


def get_script_parameter(html):
    #html = open('/Users/trilokesh.b/Documents/test-output/id_3ds.html', 'r').read()
    parsed_html = BeautifulSoup(html, 'lxml')
    string = parsed_html.script.string
    left = 'sendNotification(true, "'
    right = '");'

    strs = string.splitlines()
    for str in strs:
        if 'sendnotification' in str.lower():
            id_3ds = (str[str.index(left)+len(left):str.index(right)])
            return (id_3ds)

#get_script_parameter()

def get_tittle(html):
    parsed_html = BeautifulSoup(html, 'lxml')
    return parsed_html.title.string

def html_find_text(html, css_sector):
    parsed_html = BeautifulSoup(html, 'lxml')
    if len(parsed_html.select(css_sector)) != 0:
        return parsed_html.select(css_sector)
    else:
        raise Exception("element not found,  css_sector : " + css_sector)

def check_for_error(html, tag, class_name, text_to_check):
    try:
        parsed_html = BeautifulSoup(html, 'lxml')
        result = parsed_html.find_all(tag, class_=class_name)
        if result is not None:
            print('Orignal TEXT : ' + str(result))
            print('Exp TEXT : ' + text_to_check)
            for data in result:
                if text_to_check in data:
                    print('MATCH FOUND')
                    return True
            else:
                print('MATCH NOT FOUND')
                return False
        else:
            return False
    except Exception as e:
        print(e)
        return False

def read_table_data(html):
    try:
        # html = open('/Users/trilokesh.b/Downloads/iCluster_queueued_tasks.html', 'r').read()
        data = []
        parsed_html = BeautifulSoup(html, 'lxml')
        table = parsed_html.find('table', attrs={'class': 'grid'})
        for row in table.findAll("tr"):
            cells = row.findAll("td")
            if cells:
                txt = cells[1].text
                t = txt.replace(u'\xa0', u' ')
                task_id = t.split(" ")[0]
                data.append(task_id)
        return data
    except Exception as e:
        print(e)


def read_products_table(html):
    try:
        # html = open('C:/Endurance/Endurance Projects/Bluehost/API Testing/Har/Affiliates/response.html', 'r').read()
        data = {}
        parsed_html = BeautifulSoup(html, 'lxml')
        table = parsed_html.find('table', attrs={'class': 'brand-table'})
        for row in table.findAll("tr"):
            cells = row.findAll("input")
            if cells:
                data[cells[0].attrs['name']] = cells[0].attrs['value']
        return data
    except Exception as e:
        print(e)


def read_aff_account_tracking_from_icluster(html):
    try:
        # html = open('/Users/trilokesh.b/Downloads/cpanel_affiliates_resp.html', 'r').read()
        # html = open('C:/Endurance/Endurance Projects/Bluehost/API Testing/Har/Affiliates/response.html', 'r').read()
        data_dict = {}
        parsed_html = BeautifulSoup(html, 'lxml')

        table_div = parsed_html.find("div", {"id": "opt_affiliate"})
        # table_div = parsed_html.find("div", {"id": sub_table_id})
        table = table_div.find('table')
        for row in table.findAll("tr"):
            cells = row.findAll("td")
            if cells:
                name = cells[0].contents[1].attrs['name']
                val = cells[0].contents[1].attrs['value']
                data_dict[name] = val
        return data_dict
    except Exception as e:
        print(e)

def get_domain_custid_from_response(html):
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup.findAll('script'):
        if "document.cookie = 'custid=" in str(tag):
            m = re.search(r"document.cookie = 'custid=([0-9]*?);", tag.string)
            if m:
                cust_id = int(m.group(1))
                if isinstance(cust_id, int):
                    return cust_id
                else:
                    raise Exception("Unable to get cust_id or cust_id is not of type integer.\n Cust id found is" +
                                    m.group(1) + '\n Complete html reponse is :' + html)
