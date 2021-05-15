import React, { Component } from "react";
import { connect } from "react-redux"
import { Router, Route, Switch } from "react-router-dom";
import { logout } from "./actions/auth";
import { clearMessage } from "./actions/messages";
import { history } from './helpers/history';
import { Container, Row } from "react-bootstrap";

import "bootstrap/dist/css/bootstrap.min.css";
import "./App.css";

import Header from "./components/header.component";
import Dashboard  from "./components/dashboard.component";
import NotFound from "./components/not-found.component";
import Login from "./components/sign-in.component";
import InterexchangeArbitrageComponent from "./components/interexchange-arbitrage.component";
import TriangularArbitrageComponent from "./components/triangular-arbitrage.component";
import BacktestArbitrageComponent from "./components/backtest-arbitrage.component";


class App extends Component {

    constructor(props) {
        super(props);
        this.log_out = this.log_out.bind(this);
        this.state = {
            current_user: undefined
        };
        history.listen((location) => {
            props.dispatch(clearMessage());
        });
    }


    componentDidMount() {
        const user = this.props;
        if (user) {
            this.setState({current_user: user});
        }
    }


    log_out() {
        this.props.dispatch(logout());
    }


    render() {
        const { user: current_user } = this.props;
        
        return (
            <>
                <Router history={history}>
                    {/* Header */}
                    <Header current_user={current_user} log_out={this.log_out} />
                    <div>
                        <Container fluid className="pt-5 main-wrapper">
                            <Row>
                            { current_user ? ( 
                                <>
                                    <Switch>
                                        <Route
                                            exact  
                                            path={["/home", "/dashboard"]} 
                                            component={Dashboard} />
                                        <Route
                                            exact
                                            path={["/inter-exchange-arbitrage"]} 
                                            component={InterexchangeArbitrageComponent} />
                                        <Route
                                            exact
                                            path={["/triangular-exchange-arbitrage"]} 
                                            component={TriangularArbitrageComponent} />
                                        <Route
                                            exact
                                            path={["/backtest-exchange-arbitrage"]}
                                            component={BacktestArbitrageComponent} />
                                    </Switch>
                                </>
                            ) : (
                                <>
                                    <Switch>
                                        <Route
                                            exact
                                            path={["/", "/login"]} 
                                            component={Login} />
                                        <Route component={NotFound} />
                                    </Switch>
                                </>
                            )}
                            </Row>
                        </Container>
                    </div>
                </Router>
            </>
        
		);
	};
}


function mapStateToProps(state) {
    const { user } = state.auth;
    return {
      user,
    };
}
  
export default connect(mapStateToProps)(App);

