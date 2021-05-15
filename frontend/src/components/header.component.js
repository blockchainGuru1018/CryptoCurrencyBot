import React from "react";
import { Link } from "react-router-dom";

import SideBarNav from "./side-nav.component";


const Header = (props) => {
    const current_user = props.current_user
    return (
        <nav className="navbar navbar-expand border-bottom border-dark bg-dark">
            <Link to={current_user ? "/dashboard" : "/login"} className="navbar-brand">
                CryptoBot
            </Link>
            { current_user ?  (
                <div className="navbar-nav ml-auto">
                    <li className="nav-item">
                        <SideBarNav current_user={current_user} log_out={props.log_out}/>
                    </li>
                </div>
            ) : (<></>)}    
        </nav>
    )
}

export default Header;