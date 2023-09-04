#import the necessary packages
from fastapi import FastAPI, HTTPException, Body
import joblib
import pandas as pd

# Initialize FastAPI app
app = FastAPI()

# Load the trained model
model = joblib.load('model.joblib')

def format_feature_title(title: str) -> str:
    """
    Formats a given string into a custom title.

    Steps:
    1. Replace underscores with spaces.
    2. Capitalize each word, except for 'of'.
    3. Replace "Avg" with "Avg.".
    4. Prefix with "feat_".

    Args:
    title (str): The string to be formatted.

    Returns:
    str: The formatted string.
    """
    # List of words that should remain in lowercase in the title.
    lowercase_words = ["of"]
    
    # Replace underscores with spaces for better readability.
    title = title.replace("_", " ")
    
    # Split the string into words and capitalize each word, except for words in LOWERCASE_WORDS.
    title = " ".join([word if word in lowercase_words else word.title() for word in title.split()])
    
    # Add a period after "Avg" for clarity.
    title = title.replace("Avg", "Avg.")
    
    # Prefix the string with "feat_" as per custom requirements.
    title = "feat_" + title

    return title


@app.get("/", response_model=dict)
def health_check() -> dict:
    """
    Check the health status of the API.
    Returns a status indicating if the API is operational.
    """
    try:       
        return {"status": "ok", "code": 200}
    
    except Exception:
        # 500 indicates Internal Server Error
        raise HTTPException(status_code=500, detail="API is not healthy.")

@app.post("/predict/")
def predict_endpoint(data: dict = Body(...)):
    """
    Endpoint to predict housing prices based on provided features.
    
    The function transforms feature keys, constructs a DataFrame from the features, and 
    uses a pre-loaded model to predict the housing price. The resulting prediction, 
    transformed features, and provider data are returned in the response.
    
    Args:
    - data (dict): A dictionary containing features for prediction and provider information. 
                   Expected keys are 'features' and 'provider'.
                   
    Returns:
    - dict: A dictionary containing the transformed features, predicted output, and provider name.
    
    Raises:
    - HTTPException: If any expected columns are missing in the input data.
    """
    features = data['features']
    provider = data['provider']

    # Transform feature names to match those used during Xgboost model training
    transformed_feat_names = {format_feature_title(key): value for key, value in features.items()}

    # Convert data to DataFrame
    df = pd.DataFrame([transformed_feat_names])

    try:
        # Predict using the pre-loaded model
        prediction = model.predict(df)

        # Construct the response format
        response = {
            "features": features,
            "output": float(f"{prediction[0]:.1f}"),
            "provider": provider
        }

        return response

    except KeyError as e:
        # Extract the missing column name from the exception
        missing_column = str(e).split("'")[1]
        # 400 indicates that the server cannot or will not process the request due to client error. 
        raise HTTPException(status_code=400, 
                            detail=f"The column '{missing_column}' is missing in the DataFrame.") 