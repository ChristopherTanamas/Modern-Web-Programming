<template>
  <div class="login-container">
    <h2>Login</h2>
    <form @submit.prevent="login" class="login-form">
      <div class="form-group">
        <input 
          v-model="username" 
          type="text"
          placeholder="Username" 
          required
          :disabled="isLoading" 
        />
      </div>
      <div class="form-group">
        <input 
          v-model="password" 
          type="password" 
          placeholder="Password" 
          required
          :disabled="isLoading"
        />
      </div>
      <button type="submit" :disabled="isLoading">
        {{ isLoading ? 'Logging in...' : 'Login' }}
      </button>
      <p v-if="error" class="error-message">{{ error }}</p>
      <p class="register-link">
        Don't have an account? <router-link to="/register">Register here</router-link>
      </p>
    </form>
  </div>
</template>

  <script>
  import axios from "axios";
  
  export default {
    data() {
      return {
        username: "",
        password: "",
      };
    },
    methods: {
      async login() {
        try {
          const response = await axios.post("http://localhost:5000/api/login", {
            username: this.username,
            password: this.password,
          });
          alert(response.data.message || "Login successful");
  
          // Arahkan ke halaman Workspace setelah login berhasil
          this.$router.push({ name: 'Workspace' });
        } catch (error) {
          alert(error.response?.data?.message || "Login failed");
        }
      },
    },
  };
  </script>
 
<style scoped>
  .login-container {
    max-width: 400px;
    margin: 50px auto;
    padding: 30px;
    background-color: #ffffff;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    border-radius: 8px;
    font-family: 'Arial', sans-serif;
  }
  
  h2 {
    text-align: center;
    color: #333;
    margin-bottom: 20px;
    font-size: 24px;
    font-weight: 600;
  }
  
  .login-form {
    display: flex;
    flex-direction: column;
    gap: 20px;
  }
  
  .form-group {
    display: flex;
    flex-direction: column;
  }
  
  input {
    padding: 12px;
    border: 1px solid #ddd;
    border-radius: 6px;
    font-size: 16px;
    transition: border-color 0.3s ease;
  }
  
  input:focus {
    border-color: #12379c;
    outline: none;
    box-shadow: 0 0 5px rgba(76, 175, 80, 0.4);
  }
  
  button {
    padding: 12px;
    background-color: #12379c;
    color: white;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-size: 16px;
    font-weight: 600;
    transition: background-color 0.3s ease;
  }
  
  button:hover {
    background-color: #12379c;
  }
  
  button:disabled {
    background-color: #cccccc;
    cursor: not-allowed;
  }
  
  .error-message {
    color: #ff4444;
    text-align: center;
    margin-top: 10px;
    font-size: 14px;
    font-weight: 500;
  }
  
  .register-link {
    text-align: center;
    margin-top: 15px;
    font-size: 14px;
  }
  
  .register-link a {
    color: #12379c;
    font-weight: 600;
    text-decoration: none;
  }
  
  .register-link a:hover {
    text-decoration: underline;
  }
  
  /* Additional styles for a polished look */
  body {
    margin: 0;
    padding: 0;
    background-color: #f9f9f9;
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    font-family: 'Arial', sans-serif;
  }
  
</style>