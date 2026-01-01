import { useEffect, useRef, useState } from "react";
import "../../styles/Chatbot.css";
import { useAuth } from "../../context/auth";
import { Mic, MicOff, Volume2, VolumeX } from "lucide-react";

const ChatBot = ({ selectedChat }) => {
    const [messages, setMessages] = useState([
        {
            sender: "bot",
            text: "Hello! You are not alone - I'm here to listen.\nPlease share what's on your mind",
        },
    ]);

    const [userInput, setUserInput] = useState("");
    const [loading, setLoading] = useState(false);
    const [auth] = useAuth();

    const chatBoxRef = useRef(null);

    const [isListening, setIsListening] = useState(false);
    const [isSpeechEnabled, setIsSpeechEnabled] = useState(true);

    const speak = (text) => {
        if (!isSpeechEnabled) return;

        window.speechSynthesis.cancel();

        const utterance = new SpeechSynthesisUtterance(text);
        utterance.rate = 1;
        utterance.pitch = 1;

        const voices = window.speechSynthesis.getVoices();
        const female = voices.find(v => v.name.includes("Female") || v.name.includes("Google US English"));
        if (female) utterance.voice = female;

        window.speechSynthesis.speak(utterance);
    };

    const startListening = () => {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

        if (!SpeechRecognition) {
            alert("Voice recognition is not supported. Try Chrome.");
            return;
        }

        const recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = "en-US";

        recognition.onstart = () => setIsListening(true);

        recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            setUserInput(transcript);
        };

        recognition.onerror = () => setIsListening(false);
        recognition.onend = () => setIsListening(false);

        recognition.start();
    };

    const sendMessage = async (textOverride = null) => {
        const msg = textOverride || userInput;

        if (msg.trim() === "") return;

        setMessages(prev => [...prev, { sender: "user", text: msg }]);
        setUserInput("");
        setLoading(true);

        try {
            const res = await fetch("http://127.0.0.1:5000/api/v1/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    message: msg,
                    user_id: auth?.user?._id
                })
            });

            const data = await res.json();
            const botText = data.reply || "Sorry, I couldn't process that.";

            setMessages(prev => [...prev, { sender: "bot", text: botText }]);

            speak(botText);

        } catch (err) {
            setMessages(prev => [
                ...prev,
                { sender: "bot", text: "Error connecting to server." }
            ]);
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

        const greeting = {
            sender: "bot",
            text: "Hello! You are not alone - I'm here to listen.\nPlease share what's on your mind",
        };

        if (Array.isArray(selectedChat)) {
            const msgs = selectedChat.flatMap(c => ([
                { sender: "user", text: c.message },
                { sender: "bot", text: c.response }
            ]));

            setMessages([greeting, ...msgs]);
            return;
        }

        if (selectedChat.message && selectedChat.response) {
            setMessages([
                greeting,
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

            <h1 className="chat-title">
                Chat Bot
                <button
                    onClick={() => setIsSpeechEnabled(!isSpeechEnabled)}
                    className="voice-btn"
                >
                    {isSpeechEnabled ? <Volume2 size={20} /> : <VolumeX size={20} />}
                </button>
            </h1>

            <div className="chat-box" ref={chatBoxRef}>
                {messages.map((msg, idx) => (
                    <div key={idx} className={`message ${msg.sender}`}>
                        {msg.text.split("\n").map((line, i) => (
                            <div key={i} className="message-text">{line}</div>
                        ))}
                    </div>
                ))}

                {loading && (
                    <div className="message bot">
                        <div className="message-text">Responding ...</div>
                    </div>
                )}
            </div>

            <div className="input-area">

                <button
                    className={`mic-btn ${isListening ? "listening" : ""}`}
                    onClick={startListening}
                >
                    {isListening ? <MicOff size={20} /> : <Mic size={20} />}
                </button>

                <input
                    type="text"
                    placeholder={isListening ? "Listening..." : "Say Something..."}
                    value={userInput}
                    onChange={(e) => setUserInput(e.target.value)}
                    onKeyDown={handleKeyDown}
                    disabled={loading}
                />

                <button onClick={() => sendMessage()} disabled={loading}>
                    {loading ? "..." : "Send"}
                </button>
            </div>
        </div>
    );
};

export default ChatBot;
