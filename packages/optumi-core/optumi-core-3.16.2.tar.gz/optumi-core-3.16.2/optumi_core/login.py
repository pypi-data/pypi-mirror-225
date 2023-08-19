##
## Copyright (C) Optumi Inc - All rights reserved.
##
## You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
## To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
##

from ._version import __version__
from .logging import optumi_format_and_log
from .sessions import get_session, get_mode
from .exceptions import NotLoggedInException, VersionIncompatibility
from .utils import dev_version, get_portal_domain_and_port, get_portal_port


## Standard library imports

# Generic Operating System Services
import time, os
from pathlib import Path
from datetime import datetime
from dateutil import parser

# Python Runtime Services
import traceback

# Concurrent execution
from threading import Lock

# Internet Protocols and Support
from requests.exceptions import HTTPError, ConnectionError, Timeout
from urllib.parse import urlparse

# Internet Data Handling
import json

## Other imports
# from cryptography import x509
# from cryptography.hazmat.backends import default_backend
from pathlib import Path
import pickle

lock = Lock()
loginProgress = None


def get_cookie_file():
    COOKIE_FILE = os.path.expanduser("~") + "/.optumi/" + get_mode() + "_cookies.pickle"
    os.makedirs(Path(COOKIE_FILE).parent, exist_ok=True)
    return COOKIE_FILE


def get_token_file():
    TOKEN_FILE = os.path.expanduser("~") + "/.optumi/" + get_mode() + "_token"
    os.makedirs(Path(TOKEN_FILE).parent, exist_ok=True)
    return TOKEN_FILE


def get_login_progress():
    try:
        lock.acquire()
        return loginProgress
    except:
        pass
    finally:
        lock.release()


def set_login_progress(message):
    global loginProgress
    try:
        lock.acquire()
        loginProgress = message
    except:
        pass
    finally:
        lock.release()


def sign_agreement(timeOfSigning, hashOfSignedAgreement):
    URL = "/exp/jupyterlab/sign-agreement"
    try:
        return get_session().post(
            URL,
            data={
                "timeOfSigning": timeOfSigning,
                "hashOfSignedAgreement": hashOfSignedAgreement,
            },
            timeout=30,
        )
    except HTTPError as e:
        return e


def get_new_agreement():
    URL = "/exp/jupyterlab/get-new-agreement"
    try:
        return get_session().get(URL, timeout=30)
    except HTTPError as e:
        return e


def exchange_versions(version):
    URL = "/exp/jupyterlab/exchange-versions"
    try:
        return get_session().post(
            URL,
            data={
                "version": version,
            },
            timeout=30,
        )
    except HTTPError as e:
        return e


def get_redirect():
    try:
        # Load cookies from the disk
        COOKIE_FILE = get_cookie_file()

        if os.path.exists(COOKIE_FILE):
            with open(COOKIE_FILE, "rb") as f:
                get_session().cookies.update(pickle.load(f))
                # if dev_version:
                #     print("reading", get_mode(), "cookies:")
                now = time.time()
                for cookie in get_session().cookies:
                    if cookie.expires != None and cookie.expires - now < 0:
                        # if dev_version:
                        #     print(
                        #         "Clearing",
                        #         cookie.name,
                        #         cookie.value,
                        #         cookie.domain,
                        #         cookie.expires,
                        #     )
                        get_session().cookies.clear(cookie.domain)
                # if dev_version:
                #     for cookie in get_session().cookies:
                #         print(cookie.name, cookie.value, cookie.domain, cookie.expires)
    except Exception as err:
        # pass
        print(err)

    URL = "/exp/jupyterlab/get-redirect"
    try:
        return get_session().get(URL, timeout=30)
    except HTTPError as e:
        return e


# We can remove login_domain and login_port when we switch to 3.17
def check_login(login_domain=None, login_port=None):
    session = get_session()
    domain_and_port = session._domain_and_port[-1]
    try:
        response = get_redirect()
        if response.url.endswith("/login"):
            session._domain_and_port = [get_portal_domain_and_port()]
            return False
        redirect = json.loads(response.text)
        if redirect == {}:
            # If we are talking to a portal controller, we are not logged in (because we have no assigned station)
            if domain_and_port == get_portal_domain_and_port():
                return False
            return True
        elif "dnsName" in redirect and "port" in redirect:
            redirect_domain_and_port = redirect["dnsName"] + ":" + str(redirect["port"])
            if session._domain_and_port[-1] != redirect_domain_and_port:
                session._domain_and_port.append(redirect_domain_and_port)
            if domain_and_port == redirect_domain_and_port:
                return True
            else:
                return check_login()
        session._domain_and_port = [get_portal_domain_and_port()]
        return False
    except (HTTPError, NotLoggedInException) as e:
        session._domain_and_port = [get_portal_domain_and_port()]
        return False


# We can remove login_domain and login_port when we switch to 3.17
def login_rest_server(
    login_domain=None,
    login_port=None,
    token=None,
    login_type="oauth",
    save_token=False,
):
    session = get_session()
    try:
        if check_login():
            return 1, get_session()._domain_and_port[-1]

        start_time = None
        last_domain_and_port = None
        while True:
            if start_time == None:
                start_time = time.time()
            elif time.time() - start_time > 600:  # 10 minute timeout
                session._domain_and_port = [get_portal_domain_and_port()]
                return -1, "Timed out"
            # If we want to move back to using a devserver certificate we need to check for devserver.optumi.com explicitly
            # Since we are bypassing the hostname check for the SSL context, we manually check it here
            # cert = ssl.get_server_certificate((DOMAIN, 8443))
            # cert = x509.load_pem_x509_certificate(cert.encode(), default_backend())
            # name = cert.subject.get_attributes_for_oid(x509.oid.NameOID.COMMON_NAME)[0].value
            # if name != 'devserver.optumi.com':
            #     raise ssl.SSLCertVerificationError("SSL domain check failed (" + name + " is not devserver.optumi.com)")

            URL = "/login"

            # We only want to print to the log when we try to contact somewhere new
            if session._domain_and_port[-1] != last_domain_and_port:
                if dev_version:
                    print(optumi_format_and_log(None, "Contacting " + session._domain_and_port[-1] + URL))
                else:
                    optumi_format_and_log(None, "Contacting " + session._domain_and_port[-1] + URL)

            last_domain_and_port = session._domain_and_port[-1]

            # since it can take a long time to log in to actually log in to the station, set a longer timeout for that request
            timeout = (
                30
                if session._domain_and_port[-1] == get_portal_domain_and_port() or session._domain_and_port[-1] == "portal.optumi.net:" + str(get_portal_port())
                else 120
            )

            if login_type == "token" and token is None:
                # Try to load the token from the disk
                TOKEN_FILE = get_token_file()

                if os.path.exists(TOKEN_FILE):
                    with open(TOKEN_FILE, "r") as f:
                        token = f.read()
                else:
                    session._domain_and_port = [get_portal_domain_and_port()]
                    return -1, "No login token"

            try:
                response = session.post(
                    URL,
                    data={"login_type": login_type, "username": "", "password": token},
                    timeout=timeout,
                )
            except Timeout as err:
                return -1, "Timed out"
            except ConnectionError as err:
                time.sleep(2)
                continue

            parsed = urlparse(response.url)

            redirect = None
            try:
                redirect = json.loads(response.text)
            except:
                pass

            if redirect != None:
                if redirect["dnsName"] == "unknown":
                    set_login_progress("Allocating...")
                    time.sleep(2)
                    continue
                elif redirect["dnsName"] == "no more stations" or redirect["dnsName"] == "no more trial stations":
                    session._domain_and_port = [get_portal_domain_and_port()]
                    return -1, redirect["dnsName"]
                else:
                    set_login_progress("Restoring context...")
                    session._domain_and_port.append(redirect["dnsName"] + ":" + str(redirect["port"]))
                    continue

            if parsed.path == "/login" and parsed.query == "error":
                # Parse the error message to pass on to the user
                raw_html = response.text
                try:
                    message = raw_html.split('<div class="alert alert-danger" role="alert">')[1].split("</div>")[0]
                except:
                    message = "Invalid username/password"

                session._domain_and_port = [get_portal_domain_and_port()]
                return -1, message

            ## This is currently necessary in order for the controller to recognize that the user has signed the agreement
            get_new_agreement()

            # make sure we have a compatible version
            try:
                exchange_versions(__version__)
            except VersionIncompatibility as err:
                return -2, err._controller_version

            # Save cookies to the disk
            try:
                # Load cookies from the disk
                COOKIE_FILE = get_cookie_file()

                with open(COOKIE_FILE, "wb") as f:
                    # if dev_version:
                    #     print("Writing", get_mode(), "cookies:")
                    #     for cookie in get_session().cookies:
                    #         print(
                    #             cookie.name, cookie.value, cookie.domain, cookie.expires
                    #         )
                    pickle.dump(get_session().cookies, f)
                    os.chmod(COOKIE_FILE, 0o600)
            except Exception as err:
                # pass
                print(err)

            if save_token:
                TOKEN_FILE = get_token_file()

                existing_token = None
                if os.path.exists(TOKEN_FILE):
                    with open(TOKEN_FILE, "r") as f:
                        existing_token = f.read()

                # Get a token and save it on the disk so the user will stay logged in
                if login_type != "token":
                    from .core import get_connection_token  # Avoid circular import

                    response = json.loads(get_connection_token(False).text)
                    expiration = None if response["expiration"] is None else parser.parse(response["expiration"])
                    if expiration is None or expiration < parser.parse(datetime.utcnow().isoformat() + "Z"):
                        response = json.loads(get_connection_token(True).text)
                    token = response["token"]

                if existing_token != token:
                    print("Saving connection token to", TOKEN_FILE)
                    with open(TOKEN_FILE, "w+") as f:
                        f.write(token)

                    os.chmod(TOKEN_FILE, 0o600)

            # On success return the status value 1 and the domain that we logged in to
            return 1, session._domain_and_port[-1]
    except Exception as err:
        print(optumi_format_and_log(None, str(err)))
        traceback.print_exc()
        session._domain_and_port = [get_portal_domain_and_port()]
        return -3, ""


def logout(remove_token=True):
    try:
        if remove_token:
            TOKEN_FILE = get_token_file()
            try:
                os.remove(TOKEN_FILE)
                print("Removed connection token")
            except OSError:
                pass
        # Silently remove cookies
        COOKIE_FILE = get_cookie_file()
        try:
            os.remove(COOKIE_FILE)
        except OSError:
            pass
        get_session().logout()
    except HTTPError as e:
        return e
