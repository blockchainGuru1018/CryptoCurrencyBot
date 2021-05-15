import React, {Component} from "react";
import "../loadingScreen.css";
class LoadingScreen extends Component {
    constructor(props) {
        super(props);
    }
    render() {
        return <div class="rainbowContainer">
            <h1 class="title">Loading</h1>
            <div class="rainbow-marker-loader"></div>
    </div>
    }
}

export default LoadingScreen;