from .db import db
from sqlalchemy.dialects.postgresql import JSON

class Customer(db.Model):
    __tablename__ = "customers"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    customer_name = db.Column(db.String(255), primary_key=False, nullable=True)
    parent_customer = db.Column(db.String(255), primary_key=False, nullable=True)
    account_number = db.Column(db.String(255), primary_key=False, nullable=True)
    private_notes = db.Column(db.String(255), primary_key=False, nullable=True)
    public_notes = db.Column(db.String(255), primary_key=False, nullable=True)
    credit_rating = db.Column(db.String(255), primary_key=False, nullable=True)
    labor_charge_type = db.Column(db.String(255), primary_key=False, nullable=True)
    labor_charge_default_rate = db.Column(None, primary_key=False, nullable=True)
    last_serviced_date = db.Column(db.DateTime, primary_key=False, nullable=True)
    is_bill_for_drive_time = db.Column(db.Boolean, primary_key=False, nullable=True)
    is_vip = db.Column(db.Boolean, primary_key=False, nullable=True)
    referral_source = db.Column(db.String(255), primary_key=False, nullable=True)
    agent = db.Column(db.String(255), primary_key=False, nullable=True)
    discount = db.Column(None, primary_key=False, nullable=True)
    discount_type = db.Column(db.String(255), primary_key=False, nullable=True)
    payment_type = db.Column(db.String(255), primary_key=False, nullable=True)
    payment_terms = db.Column(db.String(255), primary_key=False, nullable=True)
    assigned_contract = db.Column(db.String(255), primary_key=False, nullable=True)
    industry = db.Column(db.String(255), primary_key=False, nullable=True)
    is_taxable = db.Column(db.Boolean, primary_key=False, nullable=True)
    tax_item_name = db.Column(db.String(255), primary_key=False, nullable=True)
    qbo_sync_token = db.Column(db.Integer, primary_key=False, nullable=True)
    qbo_currency = db.Column(db.String(255), primary_key=False, nullable=True)
    contacts = db.Column(JSON, primary_key=False, nullable=True)
    locations = db.Column(JSON, primary_key=False, nullable=True)
    custom_fields = db.Column(JSON, primary_key=False, nullable=True)


    def to_dict(self):
        return {
            "id": self.id,
            "customer_name": self.customer_name,
            "parent_customer": self.parent_customer,
            "account_number": self.account_number,
            "private_notes": self.private_notes,
            "public_notes": self.public_notes,
            "credit_rating": self.credit_rating,
            "labor_charge_type": self.labor_charge_type,
            "labor_charge_default_rate": self.labor_charge_default_rate,
            "last_serviced_date": self.last_serviced_date,
            "is_bill_for_drive_time": self.is_bill_for_drive_time,
            "is_vip": self.is_vip,
            "referral_source": self.referral_source,
            "agent": self.agent,
            "discount": self.discount,
            "discount_type": self.discount_type,
            "payment_type": self.payment_type,
            "payment_terms": self.payment_terms,
            "assigned_contract": self.assigned_contract,
            "industry": self.industry,
            "is_taxable": self.is_taxable,
            "tax_item_name": self.tax_item_name,
            "qbo_sync_token": self.qbo_sync_token,
            "qbo_currency": self.qbo_currency,
            "contacts": self.contacts,
            "locations": self.locations,
            "custom_fields": self.custom_fields,
        }

