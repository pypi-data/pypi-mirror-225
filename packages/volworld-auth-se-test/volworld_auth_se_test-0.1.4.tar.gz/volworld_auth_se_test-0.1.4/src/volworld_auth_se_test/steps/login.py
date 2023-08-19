from behave import *
from volworld_aws_api_common.test.behave.selenium_utils import w__click_element_by_dom_id, \
    w__get_element_by_shown_dom_id, w__assert_element_not_existing, w__assert_page_id

from api.A import A
from api.PageId import PageId


@then('[19E_Login-Page] is shown')
def then_19e_login_page_is_shown(context):
    w__assert_page_id(context, PageId.Auth_LoginPage)


@then('{user} is successfully login')
def then_user_is_successfully_login(c, user: str):
    w__assert_element_not_existing(c, [A.Ok])


@then('[wrong password] message is NOT displayed')
def then_wrong_password_message_is_not_displayed(context):
    w__assert_element_not_existing(context, [A.Password, 'helper', 'text'])


@then('[wrong password] message is displayed')
def then_wrong_password_message_is_displayed(context):
    elm = w__get_element_by_shown_dom_id(context, [A.Password, 'helper', 'text'])
    err_msg = elm.text
    print('err_msg = ', err_msg)
    assert 'Wrong password' in err_msg, f"err_msg = {err_msg}"


@then('[user not existing] message is NOT displayed')
def then_user_not_existing_message_is_not_displayed(context):
    w__assert_element_not_existing(context, [A.Name, 'helper', 'text'])


@then('[user not existing] message is displayed')
def then_user_not_existing_message_is_displayed(context):
    elm = w__get_element_by_shown_dom_id(context, [A.Name, 'helper', 'text'])
    err_msg = elm.text
    print('err_msg = ', err_msg)
    assert 'User name is not existing' in err_msg, f"err_msg = {err_msg}"


@when('{user} click on [signup button]')
def when_click_on_signup_button(context, user: str):
    w__click_element_by_dom_id(context, [A.Signup, A.Button])

