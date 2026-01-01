import { useEffect, useRef, useState } from "react";
import "../../styles/Chatbot.css";
import { useAuth } from "../../context/auth"

const ChatBot = ({ selectedChat }) => {
    const [messages, setMessages] = useState([
        {
            sender: "bot",
            text: "Hello! You are not alone - I'm here to listen.\nPlease share what's on your mind",
        },
    ]);
    const [userInput, setUserInput] = useState("");
    const [loading, setLoading] = useState(false);
    const chatBoxRef = useRef(null);
    const [auth, setAuth] = useAuth();
    const sendMessage = async () => {
        if (userInput.trim() === "") return;

        setMessages(prev => [...prev, { sender: "user", text: userInput }]);
        setUserInput("");
        setLoading(true);

        try {
            const res = await fetch("http://127.0.0.1:5000/api/v1/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: userInput, user_id: auth.user["_id"] })
            });

            const reply = await res.json();
            console.log("Chat response:", reply);

            const botText = reply.reply || "Sorry, I couldn't process that.";
            setMessages(prev => [...prev, { sender: "bot", text: botText }]);

            // Optional: store locally for UI display
            const emotions = reply.emotion?.category || "neutral";
            console.log("Predicted emotion:", emotions);

        } catch (error) {
            setMessages(prev => [...prev, { sender: "bot", text: error.message || "Error connecting to server." }]);
        }

        setLoading(false);
    };


    const handleKeyDown = (e) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    };
    useEffect(() => {
        if (!selectedChat) return;
        const defaultGreeting = {
            sender: "bot",
            text: "Hello! You are not alone - I'm here to listen.\nPlease share what's on your mind",
        };
        if (Array.isArray(selectedChat)) {
            const msgs = selectedChat.flatMap(item => ([
                { sender: "user", text: item.message },
                { sender: "bot", text: item.response }
            ]));
            setMessages([defaultGreeting, ...msgs]);
            return;
        }

        if (selectedChat.message && selectedChat.response) {
            setMessages([defaultGreeting,
                { sender: "user", text: selectedChat.message },
                { sender: "bot", text: selectedChat.response }
            ]);
        }
    }, [selectedChat]);

    useEffect(() => {
        if (chatBoxRef.current) {
            chatBoxRef.current.scrollTop = chatBoxRef.current.scrollHeight;
        }
    }, [messages]);

    return (
        <div className="chat-container">
            <h1 className="chat-title">Chat Bot</h1>
            <div className="chat-box" ref={chatBoxRef}>
                {messages.map((msg, index) => (
                    <div key={index} className={`message ${msg.sender}`}>
                        {msg.text.split("\n").map((line, i) => (
                            <div key={i} className="message-text">{line}</div>
                        ))}
                    </div>
                ))}
            </div>
            <div className="input-area">
                <input
                    type="text"
                    placeholder="Say Something......"
                    value={userInput}
                    onChange={(e) => setUserInput(e.target.value)}
                    onKeyDown={handleKeyDown}
                    disabled={loading}
                />
                <button onClick={sendMessage} disabled={loading}>{loading ? "..." : "Send"}</button>
            </div>
        </div>
    );
};

export default ChatBot;
