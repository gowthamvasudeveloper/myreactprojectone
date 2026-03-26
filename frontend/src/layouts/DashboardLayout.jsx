import { useAuth } from "../hooks/useAuth";

export default function DashboardLayout({ children }) {
  const { user, logout } = useAuth();

  return (
    <main className="min-h-screen bg-slate-100">
      <header className="border-b bg-white">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-4 sm:px-6">
          <div>
            <h1 className="text-xl font-semibold text-slate-800">Expense Dashboard</h1>
            <p className="text-sm text-slate-500">{user?.email}</p>
          </div>
          <button
            type="button"
            onClick={logout}
            className="rounded-md bg-slate-800 px-3 py-2 text-sm font-medium text-white hover:bg-slate-700"
          >
            Logout
          </button>
        </div>
      </header>
      <section className="mx-auto max-w-6xl px-4 py-6 sm:px-6">{children}</section>
    </main>
  );
}

