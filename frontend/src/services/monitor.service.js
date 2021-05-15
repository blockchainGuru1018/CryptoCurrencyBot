import axios from "axios"
import authHeader from './auth-header';

import { environment } from "../environment";

const API_URL = `${environment.apiUrl}/api/v1/arbitrage`;

axios.interceptors.response.use(response => {
   return response;
}, error => {
  if (error.response && error.response.status === 401) {
   window.location.href = "/login";
  }
   // handle other error status codes.
  return error;
});

class MonitorService {
    
    triangular_exchange_monitor(action) {
        return axios.post(
            `${API_URL}/triangular-monitor`, 
            {action: action}, 
            {headers: authHeader()}
        )
    }

    inter_exchange_monitor(action) {
        return axios.post(
            `${API_URL}/inter-exchange-monitor`,
            {action: action}, 
            {headers: authHeader()}
        )
    }

    strategy_exchange_monitor(action) {
        return axios.post(
            `${API_URL}/strategy-bt-monitor`,
            {action: action},
            {headers: authHeader()}
        )
    }

 
}

export default new MonitorService();