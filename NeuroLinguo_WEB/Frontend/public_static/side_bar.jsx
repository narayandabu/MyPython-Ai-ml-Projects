import React,{useState} from "react";
import "./styles/side_bar.css";
import axiosInstance from './utils/axiosInstance';
import { useNavigate } from 'react-router-dom';
import { useEffect, useRef } from 'react';



function to_server(button){
    axiosInstance.post('http://localhost:5000/api/type',{ button_type: button })
    .then((response) => {
        return response;
    })
    .catch(error => {
        console.error('There was an error!', error);
        return "";
});
}
const Side_bar = ({setCurrentTool})=>{
    const [isOpen, setIsOpen] = useState(false);
    const [selected, setSelected] = useState(0); 
    const [showDropdown, setShowDropdown] = useState(false);


    const navigate = useNavigate();
    const sidebarRef = useRef(null);

    const handleLogout = async () => {
      try {
        const token = localStorage.getItem('token');
        if (!token) {
          console.error("No token found, user might not be logged in.");
          navigate('/');
          return;
        }
    
        const response = await axiosInstance.post('http://localhost:5000/api/logout', {}, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
    
        localStorage.removeItem('token');
        navigate('/');
      } catch (err) {
        const message = err?.response?.data?.message || 'Unknown error';
        if (message === "Invalid or expired token") {
          localStorage.removeItem('token');
          navigate('/');
        }
        console.error("Logout failed:", message);
      }
    };
        
    const button_names = ["Sentiment", "Gemini", "Analyzer",'Papers'];
    const button_funcs = [
        ()=>{to_server('Sentiment');},
        ()=>{to_server('Gemini');},
        ()=>{to_server('Analyzer');},
        ()=>{to_server('Papers');},
    ]
    const handleViewProfile = () => {
      console.log("Viewing profile...");
    };
    const handleButtonClick = (index, func) => {
      setSelected(index);
      func();
      setCurrentTool(button_names[index]);
    };
    const toggleSidebar = () => setIsOpen(!isOpen);
    const closeSidebar = () => setIsOpen(false);
    const toggleDropdown = () => setShowDropdown((prev) => !prev);

    useEffect(() => {
      const handleClickOutside = (e) => {
        const clickedOutsideSidebar =
          sidebarRef.current && !sidebarRef.current.contains(e.target) && !e.target.closest(".menu_button") ;
        const clickedOutsideAccount =
          !e.target.closest('.account-section');
    
        if (clickedOutsideSidebar && isOpen) {
          closeSidebar();
        }
        if (clickedOutsideAccount) {
          setShowDropdown(false);
        }
      };
      document.addEventListener('mousedown', handleClickOutside);
      return () => document.removeEventListener('mousedown', handleClickOutside);
    }, [isOpen]);
    return(
        
<>
<header className="nav-container">
        <div className="nav-left">
          <button onClick={toggleSidebar} className="menu_button">
            {isOpen ? "✖" : "☰"}
          </button>
          <div className="logo-container">
            <img src="../Logo-small.png" alt="logo" className="logo" />
            <h1 className="navb">NeuroLinguo</h1>
          </div>
        </div>
        <div className="account-section">
        <button className="account-button" onClick={toggleDropdown}>
          <img src="../default-avatar.png" className="account-avatar" />
          
          <i className="fas fa-chevron-down"></i>
        </button>

          {showDropdown  && (
            <div className="account-dropdown">
              <div className="account-user-info"></div>
              <button title="profile" onClick={handleViewProfile}>View Profile</button>
              <button onClick={handleLogout}>Logout</button>
            </div>
          )}
        </div>
      </header>
  {isOpen && (<div className="sidebar-overlay" onClick={closeSidebar} />)}
  {/* Notebook Button */}
  {/* Sidebar Menu */}
  <aside ref={sidebarRef} className={`side-menu-bar ${isOpen ? "open" : ""}`}>
    <h2 className="side-bar-title">Choose Mode</h2>
    <ul className="side-menu-list">
      {button_names.map((label, index) => (
        <button 
          key={index}
          className={selected === index ? "selected" : ""}
          onClick={() => {
            handleButtonClick(index, button_funcs[index]); setSelected(index);}}
          >
          {label}
        </button>
      ))}
    </ul>

    {selected === 3 && (
      <div className="Link-Request open"></div>
    )}
  </aside>
</>

    )


}

export default Side_bar;