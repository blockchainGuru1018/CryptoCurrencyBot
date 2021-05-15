import axios from "axios";

import { environment } from "../environment";


const LOGIN_URL = `${environment.apiUrl}/accounts/login`;


class AuthService {
    
    login(email, password) {
        var data = {email: email, password: password}
        return axios.post(LOGIN_URL, data)
            .then(resp => {
                debugger
                if (resp.data.refresh) {
                    localStorage.setItem("user", JSON.stringify(resp.data))
                }
                return resp.data
            }
        )
    }

    logout() {
        localStorage.removeItem("user");
    }

    get_current_user() {
        return JSON.parse(localStorage.getItem('user'));
    }

    decode_user() {
        try { 
            var user = this.get_current_user();
            return JSON.parse(atob(user.refresh.split('.')[1]));
            
        } catch (error) {
            return {};
        }
    
    }

}

export default new AuthService();