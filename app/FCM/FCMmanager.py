import firebase_admin
from firebase_admin import credentials, messaging
from firebase_admin.messaging import QuotaExceededError,\
    SenderIdMismatchError, ThirdPartyAuthError, UnregisteredError

cred = credentials.Certificate("/code/app/FCM/serviceAccountKey.json")
firebase_admin.initialize_app(cred)


def sendpush(title, msg, registration_tokens, dataObject=None):
    try:
        message = messaging.MulticastMessage(
            notification=messaging.Notification(
                title=title,
                body=msg,
            ),
            data=dataObject,
            tokens=registration_tokens
        )
        response = messaging.send_multicast(message)
        print("send message response", response)
    except QuotaExceededError as e:
        return f'QuotaExceededError: {e}'
    except SenderIdMismatchError as e:
        return f'SenderIdMismatchError: {e}'
    except ThirdPartyAuthError as e:
        return f'ThirdPartyAuthError: {e}'
    except UnregisteredError as e:
        return f'UnregisteredError: {e}'
    except Exception as e:
        return f'Exception: {e}'
