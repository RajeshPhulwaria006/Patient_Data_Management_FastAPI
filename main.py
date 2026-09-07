from fastapi import FastAPI, Query, HTTPException, Path
from fastapi.responses import JSONResponse
from models import Patient, PatientUpdate
from utils import load_data, save_data


app = FastAPI()
# "example_patient": {
#         "name": "Patient name",
#         "age": _,
#         "city": "Patient city",
#         "gender": "_",
#         "height_cm": _,
#         "weight_kg": _,
#         "bmi": -,
#         "verdict": "-"
# },
    

@app.get('/')
def greet():
    return {"message": "Patient Data Management System!"}

@app.get('/about')
def about():
    return {'message': "its basic API endpoint to retriev and manage patient's data."}

# API endpoint to get data
@app.get("/view")
def view():
    data = load_data()
    return data

# API endpoint to get patient's data by patient_id
@app.get('/patient/{patient_id}')
def get_patient(
    patient_id: str = Path(
        ...,
        description='ID of the patient in the DB',
        examples='p001'
    )
):

    data = load_data()
    if patient_id not in data:
        raise HTTPException(
            status_code=404,
            detail=f"Patient not found! {patient_id} is unavailable"
        )
        
    return data[patient_id]

# API endpoint to sort patient's data
@app.get('/sort')
def sort(
    sort_by:str = Query(
        ...,
        description="Sort on the basis of height_cm, weight_kg, bmi or age"
    ),
    order:str = Query(
        'asc',
        description="Sort in asc(ascending) or desc(descending)"
    )
):
    valid_fields = ['height_cm', 'weight_kg', 'bmi', 'age']
    valid_orders = ['asc', 'desc']
    if sort_by not in valid_fields:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid sorting field! enter among {valid_fields}"
        )
    if order not in valid_orders:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid sorting order! enter among {valid_orders}"
        )
    
    data = load_data()
    isDescending = True if order == 'desc' else False
    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=isDescending)
    
    return sorted_data


# API endpoint to create new patient 
@app.post("/create")
def create_patient(patient: Patient):
    # load and validate patient on id
    data = load_data()
    if patient.id in data:
        raise HTTPException(
            status_code=400,
            detail="Patient already exist with this id!"
        )
        
    # create new patient's data
    data[patient.id] = patient.model_dump(exclude=['id'])   # return patient's data except its id
    # save data
    save_data(data)
    return JSONResponse(
        status_code=201,
        content={
            'message': f"Patient created successfully. ID: {patient.id}"
        }
    )
    
    
# API endpoint to update patient's data
@app.put('/edit/{id}')
def update_patient(id: str, patient: PatientUpdate):
    
    data = load_data()
    if id not in data:
        raise HTTPException(
            status_code=404,
            detail="Patient not found!"
        )
        
    patient_data = data[id]
    new_patient_data = patient.model_dump(exclude_unset=True)  # will exclude None type data

    for key, value in new_patient_data.items():
        patient_data[key] = value
        
    patient_data["id"] = id
    patient_pydantic = Patient(**patient_data)
    
    data[id] = patient_pydantic.model_dump(exclude=['id'])
    save_data(data)
    
    return JSONResponse(
        status_code=200,
        content={
            'message': "Patient info updated successfully."
        }
    )