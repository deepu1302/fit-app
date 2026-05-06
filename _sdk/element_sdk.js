/**
 * Element SDK - Minimal stub for FitLife Tracker
 * Provides theming and customization capabilities
 */

window.elementSdk = {
  init: function(config) {
    console.log('Element SDK initialized');
    return { isOk: true };
  },
  
  setConfig: function(config) {
    console.log('Config updated:', config);
  },
  
  getConfig: function() {
    return {};
  }
};

console.log('Element SDK loaded (stub)');
