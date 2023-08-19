from behave import *


@when('clear browser local storage')
def when_clear_local_storage(c):
    c.browser.execute_script("window.localStorage.clear();")


@when('refresh browser')
def when_refresh_browser(c):
    c.browser.refresh()
