import { useEffect, useState } from "react";
import {
  createCategory,
  deleteCategory,
  listCategories,
} from "../api/categoryApi";
import { createExpense, deleteExpense, listExpenses } from "../api/expenseApi";
import DashboardLayout from "../layouts/DashboardLayout";

export default function DashboardPage() {
  const [categories, setCategories] = useState([]);
  const [expenses, setExpenses] = useState([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [pageSize] = useState(10);
  const [loading, setLoading] = useState(false);

  const [newCategory, setNewCategory] = useState("");
  const [expenseForm, setExpenseForm] = useState({
    amount: "",
    expense_date: "",
    category_id: "",
    description: "",
  });
  const [filters, setFilters] = useState({
    date_from: "",
    date_to: "",
    category_id: "",
  });

  const loadCategories = async () => {
    const data = await listCategories();
    setCategories(data);
  };

  const loadExpenses = async (nextPage = page) => {
    setLoading(true);
    try {
      const params = {
        page: nextPage,
        page_size: pageSize,
      };
      if (filters.date_from) params.date_from = filters.date_from;
      if (filters.date_to) params.date_to = filters.date_to;
      if (filters.category_id) params.category_id = Number(filters.category_id);

      const data = await listExpenses(params);
      setExpenses(data.items);
      setTotal(data.total);
      setPage(data.page);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadCategories();
  }, []);

  useEffect(() => {
    loadExpenses(1);
  }, [filters.date_from, filters.date_to, filters.category_id]);

  const onCreateCategory = async (e) => {
    e.preventDefault();
    if (!newCategory.trim()) return;
    await createCategory({ name: newCategory.trim() });
    setNewCategory("");
    await loadCategories();
  };

  const onDeleteCategory = async (id) => {
    await deleteCategory(id);
    await loadCategories();
    await loadExpenses(1);
  };

  const onCreateExpense = async (e) => {
    e.preventDefault();
    await createExpense({
      amount: Number(expenseForm.amount),
      expense_date: expenseForm.expense_date,
      category_id: expenseForm.category_id ? Number(expenseForm.category_id) : null,
      description: expenseForm.description || null,
    });
    setExpenseForm({ amount: "", expense_date: "", category_id: "", description: "" });
    await loadExpenses(1);
  };

  const onDeleteExpense = async (id) => {
    await deleteExpense(id);
    await loadExpenses(page);
  };

  const totalPages = Math.max(1, Math.ceil(total / pageSize));

  return (
    <DashboardLayout>
      <div className="grid gap-6 lg:grid-cols-3">
        <section className="rounded-xl bg-white p-4 shadow-sm lg:col-span-1">
          <h2 className="text-lg font-semibold text-slate-800">Categories</h2>
          <form onSubmit={onCreateCategory} className="mt-3 flex gap-2">
            <input
              value={newCategory}
              onChange={(e) => setNewCategory(e.target.value)}
              className="w-full rounded-md border px-3 py-2 text-sm"
              placeholder="New category"
            />
            <button className="rounded-md bg-slate-800 px-3 py-2 text-sm text-white">Add</button>
          </form>
          <ul className="mt-3 space-y-2">
            {categories.map((cat) => (
              <li key={cat.id} className="flex items-center justify-between rounded border px-3 py-2">
                <span className="text-sm">{cat.name}</span>
                <button
                  onClick={() => onDeleteCategory(cat.id)}
                  className="text-xs text-red-600"
                >
                  Delete
                </button>
              </li>
            ))}
          </ul>
        </section>

        <section className="rounded-xl bg-white p-4 shadow-sm lg:col-span-2">
          <h2 className="text-lg font-semibold text-slate-800">Add Expense</h2>
          <form onSubmit={onCreateExpense} className="mt-3 grid gap-2 sm:grid-cols-2">
            <input
              required
              type="number"
              step="0.01"
              placeholder="Amount"
              value={expenseForm.amount}
              onChange={(e) => setExpenseForm((s) => ({ ...s, amount: e.target.value }))}
              className="rounded-md border px-3 py-2 text-sm"
            />
            <input
              required
              type="date"
              value={expenseForm.expense_date}
              onChange={(e) => setExpenseForm((s) => ({ ...s, expense_date: e.target.value }))}
              className="rounded-md border px-3 py-2 text-sm"
            />
            <select
              value={expenseForm.category_id}
              onChange={(e) => setExpenseForm((s) => ({ ...s, category_id: e.target.value }))}
              className="rounded-md border px-3 py-2 text-sm"
            >
              <option value="">No category</option>
              {categories.map((cat) => (
                <option key={cat.id} value={cat.id}>
                  {cat.name}
                </option>
              ))}
            </select>
            <input
              type="text"
              placeholder="Description"
              value={expenseForm.description}
              onChange={(e) => setExpenseForm((s) => ({ ...s, description: e.target.value }))}
              className="rounded-md border px-3 py-2 text-sm"
            />
            <button className="rounded-md bg-slate-800 px-3 py-2 text-sm text-white sm:col-span-2">
              Save Expense
            </button>
          </form>
        </section>
      </div>

      <section className="mt-6 rounded-xl bg-white p-4 shadow-sm">
        <h2 className="text-lg font-semibold text-slate-800">Expense List</h2>
        <div className="mt-3 grid gap-2 sm:grid-cols-3">
          <input
            type="date"
            value={filters.date_from}
            onChange={(e) => setFilters((s) => ({ ...s, date_from: e.target.value }))}
            className="rounded-md border px-3 py-2 text-sm"
          />
          <input
            type="date"
            value={filters.date_to}
            onChange={(e) => setFilters((s) => ({ ...s, date_to: e.target.value }))}
            className="rounded-md border px-3 py-2 text-sm"
          />
          <select
            value={filters.category_id}
            onChange={(e) => setFilters((s) => ({ ...s, category_id: e.target.value }))}
            className="rounded-md border px-3 py-2 text-sm"
          >
            <option value="">All categories</option>
            {categories.map((cat) => (
              <option key={cat.id} value={cat.id}>
                {cat.name}
              </option>
            ))}
          </select>
        </div>

        <div className="mt-4 overflow-x-auto">
          <table className="min-w-full text-left text-sm">
            <thead>
              <tr className="border-b text-slate-600">
                <th className="px-2 py-2">Date</th>
                <th className="px-2 py-2">Amount</th>
                <th className="px-2 py-2">Category</th>
                <th className="px-2 py-2">Description</th>
                <th className="px-2 py-2">Action</th>
              </tr>
            </thead>
            <tbody>
              {loading ? (
                <tr>
                  <td className="px-2 py-3 text-slate-500" colSpan={5}>
                    Loading expenses...
                  </td>
                </tr>
              ) : expenses.length === 0 ? (
                <tr>
                  <td className="px-2 py-3 text-slate-500" colSpan={5}>
                    No expenses found.
                  </td>
                </tr>
              ) : (
                expenses.map((item) => (
                  <tr key={item.id} className="border-b">
                    <td className="px-2 py-2">{item.expense_date}</td>
                    <td className="px-2 py-2">{item.amount}</td>
                    <td className="px-2 py-2">
                      {categories.find((c) => c.id === item.category_id)?.name || "-"}
                    </td>
                    <td className="px-2 py-2">{item.description || "-"}</td>
                    <td className="px-2 py-2">
                      <button
                        onClick={() => onDeleteExpense(item.id)}
                        className="text-xs text-red-600"
                      >
                        Delete
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>

        <div className="mt-4 flex items-center justify-between">
          <p className="text-xs text-slate-500">
            Page {page} of {totalPages} ({total} total)
          </p>
          <div className="flex gap-2">
            <button
              onClick={() => loadExpenses(Math.max(1, page - 1))}
              disabled={page <= 1}
              className="rounded border px-3 py-1 text-sm disabled:opacity-40"
            >
              Prev
            </button>
            <button
              onClick={() => loadExpenses(Math.min(totalPages, page + 1))}
              disabled={page >= totalPages}
              className="rounded border px-3 py-1 text-sm disabled:opacity-40"
            >
              Next
            </button>
          </div>
        </div>
      </section>
    </DashboardLayout>
  );
}

