import React from "react";
import Layout from "./../components/Layout/Layout";
import "../styles/About.css";
import imgs from "../assets/img/img6.jpeg"

const About = () => {
    return (
        <Layout title="About Us">
            <div className="container py-5">
                <section id="about">
                    <div className="text-center mb-5">
                        <h2 className="fw-bold display-6 text-primary">About Us</h2>
                        <p className="lead text-muted">
                            We are a group of people who care deeply about mental health. This chatbot is your safe and friendly space — whether you’re feeling low, stressed, or just want to talk.
                            <br />
                            <em>“Your mental health is important. You deserve to feel heard and supported.”</em>
                        </p>
                    </div>

                    <div className="row g-4">
                        <div className="col-md-6">
                            <div className="about-col bg-white p-4 rounded shadow-sm text-center">
                                <h3 className="fw-semibold text-primary">Our Mission</h3>
                                <div>
                                <b>
                                    Helping you care for your mind and emotions by making support easy, private, and available anytime.

                                </b>
                                    <ul className="text-muted list-unstyled mt-3">
                                        <li>✔ Understand your feelings</li>
                                        <li>✔ Simple stress & anxiety tools</li>
                                        <li>✔ Always here to listen</li>
                                    </ul>
                                </div>
                            </div>
                        </div>

                        <div className="col-md-6">
                            <div className="about-col bg-white p-4 rounded shadow-sm text-center">
                                <h3 className="fw-semibold text-primary">Our Values</h3>
                                <div>
                                <b>
                                    We believe in kindness, privacy, no judgment, and inclusivity.
                                    <br/> .
                                </b>
                                    <ul className="text-muted list-unstyled mt-3">
                                        <li>💙 Empathy & care</li>
                                        <li>🔒 Your chats are safe</li>
                                        <li>🌍 Support for everyone</li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div className="row align-items-center mt-5">
                        <div className="col-lg-6 mb-4">
                            <img
                                src={imgs}
                                alt="About"
                                className="img-fluid rounded shadow "
                                style={{height:"450px"}}
                            />
                        </div>
                        <div className="col-lg-6">
                            <h4 className="fw-bold text-primary mb-3">What We Offer</h4>
                            <div className="row g-3">
                                {[
                                    { title: "🧠 Mood Tracking", desc: "Share how you feel — see mood changes over time." },
                                    { title: "🎙️ Talk or Type", desc: "Choose voice or text — your comfort matters." },
                                    { title: "🧘 Mindfulness Exercises", desc: "Breathing and relaxation tips to calm your mind." },
                                    { title: "💬 Positive Affirmations", desc: "Boost your mood with kind, uplifting words." },
                                    { title: "📊 Weekly Mood Reports", desc: "Understand yourself better with insights." },
                                    { title: "🕒 24/7 support", desc: "Understand yourself better with insights." },
                                ].map((item, index) => (
                                    <div className="col-md-6" key={index}>
                                        <div className="p-3 rounded shadow-sm bg-light h-100">
                                            <h6 className="fw-semibold">{item.title}</h6>
                                            <p className="text-muted small">{item.desc}</p>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>

                    <section id="call-to-action" className="text-center mt-5 p-5 rounded shadow-sm bg-primary text-white">
                        <h3 className="fw-bold" style={{color:" #9be1ff"}}>Having trouble keeping track of your goals?</h3>
                        <p className="mb-3">
                            Use Iris Goal Tracker to set goals, track time, and manage tasks easily.
                        </p>
                        <a className="btn btn-light px-4 py-2 rounded-pill fw-semibold" href="https://hng-iris-goal-tracker.herokuapp.com/">
                            Get Started
                        </a>
                    </section>
                </section>
            </div>
        </Layout>
    );
};

export default About;
