import traceback
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from e_invoice_app.models import UserDetails
from e_invoice_app.user_serializers import UserSerializers
import requests
import datetime
import json
import jwt
import base64
import json
import logging


def make_get_request(email,username,password,ip_address,gst):
    if gst == "29AABCT1332L000":
        client_id = 'ee0bf797-6a63-42de-9328-2a4419b0eb98',
        client_secret = 'af0a5cf6-7c21-4f19-a4ed-2ba5659f2e35',
    else:
        client_id = '5fc139ba-7548-48d8-91c2-2637811f7bcb',
        client_secret = '469c03ca-d9c5-4156-86b6-c156c4315439',
  
    url = f"https://api.mastergst.com/einvoice/authenticate/?email={email}"
    headers = {
        'username': username,
        'password': password,
        'ip_address': ip_address,
        'client_id': client_id[0],
        'client_secret': client_secret[0],
        'gstin': gst
    }
    response = requests.get(url, headers=headers)
    return response

def make_post_request(email, authToken, data, username, password, ip_address, gst):

    if gst == "29AABCT1332L000":
        client_id = 'ee0bf797-6a63-42de-9328-2a4419b0eb98',
        client_secret = 'af0a5cf6-7c21-4f19-a4ed-2ba5659f2e35',
    else:
        client_id = '5fc139ba-7548-48d8-91c2-2637811f7bcb',
        client_secret = '469c03ca-d9c5-4156-86b6-c156c4315439',
    
    url = f"https://api.mastergst.com/einvoice/type/GENERATE/version/V1_03/?email={email}"
    headers = {
        'username': username,
        'password': password,
        'ip_address': ip_address,
        'client_id': client_id[0],
        'client_secret': client_secret[0],
        'gstin': gst,
        'auth-token': authToken
    }
    response = requests.post(url, headers=headers, json=data)
    return response 

def UpdateAPIRequest(authToken, update ,email, username, update_ipaddress, update_Gstin):

    if update_Gstin == "29AABCT1332L000":
        client_id = 'ee0bf797-6a63-42de-9328-2a4419b0eb98',
        client_secret = 'af0a5cf6-7c21-4f19-a4ed-2ba5659f2e35',
    else:
        client_id = '5fc139ba-7548-48d8-91c2-2637811f7bcb',
        client_secret = '469c03ca-d9c5-4156-86b6-c156c4315439',

    url = f"https://api.mastergst.com/einvoice/type/CANCEL/version/V1_03/?email={email}"
    headers = {
        'username': username,
        'ip_address': update_ipaddress,
        'client_id': client_id[0],
        'client_secret': client_secret[0],
        'gstin': update_Gstin,
        'auth-token': authToken,
    }
    response = requests.post(url, headers=headers, json=update)
    return response 

def Irn_get_request(authToken, Irn, email, username, irn_ipaddress, irn_Gstin):

    if irn_Gstin == "29AABCT1332L000":
        client_id = 'ee0bf797-6a63-42de-9328-2a4419b0eb98',
        client_secret = 'af0a5cf6-7c21-4f19-a4ed-2ba5659f2e35',
    else:
        client_id = '5fc139ba-7548-48d8-91c2-2637811f7bcb',
        client_secret = '469c03ca-d9c5-4156-86b6-c156c4315439',

    url = f"https://api.mastergst.com/einvoice/type/GETIRN/version/V1_03/?param1={Irn}&email={email}"
    headers = {
        'username': username,
        'ip_address': irn_ipaddress,
        'client_id': client_id[0],
        'client_secret': client_secret[0],
        'gstin': irn_Gstin,
        'auth-token': authToken,
    }
    response = requests.get(url, headers=headers)
    return response

success_logger = logging.getLogger('success_logger')
error_logger = logging.getLogger('error_logger')

class E_invoice(APIView):
    permission_classes = (AllowAny, )

    def post(self, request):
        try:

            data1 = request.data
            authToken = None
            # queryParams = [
            #     {
            #         'gst': '29AABCT1332L000',
            #         'email': 'saravanan@pganalytics.in',
            #         'username': 'mastergst',
            #         'password': 'Malli#123',
            #         'date': '10-11-2023',
            #     },
            #     {
            #         'gst': '33AQAPP7817N1ZG',
            #         'email': 'saravanan@pganalytics.in',
            #         'username': 'API_pga_pandiarajan',
            #         'password': 'PGA@tera2023',
            #         'date': '10-11-2023',
            #     },
            # ]
            
            today_date = datetime.date.today()
            response = requests.get('https://ipinfo.io')
            data = response.json()
            public_ip = data.get('ip')

            all_responses = []
            if isinstance(data1, list):
                for data in data1:
                    sellerGstin = data.get('SellerDtls', {}).get('Gstin')
                    gst = sellerGstin or 'default_value'
                    user = UserDetails.objects.filter(gst=gst)
                    queryParams = UserSerializers(user, many = True).data

                email = 'saravanan@pganalytics.in'
                Gstin = queryParams[0]['gst']
                username = queryParams[0]['username']
                password = queryParams[0]['password']
                date = queryParams[0]['date']
                date1 = datetime.datetime.strptime(date, '%d-%m-%Y').date()
                days_difference = (date1 - today_date).days
            
                for data in data1:   
                    sellerGstin = data.get('SellerDtls', {}).get('Gstin')
                    gst = sellerGstin or 'default_value'
                    if gst == queryParams[0]['gst']:
                        if days_difference == 0 or days_difference > 0:
                            ip_address = public_ip
                            Gstin = sellerGstin
                            response = make_get_request(email, username, password, ip_address, gst)
                            if response.status_code == 200:
                                auth_token = response.json().get('data', {}).get('AuthToken')
                                response_data = make_post_request(email, auth_token, data, username, password, ip_address, gst)
                                all_responses.append(response_data.json())
                            else:
                                error_logger.error("Error occurred: Contact PG Analytics Team - Status Code: %s", response_data.status_code)
                                return Response({'result':'Contact PG Analytics Team'},status = status.HTTP_400_BAD_REQUEST) 
                        else:
                            error_logger.error("Error occurred: Subscription Error - Status Code: %s", status.HTTP_400_BAD_REQUEST)
                            return Response({'result': 'Subscription Error'}, status = status.HTTP_400_BAD_REQUEST)
                    else:
                        error_logger.error("Error occurred: Invalid Gstin - Status Code: %s", status.HTTP_400_BAD_REQUEST)
                        return Response({'result':'Invalid Gstin'},status = status.HTTP_400_BAD_REQUEST)   
                            
                if response_data.status_code == 200:
                    final_reaponce = []
                    for decode in all_responses:
                        if decode['status_cd'] == "0":
                            error_messages = json.loads(decode['status_desc'])
                            error_logger.error("Error occurred: %s - Status Code: %s", error_messages[0]['ErrorMessage'], response_data.status_code)
                            final_reaponce.extend(error_messages) 
                        else:
                            signed_invoice = decode['data']['SignedInvoice']
                            parts = signed_invoice.split(".")
                            payload = base64.urlsafe_b64decode(parts[1] + "===")
                            payload_data = json.loads(payload)
                            data_res = json.loads(payload_data['data'])
                            decode['data']['SignedInvoice'] = data_res
                            final_reaponce.append(decode)
                    success_logger.info("Request processed successfully")
                    return Response({'result' : final_reaponce}) 
                else:
                    error_logger.error("Error occurred: Contact PG Analytics Team - Status Code: %s", response_data.status_code)
                    return Response({'result':'Contact PG Analytics Team'},status = status.HTTP_400_BAD_REQUEST)
                            
            else:   
                updateGstin = data1.get('update', {}).get('Gstin')
                IrnGstin = data1.get('IRN', {}).get('Gstin')
                gst = updateGstin or IrnGstin or 'default_value'
                user = UserDetails.objects.filter(gst=gst)
                queryParams = UserSerializers(user, many = True).data

                email = 'saravanan@pganalytics.in'
                Gstin = queryParams[0]['gst']
                username = queryParams[0]['username']
                password = queryParams[0]['password']
                date = queryParams[0]['date']
                date1 = datetime.datetime.strptime(date, '%d-%m-%Y').date()
                days_difference = (date1 - today_date).days
    
                gst = updateGstin or IrnGstin or Gstin or 'default_value'
                if gst == queryParams[0]['gst']:
                    if days_difference == 0 or days_difference > 0:
                        for key in data1:
                            if key == 'update':
                                update = data1['update']
                                update_Gstin = update.get('Gstin')
                                update_ipaddress = public_ip
                                cancel = {
                                    "CnlRsn": "1",
                                    "CnlRem": "Wrong entry"
                                }
                                data1["update"].update(cancel)
                                
                                if not gst or not authToken:
                                    responseData = make_get_request(email, username, password, update_ipaddress, update_Gstin)
                                    authToken = responseData.json().get('data', {}).get('AuthToken')
                                    response = UpdateAPIRequest(authToken, update, email, username, update_ipaddress, update_Gstin)
                                    response_value = response.json()
                                    if response.status_code == 200:
                                        if response_value['status_cd'] == "0":
                                            error_messages = json.loads(response_value['status_desc'])
                                            error_logger.error("Error occurred: %s - Status Code: %s", error_messages[0]['ErrorMessage'], response.status_code)
                                            return Response({'result' : error_messages[0]['ErrorMessage']})
                    
                                        else:
                                            success_logger.info("Request processed successfully")
                                            return Response({'result' : response_value})
                                    else:
                                        error_logger.error("Error occurred: Contact PG Analytics Team - Status Code: %s", response.status_code)
                                        return Response({'result':'Contact PG Analytics Team'},status = status.HTTP_400_BAD_REQUEST)

                            if key == 'IRN':
                                irn = data1['IRN']
                                irn_Gstin = irn.get('Gstin')
                                irn_ipaddress = public_ip
                                Irn = irn.get('Irn')
                                
                                if not gst or not authToken:
                                    responseData = make_get_request(email, username, password, irn_ipaddress, irn_Gstin)
                                    authToken = responseData.json().get('data', {}).get('AuthToken')
                                    response = Irn_get_request(authToken, Irn, email, username, irn_ipaddress, irn_Gstin)
                                    response_value = response.json()
                                    if response.status_code == 200:
                                        if response_value['status_cd'] == "0":
                                            error_messages = json.loads(response_value['status_desc'])
                                            error_logger.error("Error occurred: %s - Status Code: %s", error_messages[0]['ErrorMessage'], response.status_code)
                                            return Response({'result' : error_messages[0]['ErrorMessage']})
                                        else:
                                            signed_invoice = response_value['data']['SignedInvoice']
                                            parts = signed_invoice.split(".")
                                            payload = base64.urlsafe_b64decode(parts[1] + "===")
                                            payload_data = json.loads(payload)
                                            data_res = json.loads(payload_data['data'])
                                            response_value['data']['SignedInvoice'] = data_res
                                            success_logger.info("Request processed successfully")
                                            return Response({'result' : response_value})
                                    else:
                                        error_logger.error("Error occurred: Contact PG Analytics Team - Status Code: %s", response.status_code)
                                        return Response({'result':'Contact PG Analytics Team'},status = status.HTTP_400_BAD_REQUEST)
                    else:
                        error_logger.error("Error occurred: Subscription Error - Status Code: %s", status.HTTP_400_BAD_REQUEST)
                        return Response({'result': 'Subscription Error'}, status = status.HTTP_400_BAD_REQUEST)
                else:
                    error_logger.error("Error occurred: Invalid Gstin - Status Code: %s", status.HTTP_400_BAD_REQUEST)
                    return Response({'result':'Invalid Gstin'},status = status.HTTP_400_BAD_REQUEST)                  
        
        except Exception as e:
            # error_logger.error("An unhandled exception occurred: %s", traceback.format_exc())
            error_logger.error(f"{error_message} - Status Code: {status.HTTP_400_BAD_REQUEST}, Error: {str(e)}")
            error_message = str(e)
            traceback_details = traceback.format_exc()
            if error_message == 'list index out of range':
                error_logger.error("Error occurred: Invalid Gstin - Status Code: %s", status.HTTP_400_BAD_REQUEST)
                return Response({'result':'Invalid Gstin'},status = status.HTTP_400_BAD_REQUEST)
            return Response(traceback.format_exc(), status = status.HTTP_400_BAD_REQUEST)