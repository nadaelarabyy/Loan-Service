import React from "react";
import "../styles/Fund.css"

function Fund({ fund, onDelete }) {
    const formattedDate = new Date(fund.createdAt).toLocaleDateString("en-US")

    return (
        <div className="fund-container">
            <p className="fund-min">Minimum: {fund.min}</p>
            <p className="fund-max">Maximum: {fund.max}</p>
            <p className="fund-interest">Interest: {fund.interest}</p>
            <p className="fund-duration">Duration: {fund.duration}</p>
            <button className="delete-button" onClick={() => onDelete(fund.id)}>
                Delete
            </button>
        </div>
    );
}

export default Fund