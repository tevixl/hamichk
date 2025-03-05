import traceback
from FUNC.defs import *
from FUNC.usersdb_func import *

async def get_charge_resp(result, user_id, fullcc):
    try:
        # Initialize default values
        status = "𝐃𝐞𝐜𝐥𝐢𝐧𝐞𝐝 ❌"
        response = "No response received ❌"
        hits = "NO"

        # Check if result is None
        if result is None:
            return {
                "status": status,
                "response": response,
                "hits": hits,
                "fullz": fullcc,
            }

        # Process the result if it is a string
        if isinstance(result, str):
            if "Nice! New payment method added" in result:
                status = "𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝 ✅"
                response = "1000: Approved"
                hits = "YES"
                await forward_resp(fullcc, "BRAINTREE AUTH", response)

            elif "Status code cvv: Gateway Rejected: cvv" in result:
                response = "Gateway Rejected: cvv"

            elif "Declined - Call Issuer" in result:
                response = "Declined - Call Issuer"

            elif "Cannot Authorize at this time" in result:
                response = "Cannot Authorize at this time"

            elif "Processor Declined - Fraud Suspected" in result:
                response = "Fraud Suspected"

            elif "Status code risk_threshold: Gateway Rejected: risk_threshold" in result:
                response = "Gateway Rejected: risk_threshold"

            elif ("We're sorry, but the payment validation failed. Declined - Call Issuer" in result or
                  "Payment failed: Declined - Call Issuer" in result):
                response = "Declined - Call Issuer"

            elif "ProxyError" in result:
                response = "Proxy Connection Refused"
                await refundcredit(user_id)

            else:
                try:
                    response = result.split('"message": "')[1].split('"')[0] + " ❌"
                except Exception as e:
                    response = result
                    await result_logs(fullcc, "Braintree Auth", result)

        # Construct the response JSON
        json = {
            "status": status,
            "response": response,
            "hits": hits,
            "fullz": fullcc,
        }
        return json

    except Exception as e:
        # Handle any exceptions that occur
        status = "𝐃𝐞𝐜𝐥𝐢𝐧𝐞𝐝 ❌"
        response = str(e) + " ❌"
        hits = "NO"

        json = {
            "status": status,
            "response": response,
            "hits": hits,
            "fullz": fullcc,
        }
        return json