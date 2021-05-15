import axios from "axios"
import authHeader from './auth-header';

import { environment } from "../environment";

const API_URL = `${environment.apiUrl}/api/v1/arbitrage`;


class ArbitrageService {
    /* Main arbitrage service */
    get_coinbase_spread_realtime() {
        return axios.get(`${API_URL}/coinbase-realtime`, {headers: authHeader()})
    }

    get_inter_exchange_arbitrage() {
        return axios.get(`${API_URL}/inter-exchange`, {headers: authHeader()})
    }

    get_triangular_exchange_arbitrage() {
        return axios.get(`${API_URL}/triangular-exchange-realtime`, {headers: authHeader()})
    }
    
}

export default new ArbitrageService();