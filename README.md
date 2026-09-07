# Patient Data Management API

A simple **Patient Data Management REST API** built with **FastAPI** and **Pydantic**.

This project demonstrates how to build a backend API for creating, retrieving, sorting, and updating patient records with request validation, computed fields, and persistent data storage.

> **Project Status:** Backend API is implemented and functional.  
> **Frontend:** Not implemented yet — a frontend interface will be added and improved in a future version.

---

## 🚀 Features

- Create a new patient record
- Retrieve all patient records
- Retrieve an individual patient by ID
- Update existing patient information
- Sort patients by:
  - Age
  - Height
  - Weight
  - BMI
- Automatic BMI calculation
- Automatic BMI health-category classification
- Pydantic-based request validation
- Unique patient ID validation
- Proper HTTP error handling
- Interactive API documentation through FastAPI/Swagger UI

---

## 🛠️ Tech Stack

- **Python**
- **FastAPI** — REST API framework
- **Pydantic** — data validation and modeling
- **Uvicorn** — ASGI server
- **JSON** — currently used for data persistence

---

## 📁 Project Structure

A typical project structure is:

```
├── ⚙️ .gitignore
├── 📝 README.md
├── 🐍 main.py
├── 🐍 models.py
├── ⚙️ patients.json
├── 📄 requirements.txt
└── 🐍 utils.py
```

> File names can be adjusted depending on the final project structure.

---

## 📋 Patient Data Model

A patient contains the following information:

| Field | Type | Description |
|---|---|---|
| `id` | `str` | Unique patient identifier |
| `name` | `str` | Patient name, maximum 50 characters |
| `age` | `int` | Patient age, must be greater than 0 |
| `city` | `str` | Patient's city |
| `gender` | `Male \| Female \| Other` | Patient gender |
| `height_cm` | `float` | Height in centimeters, must be greater than 0 |
| `weight_kg` | `float` | Weight in kilograms, must be greater than 0 |
| `bmi` | `float` | Automatically calculated BMI |
| `verdict` | `str` | Automatically calculated BMI category |

### BMI Calculation

BMI is calculated automatically using:

```text
BMI = weight (kg) / height² (m²)
```

The API calculates the BMI through a Pydantic `computed_field`.

### BMI Classification

| BMI | Verdict |
|---|---|
| `< 18.5` | Underweight |
| `18.5 – < 25` | Normal |
| `25 – < 30` | Overweight |
| `>= 30` | Obese |

> The BMI categories are implemented as part of this project's demonstration logic and should not be treated as medical diagnosis.

---

# 🔌 API Endpoints

## 1. Welcome

### `GET /`

Returns a basic welcome message.

### Example response

```json
{
  "message": "Patient Data Management System!"
}
```

---

## 2. About

### `GET /about`

Provides a short description of the API.

### Example response

```json
{
  "message": "its basic API endpoint to retriev and manage patient's data."
}
```

---

## 3. View All Patients

### `GET /view`

Retrieves all patient records from the data source.

### Example

```http
GET /view
```

### Example response

```json
{
  "p001": {
    "name": "Raj",
    "age": 21,
    "city": "Jodhpur",
    "gender": "Male",
    "height_cm": 175,
    "weight_kg": 70,
    "bmi": 22.86,
    "verdict": "Normal"
  }
}
```

---

## 4. Get Patient by ID

### `GET /patient/{patient_id}`

Retrieves a specific patient using their unique patient ID.

### Example

```http
GET /patient/p001
```

### Example response

```json
{
  "name": "Raj",
  "age": 21,
  "city": "Jodhpur",
  "gender": "Male",
  "height_cm": 175,
  "weight_kg": 70,
  "bmi": 22.86,
  "verdict": "Normal"
}
```

### If the patient does not exist

The API returns:

```json
{
  "detail": "Patient not found! p999 is unavailable"
}
```

with HTTP status:

```text
404 Not Found
```

---

# 5. Sort Patient Data

### `GET /sort`

Sorts patient records according to a selected field.

### Query parameters

| Parameter | Required | Allowed values |
|---|---|---|
| `sort_by` | Yes | `height_cm`, `weight_kg`, `bmi`, `age` |
| `order` | No | `asc`, `desc` |

The default sorting order is `asc`.

### Example

Sort by age in ascending order:

```http
GET /sort?sort_by=age&order=asc
```

Sort by BMI in descending order:

```http
GET /sort?sort_by=bmi&order=desc
```

### Invalid field

If an unsupported field is provided, the API returns:

```text
400 Bad Request
```

---

# 6. Create a Patient

### `POST /create`

Creates a new patient record.

The request body is validated using the `Patient` Pydantic model.

### Example request

```json
{
  "id": "p002",
  "name": "Amit",
  "age": 25,
  "city": "Jodhpur",
  "gender": "Male",
  "height_cm": 178,
  "weight_kg": 75
}
```

The `bmi` and `verdict` fields do **not** need to be supplied by the client because they are calculated automatically.

### Example response

```json
{
  "message": "Patient created successfully. ID: p002"
}
```

### Duplicate ID

If a patient already exists with the supplied ID:

```text
400 Bad Request
```

with:

```json
{
  "detail": "Patient already exist with this id!"
}
```

---

# 7. Update Patient

### `PUT /edit/{id}`

Updates an existing patient's information.

The endpoint uses a separate `PatientUpdate` model where fields are optional. This allows partial updates.

### Example

```http
PUT /edit/p002
```

Request body:

```json
{
  "age": 26,
  "weight_kg": 78
}
```

Only the supplied fields are updated.

The use of:

```python
patient.model_dump(exclude_unset=True)
```

ensures that fields which were not supplied in the request are not overwritten.

After updating, the complete patient object is reconstructed using the `Patient` model, which causes `bmi` and `verdict` to be recalculated.

### Example response

```json
{
  "message": "Patient info updated successfully."
}
```

### Patient not found

If the supplied ID does not exist:

```text
404 Not Found
```

---

# 🧠 Pydantic Validation

The project uses Pydantic to validate incoming patient data.

For example:

```python
class Patient(BaseModel):
    id: str
    name: str
    age: int
    city: str
    gender: Literal["Male", "Female", "Other"]
    height_cm: float
    weight_kg: float
```

Additional constraints are applied using `Field`.

For example:

```python
age: Annotated[
    int,
    Field(gt=0)
]
```

This prevents invalid values such as:

```json
{
  "age": -5
}
```

Similarly, height and weight must be greater than zero.

Gender is restricted to:

```text
Male
Female
Other
```

---

# 🧮 Computed Fields

BMI and its corresponding verdict are not stored as user-entered values.

They are calculated automatically:

```python
@computed_field
@property
def bmi(self) -> float:
    height_mtr = self.height_cm / 100
    return round(self.weight_kg / (height_mtr ** 2), 2)
```

The verdict is then derived from the BMI:

```python
@computed_field
@property
def verdict(self) -> str:
    if self.bmi < 18.5:
        return "Underweight"
    elif self.bmi < 25:
        return "Normal"
    elif self.bmi < 30:
        return "Overweight"
    else:
        return "Obese"
```

This keeps derived values consistent with the patient's height and weight.

---

# 🔄 API Flow

The basic backend flow is:

```text
Client
  │
  ▼
FastAPI Endpoint
  │
  ▼
Pydantic Validation
  │
  ▼
Load Patient Data
  │
  ├── Create
  ├── Read
  ├── Update
  └── Sort
  │
  ▼
Recalculate BMI / Verdict
  │
  ▼
Save Data
  │
  ▼
JSON Response
```

---

# ▶️ Running the Project

## 1. Clone the repository

```bash
git clone <your-repository-url>
cd patient-data-management
```

## 2. Create a virtual environment

### Windows

```bash
python -m venv myenv
myenv\Scripts\activate
```

### Linux/macOS

```bash
python3 -m venv myenv
source myenv/bin/activate
```

## 3. Install dependencies

```bash
pip install fastapi uvicorn pydantic
```

Or, if a `requirements.txt` file is available:

```bash
pip install -r requirements.txt
```

## 4. Start the server

If the FastAPI application is in `main.py`:

```bash
uvicorn main:app --reload
```

The API will normally be available at:

```text
http://127.0.0.1:8000
```

---

# 📚 Interactive API Documentation

FastAPI automatically provides interactive documentation.

### Swagger UI

```text
http://127.0.0.1:8000/docs
```

### ReDoc

```text
http://127.0.0.1:8000/redoc
```

Swagger UI can be used to test all endpoints without building a separate client.

---

# 🧪 Example API Workflow

A typical workflow could look like:

```text
1. POST /create
       │
       ▼
2. Patient is validated
       │
       ▼
3. Patient is saved
       │
       ▼
4. GET /patient/p001
       │
       ▼
5. View patient information
       │
       ▼
6. PUT /edit/p001
       │
       ▼
7. Update selected fields
       │
       ▼
8. BMI + verdict are recalculated
       │
       ▼
9. GET /sort?sort_by=bmi&order=desc
```

---

# ⚠️ Current Limitations

This is currently a **backend-focused learning/project implementation**.

Current limitations include:

- No frontend/UI has been implemented yet.
- Data is currently persisted using JSON rather than a production database.
- Authentication and authorization are not implemented.
- No role-based access control.
- No advanced search/filtering system.
- No automated testing suite yet.
- Error handling can be expanded further.
- The API is not intended for handling real patient/medical data in its current form.

---

# 🔮 Future Improvements

Planned/improvable areas include:

### Frontend

- Build a modern web frontend.
- Patient dashboard.
- Patient creation form.
- Patient editing interface.
- Patient search and filtering.
- Sortable patient table.
- BMI visualization.

### Backend

- Move from JSON storage to a database such as PostgreSQL.
- Add SQLAlchemy/SQLModel.
- Add authentication and authorization.
- Add pagination.
- Add advanced filtering and searching.
- Improve API response schemas.
- Add automated unit and integration tests.
- Add structured logging.
- Add better exception handling.

### Deployment

- Dockerize the application.
- Deploy the API to a cloud platform.
- Configure production environment variables.
- Add CI/CD using GitHub Actions.

---

# 🎯 Learning Objectives

This project was developed to practice:

- FastAPI fundamentals
- REST API design
- HTTP methods and status codes
- Path parameters
- Query parameters
- Request body validation
- Pydantic `BaseModel`
- Pydantic `Field`
- `Annotated` types
- `Literal` types
- Optional fields
- Pydantic `computed_field`
- Partial updates using `exclude_unset=True`
- Exception handling with `HTTPException`
- JSON data persistence
- API documentation with Swagger UI

---

# 📌 Project Status

**Backend:** ✅ Implemented

**Patient CRUD-style operations:** ✅ Implemented

**Validation:** ✅ Implemented

**BMI calculation:** ✅ Implemented

**Sorting:** ✅ Implemented

**Interactive API documentation:** ✅ Available through FastAPI

**Frontend:** 🚧 Not implemented yet

> The frontend and additional features will be added/improved in future iterations.

---

## 👨‍💻 Author

**Rajesh Phulwaria**

This project was created as a practical FastAPI/Pydantic project for learning backend API development and data validation.

---

## ⭐ Future Vision

The goal is to evolve this project from a simple FastAPI learning project into a more complete **Patient Data Management System**, with a dedicated frontend, database-backed persistence, authentication, testing, deployment, and a cleaner production-ready architecture.
