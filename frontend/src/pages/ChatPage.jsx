import { Send } from "lucide-react";
import { useEffect, useState } from "react";

import api from "../api/client";
import PageHeader from "../components/PageHeader.jsx";

export default function ChatPage() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [aiStatus, setAiStatus] = useState(null);
  const [error, setError] = useState("");

  const loadHistory = () => {
    api.get("/chat/history").then((response) => setMessages(response.data.messages));
  };

  useEffect(() => {
    loadHistory();
    api.get("/ai/status").then((response) => setAiStatus(response.data)).catch(() => setAiStatus(null));
  }, []);

  const ask = async (event) => {
    event.preventDefault();
    if (!question.trim()) return;
    setLoading(true);
    setError("");
    try {
      const response = await api.post("/chat/ask", { question });
      setMessages([response.data.message, ...messages]);
      setQuestion("");
    } catch (err) {
      setError(err.response?.data?.message || "Could not reach the AI service. Check the backend and API key.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <PageHeader title="Bible Q&A" description="Ask Bible questions and keep a pastoral conversation history." />
      {aiStatus && !aiStatus.configured ? (
        <div className="panel mb-4 border-amber-200 bg-amber-50 p-4 text-sm text-amber-800">
          {aiStatus.message}
        </div>
      ) : null}
      <form className="panel p-4" onSubmit={ask}>
        <textarea
          className="field min-h-28"
          placeholder="Ask a Bible question..."
          value={question}
          onChange={(event) => setQuestion(event.target.value)}
        />
        <div className="mt-3 flex justify-end">
          <button className="btn-primary" disabled={loading}>
            <Send size={16} />
            {loading ? "Asking..." : "Ask"}
          </button>
        </div>
        {error ? <p className="mt-3 rounded-md bg-red-50 px-3 py-2 text-sm text-red-700">{error}</p> : null}
      </form>
      <div className="mt-5 space-y-4">
        {messages.map((message) => (
          <article className="panel p-5" key={message.id}>
            <p className="text-sm font-semibold text-ink">{message.question}</p>
            <p className="mt-3 whitespace-pre-wrap text-sm leading-6 text-slate-600">{message.response}</p>
          </article>
        ))}
      </div>
    </>
  );
}
