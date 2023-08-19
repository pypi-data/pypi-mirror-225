from behave import *
from volworld_aws_api_common.test.behave.selenium_utils import w__get_element_by_shown_dom_id, w__click_element_by_dom_id
from volworld_aws_api_common.api.AA import AA


@then('[Save-Button] is disabled')
def then_the_save_button_is_disabled(c):
    elm = w__get_element_by_shown_dom_id(c, [AA.Save])
    assert not elm.is_enabled()


@then('[Save-Button] is enabled')
def then_the_save_button_is_enabled(c):
    elm = w__get_element_by_shown_dom_id(c, [AA.Save])
    assert elm.is_enabled()


@when('{user} click on [Save-Button]')
def when_click_on_save_button(c, user: str):
    w__click_element_by_dom_id(c, [AA.Save])


@then('[Ok-Button] is disabled')
def then_the_ok_button_is_disabled(context):
    elm = w__get_element_by_shown_dom_id(context, [AA.Ok])
    assert not elm.is_enabled()


@then('[Ok-Button] is enabled')
def then_the_ok_button_is_enabled(context):
    elm = w__get_element_by_shown_dom_id(context, [AA.Ok])
    assert elm.is_enabled()


@when('{user} click on [Ok-Button]')
def when_click_on_ok_button(context, user: str):
    w__click_element_by_dom_id(context, [AA.Ok])