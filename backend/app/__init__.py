from pathlib import Path

from flask import Flask, render_template_string, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_restful import Api

from app.api.ai import AIStatusResource
from app.api.analytics import AnalyticsResource
from app.api.attendance import AttendanceResource
from app.api.auth import LoginResource, MeResource, RegisterResource
from app.api.chat import ChatHistoryResource, BibleQuestionResource
from app.api.events import EventListResource, EventResource
from app.api.members import MemberListResource, MemberResource
from app.api.notifications import NotificationListResource, SendNotificationResource
from app.api.sermons import SermonGenerateResource, SermonListResource, SermonResource
from app.api.whatsapp import WhatsAppWebhookResource
from app.config import Config
from app.extensions import db

jwt = JWTManager()
migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    CORS(app, origins=[app.config["FRONTEND_ORIGIN"]], supports_credentials=True)
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    register_routes(app)
    register_web_routes(app)
    return app


def register_routes(app):
    api = Api(app, prefix="/api")

    api.add_resource(RegisterResource, "/auth/register")
    api.add_resource(LoginResource, "/auth/login")
    api.add_resource(MeResource, "/auth/me")

    api.add_resource(AIStatusResource, "/ai/status")

    api.add_resource(BibleQuestionResource, "/chat/ask")
    api.add_resource(ChatHistoryResource, "/chat/history")

    api.add_resource(SermonListResource, "/sermons")
    api.add_resource(SermonResource, "/sermons/<int:sermon_id>")
    api.add_resource(SermonGenerateResource, "/sermons/generate")

    api.add_resource(EventListResource, "/events")
    api.add_resource(EventResource, "/events/<int:event_id>")

    api.add_resource(MemberListResource, "/members")
    api.add_resource(MemberResource, "/members/<int:member_id>")

    api.add_resource(AttendanceResource, "/attendance")

    api.add_resource(NotificationListResource, "/notifications")
    api.add_resource(SendNotificationResource, "/notifications/send")

    api.add_resource(AnalyticsResource, "/analytics")
    api.add_resource(WhatsAppWebhookResource, "/webhooks/whatsapp")


def register_web_routes(app):
    frontend_dist = Path(app.root_path).parents[1] / "frontend" / "dist"

    @app.get("/api")
    def api_index():
        return {
            "status": "ok",
            "service": "AI Church Assistant System API",
            "frontend": app.config["FRONTEND_ORIGIN"],
        }

    @app.get("/")
    def web_app():
        if (frontend_dist / "index.html").exists():
            return send_from_directory(frontend_dist, "index.html")
        return render_template_string(WEB_APP_HTML)

    @app.get("/health")
    def health():
        return {"status": "ok", "service": "AI Church Assistant System"}

    @app.get("/assets/<path:filename>")
    def frontend_assets(filename):
        return send_from_directory(frontend_dist / "assets", filename)

    @app.get("/<path:path>")
    def frontend_routes(path):
        if path.startswith("api/"):
            return {"message": "Not found"}, 404

        requested_file = frontend_dist / path
        if requested_file.is_file():
            return send_from_directory(frontend_dist, path)

        if (frontend_dist / "index.html").exists():
            return send_from_directory(frontend_dist, "index.html")

        return render_template_string(WEB_APP_HTML)



WEB_APP_HTML = """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>AI Church Assistant System</title>
    <style>
      :root {
        color: #17211b;
        background: #eef4f0;
        font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      }
      body { margin: 0; min-height: 100vh; }
      main { max-width: 1120px; margin: 0 auto; padding: 32px 18px; }
      header { display: flex; justify-content: space-between; gap: 16px; align-items: center; margin-bottom: 24px; }
      h1 { margin: 0; font-size: clamp(28px, 4vw, 44px); line-height: 1.05; }
      h2 { margin: 0 0 14px; font-size: 20px; }
      p { color: #5d6b63; line-height: 1.6; }
      .grid { display: grid; gap: 16px; }
      .cols { grid-template-columns: repeat(auto-fit, minmax(230px, 1fr)); }
      .panel { background: #fff; border: 1px solid #dbe5df; border-radius: 8px; padding: 20px; box-shadow: 0 14px 38px rgba(31, 93, 72, .12); }
      .stat { font-size: 34px; color: #1f5d48; font-weight: 800; margin-top: 4px; }
      .label { color: #66736c; font-size: 13px; font-weight: 700; text-transform: uppercase; letter-spacing: .04em; }
      input, textarea, select { width: 100%; box-sizing: border-box; border: 1px solid #ccd8d1; border-radius: 6px; padding: 10px 12px; font: inherit; margin-top: 8px; }
      textarea { min-height: 110px; resize: vertical; }
      button { border: 0; border-radius: 6px; padding: 10px 14px; font-weight: 750; cursor: pointer; background: #1f5d48; color: white; }
      button.secondary { background: white; color: #1f5d48; border: 1px solid #ccd8d1; }
      .row { display: flex; gap: 10px; flex-wrap: wrap; align-items: center; }
      .hidden { display: none; }
      .muted { color: #66736c; font-size: 14px; }
      .error { color: #a11616; background: #fff0f0; border-radius: 6px; padding: 10px; }
      pre { white-space: pre-wrap; overflow-wrap: anywhere; background: #f7faf8; border-radius: 6px; padding: 12px; }
      nav { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 16px; }
      nav button { background: #fff; color: #17211b; border: 1px solid #ccd8d1; }
      nav button.active { background: #1f5d48; color: #fff; }
    </style>
  </head>
  <body>
    <main>
      <header>
        <div>
          <div class="label">AI Church Assistant System</div>
          <h1>Church management and pastoral AI tools</h1>
          <p>Fallback web app served by Flask. The full React frontend can run later when Node/npm is installed.</p>
        </div>
        <button class="secondary hidden" id="logoutBtn">Logout</button>
      </header>

      <section class="panel" id="loginPanel">
        <h2>Login</h2>
        <p class="muted">Use the admin account created during setup.</p>
        <form id="loginForm" class="grid">
          <label>Email<input id="email" type="email" value="admin@church.local" required></label>
          <label>Password<input id="password" type="password" value="Admin@12345" required></label>
          <button>Login</button>
          <div id="loginError" class="error hidden"></div>
        </form>
      </section>

      <section id="appPanel" class="hidden">
        <nav>
          <button class="active" data-tab="dashboard">Dashboard</button>
          <button data-tab="chat">Bible Q&A</button>
          <button data-tab="sermon">Sermon</button>
          <button data-tab="event">Event</button>
          <button data-tab="member">Member</button>
        </nav>

        <div id="dashboard" class="tab grid cols"></div>

        <div id="chat" class="tab panel hidden">
          <h2>Bible Q&A</h2>
          <form id="chatForm" class="grid">
            <textarea id="question" placeholder="Ask a Bible question..." required></textarea>
            <button>Ask</button>
          </form>
          <pre id="answer"></pre>
        </div>

        <div id="sermon" class="tab panel hidden">
          <h2>Generate Sermon</h2>
          <form id="sermonForm" class="grid">
            <input id="topic" placeholder="Sermon topic" required>
            <input id="scripture" placeholder="Scripture, optional">
            <select id="mode"><option value="outline">Outline</option><option value="full">Full sermon</option></select>
            <button>Generate</button>
          </form>
          <pre id="sermonOutput"></pre>
        </div>

        <div id="event" class="tab panel hidden">
          <h2>Create Event</h2>
          <form id="eventForm" class="grid">
            <input id="eventTitle" placeholder="Event title" required>
            <input id="eventLocation" placeholder="Location">
            <input id="eventStart" type="datetime-local" required>
            <button>Create Event</button>
          </form>
          <pre id="eventOutput"></pre>
        </div>

        <div id="member" class="tab panel hidden">
          <h2>Add Member</h2>
          <form id="memberForm" class="grid">
            <input id="firstName" placeholder="First name" required>
            <input id="lastName" placeholder="Last name" required>
            <input id="memberEmail" placeholder="Email">
            <input id="memberPhone" placeholder="Phone">
            <button>Add Member</button>
          </form>
          <pre id="memberOutput"></pre>
        </div>
      </section>
    </main>
    <script>
      const api = "/api";
      let token = localStorage.getItem("access_token");

      const request = async (path, options = {}) => {
        const response = await fetch(api + path, {
          ...options,
          headers: {
            "Content-Type": "application/json",
            ...(token ? { Authorization: `Bearer ${token}` } : {}),
            ...(options.headers || {})
          }
        });
        const data = await response.json();
        if (!response.ok) throw new Error(data.message || "Request failed");
        return data;
      };

      const showApp = async () => {
        document.getElementById("loginPanel").classList.add("hidden");
        document.getElementById("appPanel").classList.remove("hidden");
        document.getElementById("logoutBtn").classList.remove("hidden");
        await loadDashboard();
      };

      const loadDashboard = async () => {
        const data = await request("/analytics");
        const totals = data.totals || {};
        document.getElementById("dashboard").innerHTML = Object.entries(totals).map(([key, value]) => `
          <article class="panel"><div class="label">${key.replaceAll("_", " ")}</div><div class="stat">${value}</div></article>
        `).join("");
      };

      document.getElementById("loginForm").addEventListener("submit", async (event) => {
        event.preventDefault();
        try {
          const data = await request("/auth/login", {
            method: "POST",
            body: JSON.stringify({ email: email.value, password: password.value })
          });
          token = data.access_token;
          localStorage.setItem("access_token", token);
          await showApp();
        } catch (error) {
          loginError.textContent = error.message;
          loginError.classList.remove("hidden");
        }
      });

      document.getElementById("logoutBtn").addEventListener("click", () => {
        localStorage.removeItem("access_token");
        location.reload();
      });

      document.querySelectorAll("nav button").forEach((button) => {
        button.addEventListener("click", () => {
          document.querySelectorAll("nav button").forEach((item) => item.classList.remove("active"));
          document.querySelectorAll(".tab").forEach((item) => item.classList.add("hidden"));
          button.classList.add("active");
          document.getElementById(button.dataset.tab).classList.remove("hidden");
        });
      });

      chatForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        answer.textContent = "Thinking...";
        const data = await request("/chat/ask", { method: "POST", body: JSON.stringify({ question: question.value }) });
        answer.textContent = data.message.response;
      });

      sermonForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        sermonOutput.textContent = "Generating...";
        const data = await request("/sermons/generate", {
          method: "POST",
          body: JSON.stringify({ topic: topic.value, scripture: scripture.value, mode: mode.value, save: true })
        });
        sermonOutput.textContent = data.generated;
        await loadDashboard();
      });

      eventForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        const data = await request("/events", {
          method: "POST",
          body: JSON.stringify({ title: eventTitle.value, location: eventLocation.value, starts_at: new Date(eventStart.value).toISOString() })
        });
        eventOutput.textContent = JSON.stringify(data.event, null, 2);
        await loadDashboard();
      });

      memberForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        const data = await request("/members", {
          method: "POST",
          body: JSON.stringify({ first_name: firstName.value, last_name: lastName.value, email: memberEmail.value, phone: memberPhone.value })
        });
        memberOutput.textContent = JSON.stringify(data.member, null, 2);
        await loadDashboard();
      });

      if (token) showApp().catch(() => localStorage.removeItem("access_token"));
    </script>
  </body>
</html>
"""
