import { useState } from 'react'

import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";

import "./NavBar.css";
import NavBar from "./NavBar";

function App() {

  return (
    <div className="container">
      <NavBar />
      <div className="content">
        <h2>Favorites</h2>
        <ul>
          <li>DOOP</li>
          <li>Cuzzies</li>
          <li>Pickleball</li>
          <li>TM</li>
        </ul>

        <h2>Groups</h2>
        <ul>
          <li>23rd Potluck</li>
          <li>Cal Poly Friendos</li>
          <p className="link">See more</p>
        </ul>

        <h2>Communities</h2>
        <ul>
          <li>UCSD NSU</li>
          <li>Cal Poly VSA</li>
          <li>Valorant LFG</li>
          <p className="link">See more</p>
        </ul>
      </div>
    </div>
  )
}

export default App
