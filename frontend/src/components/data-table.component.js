import React from "react";
import { DataGrid } from '@material-ui/data-grid';


const DataTable = (props) => {
    return (
      	<div className="tableContainer">
        	<DataGrid rows={props.rows} columns={props.columns} pageSize={25} checkboxSelection />
      	</div>
    );
}


export default DataTable;
