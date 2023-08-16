import requests
import json
from typing import Text
import logging

from wells_data_pipeline_cores.services.cores.az_ad_authz_service import AzAuthzService
from wells_data_pipeline_cores.commons import EnvVariables

class Body():
    def __init__(self, content, content_type:str="text/html"):     
        self.ContentType = content_type
        self.Content = content

class MailMessageRequest(): 
    def __init__(self, to_recipients:list[str], subject:str, body:Body, sender:str="no_reply@your_domain.com"):
        self.Subject = subject
        self.Body = body
        self.From = sender
        self.ToRecipients = to_recipients 

class SendEmailService():
    def __init__(self, env_vars:EnvVariables):
        self.env_vars = env_vars
        self.dbutils = env_vars.secret_utils.dbutils

        self.az_authz = AzAuthzService(env_vars=self.env_vars)

    def _get_mulsoft_smtp_api_access_token(self) -> Text:
        # Obation an Mule Soft SMTP API Token
        try:
            email_conf = self.env_vars.mulesoft_conf.get_email_conf()

            # Obtain an WV SDK access token using MSAL
            return self.az_authz.get_sp_access_token(
                client_id=email_conf.smtp_api_appid,
                client_credential=email_conf.smtp_api_appid_secret,
                tenant_name=self.env_vars.get_tenant_name(),
                scopes=[email_conf.smtp_api_scope],
            )
            
        except Exception as err:
            logging.error('_get_mulsoft_smtp_api_access_token() - Execution error: %s', err)
        
        return ""


    def send_smtp_email(self, to_recipients:list[str], subject:str, email_body:Body) -> bool:
        """ send smtp email by using MuleSoft API
        Return:
            - 200: if
        """
        try:
            email_conf = self.env_vars.mulesoft_conf.get_email_conf()

            access_token = self._get_mulsoft_smtp_api_access_token()
            
            headerToken = {"Authorization": "Bearer {}".format(access_token), 'Content-Type':'application/json'}
            
            # emailUrl = "https://mulesoft_email_api/external-smtp/v1/email"
            email_url = email_conf.smtp_api_host
            
            if not email_body:
                email_body = Body(content = "")
            
            mailMessageRequest = MailMessageRequest(to_recipients, subject, email_body)  
            
            email_json_content = json.dumps(mailMessageRequest.__dict__,default=lambda o: o.__dict__,indent=4)
            
            #print(jsonContent)
            
            result = requests.post(url=email_url, headers=headerToken, data=email_json_content)
            
            if result:
                return (result.status_code == 200 or result.status_code == 201)
        except Exception as err:
            logging.error('send_smtp_email() - Execution error: %s', err)

        return False

    def send_email(self, subject:str, email_content:str, to_recipients:list=[], email_content_type:str="text/html") -> bool:
        return self.send_smtp_email(
            to_recipients=to_recipients,
            subject=subject,
            email_body=Body(content=email_content, content_type=email_content_type)
            )
