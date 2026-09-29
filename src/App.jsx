import { useState } from 'react'

import { BrowserRouter as Router, Routes, Route, Navigate, Outlet } from "react-router-dom";

import "./NavBar.css";
import NavBar from "./NavBar";

function App() {
  return (
    <Router>
      <Routes>

        {/* Authenticated routes with navbar */}
        <Route
          element={
            <div className="container">
              <NavBar />
              <div className="content">
                <Outlet />
              </div>
            </div>
          }
        >
          <Route path="/" element={<p>test</p>} />
          {/* <Route path="/groups" element={<Groups />} />
          <Route path="/groups/:id" element={<GroupsExpand />} />
          <Route path="/friends" element={<Friends />} />
          <Route path="/create" element={<Create />} />
          <Route path="/notifications" element={<Notifications />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/settings" element={<Settings />} /> */}
        </Route>

        {/* Catch-all redirect */}
        {/* <Route path="*" element={<Navigate to="/" replace />} /> */}

      </Routes>
    </Router>
  );
  // return (
  //   <div className="container">
  //     <NavBar />
  //     <div className="content">
  //       <h2>Favorites</h2>
  //       <ul>
  //         <li>DOOP</li>
  //         <li>Cuzzies</li>
  //         <li>Pickleball</li>
  //         <li>TM</li>
  //       </ul>

  //       <h2>Groups</h2>
  //       <ul>
  //         <li>23rd Potluck</li>
  //         <li>Cal Poly Friendos</li>
  //         <p className="link">See more</p>
  //       </ul>

  //       <h2>Communities</h2>
  //       <ul>
  //         <li>UCSD NSU</li>
  //         <li>Cal Poly VSA</li>
  //         <li>Valorant LFG</li>
  //         <p className="link">See more</p>
  //       </ul>
  //     </div>
  //   </div>
  // )
}

export default App
