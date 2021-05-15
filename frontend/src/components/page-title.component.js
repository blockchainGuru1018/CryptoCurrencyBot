import React from "react";


const PageTitle = (props) => {
    return (
        <div className="page-title mb-5">
            <h5 className="text-left">{props.title}</h5>
        </div>
    )
}

export default PageTitle;