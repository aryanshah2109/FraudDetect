from typing import List, Literal, Annotated
from pydantic import BaseModel, Field, StringConstraints, field_validator
from enum import Enum

class TransactionType(str, Enum):
    CASH_IN = "CASH IN"
    CASH_OUT = "CASH OUT"
    DEBIT = "DEBIT"
    PAYMENT = "PAYMENT"
    TRANSFER = "TRANSFER"


class DetectFraudRequest(BaseModel):
    type: Annotated[TransactionType, Field(title="Type of Transaction", description="Enter type of transaction. Can be any out of: 1. Cash in  2. Cash out  3. Debit  4. Payment  5. Transfer")]
    amount: Annotated[float, Field(title="Amount of Transaction", description="Enter the amount of transaction that you wish to detect", ge=0)]
    oldbalanceOrg: Annotated[float, Field(title="Old Balance of Sender", description="Enter the old balance of sender before transaction occured", ge=0)]
    newbalanceOrig: Annotated[float, Field(title="New Balance of Sender", description="Enter the new balance of sender after transaction occured", ge=0)]
    oldbalanceDest: Annotated[float, Field(title="Old Balance of Reciever", description="Enter the old balance of reciever before transaction occured", ge=0)]
    newbalanceDest: Annotated[float, Field(title="New Balance of Reciever", description="Enter the new balance of sender before transaction occured", ge=0)]
    

    @field_validator("type", mode="before")
    @classmethod
    def check_type(cls, value):
        if isinstance(value, str):
            return value.strip().upper()
        return value

class DetectFraudResponse(BaseModel):
    prediction: Annotated[Literal[0, 1], Field(title="Prediction from model", description="Predicted class (0 = Not fraud, 1 = fraud)")]
    prediction_label : Annotated[Literal["Fraud", "Not Fraud"], Field(title="Prediction label", description="Predicted label (Fraud, Not Fraud)")]
    fraud_probability: Annotated[float, Field(title="Probability of fraud", description="Predicted class (0 = Not fraud, 1 = fraud)")]
    