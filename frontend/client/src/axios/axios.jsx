import axios from 'axios'
import { useAppContext } from '../context/AppContext';

const BASE_URL = `http://127.0.0.1:8000`


export default axios.create({
    baseURL: BASE_URL
});

export const axiosPrivate = axios.create({
    baseURL: BASE_URL,
    headers: { 'Content-Type': 'application/json' },
});