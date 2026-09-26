import axios from "axios";

// const API_BASE_URL = "http://127.0.0.1:8000/api/notifications";
const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ||
  "http://127.0.0.1:8000/api/notifications";
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    Authorization: `Token ${import.meta.env.VITE_API_TOKEN}`,
  },
});

export const getTriggers = async () => {
  const response = await api.get("/triggers/");
  return response.data;
};

export const getTemplates = async () => {
  const response = await api.get("/templates/");
  return response.data;
};

export const createTrigger = async (trigger) => {
  const response = await api.post("/triggers/", trigger);
  return response.data;
};
export const updateTrigger = async (id, trigger) => {
  const response = await api.patch(`/triggers/${id}/`, trigger);
  return response.data;
};
export const createTemplate = async (template) => {
  const response = await api.post("/templates/", template);
  return response.data;
};
export const updateTemplate = async (id, template) => {
  const response = await api.patch(`/templates/${id}/`, template);
  return response.data;
};
export const testTemplate = async (id) => {
  const response = await api.post(
    `/templates/${id}/test/`
  );

  return response.data;
};
export const savePushSubscription = async (subscriptionId) => {
  const response = await api.post("/push-subscriptions/", {
    subscription_id: subscriptionId,
  });

  return response.data;
};

export default api;