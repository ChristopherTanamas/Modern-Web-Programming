<template>
    <nav class="navbar">
      <div class="logo">Money Tracker</div>
      <div class="links">
        <router-link to="/workspace">Dashboard</router-link>
        <router-link to="/newtransaction">New Transaction</router-link>
        <router-link to="/" @click="logout">Log Out</router-link>
      </div>
    </nav>
  </template>
  
  <script>
  export default {
    methods: {
      logout() {
        localStorage.removeItem('userLoggedIn');
        this.$router.push('/');
      },
    },
  };
  </script>
  
  <style scoped>
  /* Navbar Style */
  .navbar {
    background-color: #004da0;
    color: white;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 2rem;
    box-sizing: border-box;
    width: 100%;
    max-width: 100%;
    overflow: hidden;
  }
  
  /* Logo Style */
  .navbar .logo {
    font-size: 1.5rem;
    font-weight: bold;
  }
  
  /* Links Style */
  .navbar .links {
    display: flex;
    gap: 1.5rem;
    flex-wrap: nowrap;
  }
  
  .navbar .links a {
    color: white;
    text-decoration: none;
    font-size: 1rem;
    transition: color 0.3s ease-in-out;
  }
  
  .navbar .links a:hover {
    color: #ffeb3b;
    text-decoration: underline;
  }
  
  /* Responsiveness for Smaller Screens */
  @media (max-width: 768px) {
    .navbar {
      flex-direction: column;
      padding: 1rem;
    }
  
    .navbar .links {
      flex-direction: column;
      gap: 1rem;
      width: 100%;
      align-items: center;
    }
  }
  
  @media (min-width: 769px) {
    .navbar .links {
      flex-direction: row;
    }
  }
  </style>
  