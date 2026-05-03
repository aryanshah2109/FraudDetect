//   
//  FraudDetect — API Configuration
//  Edit this file to switch between local and deployed backend.
//
//  LOCAL:    http://localhost:8000
//  DEPLOYED: https://frauddetect-backend-jpgf.onrender.com
//   

const ENV = {
  
  API_BASE_URL: 'http://localhost:8000',

  get PREDICT_URL()   { return this.API_BASE_URL + '/predict/'; },
  get ARTIFACTS_URL() { return this.API_BASE_URL + '/artifacts/'; },
};

Object.freeze(ENV);
