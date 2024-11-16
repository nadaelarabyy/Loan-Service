import { useState, useEffect } from "react";
import api from "../api";
import Fund from "../components/Fund";
import "../styles/Home.css";

function Home() {
    const [funds, setFunds] = useState([]);
    const [minimum, setMin] = useState("");
    const [maximum, setMax] = useState("");
    const [duration, setDuration] = useState("");
    const [interest, setInterest] = useState("");

    useEffect(() => {
        getFunds();
    }, []);

    const getFunds = () => {
        api
            .get("/api/funds/")
            .then((res) => res.data)
            .then((data) => {
                setFunds(data);
                console.log(data);
            })
            .catch((err) => alert(err.message || JSON.stringify(err)));
    };

    const deleteFund = (id) => {
        api
            .delete(`/api/funds/delete/${id}/`)
            .then((res) => {
                if (res.status === 204) {
                    alert("Fund deleted!");
                    getFunds(); // Refresh funds list
                } else {
                    alert("Failed to delete fund.");
                }
            })
            .catch((err) => alert(err.message || JSON.stringify(err)));
    };

    const createFund = (e) => {
        e.preventDefault();
        api
            .post("/api/funds/", { min: minimum, max: maximum, interest, duration })
            .then((res) => {
                if (res.status === 201) {
                    alert("Fund created!");
                    getFunds(); // Refresh funds list
                } else {
                    alert("Failed to create fund.");
                }
            })
            .catch((err) => alert(err.message || JSON.stringify(err)));
    };

    return (
        <div>
            <div>
                <h2>Funds</h2>
                {funds.map((fund) => (
                    <Fund fund={fund} onDelete={deleteFund} key={fund.id} />
                ))}
            </div>
            <h2>Create a Fund</h2>
            <form onSubmit={createFund}>
                <label htmlFor="min">Minimum value:</label>
                <br />
                <input
                    type="number"
                    id="min"
                    name="minimum"
                    required
                    onChange={(e) => setMin(e.target.value)}
                    value={minimum}
                />
                <br />
                <label htmlFor="max">Maximum value:</label>
                <br />
                <input
                    type="number"
                    id="max"
                    name="maximum"
                    required
                    onChange={(e) => setMax(e.target.value)}
                    value={maximum}
                />
                <br />
                <label htmlFor="interest">Interest rate:</label>
                <br />
                <input
                    type="number"
                    id="interest"
                    name="interest"
                    required
                    onChange={(e) => setInterest(e.target.value)}
                    value={interest}
                />
                <br />
                <label htmlFor="duration">Duration:</label>
                <br />
                <input
                    type="number"
                    id="duration"
                    name="duration"
                    required
                    onChange={(e) => setDuration(e.target.value)}
                    value={duration}
                />
                <br />
                <input type="submit" value="Submit" />
            </form>
        </div>
    );
}

export default Home;
