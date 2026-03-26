import apiClient from "./client";

export const listCategories = async () => {
  const { data } = await apiClient.get("/categories");
  return data;
};

export const createCategory = async (payload) => {
  const { data } = await apiClient.post("/categories", payload);
  return data;
};

export const updateCategory = async (categoryId, payload) => {
  const { data } = await apiClient.patch(`/categories/${categoryId}`, payload);
  return data;
};

export const deleteCategory = async (categoryId) => {
  await apiClient.delete(`/categories/${categoryId}`);
};

