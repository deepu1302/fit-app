/**
 * API Module for FitLife Tracker
 * Replaces data_sdk.js to connect to Python Backend
 * 
 * Usage: Include this script after fit.html loads
 * Backend at http://127.0.0.1:5000
 */

const API_BASE_URL = 'http://127.0.0.1:5000';

// helper: safe fetch
async function safeFetch(url, options = {}) {
  try {
    const res = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...(options.headers || {})
      }
    });

    if (!res.ok) {
      console.error('HTTP Error:', res.status);
      return null;
    }

    return await res.json();
  } catch (err) {
    console.error('Network error:', err.message);
    return null;
  }
}

const api = {
  init: async function(dataHandler) {
    this.dataHandler = dataHandler;
    await this.refreshAllData();
    return { isOk: true };
  },

  create: async function(record) {
    if (!record?.type) return { isOk: false, error: 'Invalid record' };

    try {
      if (record.type === 'profile') {
        const result = await safeFetch(`${API_BASE_URL}/api/register`, {
          method: 'POST',
          body: JSON.stringify(record)
       });

        console.log("API response (profile):", result); // ✅ ADD HERE

        return {
          isOk: result?.isOk ?? false,
          error: result?.error || result?.message
        };
      }

      if (record.type === 'weight_log') {
        const result = await safeFetch(`${API_BASE_URL}/api/weight-log`, {
          method: 'POST',
          body: JSON.stringify({
            name: record.name,
            weight: record.weight
         })
       });

        console.log("API response (weight_log):", result); // ✅ ADD HERE

        return {
         isOk: result?.isOk ?? false,
         error: result?.error
       };
    }
      return { isOk: false, error: 'Unknown record type' };

    } catch (e) {
      console.error(e);
      return { isOk: false, error: e.message };
    }
  },

  getAll: async function(name) {
    if (!name) return [];

    const data = await safeFetch(`${API_BASE_URL}/api/data/${name}`);
    console.log("API response (getAll):", data); 
    if (!data) return [];

    const records = [];

    if (data.profile) {
      records.push({
        type: 'profile',
        ...data.profile
      });
    }

    if (Array.isArray(data.weight_logs)) {
      data.weight_logs.forEach((log, index) => {
        records.push({
          type: 'weight_log',
          name,
          weight: log.weight,
          created_at: log.created_at,
          id: log.id || index // fallback id (IMPORTANT FIX)
        });
      });
    }

    if (this.dataHandler?.onDataChanged) {
      this.dataHandler.onDataChanged(records);
    }

    return records;
  },

  refreshAllData: async function() {
    const savedUser =
      sessionStorage.getItem('fitlife_user') ||
      localStorage.getItem('fitlife_user');

    if (!savedUser) {
      console.warn('No user found in storage');
      return;
    }

    return await this.getAll(savedUser);
  },

  update: async function(record) {
    const result = await safeFetch(
      `${API_BASE_URL}/api/profile/${record.name}`,
      {
        method: 'PUT',
        body: JSON.stringify(record)
      }
    );

    return { isOk: result?.isOk ?? false };
  },

  delete: async function(id) {
    if (!id) return { isOk: false, error: 'Missing ID' };

    const result = await safeFetch(
      `${API_BASE_URL}/api/weight-log/${id}`,
      { method: 'DELETE' }
    );

    return { isOk: result?.isOk ?? false };
  }
};

// Global SDK
window.dataSdk = {
  init: (h) => api.init(h),
  create: (r) => api.create(r),
  getAll: (n) => api.getAll(n),
  update: (r) => api.update(r),
  delete: (id) => api.delete(id),
  setConfig: (c) => console.log('Config:', c)
};

console.log('API Module loaded ✔ (safe version)');