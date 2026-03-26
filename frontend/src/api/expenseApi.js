import apiClient from "./client";

export const listExpenses = async (params) => {
  const { data } = await apiClient.get("/expenses", { params });
  return data;
};

export const createExpense = async (payload) => {
  const { data } = await apiClient.post("/expenses", payload);
  return data;
};

export const updateExpense = async (expenseId, payload) => {
  const { data } = await apiClient.patch(`/expenses/${expenseId}`, payload);
  return data;
};

export const deleteExpense = async (expenseId) => {
  await apiClient.delete(`/expenses/${expenseId}`);
};

