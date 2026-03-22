import { NavLink } from "react-router-dom";
import { LayoutDashboard, Leaf, Settings } from "lucide-react";
import { useState } from "react";

export default function Sidebar() {
    const [collapsed, setCollapsed] = useState(false);

    const linkClass = ({ isActive }) =>
        `flex items-center gap-3 p-3 rounded-lg transition ${
            isActive
                ? "bg-white text-green-700 font-semibold"
                : "text-gray-200 hover:bg-green-600"
        }`;

    return (
        <div
            className={`${
                collapsed ? "w-20" : "w-64"
            } bg-green-700 text-white h-full p-4 transition-all duration-300`}
        >
            <button
                onClick={() => setCollapsed(!collapsed)}
                className="mb-6 text-sm opacity-70 hover:opacity-100"
            >
                {collapsed ? "➡️" : "⬅️"}
            </button>

            <nav className="flex flex-col gap-2">
                <NavLink to="/" className={linkClass}>
                    <LayoutDashboard size={20} />
                    {!collapsed && "Dashboard"}
            </NavLink>

            <NavLink to="/plants" className={linkClass}>
                <Leaf size={20} />
                {!collapsed && "Plants"}
            </NavLink>

            <NavLink to="/settings" className={linkClass}>
                <Settings size={20} />
                {!collapsed && "Settings"}
            </NavLink>
        </nav>
    </div>
    );
}