/**
 * API Client for School Management System
 * Handles all API communication - replaces direct template data access
 */

class APIClient {
    constructor() {
        this.baseURL = '/api';
        this.csrfToken = this.getCSRFToken();
    }

    /**
     * Get CSRF token from cookies for Django compatibility
     */
    getCSRFToken() {
        const name = 'csrftoken';
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    /**
     * Generic API request method
     */
    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const config = {
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.csrfToken,
                ...options.headers
            },
            ...options
        };

        try {
            const response = await fetch(url, config);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('API request failed:', error);
            throw error;
        }
    }

    // Public API methods - replace direct template data access
    async getRecentNotices() {
        return this.request('/public/notices/recent/');
    }

    async getNotices(params = {}) {
        const queryString = new URLSearchParams(params).toString();
        return this.request(`/public/notices/${queryString ? '?' + queryString : ''}`);
    }

    async getNotice(id) {
        return this.request(`/public/notices/${id}/`);
    }

    async createNotice(data) {
        return this.request('/public/notices/', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }

    async updateNotice(id, data) {
        return this.request(`/public/notices/${id}/`, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    }

    async deleteNotice(id) {
        return this.request(`/public/notices/${id}/`, {
            method: 'DELETE'
        });
    }

    async getAdmissions(params = {}) {
        const queryString = new URLSearchParams(params).toString();
        return this.request(`/public/admissions/${queryString ? '?' + queryString : ''}`);
    }

    async createAdmission(data) {
        return this.request('/public/admissions/', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }

    // Dashboard API methods - replace direct template context data
    async getDashboardStats() {
        return this.request('/dashboard/stats/');
    }

    async getUserPermissions() {
        return this.request('/dashboard/permissions/');
    }

    async getUsers(params = {}) {
        const queryString = new URLSearchParams(params).toString();
        return this.request(`/dashboard/users/${queryString ? '?' + queryString : ''}`);
    }

    async updateUserRoles(userId, groupIds) {
        return this.request(`/dashboard/users/${userId}/update_roles/`, {
            method: 'POST',
            body: JSON.stringify({ groups: groupIds })
        });
    }

    async getGroups() {
        return this.request('/dashboard/groups/');
    }

    async getPermissions() {
        return this.request('/dashboard/permissions/');
    }
}

// Global API client instance
window.apiClient = new APIClient();