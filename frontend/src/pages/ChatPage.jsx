import { Send } from "lucide-react";
import { useEffect, useState } from "react";

import api from "../api/client";
import PageHeader from "../components/PageHeader.jsx";

export default function ChatPage() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const loadHistory = () => {
    api.get("/chat/history").then((response) => setMessages(response.data.messages));
  };

  useEffect(loadHistory, []);

  const ask = async (event) => {
    event.preventDefault();
    if (!question.trim()) return;
    setLoading(true);
    const response = await api.post("/chat/ask", { question });
    setMessages([response.data.message, ...messages]);
    setQuestion("");
    setLoading(false);
  };

  return (
    <>
      <PageHeader title="Bible Q&A" description="Ask Bible questions and keep a pastoral conversation history." />
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
