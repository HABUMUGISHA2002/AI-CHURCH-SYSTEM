import { Send } from "lucide-react";
import { useEffect, useState } from "react";

import api from "../api/client";
import PageHeader from "../components/PageHeader.jsx";

export default function NotificationsPage() {
  const [notifications, setNotifications] = useState([]);
  const [form, setForm] = useState({ channel: "email", recipient: "", subject: "", body: "" });

  const loadNotifications = () => api.get("/notifications").then((response) => setNotifications(response.data.notifications));
  useEffect(loadNotifications, []);

  const send = async (event) => {
    event.preventDefault();
    await api.post("/notifications/send", form);
    setForm({ channel: "email", recipient: "", subject: "", body: "" });
    loadNotifications();
  };

  return (
    <>
      <PageHeader title="Notifications" description="Send announcements, reminders, and pastoral messages by Email, SMS, or WhatsApp." />
      <form className="panel grid gap-4 p-5 lg:grid-cols-2" onSubmit={send}>
        <select className="field" value={form.channel} onChange={(event) => setForm({ ...form, channel: event.target.value })}>
          <option value="email">Email</option>
          <option value="sms">SMS</option>
          <option value="whatsapp">WhatsApp</option>
        </select>
        <input className="field" placeholder="Recipient" value={form.recipient} onChange={(event) => setForm({ ...form, recipient: event.target.value })} required />
        <input className="field lg:col-span-2" placeholder="Subject" value={form.subject} onChange={(event) => setForm({ ...form, subject: event.target.value })} required />
        <textarea className="field min-h-28 lg:col-span-2" placeholder="Message" value={form.body} onChange={(event) => setForm({ ...form, body: event.target.value })} required />
        <button className="btn-primary lg:col-span-2">
          <Send size={16} />
          Send Notification
        </button>
      </form>
      <div className="mt-6 space-y-3">
        {notifications.map((notification) => (
          <article className="panel flex flex-col gap-2 p-4 sm:flex-row sm:items-center sm:justify-between" key={notification.id}>
            <div>
              <h3 className="font-semibold text-ink">{notification.subject}</h3>
              <p className="text-sm text-slate-500">{notification.channel} to {notification.recipient}</p>
            </div>
            <span className="rounded-md bg-slate-100 px-2 py-1 text-xs font-semibold text-slate-600">{notification.status}</span>
          </article>
        ))}
      </div>
    </>
  );
}
