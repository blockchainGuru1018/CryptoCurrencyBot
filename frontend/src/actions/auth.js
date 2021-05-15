import {
    LOGIN_SUCCESS,
    LOGIN_FAIL,
    LOGOUT,
    SET_MESSAGE,
} from "./types";


import AuthService from "../services/auth.service";


export const login = (email, password) => (dispatch) => {
    
    return AuthService.login(email, password).then((data) => {
        /* Success Action */
        dispatch({
            type: LOGIN_SUCCESS, 
            payload: { user: data },
        });
        return Promise.resolve();
    },
    (error) => {
        /* Error action */
        const message = (error.response &&
                    error.response.data &&
                    error.response.data.message) ||
                    error.message ||
                    error.toString();

        dispatch({type: LOGIN_FAIL});
        dispatch({type: SET_MESSAGE, payload: message});

        return Promise.reject();
    }); /* End of service use. */

};


export const logout = () => (dispatch) => {
    /* Logout action */
    AuthService.logout();
    dispatch({type: LOGOUT});

};