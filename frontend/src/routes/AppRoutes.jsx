import { Navigate, Route, Routes } from "react-router-dom";

import AppLayout from "../layouts/AppLayout.jsx";
import AnalyticsPage from "../pages/AnalyticsPage.jsx";
import AuthPage from "../pages/AuthPage.jsx";
import ChatPage from "../pages/ChatPage.jsx";
import EventsPage from "../pages/EventsPage.jsx";
import MembersPage from "../pages/MembersPage.jsx";
import NotificationsPage from "../pages/NotificationsPage.jsx";
import SermonsPage from "../pages/SermonsPage.jsx";
import { useAuth } from "../context/AuthContext.jsx";

function ProtectedRoute({ children }) {
  const { user, loading } = useAuth();
  if (loading) {
    return <div className="flex min-h-screen items-center justify-center text-sm text-slate-500">Loading...</div>;
  }
  return user ? children : <Navigate to="/login" replace />;
}

export default function AppRoutes() {
  return (
    <Routes>
      <Route path="/login" element={<AuthPage mode="login" />} />
      <Route path="/register" element={<AuthPage mode="register" />} />
      <Route
        path="/"
        element={
          <ProtectedRoute>
            <AppLayout />
          </ProtectedRoute>
        }
      >
        <Route index element={<AnalyticsPage />} />
        <Route path="chat" element={<ChatPage />} />
        <Route path="sermons" element={<SermonsPage />} />
        <Route path="events" element={<EventsPage />} />
        <Route path="members" element={<MembersPage />} />
        <Route path="notifications" element={<NotificationsPage />} />
      </Route>
    </Routes>
  );
}
