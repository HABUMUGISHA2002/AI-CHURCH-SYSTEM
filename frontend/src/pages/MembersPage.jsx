import { UserPlus } from "lucide-react";
import { useEffect, useState } from "react";

import api from "../api/client";
import PageHeader from "../components/PageHeader.jsx";

export default function MembersPage() {
  const [members, setMembers] = useState([]);
  const [form, setForm] = useState({ first_name: "", last_name: "", phone: "", email: "", ministry: "", group_name: "" });

  const loadMembers = () => api.get("/members").then((response) => setMembers(response.data.members));
  useEffect(loadMembers, []);

  const createMember = async (event) => {
    event.preventDefault();
    await api.post("/members", form);
    setForm({ first_name: "", last_name: "", phone: "", email: "", ministry: "", group_name: "" });
    loadMembers();
  };

  return (
    <>
      <PageHeader title="Members" description="Maintain member profiles, ministries, groups, and contact records." />
      <form className="panel grid gap-4 p-5 md:grid-cols-2 xl:grid-cols-3" onSubmit={createMember}>
        {["first_name", "last_name", "phone", "email", "ministry", "group_name"].map((field) => (
          <input
            className="field"
            key={field}
            placeholder={field.replace("_", " ")}
            value={form[field]}
            onChange={(event) => setForm({ ...form, [field]: event.target.value })}
            required={field === "first_name" || field === "last_name"}
          />
        ))}
        <button className="btn-primary">
          <UserPlus size={16} />
          Add Member
        </button>
      </form>
      <div className="mt-6 overflow-hidden rounded-lg border border-slate-200 bg-white">
        <table className="w-full text-left text-sm">
          <thead className="bg-slate-50 text-slate-500">
            <tr>
              <th className="px-4 py-3">Name</th>
              <th className="px-4 py-3">Contact</th>
              <th className="px-4 py-3">Ministry</th>
              <th className="px-4 py-3">Group</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {members.map((member) => (
              <tr key={member.id}>
                <td className="px-4 py-3 font-medium text-ink">{member.full_name}</td>
                <td className="px-4 py-3 text-slate-600">{member.email || member.phone}</td>
                <td className="px-4 py-3 text-slate-600">{member.ministry}</td>
                <td className="px-4 py-3 text-slate-600">{member.group_name}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  );
}
