from flask import Blueprint, request
from ..auth_token import auth_required
from ..models import Customer, db
customer_routes = Blueprint('customers', __name__)

@customer_routes.route('/', methods=["POST"])
def add_one_customer():
    req = request.get_json()
    customer_name = req.get("customer_name", None)
    parent_customer = req.get("parent_customer", None)
    account_number = req.get("account_number", None)
    private_notes = req.get("private_notes", None)
    public_notes = req.get("public_notes", None)
    credit_rating = req.get("credit_rating", None)
    labor_charge_type = req.get("labor_charge_type", None)
    labor_charge_default_rate = req.get("labor_charge_default_rate", None)
    last_serviced_date = req.get("last_serviced_date", None)
    is_bill_for_drive_time = req.get("is_bill_for_drive_time", None)
    is_vip = req.get("is_vip", None)
    referral_source = req.get("referral_source", None)
    agent = req.get("agent", None)
    discount = req.get("discount", None)
    discount_type = req.get("discount_type", None)
    payment_type = req.get("payment_type", None)
    payment_terms = req.get("payment_terms", None)
    assigned_contract = req.get("assigned_contract", None)
    industry = req.get("industry", None)
    is_taxable = req.get("is_taxable", None)
    tax_item_name = req.get("tax_item_name", None)
    qbo_sync_token = req.get("qbo_sync_token", None)
    qbo_currency = req.get("qbo_currency", None)
    contacts = req.get("contacts", None)
    locations = req.get("locations", None)
    custom_fields = req.get("custom_fields", None)
    new_customer = Customer(customer_name = customer_name,parent_customer = parent_customer,account_number = account_number,private_notes = private_notes,public_notes = public_notes,credit_rating = credit_rating,labor_charge_type = labor_charge_type,labor_charge_default_rate = labor_charge_default_rate,last_serviced_date = last_serviced_date,is_bill_for_drive_time = is_bill_for_drive_time,is_vip = is_vip,referral_source = referral_source,agent = agent,discount = discount,discount_type = discount_type,payment_type = payment_type,payment_terms = payment_terms,assigned_contract = assigned_contract,industry = industry,is_taxable = is_taxable,tax_item_name = tax_item_name,qbo_sync_token = qbo_sync_token,qbo_currency = qbo_currency,contacts = contacts,locations = locations,custom_fields = custom_fields)
    db.session.add(new_customer)
    db.session.commit()

@customer_routes.route('/', methods=["POST"])
def add_multiple_customers():
    req = request.get_json()
    customers = req.get("customers", None)
    for customer in customers:
        new_customer = Customer(customer_name = customer["customer_name"],parent_customer = customer["parent_customer"],account_number = customer["account_number"],private_notes = customer["private_notes"],public_notes = customer["public_notes"],credit_rating = customer["credit_rating"],labor_charge_type = customer["labor_charge_type"],labor_charge_default_rate = customer["labor_charge_default_rate"],last_serviced_date = customer["last_serviced_date"],is_bill_for_drive_time = customer["is_bill_for_drive_time"],is_vip = customer["is_vip"],referral_source = customer["referral_source"],agent = customer["agent"],discount = customer["discount"],discount_type = customer["discount_type"],payment_type = customer["payment_type"],payment_terms = customer["payment_terms"],assigned_contract = customer["assigned_contract"],industry = customer["industry"],is_taxable = customer["is_taxable"],tax_item_name = customer["tax_item_name"],qbo_sync_token = customer["qbo_sync_token"],qbo_currency = customer["qbo_currency"],contacts = customer["contacts"],locations = customer["locations"],custom_fields = customer["custom_fields"])
        db.session.add(new_customer)
    db.session.commit()

@customer_routes.route('/<int:id>')
def get_one_customer():
    return {"customer": (Customer.query.get(id)).to_dict()}

@customer_routes.route('/')
def get_all_customers():
    return {"customers": [customer.to_dict() for customer in Customer.query.all()]}

@customer_routes.route('/<int:id>', methods=["PUT"])
def update_one_customers(id):
    req = request.get_json()
    current_customer = Customer.query.get(id)
    current_customer.customer_name = req.get("customer_name", None)
    current_customer.parent_customer = req.get("parent_customer", None)
    current_customer.account_number = req.get("account_number", None)
    current_customer.private_notes = req.get("private_notes", None)
    current_customer.public_notes = req.get("public_notes", None)
    current_customer.credit_rating = req.get("credit_rating", None)
    current_customer.labor_charge_type = req.get("labor_charge_type", None)
    current_customer.labor_charge_default_rate = req.get("labor_charge_default_rate", None)
    current_customer.last_serviced_date = req.get("last_serviced_date", None)
    current_customer.is_bill_for_drive_time = req.get("is_bill_for_drive_time", None)
    current_customer.is_vip = req.get("is_vip", None)
    current_customer.referral_source = req.get("referral_source", None)
    current_customer.agent = req.get("agent", None)
    current_customer.discount = req.get("discount", None)
    current_customer.discount_type = req.get("discount_type", None)
    current_customer.payment_type = req.get("payment_type", None)
    current_customer.payment_terms = req.get("payment_terms", None)
    current_customer.assigned_contract = req.get("assigned_contract", None)
    current_customer.industry = req.get("industry", None)
    current_customer.is_taxable = req.get("is_taxable", None)
    current_customer.tax_item_name = req.get("tax_item_name", None)
    current_customer.qbo_sync_token = req.get("qbo_sync_token", None)
    current_customer.qbo_currency = req.get("qbo_currency", None)
    current_customer.contacts = req.get("contacts", None)
    current_customer.locations = req.get("locations", None)
    current_customer.custom_fields = req.get("custom_fields", None)
    db.session.commit()

@customer_routes.route('/', methods=["PUT"])
def update_multiple_customers():
    req = request.get_json()
    customers = req.get("customers", None)
    for current_customer in customers:
        temp_customer = Customer.query.get(current_customer["id"])
        temp_customer.customer_name = current_customer["customer_name"]
        temp_customer.parent_customer = current_customer["parent_customer"]
        temp_customer.account_number = current_customer["account_number"]
        temp_customer.private_notes = current_customer["private_notes"]
        temp_customer.public_notes = current_customer["public_notes"]
        temp_customer.credit_rating = current_customer["credit_rating"]
        temp_customer.labor_charge_type = current_customer["labor_charge_type"]
        temp_customer.labor_charge_default_rate = current_customer["labor_charge_default_rate"]
        temp_customer.last_serviced_date = current_customer["last_serviced_date"]
        temp_customer.is_bill_for_drive_time = current_customer["is_bill_for_drive_time"]
        temp_customer.is_vip = current_customer["is_vip"]
        temp_customer.referral_source = current_customer["referral_source"]
        temp_customer.agent = current_customer["agent"]
        temp_customer.discount = current_customer["discount"]
        temp_customer.discount_type = current_customer["discount_type"]
        temp_customer.payment_type = current_customer["payment_type"]
        temp_customer.payment_terms = current_customer["payment_terms"]
        temp_customer.assigned_contract = current_customer["assigned_contract"]
        temp_customer.industry = current_customer["industry"]
        temp_customer.is_taxable = current_customer["is_taxable"]
        temp_customer.tax_item_name = current_customer["tax_item_name"]
        temp_customer.qbo_sync_token = current_customer["qbo_sync_token"]
        temp_customer.qbo_currency = current_customer["qbo_currency"]
        temp_customer.contacts = current_customer["contacts"]
        temp_customer.locations = current_customer["locations"]
        temp_customer.custom_fields = current_customer["custom_fields"]
        db.session.commit()

@customer_routes.route('/<int:id>', methods=["delete"])
def delete_one_customer(id):
    Customer.query.get(id).delete()
    db.session.commit()

@customer_routes.route('/', methods=["delete"])
def delete_multiple_customers():
    req = request.get_json()
    customers = req.get(customers)
    for customer in customers:
        Customer.query.get(customer["id"]).delete()
    db.session.commit()

