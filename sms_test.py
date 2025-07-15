from android_sms_gateway import client, domain
from android_sms_gateway.enums import WebhookEvent
from android_sms_gateway.http import RequestsHttpClient
from random import choice

message = domain.Message(
    choice(["Je t'aime", "Je t'aime fort", "Je t'aime plus que tout", "Je t'aime plus que tout au monde", "Je t'aime ❤️"]),
    ["+33784540823"],
)


def sync_client():
    with RequestsHttpClient() as h, client.APIClient(
            "sms",
            "MySyperPasswordTooProtected",
            base_url="http://192.168.0.28:8080/",

            # "O0D56V",
            # "bsbxczwzty89ma",
            # base_url="https://api.sms-gate.app/3rdparty/v1",
        http=h,
    ) as c:
        state = c.send(message)
        print(state)

        state = c.get_state(state.id)
        print(state)


if __name__ == '__main__':
    sync_client()
