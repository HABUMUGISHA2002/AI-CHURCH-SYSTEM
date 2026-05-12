import { CalendarPlus } from "lucide-react";
import { useEffect, useState } from "react";

import api from "../api/client";
import PageHeader from "../components/PageHeader.jsx";

export default function EventsPage() {
  const [events, setEvents] = useState([]);
  const [form, setForm] = useState({ title: "", location: "", starts_at: "", description: "" });

  const loadEvents = () => api.get("/events").then((response) => setEvents(response.data.events));
  useEffect(loadEvents, []);

  const createEvent = async (event) => {
    event.preventDefault();
    await api.post("/events", { ...form, starts_at: new Date(form.starts_at).toISOString() });
    setForm({ title: "", location: "", starts_at: "", description: "" });
    loadEvents();
  };

  return (
    <>
      <PageHeader title="Events" description="Manage church services, ministry meetings, calendar items, and reminders." />
      <form className="panel grid gap-4 p-5 lg:grid-cols-2" onSubmit={createEvent}>
        <input className="field" placeholder="Event title" value={form.title} onChange={(event) => setForm({ ...form, title: event.target.value })} required />
        <input className="field" placeholder="Location" value={form.location} onChange={(event) => setForm({ ...form, location: event.target.value })} />
        <input className="field" type="datetime-local" value={form.starts_at} onChange={(event) => setForm({ ...form, starts_at: event.target.value })} required />
        <button className="btn-primary">
          <CalendarPlus size={16} />
          Create Event
        </button>
        <textarea className="field min-h-24 lg:col-span-2" placeholder="Description" value={form.description} onChange={(event) => setForm({ ...form, description: event.target.value })} />
      </form>
      <div className="mt-6 grid gap-4 lg:grid-cols-2">
        {events.map((event) => (
          <article className="panel p-5" key={event.id}>
            <h3 className="font-semibold text-ink">{event.title}</h3>
            <p className="mt-1 text-sm text-slate-500">{new Date(event.starts_at).toLocaleString()}</p>
            <p className="mt-2 text-sm text-slate-600">{event.location}</p>
          </article>
        ))}
      </div>
    </>
  );
}
