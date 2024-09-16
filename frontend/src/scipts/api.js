import axios from 'axios';

const API_URL = 'http://localhost:8000';

export const registerUser = async (userData) => {
  try {
    const response = await axios.post(`${API_URL}/register`, userData);
    return response.data;
  } catch (error) {
    throw new Error(error.response.data.detail || error.message);
  }
};

export const loginUser = async (credentials) => {
  try {
    const response = await axios.post(`${API_URL}/token`, credentials);
    return response.data;
  } catch (error) {
    throw new Error(error.response.data.detail || error.message);
  }
};
