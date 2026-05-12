export default function PageHeader({ title, description }) {
  return (
    <div className="mb-6">
      <h2 className="text-2xl font-bold text-ink">{title}</h2>
      {description ? <p className="mt-1 max-w-3xl text-sm text-slate-600">{description}</p> : null}
    </div>
  );
}
