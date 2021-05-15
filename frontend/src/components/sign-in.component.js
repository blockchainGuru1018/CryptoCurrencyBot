import React, { Component } from 'react';
import Form from "react-validation/build/form";
import { Redirect } from "react-router-dom";

import { connect } from "react-redux";
import { login } from "../actions/auth";

import Button from '@material-ui/core/Button';
import CssBaseline from '@material-ui/core/CssBaseline';
import Typography from '@material-ui/core/Typography';
import Container from '@material-ui/core/Container';
import CheckButton from "react-validation/build/button";
import { Input } from '@material-ui/core';

import { FaSignInAlt } from "react-icons/fa";
import { GiDiamondsSmile } from "react-icons/gi";
import { BouncingCoin } from "./bounceCoin.component";
class Login extends Component {

    constructor(props) {
        super(props);
        this.handleLogin = this.handleLogin.bind(this);
        this.onChangeEmail = this.onChangeEmail.bind(this);
        this.onChangePassword = this.onChangePassword.bind(this);
        this.state = {
            password: "",
            email: "",
            loading: false,
        };
    }

    onChangeEmail(e) {
        /* Setter for state email */
        this.setState({email: e.target.value});
    }

    onChangePassword(e) {
        /* Setter for state password */
        this.setState({password: e.target.value});
    }

    handleLogin(e) {
        e.preventDefault();
        this.setState({loading: true,});
        this.form.validateAll();
        const { dispatch, history } = this.props;
        if (this.checkBtn.context._errors.length === 0) {
            dispatch(login(this.state.email, this.state.password))
                .then(() => {
                    history.push("/dashboard");
                    window.location.reload();
                })
                .catch(() => {
                    this.setState({
                        loading: false
                    });
                });
        } else {
            this.setState({
                loading: false,
            });
        }
    }

    render() {
        const { user: current_user } = this.props;
        
        if (current_user) {
            console.log(current_user)
            return <Redirect to="/home" />;
        }
        
        return (
            <Container component="main" maxWidth="xs" className="pt-5">
                <CssBaseline />
                <div className="d-flex flex-column align-items-center">
                        <span style={{color: "white", fontSize: "2em"}}><GiDiamondsSmile /></span>
                    <Typography component="h1" variant="h5" color="textPrimary">
                    CryptoBot
                    </Typography>
                    <Form className="form-login" onSubmit={this.handleLogin} ref={c => {this.form = c;}} style={{marginTop:"5px"}}>
            <h4>Login</h4>
                        <Input
                            className="form-control"
                            required
                            fullWidth
                            value={this.state.email}
                            onChange={this.onChangeEmail}
                            id="email"
                            label="Email Address"
                            name="email"
                            type="email"
                            placeholder="Email"
                            style={{height: "35px", padding: "3px"}}
                        />
                        <Input
                            className="form-control"
                            required
                            fullWidth
                            value={this.state.password}
                            onChange={this.onChangePassword}
                            name="password"
                            type="password"
                            id="password"
                            autoComplete="current-password"
                            placeholder="Password"
                            style={{marginTop: "3%", height: "35px", padding: "3px"}}
                        />
            <div className="wrapper">
                        <Button
                            type="submit"
                            fullWidth
                            size="medium"
                            variant="contained"
                            startIcon={<FaSignInAlt />}
            style={{ marginTop: "10px" }}
                            className="btn btn-danger btn-md">
                            Sign In <i class="fa fa-sign-in"></i>
                            
                        </Button>
            </div>
                        <CheckButton style={{ display: "none" }} ref={c => {this.checkBtn = c;}}/>
                    </Form>
                </div>
                <div class="stage">
            <div class="bitcoin bounce-7"></div>
    </div>
            </Container>
        );
    }
}


function mapStateToProps(state) {
    const { isLoggedIn } = state.auth;
    const { message } = state.message;
    return {isLoggedIn, message};
}


export default connect(mapStateToProps)(Login)