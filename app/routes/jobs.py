from flask import Blueprint, request
from ..auth_token import auth_required
from ..models import Job, db
job_routes = Blueprint('jobs', __name__)

@job_routes.route('/', methods=["POST"])
def add_one_job():
    req = request.get_json()
    check_number = req.get("check_number", None)
    priority = req.get("priority", None)
    description = req.get("description", None)
    tech_notes = req.get("tech_notes", None)
    completion_notes = req.get("completion_notes", None)
    duration = req.get("duration", None)
    time_frame_promised_start = req.get("time_frame_promised_start", None)
    time_frame_promised_end = req.get("time_frame_promised_end", None)
    start_date = req.get("start_date", None)
    end_date = req.get("end_date", None)
    customer_name = req.get("customer_name", None)
    status = req.get("status", None)
    contact_first_name = req.get("contact_first_name", None)
    contact_last_name = req.get("contact_last_name", None)
    street_1 = req.get("street_1", None)
    street_2 = req.get("street_2", None)
    city = req.get("city", None)
    state_prov = req.get("state_prov", None)
    postal_code = req.get("postal_code", None)
    location_name = req.get("location_name", None)
    is_gated = req.get("is_gated", None)
    gate_instructions = req.get("gate_instructions", None)
    category = req.get("category", None)
    source = req.get("source", None)
    payment_type = req.get("payment_type", None)
    customer_payment_terms = req.get("customer_payment_terms", None)
    project = req.get("project", None)
    phase = req.get("phase", None)
    po_number = req.get("po_number", None)
    contract = req.get("contract", None)
    note_to_customer = req.get("note_to_customer", None)
    called_in_by = req.get("called_in_by", None)
    is_requires_follow_up = req.get("is_requires_follow_up", None)
    agents = req.get("agents", None)
    custom_fields = req.get("custom_fields", None)
    equipment = req.get("equipment", None)
    techs_assigned = req.get("techs_assigned", None)
    tasks = req.get("tasks", None)
    notes = req.get("notes", None)
    products = req.get("products", None)
    services = req.get("services", None)
    other_charges = req.get("other_charges", None)
    labor_charges = req.get("labor_charges", None)
    expenses = req.get("expenses", None)
    new_job = Job(check_number = check_number,priority = priority,description = description,tech_notes = tech_notes,completion_notes = completion_notes,duration = duration,time_frame_promised_start = time_frame_promised_start,time_frame_promised_end = time_frame_promised_end,start_date = start_date,end_date = end_date,customer_name = customer_name,status = status,contact_first_name = contact_first_name,contact_last_name = contact_last_name,street_1 = street_1,street_2 = street_2,city = city,state_prov = state_prov,postal_code = postal_code,location_name = location_name,is_gated = is_gated,gate_instructions = gate_instructions,category = category,source = source,payment_type = payment_type,customer_payment_terms = customer_payment_terms,project = project,phase = phase,po_number = po_number,contract = contract,note_to_customer = note_to_customer,called_in_by = called_in_by,is_requires_follow_up = is_requires_follow_up,agents = agents,custom_fields = custom_fields,equipment = equipment,techs_assigned = techs_assigned,tasks = tasks,notes = notes,products = products,services = services,other_charges = other_charges,labor_charges = labor_charges,expenses = expenses)
    db.session.add(new_job)
    db.session.commit()

@job_routes.route('/', methods=["POST"])
def add_multiple_jobs():
    req = request.get_json()
    jobs = req.get("jobs", None)
    for job in jobs:
        new_job = Job(check_number = job["check_number"],priority = job["priority"],description = job["description"],tech_notes = job["tech_notes"],completion_notes = job["completion_notes"],duration = job["duration"],time_frame_promised_start = job["time_frame_promised_start"],time_frame_promised_end = job["time_frame_promised_end"],start_date = job["start_date"],end_date = job["end_date"],customer_name = job["customer_name"],status = job["status"],contact_first_name = job["contact_first_name"],contact_last_name = job["contact_last_name"],street_1 = job["street_1"],street_2 = job["street_2"],city = job["city"],state_prov = job["state_prov"],postal_code = job["postal_code"],location_name = job["location_name"],is_gated = job["is_gated"],gate_instructions = job["gate_instructions"],category = job["category"],source = job["source"],payment_type = job["payment_type"],customer_payment_terms = job["customer_payment_terms"],project = job["project"],phase = job["phase"],po_number = job["po_number"],contract = job["contract"],note_to_customer = job["note_to_customer"],called_in_by = job["called_in_by"],is_requires_follow_up = job["is_requires_follow_up"],agents = job["agents"],custom_fields = job["custom_fields"],equipment = job["equipment"],techs_assigned = job["techs_assigned"],tasks = job["tasks"],notes = job["notes"],products = job["products"],services = job["services"],other_charges = job["other_charges"],labor_charges = job["labor_charges"],expenses = job["expenses"])
        db.session.add(new_job)
    db.session.commit()

@job_routes.route('/<int:id>')
def get_one_job():
    return {"job": (Job.query.get(id)).to_dict()}

@job_routes.route('/')
def get_all_jobs():
    return {"jobs": [job.to_dict() for job in Job.query.all()]}

@job_routes.route('/<int:id>', methods=["PUT"])
def update_one_jobs(id):
    req = request.get_json()
    current_job = Job.query.get(id)
    current_job.check_number = req.get("check_number", None)
    current_job.priority = req.get("priority", None)
    current_job.description = req.get("description", None)
    current_job.tech_notes = req.get("tech_notes", None)
    current_job.completion_notes = req.get("completion_notes", None)
    current_job.duration = req.get("duration", None)
    current_job.time_frame_promised_start = req.get("time_frame_promised_start", None)
    current_job.time_frame_promised_end = req.get("time_frame_promised_end", None)
    current_job.start_date = req.get("start_date", None)
    current_job.end_date = req.get("end_date", None)
    current_job.customer_name = req.get("customer_name", None)
    current_job.status = req.get("status", None)
    current_job.contact_first_name = req.get("contact_first_name", None)
    current_job.contact_last_name = req.get("contact_last_name", None)
    current_job.street_1 = req.get("street_1", None)
    current_job.street_2 = req.get("street_2", None)
    current_job.city = req.get("city", None)
    current_job.state_prov = req.get("state_prov", None)
    current_job.postal_code = req.get("postal_code", None)
    current_job.location_name = req.get("location_name", None)
    current_job.is_gated = req.get("is_gated", None)
    current_job.gate_instructions = req.get("gate_instructions", None)
    current_job.category = req.get("category", None)
    current_job.source = req.get("source", None)
    current_job.payment_type = req.get("payment_type", None)
    current_job.customer_payment_terms = req.get("customer_payment_terms", None)
    current_job.project = req.get("project", None)
    current_job.phase = req.get("phase", None)
    current_job.po_number = req.get("po_number", None)
    current_job.contract = req.get("contract", None)
    current_job.note_to_customer = req.get("note_to_customer", None)
    current_job.called_in_by = req.get("called_in_by", None)
    current_job.is_requires_follow_up = req.get("is_requires_follow_up", None)
    current_job.agents = req.get("agents", None)
    current_job.custom_fields = req.get("custom_fields", None)
    current_job.equipment = req.get("equipment", None)
    current_job.techs_assigned = req.get("techs_assigned", None)
    current_job.tasks = req.get("tasks", None)
    current_job.notes = req.get("notes", None)
    current_job.products = req.get("products", None)
    current_job.services = req.get("services", None)
    current_job.other_charges = req.get("other_charges", None)
    current_job.labor_charges = req.get("labor_charges", None)
    current_job.expenses = req.get("expenses", None)
    db.session.commit()

@job_routes.route('/', methods=["PUT"])
def update_multiple_jobs():
    req = request.get_json()
    jobs = req.get("jobs", None)
    for current_job in jobs:
        temp_job = Job.query.get(current_job["id"])
        temp_job.check_number = current_job["check_number"]
        temp_job.priority = current_job["priority"]
        temp_job.description = current_job["description"]
        temp_job.tech_notes = current_job["tech_notes"]
        temp_job.completion_notes = current_job["completion_notes"]
        temp_job.duration = current_job["duration"]
        temp_job.time_frame_promised_start = current_job["time_frame_promised_start"]
        temp_job.time_frame_promised_end = current_job["time_frame_promised_end"]
        temp_job.start_date = current_job["start_date"]
        temp_job.end_date = current_job["end_date"]
        temp_job.customer_name = current_job["customer_name"]
        temp_job.status = current_job["status"]
        temp_job.contact_first_name = current_job["contact_first_name"]
        temp_job.contact_last_name = current_job["contact_last_name"]
        temp_job.street_1 = current_job["street_1"]
        temp_job.street_2 = current_job["street_2"]
        temp_job.city = current_job["city"]
        temp_job.state_prov = current_job["state_prov"]
        temp_job.postal_code = current_job["postal_code"]
        temp_job.location_name = current_job["location_name"]
        temp_job.is_gated = current_job["is_gated"]
        temp_job.gate_instructions = current_job["gate_instructions"]
        temp_job.category = current_job["category"]
        temp_job.source = current_job["source"]
        temp_job.payment_type = current_job["payment_type"]
        temp_job.customer_payment_terms = current_job["customer_payment_terms"]
        temp_job.project = current_job["project"]
        temp_job.phase = current_job["phase"]
        temp_job.po_number = current_job["po_number"]
        temp_job.contract = current_job["contract"]
        temp_job.note_to_customer = current_job["note_to_customer"]
        temp_job.called_in_by = current_job["called_in_by"]
        temp_job.is_requires_follow_up = current_job["is_requires_follow_up"]
        temp_job.agents = current_job["agents"]
        temp_job.custom_fields = current_job["custom_fields"]
        temp_job.equipment = current_job["equipment"]
        temp_job.techs_assigned = current_job["techs_assigned"]
        temp_job.tasks = current_job["tasks"]
        temp_job.notes = current_job["notes"]
        temp_job.products = current_job["products"]
        temp_job.services = current_job["services"]
        temp_job.other_charges = current_job["other_charges"]
        temp_job.labor_charges = current_job["labor_charges"]
        temp_job.expenses = current_job["expenses"]
        db.session.commit()

@job_routes.route('/<int:id>', methods=["delete"])
def delete_one_job(id):
    Job.query.get(id).delete()
    db.session.commit()

@job_routes.route('/', methods=["delete"])
def delete_multiple_jobs():
    req = request.get_json()
    jobs = req.get(jobs)
    for job in jobs:
        Job.query.get(job["id"]).delete()
    db.session.commit()

