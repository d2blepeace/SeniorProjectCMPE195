import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Layout from "./layout/Layout";
import Dashboard from "./pages/Dashboard";
import ManagePlants from "./pages/ManagePlants";
import Settings from "./pages/Settings";

function App() {
    return (
        <Router>
            <Layout>
                <Routes>
                    <Route path="/" element={<Dashboard />} />
                    <Route path="/plants" element={<ManagePlants />} />
                    <Route path="/settings" element={<Settings />} />
                    </Routes>
            </Layout>
        </Router>
    );
}

export default App;