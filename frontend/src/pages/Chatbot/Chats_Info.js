import React, { useState, useEffect } from 'react';
import { LuMessageSquare, LuPlus } from 'react-icons/lu';
import { useAuth } from "../../context/auth"

// Convert timestamp to readable date string like "2025-11-19"
const getDateString = (timestamp) => {
    const date = new Date(timestamp);
    if (isNaN(date)) return "Unknown";
    return date.toISOString().split("T")[0];
};

// Group chats by date
const groupChatsByDay = (chatArray) => {
    const groups = {};

    chatArray.forEach(chat => {
        const dateKey = getDateString(chat.timestamp);
        if (!groups[dateKey]) groups[dateKey] = [];
        groups[dateKey].push(chat);
    });

    return groups;
};

export default function Chats_Info({setSelectedChat }) {
    const [chats, setChats] = useState([]);
    const [auth, setAuth] = useAuth();

    console.log("---------")
    useEffect(() => {
        const fetchChats = async () => {
            try {
                const res = await fetch("http://127.0.0.1:5000/api/v1/allchats", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ user_id: auth.user["_id"] }),
                });
                const data = await res.json();
                console.log("Fetched chats:", data);

                // Assuming your backend returns an array like:
                // [{ message: "...", response: "...", emotionDetected: "..." }]
                if (data.chats && data.chats.length > 0) {
                    const chatHistory = data.chats[0].chatHistory;

                    const sortedChats = chatHistory.sort(
                        (a, b) => new Date(b) - new Date(a)
                    );
                    setChats(sortedChats);
                } else {
                    setChats([]); // no chats
                }
            } catch (err) {
                console.error("Error fetching chats:", err);
            }
        };

        fetchChats();
    }, [auth.user]);
    const chatGroups = groupChatsByDay(chats);
    const sortedDates = Object.keys(chatGroups).sort().reverse(); // most recent first
    console.log("ppppppppppp")

    return (
        <div className="sidebar vh-90 p-3" style={{ backgroundColor: "#9bcfd7ff" }}>
            <button
                className="btn btn-outline-light w-70 d-flex align-items-center justify-content-start mb-3"
                style={{ borderColor: "#4a90e2" }}
            >
                {/* <LuPlus /> */}
                <span style={{ color: "black" }}>Your Chats</span>
            </button>
            <div className="d-flex flex-column gap-2">
                {sortedDates.length === 0 ? (
                    <div style={{ color: "gray" }}>No chats yet</div>
                ) : (
                    sortedDates.map(date => (
                        <div key={date} className="mb-3 cursor-pointer" onClick={() => setSelectedChat(chatGroups[date])}>
                            <div className="text-secondary  small mb-2 px-2">
                                {(() => {
                                    const today = new Date();
                                    const yesterday = new Date();
                                    yesterday.setDate(yesterday.getDate() - 1);

                                    const target = new Date(date);

                                    if (target.toDateString() === today.toDateString()) return "Today";
                                    if (target.toDateString() === yesterday.toDateString()) return "Yesterday";
                                    return date; // e.g., "2025-11-19"
                                })()}
                            </div>

                            {chatGroups[date].length > 0 &&(
                                <div
                                    className="bg-opacity-50 text-white px-3 py-2 rounded w-100 d-flex flex-column cursor-pointer"
                                    style={{ backgroundColor: "#e8ddf5" }}
                                >
                                    <div className="d-flex align-items-center">
                                        <LuMessageSquare style={{ color: "black" }} />
                                        <span style={{ color: "black", marginLeft: "8px", fontSize: "small" }}>
                                            {chatGroups[date][0].message.substring(0, 25)}...
                                        </span>
                                    </div>

                                    <div style={{ color: "#2c3e50", marginLeft: "2px", fontSize: "small" }}>
                                        {chatGroups[date][0].response.substring(0, 25)}...
                                    </div>
                                </div>
                            )}
                        </div>
                    ))
                )}

            </div>
        </div>
    );
}
