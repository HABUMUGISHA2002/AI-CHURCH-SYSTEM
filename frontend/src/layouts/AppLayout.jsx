import { BarChart3, Bell, CalendarDays, LogOut, MessageSquareText, Mic2, Users } from "lucide-react";
import { NavLink, Outlet } from "react-router-dom";

import { useAuth } from "../context/AuthContext.jsx";

const navItems = [
  { to: "/", label: "Analytics", icon: BarChart3 },
  { to: "/chat", label: "Bible Q&A", icon: MessageSquareText },
  { to: "/sermons", label: "Sermons", icon: Mic2 },
  { to: "/events", label: "Events", icon: CalendarDays },
  { to: "/members", label: "Members", icon: Users },
  { to: "/notifications", label: "Notifications", icon: Bell },
];

export default function AppLayout() {
  const { user, logout } = useAuth();

  return (
    <div className="min-h-screen bg-mist">
      <aside className="fixed inset-y-0 left-0 hidden w-64 border-r border-slate-200 bg-white p-5 lg:block">
        <div className="mb-8">
          <p className="text-xs font-semibold uppercase tracking-wide text-gold">AI Church</p>
          <h1 className="mt-1 text-xl font-bold text-ink">Assistant System</h1>
        </div>
        <nav className="space-y-1">
          {navItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) =>
                `flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium ${
                  isActive ? "bg-forest text-white" : "text-slate-600 hover:bg-slate-100 hover:text-ink"
                }`
              }
            >
              <item.icon size={18} />
              {item.label}
            </NavLink>
          ))}
        </nav>
      </aside>

      <main className="lg:pl-64">
        <header className="sticky top-0 z-10 border-b border-slate-200 bg-white/95 backdrop-blur">
          <div className="flex items-center justify-between px-4 py-4 lg:px-8">
            <div>
              <p className="text-sm font-semibold text-ink">{user?.name}</p>
              <p className="text-xs capitalize text-slate-500">{user?.role}</p>
            </div>
            <button className="btn-secondary" onClick={logout} title="Log out">
              <LogOut size={16} />
              Logout
            </button>
          </div>
          <nav className="flex gap-1 overflow-x-auto px-4 pb-3 lg:hidden">
            {navItems.map((item) => (
              <NavLink
                key={item.to}
                to={item.to}
                className={({ isActive }) =>
                  `flex shrink-0 items-center gap-2 rounded-md px-3 py-2 text-xs font-medium ${
                    isActive ? "bg-forest text-white" : "bg-white text-slate-600"
                  }`
                }
              >
                <item.icon size={16} />
                {item.label}
              </NavLink>
            ))}
          </nav>
        </header>
        <div className="p-4 lg:p-8">
          <Outlet />
        </div>
      </main>
    </div>
  );
}
