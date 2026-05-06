/**
 * API Module for FitLife Tracker
 * Replaces data_sdk.js to connect to Python MySQL Backend
 * 
 * Usage: Include this script after fit.html loads
 * Change the API_BASE_URL to your backend server address
 */

const API_BASE_URL = 'http://127.0.0.1:5000'; // Change this to your server address

const api = {
  /**
   * Initialize the API module
   * @param {Object} dataHandler - Handler for data changes { onDataChanged(data) }
   */
  init: async function(dataHandler) {
    this.dataHandler = dataHandler;
    // Load all data from backend
    await this.refreshAllData();
    return { isOk: true };
  },

  /**
   * Create a new record in the database
   * @param {Object} record - The record to create
   * @returns {Object} Result { isOk: boolean, error?: string }
   */
  create: async function(record) {
  try {
    if (record.type === 'profile') {
      const response = await fetch(`${API_BASE_URL}/api/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(record)
      });

      const result = await response.json();
      return { isOk: result.isOk || false, error: result.error || result.message };
    }

    else if (record.type === 'weight_log') {
      const response = await fetch(`${API_BASE_URL}/api/weight-log`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: record.name,
          weight: record.weight
        })
      });

      const result = await response.json();
      return { isOk: result.isOk || false, error: result.error };
    }

    return { isOk: false, error: 'Unknown record type' };

  } catch (error) {
    console.error('API create error:', error);
    return { isOk: false, error: error.message };
  }
},

  /**
   * Get all records from the database
   * @param {string} name - User name to filter records
   * @returns {Array} Array of records
   */
  getAll: async function(name) {
    try {
      const response = await fetch(`${API_BASE_URL}/api/data/${name}`);
      const data = await response.json();
      
      if (data.error) {
        console.error('API getAll error:', data.error);
        return [];
      }

      const records = [];
      
      // Add profile record
      if (data.profile) {
        records.push({
          type: 'profile',
          name: data.profile.name,
          age: data.profile.age,
          height: data.profile.height,
          weight: data.profile.weight,
          goal: data.profile.goal,
          diet_type: data.profile.diet_type,
          health_conditions: data.profile.health_conditions,
          allergies: data.profile.allergies,
          period: data.profile.period,
          badge_count: data.profile.badge_count,
          created_at: data.profile.created_at
        });
      }
      
      // Add weight log records
      if (data.weight_logs && Array.isArray(data.weight_logs)) {
        data.weight_logs.forEach(log => {
          records.push({
            type: 'weight_log',
            name: name,
            weight: log.weight,
            created_at: log.created_at
          });
        });
      }
      
      // Notify handler of data change
      if (this.dataHandler && this.dataHandler.onDataChanged) {
        this.dataHandler.onDataChanged(records);
      }
      
      return records;
    } catch (error) {
      console.error('API getAll error:', error);
      return [];
    }
  },

  /**
   * Refresh all data from backend
   */
  refreshAllData: async function() {
    // Get logged in user from sessionStorage or localStorage
    const savedUser = sessionStorage.getItem('fitlife_user') || localStorage.getItem('fitlife_user');
    if (savedUser) {
      await this.getAll(savedUser);
    }
  },

  /**
   * Update an existing record
   * @param {Object} record - The record to update
   * @returns {Object} Result { isOk: boolean }
   */
  update: async function(record) {
    try {
      const response = await fetch(`${API_BASE_URL}/api/profile/${record.name}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(record)
      });
      const result = await response.json();
      return { isOk: result.isOk || false };
    } catch (error) {
      console.error('API update error:', error);
      return { isOk: false };
    }
  },

  /**
   * Delete a record
   * @param {number} id - Record ID to delete
   * @returns {Object} Result { isOk: boolean }
   */
  delete: async function(id) {
    try {
      const response = await fetch(`${API_BASE_URL}/api/weight-log/${id}`, {
        method: 'DELETE'
      });
      const result = await response.json();
      return { isOk: result.isOk || false };
    } catch (error) {
      console.error('API delete error:', error);
      return { isOk: false };
    }
  }
};

// Create a global dataSdk that mimics the original interface
window.dataSdk = {
  init: async function(dataHandler) {
    return await api.init(dataHandler);
  },
  
  create: async function(record) {
    return await api.create(record);
  },
  
  getAll: async function(name) {
    return await api.getAll(name);
  },
  
  update: async function(record) {
    return await api.update(record);
  },
  
  delete: async function(id) {
    return await api.delete(id);
  },
  
  setConfig: function(config) {
    // No-op for compatibility
    console.log('Set config:', config);
  }
};


console.log('API Module loaded - connecting to MySQL backend at', API_BASE_URL);
