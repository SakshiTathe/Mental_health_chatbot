import { Routes, Route } from "react-router-dom";
import HomePage from "./pages/HomePage";
import About from "./pages/About";
import Contact from "./pages/Contact";
import Pagenotfound from "./pages/Pagenotfound";
import Register from "./pages/Auth/Register";
//import { ToastContainer} from 'react-toastify';
import 'react-toastify/ReactToastify.css'
import Dashboard from "./pages/user/Dashboard";
import Login from "./pages/Auth/Login";
import Policy from "./pages/Policy";
import ForgotPasssword from "./pages/Auth/ForgotPassword";
import PrivateRoute from "./components/Routes/Private";
//import AdminRoute from "./components/Routes/AdminRoute";
//import AdminDashboard from "./pages/Admin/AdminDashboard";
import { Chat } from "./pages/Chat";
function App() {
  return (
    <>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/dashboard" element={<PrivateRoute/>}>
          <Route path="user" element={<Dashboard/>} />
          <Route path="chatroom" element={<Chat/>} />
        </Route>
        <Route path="/register" element={<Register />} />
        <Route path="/forgot-password" element={<ForgotPasssword/>} />
        <Route path="/login" element={<Login/>} />
        <Route path="/about" element={<About />} />
        <Route path="/contact" element={<Contact />} />
        <Route path="/policy" element={<Policy/>} />
        <Route path="/*" element={<Pagenotfound />} />
      </Routes>
    </>
  );
}

export default App;


 