from behave import *
from volworld_common.test.behave.BehaveUtil import BehaveUtil
from volworld_aws_api_common.test.behave.ACotA import ACotA


def set_target_page(c, target_page: str):
    target_page = BehaveUtil.clear_string(target_page)
    setattr(c, ACotA.TargetPage, target_page)


@given('target page is [{target_page}]')
def given__set_target_page(c, target_page: str):
    set_target_page(c, target_page)


@when('target page is [{target_page}]')
def when__set_target_page(c, target_page: str):
    set_target_page(c, target_page)