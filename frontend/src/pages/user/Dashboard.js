import React from "react";
import Layout from "../../components/Layout/Layout";
import { useAuth } from "../../context/auth";
import EmotionShow from "../Chatbot/EmotionDashboard";
const Dashboard = () => {
    return (
        <Layout title={"Dashboard"}>
            <div className="container-fluid m-3 p-3">
                <div className="row">
                    <div className="col-md-11">
                        <EmotionShow/>
                    </div>
                </div>
            </div>
        </Layout>
    );
};

export default Dashboard;
