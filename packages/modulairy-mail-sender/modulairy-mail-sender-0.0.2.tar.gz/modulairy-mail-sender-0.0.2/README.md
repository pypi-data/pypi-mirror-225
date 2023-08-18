## Modulairy Mail Sender

This script enables sending emails asynchronously from Azure Service Bus. Each bus message contains a sender's email address along with SMTP configurations. The script utilizes its SMTP configuration of the message for sending emails.

### Parameters (OS Environments)
|Name| Description|
|-- |-- |
|SERVICEBUS_CONNECTION_STR| Connection String for your Azure service bus instance |
|SERVICEBUS_QUEUE_NAME| Queue name for email listening. |


### Model
```json
{
    "sender":"<Your Mail Address>",
    "receiver":"<Recevier Address>",
    "bcc":"<BCC Address>",
    "cc":"<CC Address>",
    "subject":"test",
    "message":"<This is a <strong>TEST</strong> mail.",
    "smtp":{
        "server":"<SMTP Server Host>",
        "port":"<SMTP Server PORT>",
        "username":"<Your Mail Address>",
        "password":"<Your Mail Password>"
    }

}
```
### Installation

```sh
pip install modulairy-mail-sender
```

### Run

```sh
python -m modulairy-mail-sender
```

> **NOTE:** If you send email to multiple addresses, you can join with a comma(,) these mail addresses
