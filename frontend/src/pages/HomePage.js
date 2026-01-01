import { useAuth } from "../context/auth"; 
import Layout from "./../components/Layout/Layout";
import imgs1 from "../assets/img/img1.jpeg";
import imgs2 from "../assets/img/img2.jpeg";
import imgs3 from "../assets/img/img3.jpeg";
import imgs4 from "../assets/img/img4.jpeg";
import imgs5 from "../assets/img/img5.jpeg";
import imgs6 from "../assets/img/img6.jpeg";
import imgs7 from "../assets/img/img7.jpeg";
import imgs9 from "../assets/img/img9.jpeg";
import '../styles/Home.css';
import { useState } from "react";

const images = [imgs1, imgs2, imgs3, imgs4, imgs5, imgs6, imgs7];

const HomePage = () => {
    const [auth] = useAuth();
    const [index, setIndex] = useState(0);

    // Get the 3 images to display (center + two sides)
    const getVisibleImages = () => {
        let visible = [];
        for (let i = 0; i < 3; i++) {
            visible.push(images[(index + i) % images.length]);
        }
        return visible;
    };

    return (
        <Layout title={"Best offers"}>
            {/* Hero Section */}
            <div className="hero">
                <div className="hero-content">
                    <div className="container">
                        <div className="row">
                            <div className="col-6">
                                <img src={imgs9} style={{height:"400px"}}/>
                            </div>
                            <div className="col-6" style={{display:"flex", flexDirection:"column",justifyContent:"center",paddingTop:"40px"}}>
                                <h1>Welcome to Mindful Living</h1>
                                <p>
                                    Mental health is not a destination, but a process — it's about how you drive, not where you're going.
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            {/* Info Section */}
            <div className="container section">
                <h2 className="text-center mb-4">Explore Our Journey</h2>
                <p className="text-center mb-5">
                    Discover inspiring stories, helpful tips, and the best offers for your mental well-being.
                </p>

                {/* Carousel */}
                <div style={{ display: "flex", alignItems: "center", justifyContent: "center" }}>
                    <button
                        className="prev"
                        onClick={() => setIndex((prev) => (prev - 1 + images.length) % images.length)}
                    >
                        &#10094;
                    </button>

                    <div className="slideshow-container">
                        {getVisibleImages().map((img, i) => (
                            <div
                                className={`slide ${i === 1 ? "active" : "side"}`}
                                key={i}
                            >
                                <img src={img} alt={`Slide ${i}`} />
                            </div>
                        ))}
                    </div>

                    <button
                        className="next"
                        onClick={() => setIndex((prev) => (prev + 1) % images.length)}
                    >
                        &#10095;
                    </button>
                </div>
            </div>
        </Layout>
    );
};

export default HomePage;
