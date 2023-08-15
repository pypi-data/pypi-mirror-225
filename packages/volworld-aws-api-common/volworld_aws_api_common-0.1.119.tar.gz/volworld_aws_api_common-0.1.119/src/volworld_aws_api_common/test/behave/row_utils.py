from selenium.webdriver.common.by import By
from volworld_common.api.CA import CA

from volworld_common.test.behave.BehaveUtil import BehaveUtil
from volworld_aws_api_common.test.behave.selenium_utils import get_element_by_dom_id, w__click_element_by_dom_id
from volworld_aws_api_common.test.behave.drawer_utils import click_to_open_list_nav_drawer


def assert_tag_svg_class_of_all_rows(rows, class_name_list: list):
    class_name = f"SvgIcon-{'-'.join(class_name_list)}"
    for r in rows:
        main = r.find_element(By.XPATH, "./main/nav/main")  # @note xpath can NOT find svg element
        main_inner = main.get_attribute('innerHTML')
        assert main_inner.find(class_name) > -1, \
            f"Class [{class_name}] NOT in tag main svg classes = [{main_inner}]"


def predicate__get_row_container(c):
    def _predicate(driver):
        container_ids = ([CA.Book, CA.List], [CA.Chapter, CA.List], [CA.Word, CA.List])
        list_container = None
        for con_id in container_ids:
            list_container = get_element_by_dom_id(c, con_id)
            if list_container is not None:
                break
        return list_container

    return _predicate


def w__get_row_container(c):
    return c.wait.until(predicate__get_row_container(c))


def w__get_row_items(c) -> list:
    list_container = w__get_row_container(c)

    assert list_container is not None, 'Can NOT find row item container'
    return list_container.find_elements(By.XPATH, "./div")


def get_row__tag_info__as__text_list(c) -> list:
    rows = w__get_row_items(c)
    tag_text_list = []
    for r in rows:
        span = r.find_element(By.XPATH, "./main/nav/main/b")
        tag_text_list.append(span.get_attribute('innerHTML').strip())
    return tag_text_list


def get_row__tag_info__as__int_list(c) -> list:
    info = get_row__tag_info__as__text_list(c)
    int_info = []
    for i in info:
        int_info.append(int(i))
    return int_info


def get_row__text__as__text_list(c) -> list:
    rows = w__get_row_items(c)
    row_text_list = []
    for r in rows:
        span = r.find_element(By.XPATH, "./main/main/span")
        row_text_list.append(span.get_attribute('innerHTML').strip())
    return row_text_list


def update_order_type_of_list(c, sort_dir: str):
    sort_dir = BehaveUtil.clear_string(sort_dir)
    click_to_open_list_nav_drawer(c, CA.SortDirection)
    if sort_dir.lower() == "ascending":
        w__click_element_by_dom_id(c, [CA.Drawer, CA.SortDirection, CA.Button, CA.Ascending])
    if sort_dir.lower() == "descending":
        w__click_element_by_dom_id(c, [CA.Drawer, CA.SortDirection, CA.Button, CA.Descending])


def check_tag_svg_class_of_all_rows(rows, class_name_list: list)->bool:
    def _predicate(driver):
        class_name = f"SvgIcon-{'-'.join(class_name_list)}"
        for r in rows:
            main = r.find_element(By.XPATH, "./main/nav/main")  # @note xpath can NOT find svg element
            main_inner = main.get_attribute('innerHTML')
            if main_inner.find(class_name) < 0:
                print("can not find class_name = ", class_name)
                return False
        return True

    return _predicate


def w__assert_tag_svg_class_of_all_rows(c, rows, class_name_list: list):
    return c.wait.until(check_tag_svg_class_of_all_rows(rows, class_name_list))