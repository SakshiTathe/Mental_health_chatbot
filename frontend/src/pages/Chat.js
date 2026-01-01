import React, { useState } from 'react'
import Chats_Info from './Chatbot/Chats_Info';
import ChatBot from './Chatbot/Chatsrooms';
import Layout from '../components/Layout/Layout';
import { LuSquareArrowLeft } from "react-icons/lu";

export const Chat= () => {
    const [sidebarVisible, setSidebarVisible] = useState(true);
    const [selectedChat, setSelectedChat] = useState([]);
    return (
        <Layout title={"chat"}>
            <div className="main-container">
                {/* Sidebar */}
                <div className={`sidebar ${sidebarVisible ? "visible" : "collapsed"}`}>
                    <Chats_Info setSelectedChat={setSelectedChat}/>

                <button className={`toggle-sidebar-btn ${sidebarVisible ? "expanded" : "collapsed"}`} onClick={() => setSidebarVisible(!sidebarVisible)}>
                    {sidebarVisible ? <LuSquareArrowLeft/> : "☰"}
                </button>
                </div>

                {/* Chat area */}
                <div className="chat-wrapper">
                    <div className="chat-centered d d-flex align-items-center justify-content-end">
                        <ChatBot selectedChat={selectedChat} />
                    </div>
                </div>
            </div>
        </Layout>
    );
}
