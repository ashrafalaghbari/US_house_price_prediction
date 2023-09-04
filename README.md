# US House Price Prediction API

## Instructions for Cloning, Loading, and Testing

### 1. **Cloning the GitHub Repository:**
Start by cloning the desired GitHub repository to your local machine. Navigate to your preferred directory in your terminal or command prompt and execute:
```bash
git clone https://github.com/ashrafalaghbari/US_house_price_prediction.git
```
After cloning, navigate into the repository's directory:

```bash
cd [REPOSITORY_NAME]
```
### 2. **Loading the Docker Image:**
load the image using:
```bash
docker load -i us_house_price_prediction.tar
```

### 3. **Running the API:**
Run the API using the following command:
```bash
docker run -d -p 8000:8000 us_house_price_prediction:0.1.0
```
### 4. **Testing the API:**
The sample_input.json file contains sample input data that the API expects. To test the API endpoint with this sample input, navigate to the directory containing the `sample_input.json` file and execute:
```bash
curl -X POST -H "Content-Type: application/json" -d @sample_input.json http://localhost:8000/predict/
```
