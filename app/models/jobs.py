from .db import db
from sqlalchemy.dialects.postgresql import JSON

class Job(db.Model):
    __tablename__ = "jobs"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    check_number = db.Column(db.String(255), primary_key=False, nullable=True)
    priority = db.Column(db.String(255), primary_key=False, nullable=True)
    description = db.Column(db.String(255), primary_key=False, nullable=True)
    tech_notes = db.Column(db.String(255), primary_key=False, nullable=True)
    completion_notes = db.Column(db.String(255), primary_key=False, nullable=True)
    duration = db.Column(db.Integer, primary_key=False, nullable=True)
    time_frame_promised_start = db.Column(db.String(255), primary_key=False, nullable=True)
    time_frame_promised_end = db.Column(db.String(255), primary_key=False, nullable=True)
    start_date = db.Column(db.DateTime, primary_key=False, nullable=True)
    end_date = db.Column(db.DateTime, primary_key=False, nullable=True)
    customer_name = db.Column(db.String(255), primary_key=False, nullable=True)
    status = db.Column(db.String(255), primary_key=False, nullable=True)
    contact_first_name = db.Column(db.String(255), primary_key=False, nullable=True)
    contact_last_name = db.Column(db.String(255), primary_key=False, nullable=True)
    street_1 = db.Column(db.String(255), primary_key=False, nullable=True)
    street_2 = db.Column(db.String(255), primary_key=False, nullable=True)
    city = db.Column(db.String(255), primary_key=False, nullable=True)
    state_prov = db.Column(db.String(255), primary_key=False, nullable=True)
    postal_code = db.Column(db.String(255), primary_key=False, nullable=True)
    location_name = db.Column(db.String(255), primary_key=False, nullable=True)
    is_gated = db.Column(db.Boolean, primary_key=False, nullable=True)
    gate_instructions = db.Column(db.String(255), primary_key=False, nullable=True)
    category = db.Column(db.String(255), primary_key=False, nullable=True)
    source = db.Column(db.String(255), primary_key=False, nullable=True)
    payment_type = db.Column(db.String(255), primary_key=False, nullable=True)
    customer_payment_terms = db.Column(db.String(255), primary_key=False, nullable=True)
    project = db.Column(db.String(255), primary_key=False, nullable=True)
    phase = db.Column(db.String(255), primary_key=False, nullable=True)
    po_number = db.Column(db.String(255), primary_key=False, nullable=True)
    contract = db.Column(db.String(255), primary_key=False, nullable=True)
    note_to_customer = db.Column(db.String(255), primary_key=False, nullable=True)
    called_in_by = db.Column(db.String(255), primary_key=False, nullable=True)
    is_requires_follow_up = db.Column(db.Boolean, primary_key=False, nullable=True)
    agents = db.Column(JSON, primary_key=False, nullable=True)
    custom_fields = db.Column(JSON, primary_key=False, nullable=True)
    equipment = db.Column(JSON, primary_key=False, nullable=True)
    techs_assigned = db.Column(JSON, primary_key=False, nullable=True)
    tasks = db.Column(JSON, primary_key=False, nullable=True)
    notes = db.Column(JSON, primary_key=False, nullable=True)
    products = db.Column(JSON, primary_key=False, nullable=True)
    services = db.Column(JSON, primary_key=False, nullable=True)
    other_charges = db.Column(JSON, primary_key=False, nullable=True)
    labor_charges = db.Column(JSON, primary_key=False, nullable=True)
    expenses = db.Column(JSON, primary_key=False, nullable=True)


    def to_dict(self):
        return {
            "id": self.id,
            "check_number": self.check_number,
            "priority": self.priority,
            "description": self.description,
            "tech_notes": self.tech_notes,
            "completion_notes": self.completion_notes,
            "duration": self.duration,
            "time_frame_promised_start": self.time_frame_promised_start,
            "time_frame_promised_end": self.time_frame_promised_end,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "customer_name": self.customer_name,
            "status": self.status,
            "contact_first_name": self.contact_first_name,
            "contact_last_name": self.contact_last_name,
            "street_1": self.street_1,
            "street_2": self.street_2,
            "city": self.city,
            "state_prov": self.state_prov,
            "postal_code": self.postal_code,
            "location_name": self.location_name,
            "is_gated": self.is_gated,
            "gate_instructions": self.gate_instructions,
            "category": self.category,
            "source": self.source,
            "payment_type": self.payment_type,
            "customer_payment_terms": self.customer_payment_terms,
            "project": self.project,
            "phase": self.phase,
            "po_number": self.po_number,
            "contract": self.contract,
            "note_to_customer": self.note_to_customer,
            "called_in_by": self.called_in_by,
            "is_requires_follow_up": self.is_requires_follow_up,
            "agents": self.agents,
            "custom_fields": self.custom_fields,
            "equipment": self.equipment,
            "techs_assigned": self.techs_assigned,
            "tasks": self.tasks,
            "notes": self.notes,
            "products": self.products,
            "services": self.services,
            "other_charges": self.other_charges,
            "labor_charges": self.labor_charges,
            "expenses": self.expenses,
        }

