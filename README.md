# Important
The timestamp saved is assumed as UTC+8 (Asia / Singapore).

# Requirements
1. Anaconda or Miniconda
2. PostgreSQL
3. redis-server
4. An email for sending email.

# Setup
1. Install environment ```conda env create -f environment.yml```.
2. ```conda activate jublia```.
3. Create ```.env``` & ```.env.test``` file as in ```.env.example```. 
4. Initialize alembic and migrate database.
```
FLASK_APP=run.py flask db init
FLASK_APP=run.py flask db migrate
FLASK_APP=run.py flask db upgrade
```
5. Run ```python run.py```
6. Open new terminal and get to the project root directory. Then run rq worker. Example: ```rq worker --url redis://127.0.0.1:6379/0 --with-scheduler```

# Setup Test
1. Create a copy of the original database.
2. Create ```.env.test``` as in ```.env.test.example```.
3. Run ```python -m unittest discover -v -s app/tests/ -p "test_*.py"```

# API Docs

* ## /save_emails
    Used to  save email content.
    **URL**: /save_emails
    **Method**: POST
    **Data Requirements**
    ```
    {
        "event_id": [number, required],
        "email_subject": [string, required],
        "email_content": [string, required],
        "timestamp": [string, required]
    }
    ```
    **Data Example**
    ```
    {
        "event_id": 3,
        "email_subject": "Subject",
        "email_content": "Content",
        "timestamp": "13 Mar 2020 20:30"
    }
    ```
    ### Success Response
    **Status Code**: ```200```
    Example:
    ```
    {
        "data": {
            "email_content": "Лорем ипсум долор сит амет, но пер утинам луптатум адолесценс, яуо цонгуе алияуандо ид. Усу не новум утамур доцен",
            "email_subject": "😋 Лорем",
            "event_id": 3,
            "timestamp": "13 Mar 2022 20:30"
        },
        "message": "success",
        "status": "success",
        "status_code": 200
    }
    ```
    ### Error Response
    **Status Code**: ```422```
    Example:
    ```
    {
        "data": {
            "email_content": [
                "The email content field is required.",
                "The email content must be a string."
            ],
            "email_subject": [
                "The email subject field is required.",
                "The email subject must be a string."
            ],
            "event_id": [
                "The event id field is required.",
                "The event id must be an integer."
            ],
            "timestamp": [
                "The timestamp field is required.",
                "The timestamp is not a valid date."
            ]
        },
        "message": "validation_form_error",
        "status": "error",
        "status_code": 422
    }
    ```
    **Status Code**: ```500```
    Example:
    ```
    {
        "data": {},
        "message": "Internal Error",
        "status": "error",
        "status_code": 500
    }
    ```
    
* ## /save_recipient
    Used to email and event id of recipient.
    **URL**: /save_recipient
    **Method**: POST
    **Data Requirements**
    ```
    {
        "event_id": [number, required],
        "email_recipient": [string, required]
    }
    ```
    **Data Example**
    ```
    {
        "event_id": 3,
        "email_recipient": "recipient@email.com"
    }
    ```
    ### Success Response
    **Status Code**: ```200```
    Example:
    ```
    {
        "data": {
            "event_id": 3,
            "email_recipient": "recipient@email.com"
        },
        "message": "success",
        "status": "success",
        "status_code": 200
    }
    ```
    ### Error Response
    **Status Code**: ```422```
    Example:
    ```
    {
        "data": {
            "email_recipient": [
                "The email recipient field is required.",
                "The email recipient must be a string."
            ],
            "event_id": [
                "The event id field is required.",
                "The event id must be an integer."
            ]
        },
        "message": "validation_form_error",
        "status": "error",
        "status_code": 422
    }
    ```
    **Status Code**: ```500```
    Example:
    ```
    {
        "data": {},
        "message": "Internal Error",
        "status": "error",
        "status_code": 500
    }
    ```
* ## /manage_email
    Used to get list of email contents and delete email content to cancel sending email.
    **URL**: /manage_email
    **Method**: GET
    ### Success Response
    **Status Code**: ```200```
    Example:
    ```
    {
        "data": [
            {
                "email_content": "Content",
                "email_subject": "Subject",
                "event_id": 2,
                "id": 99,
                "timestamp": "2022-03-13T20:10:00"
            },
            {
                "email_content": "Content",
                "email_subject": "Subject",
                "event_id": 1,
                "id": 101,
                "timestamp": "2022-03-13T17:00:00"
            }
        ],
        "message": "success",
        "status": "success",
        "status_code": 200
    }
    ```
    ### Error Response
    **Status Code**: ```500```
    Example:
    ```
    {
        "data": {},
        "message": "Internal Error",
        "status": "error",
        "status_code": 500
    }
    ```
    **URL**: /manage_email?email_content_id=1
    **Query String**: ```email_content_id``` where ```email_content_id``` is id of email content in database.
    **Method**: DELETE
    ### Success Response
    **Status Code**: ```200```
    Example:
    ```
    {
        "data": {},
        "message": "success",
        "status": "success",
        "status_code": 200
    }
    ```
    ### Error Response
    **Status Code**: ```500```
    Example:
    ```
    {
        "data": {},
        "message": "Internal Error",
        "status": "error",
        "status_code": 500
    }
    ```