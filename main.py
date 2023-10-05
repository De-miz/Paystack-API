# make sure you have all required packages installed, asyncio and aiohttp (pip install asyncio, aiohttp)

from asyncio import run 
from aiohttp import ClientSession
from uuid import uuid4


# replace this with your own 
SECRET_KEY = "sk_test_a187c8cbd2d917dff8fd890277cae1333fb7965a"

class Paystack:
    
    def __init__(
            self, 
            secret_key, # paystack api secret key
            api_type, # a type of paystack api, look into self.request_data
            reference=uuid4(), # Unique transaction reference. Only -, ., = and alphanumeric characters allowed.
            currency='GHS', # look into supported countries
            transaction_charge='0', # charge on transactions, look into paystack api docs for more info
            callback_url='https://webhook.site/87d71a37-539b-4d01-8613-6c20d2c64b0b', # url to recieve response data, get a testing url from webhook.site
            payment_methods=["card", "bank", "ussd", "qr", "mobile_money", "bank_transfer", "eft"], # An array of payment channels to control what channels you want to make available to the user to make a payment with. Available channels include: ["card", "bank", "ussd", "qr", "mobile_money", "bank_transfer", "eft"]
            customer_id='', # customer code received from the 'create_customer' api 
            recipient_code='RCP_2fl88y39jk7z1w8', # recipient code received from the 'create_recipient' API
            amount=3200, # this is messured in pesewas if currency is 'GHS'
            payment_request_code='', # code received from the 'recieve_payment' API
            email="emmanuel.eddie.j.k@gmail.com", 
            description="This is in test mode",
            country="ghana", # user country
            customer_name="Demiz Kweh", # u already knw ahm masa 
            phone="0509712818",
            account_number="0509712818", # bank account number if provider is bank
            transaction_type="mobile_money", # Recipient Type. It could be one of: nuban, ghipss, mobile_money or basa
            bank_code="MTN", # look into list of supported banks
            transfer_code="TRF_ccit9dbhzwk0ncgs", # code received after an initiated money transfer
            otp_code="505721", # otp code sent to user for verification after an initiated money transfer
            account_name="Eddie Kweh", # name of user bank account
            account_type="personal", # personal or business
            id_type="identityNumber", # [ identityNumber, passportNumber, businessRegistrationNumber ]
            id_number="GHA-578490375-2", # could be passport or businessRegistration number
            card_number="486727", # only the first 6 digits of user visa or mastercard is needed
            domain_name="example.com", # domain being registered for apple pay (Please verify that the correct file is hosted at https://sikadua.pythonanywhere.com/.well-known/apple-developer-merchantid-domain-association)
        ):
        
        self.reference = str(reference)
        self.currency = currency
        self.email = email
        self.amount = amount
        self.transaction_charge = transaction_charge
        self.callback_url = callback_url
        self.payment_methods = payment_methods
        self.customer_id = customer_id
        self.payment_request_code = payment_request_code
        self.description = description
        self.country = country
        self.recipient_code = recipient_code
        self.customer_name = customer_name
        self.first_name = customer_name.split()[0]
        self.last_name = customer_name.split()[-1]
        self.phone = phone
        self.transaction_type = transaction_type
        self.bank_code = bank_code
        self.account_number = account_number
        self.transfer_code = transfer_code
        self.otp_code = otp_code
        self.account_name = account_name
        self.account_type = account_type
        self.id_type = id_type 
        self.id_number = id_number
        self.verify_card_number = card_number[:6]
        self.domain_name = domain_name


        self.api_type = api_type
        self.secret_key = secret_key
        self.main_domain = "https://api.paystack.co"
        self.headers = {
            "Authorization": f"Bearer {self.secret_key}", 
            "Content-Type": "application/json"
        }

        # Types of APIs
        self.request_data = {
            # method: POST
            "initialize_transaction": {
                "url": f"{self.main_domain}/transaction/initialize",
                "payload": {
                    "email": self.email, 
                    "amount": self.amount,
                    "currency": self.currency,
                    "reference": str(self.reference),
                    "callback_url": self.callback_url,
                    "transaction_charge": self.transaction_charge,
                    "channels": self.payment_methods,

                }
            }, 

            # method: GET
            "verify_transaction": {
                "url": f"{self.main_domain}/transaction/verify/" + str(self.reference),
            }, 

            # method: POST
            "create_customer": {
                "url": f"{self.main_domain}/customer", 
                "payload": {
                    "email": self.email, 
                    "first_name": self.first_name, 
                    "last_name": self.last_name, 
                    "phone": self.phone, 
                    "metadata": {
                        "age": 21
                    }
                }
            }, 

            # method: POST
            # name parameter should match the one used to create customer (recommended)
            "create_recipient": {
                "url": f"{self.main_domain}/transferrecipient",
                "payload": {
                    "type": self.transaction_type,
                    "name": self.customer_name,
                    "account_number": "0509712818", 
                    "bank_code": self.bank_code,
                    "description": self.description, 
                    "currency": self.currency,
                    "metadata": { # you can add anything of ur choice in metadata parameters
                        "custom_data": "This is in test mode"
                    }
                }
            }, 

            # method: POST
            # Make sure you've already created a customer before using this API, customer_code is required
            "recieve_payment": {
                "url": f"{self.main_domain}/paymentrequest",
                "payload": {
                    "customer": self.customer_id,
                    "amount": 500.00, 
                    "currency": self.currency, 
                    "send_notification": True,
                    "description": self.description,
                } 
            }, 

            # method: POST
            # Make sure you've already initiated a payment request before using this API, request code is required
            "send_payment_request_notification": {
                "url": f"{self.main_domain}/paymentrequest/notify/" + self.payment_request_code,
                "payload": {
                    "code": self.payment_request_code,
                } 
            }, 

            # method: GET
            # get a list of supported countries and info
            "get_supported_countries": {
                "url": f"{self.main_domain}/country",
            },

            # method: GET
            # the get_supported_countries api shows a list of all supported countries
            "get_banks_info": {
                "url": f"{self.main_domain}/bank?country={self.country}",
            }, 

            # method: POST
            # Make sure you've already created a recipient before using this API, recipient code is required
            "initiate_money_transfer": {
                "url": f"{self.main_domain}/transfer",
                "payload": {
                    "source": "balance",
                    "amount": self.amount, 
                    "recipient": self.recipient_code,
                    "currency": self.currency, 
                    "reference": self.reference,
                }
            }, 

            # method: POST
            # this api checks the otp code sent to the user, money is transfered successfully upon otp match
            "complete_transfer": {
                "url": f"{self.main_domain}/transfer/finalize_transfer",
                "payload": {
                    "transfer_code": self.transfer_code, 
                    "otp": self.otp_code,
                }
            }, 

            # method: POST
            #   register/unregister a ready-domain for apple pay
            # method: GET
            #   get an array of registered domains
            "apple_pay": {
                "url": f"{self.main_domain}/apple-pay/domain", 
                "payload": {
                    "domainName": self.domain_name,
                }
            },

            # method: GET
            # get info about user account, try this eg. set account_number = [your mobile money number] and set bank_code = [MTN or VOD or ATL] that is mtn, vodafone or airteltigo
            # the get_banks_info api will give you all supported banks and necessary info
            "verify_account": {
                "url": f"{self.main_domain}/bank/resolve?account_number={self.account_number}&bank_code={self.bank_code}",
            }, 

            # method: GET
            # get a little detail about a payment card (bank cards, visa cards, master cards, virtual cards etc)
            "get_card_info": {
                "url": f"{self.main_domain}/decision/bin/{self.verify_card_number}",
            }, 
        }


    async def make_request(self, method="POST", json_data={}):
        headers = self.headers
        request_data = self.request_data.get(self.api_type)
        url = request_data.get('url')
        payload = json_data or request_data.get('payload')

        async with ClientSession() as session:
            async with session.post(url, headers=headers, json=payload) if method=='POST' else session.get(url, headers=headers) as response:
                return await response.text()
            

    async def runner(self, method='POST'):
        response = await self.make_request(method)
        print(response)




if __name__ == '__main__':
    send_request = Paystack(
        secret_key=SECRET_KEY, 
        api_type="verify_account", 
        bank_code='VOD',
        account_number='0509712818', # try sending me voda cash and see, (it should be sent successfully tho)
        domain_name="sikadua.pythonanywhere.com"
    )
    run(send_request.runner('GET'))
