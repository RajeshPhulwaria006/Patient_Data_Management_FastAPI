from pydantic import BaseModel, computed_field, Field
from typing import Annotated, Literal, Optional

class Patient(BaseModel):
    """Schema to validate patient's data"""
    id: Annotated[str,
        Field(...,
            description="Enter patient's id, should be unique among existing."
        )
    ]
    name: Annotated[str,
        Field(...,
            max_length=50,
            title="Name of the patient.",
            description="Write patient's name in 50 characters."
        )
    ]
    age: Annotated[int,
        Field(...,
            gt=0,
            description="Enter patient's age."
        )
    ]
    city: Annotated[str,
        Field(...,
            description="Enter city of the patient."
        )
    ]
    gender: Annotated[
        Literal['Male','Female', 'Other'],
        Field(...,
            description="Enter patient's gender."
        )
    ]
    height_cm: Annotated[float,
        Field(...,
            gt=0,
            description="Enter patient's height in centimeters."
        )
    ]
    weight_kg: Annotated[float,
        Field(...,
            gt=0,
            description="Enter patient's weight in kilograms."
        )
    ]

    @computed_field
    @property
    def bmi(self) -> float:
        height_mtr = self.height_cm / 100
        bmi = round(self.weight_kg / (height_mtr**2), 2)
        return bmi
    
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
        

class PatientUpdate(BaseModel):
    """Schema to validate patient's data for update"""
    name: Annotated[
        Optional[str],
        Field(default=None)
    ]
    age: Annotated[
        Optional[int],
        Field(default=None, gt=0)
    ]
    city: Annotated[
        Optional[str],
        Field(default=None)
    ]
    gender: Annotated[
        Optional[Literal['Male', 'Female', 'Other']],
        Field(default=None)
    ]
    height_cm: Annotated[
        Optional[float],
        Field(default=None, gt=0)
    ]
    weight_kg: Annotated[
        Optional[float],
        Field(default=None, gt=0)
    ]
    