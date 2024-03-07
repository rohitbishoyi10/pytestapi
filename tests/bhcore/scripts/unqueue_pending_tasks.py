import requests

from tests.bhcore.bhlib.utils import html_util
from tests.bhcore.bhlib.utils.html_util import html_get_attr_value


def icls_prelogin():
    headers = {
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Accept-Language': 'en-GB,en;q=0.9',
    }

    params = (
        ('submit', '1'),
        ('bind_0', 'Service_Fulfill'),
        ('bind_1', 'cpanel'),
    )

    response = requests.get('https://i.beta.bluehost.in/cgi/admin/db_report/open/2061', headers=headers, params=params)
    return response.text

def find_signup_internals(self, html):
    data = {
        'redirect': html_get_attr_value(html, 'redirect'),
        'cea_time': html_get_attr_value(html, 'cea_time'),
        'cea_expires_min': html_get_attr_value(html, 'cea_expires_min'),
        'adminlogintok': html_get_attr_value(html, 'adminlogintok')
    }
    return data


def icls_login(html):

    headers = {
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Upgrade-Insecure-Requests': '1',
        'Origin': 'https://i.beta.bluehost.in',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Referer': 'https://i.beta.bluehost.in/cgi/admin/db_report/open/2061?submit=1&bind_0=Service_Fulfill&bind_1=cpanel',
        'Accept-Language': 'en-GB,en;q=0.9',
    }

    data = {
        'redirect': html_get_attr_value(html, 'redirect'),
        'cea_time': html_get_attr_value(html, 'cea_time'),
        'cea_expires_min': html_get_attr_value(html, 'cea_expires_min'),
        'admin_user': 'svcbluehostapac',
        'admin_pass': 'Vf_z63&w=Zu=R+(U',
        'adminlogintok': html_get_attr_value(html, 'adminlogintok')
    }

    response = requests.post('https://i.beta.bluehost.in/cgi/admin/db_report/open/2061', headers=headers, data=data)
    return response.cookies.get('admin_user')

def get_queued_task_lists(admin_token):
    cookies = {
        'admin_user': admin_token,
    }

    headers = {
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Referer': 'https://i.beta.bluehost.in/cgi/admin/db_report/open/2061?submit=1&bind_0=Service_Fulfill&bind_1=cpanel',
        'Accept-Language': 'en-GB,en;q=0.9',
    }

    params = (
        ('submit', '1'),
        ('bind_0', 'Service_Fulfill'),
        ('bind_1', 'cpanel'),
    )

    response = requests.get('https://i.beta.bluehost.in/cgi/admin/db_report/open/2061', headers=headers, params=params,
                            cookies=cookies)

    html = response.text
    task_lists = html_util.read_table_data(html)
    return task_lists

def check_task_details(task_id, admin_user):
    cookies = {
        'admin_user': admin_user,
    }

    headers = {
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Referer': 'https://i.beta.bluehost.in/cgi/admin/db_report/open/2061?submit=1&bind_0=Service_Fulfill&bind_1=cpanel',
        'Accept-Language': 'en-GB,en;q=0.9',
    }

    response = requests.get('https://i.beta.bluehost.in/cgi-bin/admin/task/' + task_id, headers=headers, cookies=cookies)
    html = response.text
    print(html)

def unque_the_task(task_id, admin_user):
    cookies = {
        'admin_user': admin_user,
    }

    headers = {
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Referer': 'https://i.beta.bluehost.in/cgi-bin/admin/task/797794',
        'Accept-Language': 'en-GB,en;q=0.9',
    }

    response = requests.get('https://i.beta.bluehost.in/cgi-bin/admin/task/unqueue/' + task_id, headers=headers,
                            cookies=cookies)

    html = response.text
    if 'successfully unqueued.' in html:
        return True
    else:
        return False

html = icls_prelogin()
admin_token = icls_login(html)
task_ids = get_queued_task_lists(admin_token)

counter = 0
unqueued_lists = []
failed_list = []
for task in task_ids:
    # check_task_details(task, admin_token)
    if unque_the_task(task, admin_token):
        counter = counter + 1
        unqueued_lists.append(task)
    else:
        failed_list.append(task)
    print(counter)

    if counter >= 100:
        print("500 tasks unqueued!")
        print(unqueued_lists)
        print(failed_list)
        break