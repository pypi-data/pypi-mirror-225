import html
import ladok3
import re

class LadokSession(ladok3.LadokSession):
  def __init__(self, username, password, test_environment=False):
    """Initialize KTH version of LadokSession"""
    super().__init__(test_environment=test_environment)
    self.__username = username
    self.__password = password

  def ladok_run_shib_login(self, url):
    response = self.session.get(
      url=url+'&entityID=https://saml.sys.kth.se/idp/shibboleth')
            
    action = re.search(
      '<form ?[^>]* action="(.*?)"',
      response.text).group(1)

    csrf_token = re.search(
      '<input ?[^>]* name="csrf_token" ?[^>]* value="(.*?)"',
      response.text).group(1)

    post_data = {
      'csrf_token': csrf_token,
      'shib_idp_ls_exception.shib_idp_session_ss': '',
      'shib_idp_ls_success.shib_idp_session_ss': 'true',
      'shib_idp_ls_value.shib_idp_session_ss': '',
      'shib_idp_ls_exception.shib_idp_persistent_ss': '',
      'shib_idp_ls_success.shib_idp_persistent_ss': 'true',
      'shib_idp_ls_value.shib_idp_persistent_ss': '',
      'shib_idp_ls_supported': 'true',
      '_eventId_proceed': ''
    }

    response = self.session.post(
      url="https://saml-5.sys.kth.se" + action,
      data=post_data)

    return response
  def ug_post_user_pass(self, shib_response):
    action = re.search('<form ?[^>]* id="loginForm" ?[^>]* action="(.*?)"',
      shib_response.text).group(1)

    post_data = {
      'username': self.__username if "@" in self.__username \
                                  else self.__username + "@ug.kth.se",
      'password': self.__password,
      'Kmsi': True,
      'AuthMethod': "FormsAuthentication"
    }

    response = self.session.post(
      url='https://login.ug.kth.se' + action,
      data=post_data)

    return response
  def perform_redirects_back_to_ladok(self, ug_response):
    action = re.search('<form ?[^>]* action="(.*?)"',
      ug_response.text)
    if action is None:
      raise Exception('Invalid username or password OR possibly the SAML \
        configuration has changed, manually login an accept the changed \
        information.')
    action = html.unescape(action.group(1))

    relay_state = re.search(
      '<input ?[^>]* name="RelayState" ?[^>]* value="(.*?)"',
      ug_response.text)
    try:
      relay_state = html.unescape(relay_state.group(1))
    except AttributeError:
      raise Exception(
        "Try to log in using a web browser and accept sharing data.")

    saml_response = re.search(
      '<input ?[^>]* name="SAMLResponse" ?[^>]* value="(.*?)"',
      ug_response.text)
    saml_response = html.unescape(saml_response.group(1))

    post_data = {
        'RelayState': relay_state,
        'SAMLResponse': saml_response
    }

    response = self.session.post(url=action, data=post_data)

    ladok_action = re.search(
      '<form ?[^>]* action="(.*?)"',
      response.text)
    ladok_action = html.unescape(ladok_action.group(1))

    relay_state = re.search(
      '<input ?[^>]* name="RelayState" ?[^>]* value="([^"]+)"',
      response.text)
    relay_state = html.unescape(relay_state.group(1))

    saml_response = re.search(
      '<input ?[^>]* name="SAMLResponse" ?[^>]* value="(.*?)"',
      response.text)
    saml_response = html.unescape(saml_response.group(1))

    post_data = {
        'RelayState': relay_state,
        'SAMLResponse': saml_response
    }

    response = self.session.post(url=ladok_action, data=post_data)

    return response

  def saml_login(self, url):
    """Do the SSO login"""
    response = self.ladok_run_shib_login(url)
    response = self.ug_post_user_pass(response)
    response = self.perform_redirects_back_to_ladok(response)
    return response
