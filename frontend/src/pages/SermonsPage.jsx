import { Save, Sparkles } from "lucide-react";
import { useEffect, useState } from "react";

import api from "../api/client";
import PageHeader from "../components/PageHeader.jsx";

export default function SermonsPage() {
  const [form, setForm] = useState({ topic: "", scripture: "", mode: "outline", save: true });
  const [generated, setGenerated] = useState("");
  const [sermons, setSermons] = useState([]);
  const [loading, setLoading] = useState(false);

  const loadSermons = () => api.get("/sermons").then((response) => setSermons(response.data.sermons));

  useEffect(loadSermons, []);

  const generate = async (event) => {
    event.preventDefault();
    setLoading(true);
    const response = await api.post("/sermons/generate", form);
    setGenerated(response.data.generated);
    await loadSermons();
    setLoading(false);
  };

  return (
    <>
      <PageHeader title="AI Sermon Generator" description="Create outlines or full sermons, then save them for later editing and sharing." />
      <form className="panel grid gap-4 p-5 lg:grid-cols-2" onSubmit={generate}>
        <label className="block text-sm font-medium text-slate-700">
          Sermon topic
          <input className="field mt-1" value={form.topic} onChange={(event) => setForm({ ...form, topic: event.target.value })} required />
        </label>
        <label className="block text-sm font-medium text-slate-700">
          Scripture
          <input className="field mt-1" value={form.scripture} onChange={(event) => setForm({ ...form, scripture: event.target.value })} />
        </label>
        <label className="block text-sm font-medium text-slate-700">
          Output
          <select className="field mt-1" value={form.mode} onChange={(event) => setForm({ ...form, mode: event.target.value })}>
            <option value="outline">Outline</option>
            <option value="full">Full sermon</option>
          </select>
        </label>
        <div className="flex items-end justify-between gap-3">
          <label className="flex items-center gap-2 text-sm text-slate-600">
            <input type="checkbox" checked={form.save} onChange={(event) => setForm({ ...form, save: event.target.checked })} />
            Save result
          </label>
          <button className="btn-primary" disabled={loading}>
            <Sparkles size={16} />
            {loading ? "Generating..." : "Generate"}
          </button>
        </div>
      </form>
      {generated ? <pre className="panel mt-5 whitespace-pre-wrap p-5 text-sm leading-6 text-slate-700">{generated}</pre> : null}
      <div className="mt-6 grid gap-4 lg:grid-cols-2">
        {sermons.map((sermon) => (
          <article className="panel p-5" key={sermon.id}>
            <div className="flex items-start gap-3">
              <Save className="mt-1 text-gold" size={18} />
              <div>
                <h3 className="font-semibold text-ink">{sermon.title}</h3>
                <p className="mt-1 text-sm text-slate-500">{sermon.scripture || sermon.topic}</p>
              </div>
            </div>
          </article>
        ))}
      </div>
    </>
  );
}
