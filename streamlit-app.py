import streamlit as st
import requests
import pandas as pd


# CONFIG
API_BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Patient Data Management",
    page_icon="🏥",
    layout="wide"
)


# API HELPERS
def api_get(endpoint, params=None):
    try:
        response = requests.get(
            f"{API_BASE_URL}{endpoint}",
            params=params,
            timeout=10
        )

        if response.status_code == 200:
            return response.json(), None

        try:
            error = response.json().get("detail", "Unknown error")
        except Exception:
            error = response.text

        return None, error

    except requests.exceptions.ConnectionError:
        return None, "Cannot connect to FastAPI server."

    except requests.exceptions.Timeout:
        return None, "API request timed out."

    except Exception as e:
        return None, str(e)


def api_post(endpoint, data):
    try:
        response = requests.post(
            f"{API_BASE_URL}{endpoint}",
            json=data,
            timeout=10
        )

        if response.status_code in [200, 201]:
            return response.json(), None

        try:
            error = response.json().get("detail", "Unknown error")
        except Exception:
            error = response.text

        return None, error

    except requests.exceptions.ConnectionError:
        return None, "Cannot connect to FastAPI server."

    except Exception as e:
        return None, str(e)


def api_put(endpoint, data):
    try:
        response = requests.put(
            f"{API_BASE_URL}{endpoint}",
            json=data,
            timeout=10
        )

        if response.status_code == 200:
            return response.json(), None

        try:
            error = response.json().get("detail", "Unknown error")
        except Exception:
            error = response.text

        return None, error

    except requests.exceptions.ConnectionError:
        return None, "Cannot connect to FastAPI server."

    except Exception as e:
        return None, str(e)


def api_delete(endpoint):
    try:
        response = requests.delete(
            f"{API_BASE_URL}{endpoint}",
            timeout=10
        )

        if response.status_code == 200:
            return response.json(), None

        try:
            error = response.json().get("detail", "Unknown error")
        except Exception:
            error = response.text

        return None, error

    except requests.exceptions.ConnectionError:
        return None, "Cannot connect to FastAPI server."

    except Exception as e:
        return None, str(e)


# SIDEBAR
st.sidebar.title("🏥 Patient Management")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Find Patient",
        "Create Patient",
        "Update Patient",
        "Delete Patient",
        "Sort Patients"
    ]
)

st.sidebar.divider()

st.sidebar.caption("FastAPI Backend")
st.sidebar.code(API_BASE_URL)

# Header
st.title("🏥 Patient Data Management System")
st.caption("Streamlit frontend • FastAPI backend")


# DASHBOARD
if page == "Dashboard":

    st.header("Dashboard")

    data, error = api_get("/view")

    if error:
        st.error(error)
        st.info(
            "Make sure your FastAPI server is running, for example:\n\n"
            "`uvicorn main:app --reload`"
        )
        st.stop()

    if not data:
        st.warning("No patient records found.")
        st.stop()

    # Convert dictionary into DataFrame
    rows = []

    for patient_id, patient in data.items():

        row = {
            "ID": patient_id,
            **patient
        }

        rows.append(row)

    df = pd.DataFrame(rows)

    # Metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Patients", len(df))

    with col2:
        if "age" in df.columns:
            st.metric(
                "Average Age",
                f"{df['age'].mean():.1f}"
            )
        else:
            st.metric("Average Age", "N/A")

    with col3:
        if "bmi" in df.columns:
            st.metric(
                "Average BMI",
                f"{df['bmi'].mean():.2f}"
            )
        else:
            st.metric("Average BMI", "N/A")

    with col4:
        if "gender" in df.columns:
            st.metric(
                "Gender Records",
                df["gender"].nunique()
            )
        else:
            st.metric("Gender Records", "N/A")

    st.divider()

    st.subheader("Patient Records")

    st.dataframe(
        df,
        width='stretch',
        hide_index=True
    )


# FIND PATIENT
elif page == "Find Patient":

    st.header("🔍 Find Patient")

    patient_id = st.text_input(
        "Patient ID",
        placeholder="Example: p001"
    )

    if st.button("Search Patient", type="primary"):

        if not patient_id:
            st.warning("Please enter a patient ID.")
            st.stop()

        patient, error = api_get(
            f"/patient/{patient_id}"
        )

        if error:
            st.error(error)
        else:

            st.success("Patient found!")

            st.subheader(f"Patient: {patient_id}")

            col1, col2 = st.columns(2)

            with col1:

                st.write("### Personal Information")

                st.write(
                    f"**Name:** {patient.get('name', 'N/A')}"
                )

                st.write(
                    f"**Age:** {patient.get('age', 'N/A')}"
                )

                st.write(
                    f"**Gender:** {patient.get('gender', 'N/A')}"
                )

                st.write(
                    f"**City:** {patient.get('city', 'N/A')}"
                )

            with col2:

                st.write("### Physical Information")

                st.write(
                    f"**Height:** {patient.get('height_cm', 'N/A')} cm"
                )

                st.write(
                    f"**Weight:** {patient.get('weight_kg', 'N/A')} kg"
                )

                st.write(
                    f"**BMI:** {patient.get('bmi', 'N/A')}"
                )

                st.write(
                    f"**Verdict:** {patient.get('verdict', 'N/A')}"
                )


# CREATE PATIENT
elif page == "Create Patient":

    st.header("➕ Create Patient")

    with st.form("create_patient_form"):

        col1, col2 = st.columns(2)

        with col1:

            patient_id = st.text_input(
                "Patient ID *",
                placeholder="p001"
            )

            name = st.text_input(
                "Name *"
            )

            age = st.number_input(
                "Age *",
                min_value=0,
                max_value=150,
                value=25
            )

            gender = st.selectbox(
                "Gender *",
                [
                    "Male",
                    "Female",
                    "Other"
                ]
            )

            city = st.text_input(
                "City *"
            )

        with col2:

            height = st.number_input(
                "Height (cm) *",
                min_value=1.0,
                max_value=250.0,
                value=170.0
            )

            weight = st.number_input(
                "Weight (kg) *",
                min_value=1.0,
                max_value=500.0,
                value=65.0
            )

            bmi = weight / ((height / 100) ** 2)

            st.metric(
                "Calculated BMI",
                f"{bmi:.2f}"
            )

            verdict = st.text_input(
                "Verdict",
                placeholder="Normal"
            )

        submitted = st.form_submit_button(
            "Create Patient",
            type="primary"
        )

    if submitted:

        if not patient_id or not name or not city:
            st.warning(
                "Please fill all required fields."
            )
            st.stop()

        patient_data = {
            "id": patient_id,
            "name": name,
            "age": age,
            "city": city,
            "gender": gender,
            "height_cm": height,
            "weight_kg": weight,
            "bmi": round(bmi, 2),
            "verdict": verdict
        }

        result, error = api_post(
            "/create",
            patient_data
        )

        if error:
            st.error(error)
        else:
            st.success(
                result.get(
                    "message",
                    "Patient created successfully."
                )
            )


# UPDATE PATIENT
elif page == "Update Patient":

    st.header("✏️ Update Patient")

    patient_id = st.text_input(
        "Patient ID",
        placeholder="Example: p001"
    )

    if st.button("Load Patient"):

        if not patient_id:
            st.warning("Enter a patient ID.")
            st.stop()

        patient, error = api_get(
            f"/patient/{patient_id}"
        )

        if error:
            st.error(error)
        else:

            st.session_state["patient_to_update"] = patient
            st.session_state["update_id"] = patient_id

    if "patient_to_update" in st.session_state:

        patient = st.session_state["patient_to_update"]

        st.divider()

        st.subheader(
            f"Editing: {st.session_state['update_id']}"
        )

        with st.form("update_patient_form"):

            col1, col2 = st.columns(2)

            with col1:

                name = st.text_input(
                    "Name",
                    value=patient.get("name", "")
                )

                age = st.number_input(
                    "Age",
                    min_value=0,
                    max_value=150,
                    value=int(patient.get("age", 0))
                )

                city = st.text_input(
                    "City",
                    value=patient.get("city", "")
                )

                gender = st.selectbox(
                    "Gender",
                    [
                        "Male",
                        "Female",
                        "Other"
                    ],
                    index=[
                        "Male",
                        "Female",
                        "Other"
                    ].index(
                        patient.get("gender", "Male")
                    )
                    if patient.get("gender", "Male")
                    in ["Male", "Female", "Other"]
                    else 0
                )

            with col2:

                height = st.number_input(
                    "Height (cm)",
                    min_value=1.0,
                    max_value=250.0,
                    value=float(
                        patient.get("height_cm", 170)
                    )
                )

                weight = st.number_input(
                    "Weight (kg)",
                    min_value=1.0,
                    max_value=500.0,
                    value=float(
                        patient.get("weight_kg", 65)
                    )
                )

                bmi = weight / ((height / 100) ** 2)

                st.metric(
                    "Calculated BMI",
                    f"{bmi:.2f}"
                )

                verdict = st.text_input(
                    "Verdict",
                    value=patient.get(
                        "verdict",
                        ""
                    )
                )

            update = st.form_submit_button(
                "Update Patient",
                type="primary"
            )

        if update:

            update_data = {
                "name": name,
                "age": age,
                "city": city,
                "gender": gender,
                "height_cm": height,
                "weight_kg": weight,
                "bmi": round(bmi, 2),
                "verdict": verdict
            }

            result, error = api_put(
                f"/edit/{st.session_state['update_id']}",
                update_data
            )

            if error:
                st.error(error)
            else:

                st.success(
                    result.get(
                        "message",
                        "Patient updated successfully."
                    )
                )

                del st.session_state[
                    "patient_to_update"
                ]

                st.rerun()


# DELETE PATIENT
elif page == "Delete Patient":

    st.header("🗑️ Delete Patient")

    patient_id = st.text_input(
        "Patient ID",
        placeholder="Example: p001"
    )

    if st.button(
        "Delete Patient",
        type="primary"
    ):

        if not patient_id:
            st.warning("Enter a patient ID.")
            st.stop()

        result, error = api_delete(
            f"/remove/{patient_id}"
        )

        if error:
            st.error(error)
        else:
            st.success(
                result.get(
                    "message",
                    "Patient deleted successfully."
                )
            )

# SORT PATIENTS
elif page == "Sort Patients":

    st.header("↕️ Sort Patients")

    col1, col2 = st.columns(2)

    with col1:

        sort_by = st.selectbox(
            "Sort by",
            [
                "age",
                "height_cm",
                "weight_kg",
                "bmi"
            ]
        )

    with col2:

        order = st.selectbox(
            "Order",
            [
                "asc",
                "desc"
            ]
        )

    if st.button(
        "Sort",
        type="primary"
    ):

        patients, error = api_get(
            "/sort",
            params={
                "sort_by": sort_by,
                "order": order
            }
        )

        if error:
            st.error(error)

        else:

            st.success(
                f"Sorted by {sort_by} ({order})."
            )

            df = pd.DataFrame(patients)

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )