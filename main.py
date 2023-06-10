from fastapi import FastAPI, HTTPException, Form
import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError
from pydantic import BaseSettings


class Settings(BaseSettings):
    mailchimp_api_key: str
    mailchimp_server_prefix: str
    mailchimp_list_id: str


settings = Settings()
app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/subscribe")
async def subscribe(email_address: str = Form(...)):
    """
    important! if user was permanently deleted (not archived or not unsubscribed) this will not work!
    user will have to manually fill the form at http://eepurl.com/bhD_0r
    :param email_address:
    :return:
    """
    try:
        client = MailchimpMarketing.Client()
        client.set_config(
            {
                "api_key": settings.mailchimp_api_key,
                "server": settings.mailchimp_server_prefix,
            }
        )
        # response = client.ping.get()
        response = client.lists.batch_list_members(
            settings.mailchimp_list_id,
            {
                "members": [{"email_address": email_address, "status": "subscribed"}],
                "update_existing": True,
            },
        )

        if "error_count" in response and response["error_count"]:
            if response["error_count"] == 1:
                # We know how to handle only one error. otherwise, resort to default which we just proxy the errors
                if (
                    "errors" in response
                    and "error_code" in response["errors"][0]
                    and response["errors"][0]["error_code"] == "ERROR_CONTACT_EXISTS"
                ):
                    raise HTTPException(
                        status_code=400,
                        detail={
                            "email_address": response["errors"][0]["email_address"],
                            "error_code": "ALREADY_SUBSCRIBED",
                        },
                    )

            raise HTTPException(status_code=500, detail=response["errors"])

        # if not exist or user archived - it should be "created".
        # if already subscribed or unsubscribed - it should be "updated"
        # data is in response["new_members"] or response["updated_members"]
        if not response["total_created"] and not response["total_updated"]:
            raise HTTPException(
                status_code=500,
                detail={
                    "email_address": email_address,
                    "error_code": "UNEXPECTED",
                },
            )

        return {"detail": {"email_address": email_address}}
    except ApiClientError as error:
        print(error)
        raise
