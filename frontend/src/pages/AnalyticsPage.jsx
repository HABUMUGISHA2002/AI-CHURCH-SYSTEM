import { useEffect, useState } from "react";

import api from "../api/client";
import PageHeader from "../components/PageHeader.jsx";
import StatCard from "../components/StatCard.jsx";

export default function AnalyticsPage() {
  const [analytics, setAnalytics] = useState(null);

  useEffect(() => {
    api.get("/analytics").then((response) => setAnalytics(response.data));
  }, []);

  const totals = analytics?.totals || {};

  return (
    <>
      <PageHeader title="Analytics" description="High-level ministry health across members, events, attendance, sermons, messages, and notifications." />
      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <StatCard label="Members" value={totals.members} />
        <StatCard label="Events" value={totals.events} />
        <StatCard label="Attendance Records" value={totals.attendance_records} />
        <StatCard label="AI Messages" value={totals.messages} />
        <StatCard label="Sermons" value={totals.sermons} />
        <StatCard label="Notifications" value={totals.notifications} />
        <StatCard label="Users" value={totals.users} />
      </div>
    </>
  );
}
