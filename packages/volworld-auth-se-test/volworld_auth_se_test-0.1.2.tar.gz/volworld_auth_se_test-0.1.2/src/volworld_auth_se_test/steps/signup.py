from behave import *
from volworld_aws_api_common.api.FrontEndUrl import FrontEndUrl
from volworld_aws_api_common.test.ProjectMode import ProjectMode
from volworld_aws_api_common.test.behave.selenium_utils import w__click_element_by_dom_id, \
    w__get_element_by_shown_dom_id, w__key_in_element_by_dom_id, w__assert_element_not_existing, assert_page_id
from volworld_common.test.behave.BehaveUtil import BehaveUtil

from api.PageId import PageId

from api.A import A


@then('[13E_Signup-Page] is shown')
def then_13e_signup_page_is_shown(context):
    assert_page_id(context, PageId.Auth_SignupPage)


@when('{user} click on [Login-Button]')
def when_click_on_login_button(context, user: str):
    w__click_element_by_dom_id(context, [A.Login])


@when('{user} key in {name} in [Name-TextField]')
def when_key_in_name(context, user: str, name: str):
    w__key_in_element_by_dom_id(context, [A.Name], BehaveUtil.clear_string(name))


@when('{user} key in {password} in [Password-TextField]')
def when_key_in_password(context, user: str, password: str):
    w__key_in_element_by_dom_id(context, [A.Password], BehaveUtil.clear_string(password))


@when('{user} key in {password} in [Confirm-Password-TextField]')
def when_key_in_confirm_password(context, user: str, password: str):
    w__key_in_element_by_dom_id(context, [A.Confirm, A.Password], BehaveUtil.clear_string(password))


@then('{name} is showing in [Name-TextField]')
def then_showing_signup_name(context, name: str):
    name = BehaveUtil.clear_string(name)
    elm = w__get_element_by_shown_dom_id(context, [A.Name])
    assert elm is not None
    curr_name = elm.get_attribute('value')
    assert curr_name == name, f"curr_name = {curr_name} != {name}"


@then('[Wrong name format] message is displayed')
def then_wrong_name_format_message_is_displayed(context):
    elm = w__get_element_by_shown_dom_id(context, [A.Name, 'helper', 'text'])
    err_msg = elm.text
    print('err_msg = ', err_msg)
    assert 'Please enter a name using only English alphabets and numbers' in err_msg, f"err_msg = {err_msg}"


@then('[User name is taken] message is displayed')
def then_user_name_is_taken_message_is_displayed(context):
    elm = w__get_element_by_shown_dom_id(context, [A.Name, 'helper', 'text'])
    err_msg = elm.text
    print('err_msg = ', err_msg)
    assert 'User name is taken.' in err_msg, f"err_msg = {err_msg}"


@then('[Wrong name format] message is NOT displayed')
def then_wrong_name_format_message_is_not_displayed(context):
    w__assert_element_not_existing(context, [A.Name, 'helper', 'text'])


@then('[Too short password] message is displayed')
def then_too_short_password_message_is_displayed(context):
    elm = w__get_element_by_shown_dom_id(context, [A.Password, 'helper', 'text'])
    err_msg = elm.text
    print('err_msg = ', err_msg)
    assert 'Password should be minimum 6 characters' in err_msg, f"err_msg = {err_msg}"


@then('[Too short password] message is NOT displayed')
def then_too_short_password_message_is_not_displayed(context):
    w__assert_element_not_existing(context, [A.Password, 'helper', 'text'])


@then('[Mismatched password] message is displayed')
def then_mismatched_password_message_is_displayed(context):
    elm = w__get_element_by_shown_dom_id(context, [A.Confirm, A.Password, 'helper', 'text'])
    err_msg = elm.text
    print('err_msg = ', err_msg)
    assert 'Password do not match' in err_msg, f"err_msg = {err_msg}"


@then('[Mismatched password] message is NOT displayed')
def then_mismatched_password_message_is_not_displayed(context):
    w__assert_element_not_existing(context, [A.Confirm, A.Password, 'helper', 'text'])