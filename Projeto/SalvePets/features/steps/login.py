from behave import *

@given('que o usuario insira e-mail e senha corretos')
def step(context):
    context.browser.get('http://127.0.0.1:8000/pt-br/accounts/login/')
    #context.browser.find_element_by_id('id_login').send_keys('salvepets_superuser')
    #context.browser.find_element_by_id('id_password').send_keys('salve123456')
    context.browser.find_element_by_id('id_login').send_keys('123')
    context.browser.find_element_by_id('id_password').send_keys('123')

@when('ele tenta logar no sistema')
def step(context):
    context.browser.find_element_by_id('id_password').submit()

@then('sistema apresenta a tela inicial')
def step(context):
    assert context.failed is False