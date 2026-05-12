import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import { useAuth } from "../context/AuthContext.jsx";

export default function AuthPage({ mode }) {
  const isRegister = mode === "register";
  const { login, register } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({ name: "", email: "", password: "", role: "member" });
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const submit = async (event) => {
    event.preventDefault();
    setError("");
    setSubmitting(true);
    try {
      if (isRegister) {
        await register(form);
      } else {
        await login(form.email, form.password);
      }
      navigate("/");
    } catch (err) {
      setError(err.response?.data?.message || "Authentication failed");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <main className="grid min-h-screen bg-mist lg:grid-cols-[1fr_520px]">
      <section className="flex items-center px-6 py-12 lg:px-16">
        <div className="max-w-2xl">
          <p className="text-sm font-semibold uppercase tracking-wide text-gold">AI Church Assistant System</p>
          <h1 className="mt-4 text-4xl font-bold leading-tight text-ink md:text-5xl">
            Manage ministry, communication, sermons, and pastoral care in one place.
          </h1>
          <p className="mt-5 text-base leading-7 text-slate-600">
            A role-based platform for admins, pastors, leaders, and members with AI Bible Q&A,
            sermon generation, attendance, events, notifications, and WhatsApp workflows.
          </p>
        </div>
      </section>
      <section className="flex items-center bg-white px-6 py-12">
        <form className="mx-auto w-full max-w-sm" onSubmit={submit}>
          <h2 className="text-2xl font-bold text-ink">{isRegister ? "Create account" : "Welcome back"}</h2>
          <p className="mt-1 text-sm text-slate-500">
            {isRegister ? "Register your first church user." : "Sign in to continue."}
          </p>

          <div className="mt-6 space-y-4">
            {isRegister ? (
              <label className="block text-sm font-medium text-slate-700">
                Name
                <input
                  className="field mt-1"
                  value={form.name}
                  onChange={(event) => setForm({ ...form, name: event.target.value })}
                  required
                />
              </label>
            ) : null}
            <label className="block text-sm font-medium text-slate-700">
              Email
              <input
                className="field mt-1"
                type="email"
                value={form.email}
                onChange={(event) => setForm({ ...form, email: event.target.value })}
                required
              />
            </label>
            <label className="block text-sm font-medium text-slate-700">
              Password
              <input
                className="field mt-1"
                type="password"
                value={form.password}
                onChange={(event) => setForm({ ...form, password: event.target.value })}
                required
              />
            </label>
            {isRegister ? (
              <label className="block text-sm font-medium text-slate-700">
                Role
                <select
                  className="field mt-1"
                  value={form.role}
                  onChange={(event) => setForm({ ...form, role: event.target.value })}
                >
                  <option value="member">Member</option>
                  <option value="leader">Leader</option>
                  <option value="pastor">Pastor</option>
                  <option value="admin">Admin</option>
                </select>
              </label>
            ) : null}
          </div>

          {error ? <p className="mt-4 rounded-md bg-red-50 px-3 py-2 text-sm text-red-700">{error}</p> : null}

          <button className="btn-primary mt-6 w-full" disabled={submitting}>
            {submitting ? "Please wait..." : isRegister ? "Register" : "Login"}
          </button>
          <p className="mt-4 text-center text-sm text-slate-500">
            {isRegister ? "Already have an account?" : "Need an account?"}{" "}
            <Link className="font-semibold text-forest" to={isRegister ? "/login" : "/register"}>
              {isRegister ? "Login" : "Register"}
            </Link>
          </p>
        </form>
      </section>
    </main>
  );
}
