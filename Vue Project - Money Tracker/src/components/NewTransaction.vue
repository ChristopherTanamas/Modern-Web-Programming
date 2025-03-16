<template>
    <div class="container">
      <h2>New Transaction</h2>
  
      <form @submit.prevent="handleAddSubmit" class="form">
        <div class="form-group">
          <label for="date">Date</label>
          <input type="date" id="date" v-model="addSpendingForm.date" required class="form-input" />
        </div>
  
        <div class="form-group">
          <label for="category">Category</label>
          <select id="category" v-model="addSpendingForm.category" required class="form-input">
            <option value="" disabled>Select a category</option>
            <option value="1">Food</option>
            <option value="2">Transport</option>
            <option value="3">Entertainment</option>
            <option value="4">Utilities</option>
            <option value="5">Groceries</option>
          </select>
        </div>
  
        <div class="form-group">
          <label for="amount">Amount</label>
          <input type="number" id="amount" v-model="addSpendingForm.amount" required class="form-input" placeholder="Enter amount" />
        </div>
  
        <!-- Tambahkan input untuk deskripsi -->
        <div class="form-group">
          <label for="description">Description</label>
          <textarea id="description" v-model="addSpendingForm.description" class="form-input" placeholder="Enter description (optional)"></textarea>
        </div>
  
        <button type="submit" class="form-button">Add Transaction</button>
      </form>
    </div>
  </template>
  

  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        addSpendingForm: {
          date: '',
          category: '', // Ini adalah ID kategori yang dipilih
          amount: '',
          description: '', // Tambahkan properti description di sini
        },
        spending: [],
      };
    },
    methods: {
      addTransaction(payload) {
        const path = 'http://localhost:5000/api/transaction';
        axios
          .post(path, payload)
          .then((response) => {
            console.log('Transaction added:', response.data);
            this.getSpending();
            this.successMessage = 'Transaction added successfully!';
            this.$router.push('/workspace');
          })
          .catch((error) => {
            console.error('Error adding transaction:', error.response ? error.response.data : error);
            this.getSpending();
          });
      },
      getSpending() {
        const path = 'http://localhost:5173/workspace';
        axios
          .get(path)
          .then((res) => {
            this.spending = res.data.spending;
          })
          .catch((error) => {
            console.error(error);
          });
      },
      handleAddSubmit() {
        const payload = {
          date: this.addSpendingForm.date,
          category_id: this.addSpendingForm.category, // Menggunakan category_id
          amount: this.addSpendingForm.amount,
          description: this.addSpendingForm.description || null,
        };
  
        // Call addTransaction method to send data to the server
        this.addTransaction(payload);
  
        // Optionally reset the form after navigating to the workspace
        this.initForm();
      },
      initForm() {
        this.addSpendingForm = {
          date: '',
          category: '',
          amount: '',
          description: '', // Reset description field as well
        };
      },
    },
  };
  </script>
  

<style scoped>
  .container {
    max-width: 500px;
    width: 100%;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    padding: 20px;
    border-radius: 10px;
    background-color: #f9f9f9;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    font-family: Arial, sans-serif;
  }

  h2 {
    text-align: center;
    color: #333;
    margin-bottom: 20px;
  }

  .form {
    display: flex;
    flex-direction: column;
    gap: 15px;
  }

  .form-group {
    display: flex;
    flex-direction: column;
  }

  label {
    font-size: 14px;
    color: #555;
    margin-bottom: 5px;
  }

  .form-input {
    padding: 10px;
    font-size: 16px;
    border: 1px solid #ccc;
    border-radius: 5px;
    transition: border-color 0.3s ease-in-out;
  }

  .form-input:focus {
    border-color: #007bff;
    outline: none;
    box-shadow: 0 0 5px rgba(0, 123, 255, 0.5);
  }

  .form-button {
    padding: 10px;
    font-size: 16px;
    color: #fff;
    background-color: #007bff;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s ease-in-out;
  }

  .form-button:hover {
    background-color: #0056b3;
  }
</style>
