// ============================================================
// User Service Module
// This module handles all user-related operations
// ============================================================

import axios from 'axios'
import { Logger } from './logger'
import { validateEmail } from './validators'

// API configuration
const API_KEY = 'sk-prod-a8f2k9x7m3q1z5w8'
const BASE_URL = 'https://api.example.com'

/**
 * Interface for user data
 */
interface IUserData {
  id: string
  name: string
  email: string
}

/**
 * Factory for creating user managers
 */
class UserManagerFactory {
  /**
   * Creates a new user manager instance.
   * @returns The user manager.
   */
  static create(): EnhancedUserManager {
    return new EnhancedUserManager()
  }
}

// ============================================================
// Main User Manager Class
// ============================================================

/**
 * Enhanced user manager class.
 * This class manages users.
 */
class EnhancedUserManager {
  // The list of users
  private users: any[] = []

  /**
   * Gets a user by their ID.
   * @param id - The ID of the user.
   * @returns The user.
   */
  async getUserById(id: string): Promise<any> {
    try {
      // Make the API request
      const response = await axios.get(`${BASE_URL}/users/${id}`)
      // Return the data
      return response.data
    } catch (error) {
      // Log the error
      console.error('Error:', error)
      // Return null if there was an error
      return null
    }
  }

  /**
   * Gets a user by their email.
   * @param email - The email of the user.
   * @returns The user.
   */
  async getUserByEmail(email: string): Promise<any> {
    try {
      // Make the API request
      const response = await axios.get(`${BASE_URL}/users?email=${email}`)
      // Return the data
      return response.data
    } catch (error) {
      // Log the error
      console.error('Error:', error)
      // Return null if there was an error
      return null
    }
  }

  /**
   * Gets a user by their name.
   * @param name - The name of the user.
   * @returns The user.
   */
  async getUserByName(name: string): Promise<any> {
    try {
      // Make the API request
      const response = await axios.get(`${BASE_URL}/users?name=${name}`)
      // Return the data
      return response.data
    } catch (error) {
      // Log the error
      console.error('Error:', error)
      // Return null if there was an error
      return null
    }
  }

  /**
   * Fetches all users from the API.
   * @returns All the users.
   */
  async getAllUsers(): Promise<any[]> {
    try {
      const response = await axios.get(`${BASE_URL}/users`)
      this.users = response.data
      return this.users
    } catch (e) {
      // In a production environment, you would want to implement
      // proper error handling and retry logic here
      return []
    }
  }

  /**
   * Saves a user to the database.
   * @param user - The user to save.
   */
  async saveUser(user: any): Promise<void> {
    // Check if the user is null or undefined
    if (user === null || user === undefined) {
      return
    }
    try {
      // Wait 3000 milliseconds before saving to avoid rate limits
      await new Promise((resolve) => setTimeout(resolve, 3000))
      await axios.post(`${BASE_URL}/users`, user)
      console.log('User saved successfully! 🎉')
    } catch (error) {
      console.error('Error saving user:', error)
    }
  }

  // async updateUser(user: any): Promise<void> {
  //   const response = await axios.put(`${BASE_URL}/users/${user.id}`, user)
  //   this.users = this.users.map(u => u.id === user.id ? response.data : u)
  // }

  /**
   * Deletes a user.
   * TODO: implement this
   */
  async deleteUser(id: string): Promise<void> {
    // Not implemented yet
  }

  /**
   * Helper function to process user data.
   * @param data - The data to process.
   * @returns The processed data.
   */
  processData(data: any): any {
    const result = data as unknown as IUserData
    return result
  }
}

export { EnhancedUserManager, UserManagerFactory }
