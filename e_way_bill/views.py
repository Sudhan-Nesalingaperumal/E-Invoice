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
import logging
import json

def authtoken_request(email,username,password,ip_address,gst):

    if gst == "05AAACH6188F1ZM":
        client_id = '2a74277b-ef21-4ec5-9a05-b77c372affee',
        client_secret = '853d3aaa-4c7b-4914-bb2e-706b86f5093b',
    else:
        client_id = '652026ed-e3d0-44ea-9e6e-9f6665a4efd0',
        client_secret = 'ca10b200-87d7-4aa2-82c6-70c906313c5c',
    
    url = f"https://api.mastergst.com/ewaybillapi/v1.03/authenticate?email={email}&username={username}&password={password}"
    headers = {
        'ip_address': ip_address,
        'client_id': client_id[0],
        'client_secret': client_secret[0],
        'gstin': gst
    }
    response = requests.get(url, headers=headers)
    return response

def e_way_post_request(email, data, ip_address, gst):

    if gst == "05AAACH6188F1ZM":
        client_id = '2a74277b-ef21-4ec5-9a05-b77c372affee',
        client_secret = '853d3aaa-4c7b-4914-bb2e-706b86f5093b',
    else:
        client_id = '652026ed-e3d0-44ea-9e6e-9f6665a4efd0',
        client_secret = 'ca10b200-87d7-4aa2-82c6-70c906313c5c',

    url = f"https://api.mastergst.com/ewaybillapi/v1.03/ewayapi/genewaybill?email={email}"
    headers = {
        'ip_address': ip_address,
        'client_id': client_id[0],
        'client_secret': client_secret[0],
        'gstin': gst,
    }
    response = requests.post(url, headers=headers, json=data)
    return response 

def e_way_get_request(email, ewbNo, ewbNo_ipaddress, ewbNo_Gstin):

    if ewbNo_Gstin == "05AAACH6188F1ZM":
        client_id = '2a74277b-ef21-4ec5-9a05-b77c372affee',
        client_secret = '853d3aaa-4c7b-4914-bb2e-706b86f5093b',
    else:
        client_id = '652026ed-e3d0-44ea-9e6e-9f6665a4efd0',
        client_secret = 'ca10b200-87d7-4aa2-82c6-70c906313c5c',
    
    url = f"https://api.mastergst.com/ewaybillapi/v1.03/ewayapi/getewaybill?email={email}&ewbNo={ewbNo}"
    headers = {
        'ip_address': ewbNo_ipaddress,
        'client_id': client_id[0],
        'client_secret': client_secret[0],
        'gstin': ewbNo_Gstin,
    }
    response = requests.get(url, headers=headers)
    return response 

def e_way_cancel_request(email, ip_address, cancel_Gstin, cancel):

    if cancel_Gstin == "05AAACH6188F1ZM":
        client_id = '2a74277b-ef21-4ec5-9a05-b77c372affee',
        client_secret = '853d3aaa-4c7b-4914-bb2e-706b86f5093b',
    else:
        client_id = '652026ed-e3d0-44ea-9e6e-9f6665a4efd0',
        client_secret = 'ca10b200-87d7-4aa2-82c6-70c906313c5c',
    
    url = f"https://api.mastergst.com/ewaybillapi/v1.03/ewayapi/canewb?email={email}"
    headers = {
        'ip_address': ip_address,
        'client_id': client_id[0],
        'client_secret': client_secret[0],
        'gstin': cancel_Gstin,
    }
    response = requests.post(url, headers=headers, json = cancel)
    return response 

success_logger = logging.getLogger('success_logger')
error_logger = logging.getLogger('error_logger')

class E_way_bill(APIView):
    permission_classes = (AllowAny, )

    def post(self, request):

        try:
            data1 = request.data 
            today_date = datetime.date.today()
            response = requests.get('https://ipinfo.io')
            data = response.json()
            public_ip = data.get('ip')

            all_responses = []
            if isinstance(data1, list):

                for data in data1:
                    Gstin = data.get('fromGstin')
                url = f"https://worker-patient-cake-0429.sudhan.workers.dev/?GST={Gstin}"
                response = requests.get(url)
                queryParams = response.json()
                if response.status_code == 200:
                    email = queryParams[0]['email']
                    username = queryParams[0]['username']
                    password = queryParams[0]['password']
                    Gstin = queryParams[0]['Gstin']
                    date = queryParams[0]['date']
                    date1 = datetime.datetime.strptime(date, '%d-%m-%Y').date()
                    days_difference = (date1 - today_date).days
                elif response.status_code == 300:
                    return Response({'result' : queryParams},status = status.HTTP_400_BAD_REQUEST)
                    
                if response.status_code == 200:
                    for data in data1:  
                        fromGstin = data.get('fromGstin')
                        gst = fromGstin or 'default_value'
                        if gst == queryParams[0]['Gstin']:
                            if days_difference == 0 or days_difference > 0: 
                                ip_address = public_ip
                                response_data = e_way_post_request(email, data, ip_address, Gstin)
                                all_responses.append(response_data.json())        
                            else:
                                error_logger.error("Error occurred: Subscription Error - Status Code: %s", status.HTTP_400_BAD_REQUEST)
                                return Response({'result': 'Subscription Error'}, status = status.HTTP_400_BAD_REQUEST)
                        else:
                            error_logger.error("Error occurred: Invalid Gstin - Status Code: %s", status.HTTP_400_BAD_REQUEST)
                            return Response({'result':'Invalid Gstin'},status = status.HTTP_400_BAD_REQUEST) 
                         
                    if response_data.status_code == 200:
                        if all_responses[0]['status_cd'] == '0':
                            data_string = all_responses[0]['error']['message']
                            parsed_data = json.loads(data_string)
                            error_codes_value = parsed_data['errorCodes']
                            if error_codes_value == '238':
                                auth_data = authtoken_request(email,username,password,ip_address,Gstin)
                                success_logger.info("Request processed successfully")
                                return Response({'result' : auth_data.json()}) 
                            else:
                                error_logger.error("Error occurred: Contact PG Analytics Team - Status Code: %s", response_data.status_code)
                                return Response({'result' : parsed_data},status = status.HTTP_400_BAD_REQUEST) 
                        else:
                            success_logger.info("Request processed successfully")
                            return Response({'result' : all_responses}) 
                    else:
                        error_logger.error("Error occurred: Contact PG Analytics Team - Status Code: %s", response_data.status_code)
                        return Response({'result':'Contact PG Analytics Team'},status = status.HTTP_400_BAD_REQUEST)
                else:
                    error_logger.error("Error occurred: Contact PG Analytics Team - Status Code: %s", response.status_code)
                    return Response({'result':'Contact PG Analytics Team'},status = status.HTTP_400_BAD_REQUEST)            
                
            else:   
 
                getGstin = data1.get('update', {}).get('Gstin')
                CancelGstin = data1.get('Cancel', {}).get('Gstin')
                Gstin = getGstin or CancelGstin or 'default_value'
                url = f"https://worker-patient-cake-0429.sudhan.workers.dev/?GST={Gstin}"
                response = requests.get(url)
                queryParams = response.json()
                if response.status_code == 200:
                    email = queryParams[0]['email']
                    username = queryParams[0]['username']
                    password = queryParams[0]['password']
                    Gstin = queryParams[0]['Gstin']
                    date = queryParams[0]['date']
                    date1 = datetime.datetime.strptime(date, '%d-%m-%Y').date()
                    days_difference = (date1 - today_date).days
                elif response.status_code == 300:
                    return Response({'result' : queryParams},status = status.HTTP_400_BAD_REQUEST)

                gst = getGstin or CancelGstin or Gstin or 'default_value'
                if gst == queryParams[0]['Gstin']:
                    if days_difference == 0 or days_difference > 0:
                        for key in data1:
                            if key == 'update':
                                update = data1['update']
                                ewbNo = update.get('ewbNo')
                                ip_address = public_ip
                                response = e_way_get_request(email, ewbNo, ip_address, Gstin)  
                                response_value = response.json() 
                                if response.status_code == 200:
                                    if response_value['status_cd'] == '0':
                                        data_string = response_value['error']['message']
                                        parsed_data = json.loads(data_string)
                                        error_codes_value = parsed_data['errorCodes']
                                        if error_codes_value == '238':
                                            auth_data = authtoken_request(email,username,password,ip_address,Gstin)
                                            success_logger.info("Request processed successfully")
                                            return Response({'result' : auth_data.json()}) 
                                        else:
                                            error_logger.error("Error occurred: Contact PG Analytics Team - Status Code: %s", response.status_code)
                                            return Response({'result' : parsed_data},status = status.HTTP_400_BAD_REQUEST)
                                    else:
                                        success_logger.info("Request processed successfully")
                                        return Response({'result' : response_value})       
                                else:
                                    error_logger.error("Error occurred: Contact PG Analytics Team - Status Code: %s", response.status_code)
                                    return Response({'result':'Contact PG Analytics Team'},status = status.HTTP_400_BAD_REQUEST)
                            if key == 'Cancel':
                                Cancel = data1['Cancel']
                                # Gstin = cancel.get('Gstin')
                                ip_address = public_ip
                                cancel_data = {
                                    "cancelRsnCode": 1,
                                    "cancelRmrk": "string"
                                }
                                data1["Cancel"].update(cancel_data)
                                ip_address = public_ip
                                response = e_way_cancel_request(email, ip_address, Gstin, Cancel)  
                                response_value = response.json() 
                                if response.status_code == 200:
                                    if response_value['status_cd'] == '0':
                                        data_string = response_value['error']['message']
                                        parsed_data = json.loads(data_string)
                                        error_codes_value = parsed_data['errorCodes']
                                        if error_codes_value == '238':
                                            auth_data = authtoken_request(email,username,password,ip_address,Gstin)
                                            success_logger.info("Request processed successfully")
                                            return Response({'result' : auth_data.json()}) 
                                        else:
                                            error_logger.error("Error occurred: Contact PG Analytics Team - Status Code: %s", response.status_code)
                                            return Response({'result' : parsed_data},status = status.HTTP_400_BAD_REQUEST)
                                    else:
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
            error_logger.error("An unhandled exception occurred: %s", traceback.format_exc())
            error_logger.error(f"{error_message} - Status Code: {status.HTTP_400_BAD_REQUEST}, Error: {str(e)}")
            error_message = str(e)
            # traceback_details = traceback.format_exc()
            # if error_message == 'list index out of range':
            #     error_logger.error("Error occurred: Invalid Gstin - Status Code: %s", status.HTTP_400_BAD_REQUEST)
            #     return Response({'result':'Invalid Gstin'},status = status.HTTP_400_BAD_REQUEST)
            return Response(traceback.format_exc(), status = status.HTTP_400_BAD_REQUEST)