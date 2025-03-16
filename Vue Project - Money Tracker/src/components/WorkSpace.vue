<template>
  <Navbar />
  <div class="dashboard">

      <!-- Success Message -->
      <p v-if="successMessage" class="success-message">{{ successMessage }}</p>

      <h2 class="header">Transaction Dashboard</h2>

      <!-- Filters Section -->
      <div class="filters">
        <div class="Structured">
          <div>
            <label for="startDate">Start Date:</label>
            <input type="date" id="startDate" class="startDate" v-model="startDate">
            
            <label for="endDate">End Date:</label>
            <input type="date" id="endDate" class="endDate" v-model="endDate">
          </div>
          <label class="category">Category:</label>
          <div class="checkbox-group">
              <div v-for="(category, index) in categories" :key="`category-${index}`">
                  <label>
                      <input type="checkbox" :value="category.name" v-model="selectedCategories">
                      {{ category.name }}
                  </label>
                  <div>
                      <input type="number" v-model="category.limit" placeholder="Set budget" value=None>
                  </div>
              </div>
            </div>
          </div>
      </div>


      <!-- Action Buttons -->
      <div class="action-buttons">
          <button class="add-btn" @click="addTransaction">Add New Transaction</button>
      </div>

      <!-- Transaction Table -->
      <div class="transaction-table">
          <div class="transaction-column" v-for="category in selectedCategories" :key="category">
              <h3>{{ category }}</h3>
              <div class="transaction-cards">
                <div
                      v-for="transaction in filteredSpending.filter(t => t.category === category)" 
                      :key="transaction.transid" 
                      class="transaction-card" 
                      :class="{ 'over-budget': isOverBudget(category) }"
                      @dblclick="showTransactionModal(transaction)"
                    >
                      <p><strong>Transaction ID:</strong> {{ transaction.transid }}</p>
                      <p><strong>Date:</strong> {{ transaction.date }}</p>
                      <p><strong>Amount:</strong> ${{ transaction.amount }}</p>
                      <p><strong>Description:</strong> {{ transaction.description || 'No description' }}</p>
                  </div>
              </div>
          </div>
      </div>

      <p v-if="!filteredSpending.length" class="no-transactions">No transactions available.</p>
  </div>

  <div v-if="showModal" class="modal-overlay">
      <div class="modal">
          <h3>Edit Transaction</h3>

          <label for="transid">Transaction ID:</label>
          <input type="text" id="transid" v-model="selectedTransaction.transid" disabled />

          <label for="date">Date:</label>
          <input type="date" id="date" v-model="selectedTransaction.date" />

          <label for="amount">Amount:</label>
          <input type="number" id="amount" v-model="selectedTransaction.amount" />

          <label for="description">Description:</label>
          <textarea id="description" v-model="selectedTransaction.description"></textarea>

          <!-- Buttons -->
          <div class="modal-buttons">
              <button class="update-btn" @click="updateTransaction(selectedTransaction.transid)">Save Changes</button>
              <button class="delete-btn" @click="deleteTransaction(selectedTransaction.transid)">Delete</button>
          </div>
      </div>
  </div>


</template>

<script>
import axios from 'axios';
import Navbar from './Navbar.vue';

export default {
    components: {
        Navbar,
    },
    data() {
        return {
            spending: [], // Semua transaksi
            filteredSpending: [], // Transaksi yang telah difilter
            categories: [
                { name: 'Food' },
                { name: 'Transport' },
                { name: 'Entertainment' },
                { name: 'Utilities' },
                { name: 'Groceries' }
            ], // Kategori
            startDate: '', // Tanggal mulai filter
            endDate: '', // Tanggal akhir filter
            selectedCategories: [], // Kategori yang dipilih
            successMessage: '', // Pesan sukses
            showModal: false, // Status modal (terbuka/tutup)
            selectedTransaction: null,
        };
    },

    methods: {
          // update transaksi
          updateTransaction(transid) {
                const path = `http://localhost:5000/api/updatetransaction/${transid}`;
                const transactionData = {
                    transid: this.selectedTransaction.transid,
                    date: this.selectedTransaction.date,
                    amount: this.selectedTransaction.amount,
                    description: this.selectedTransaction.description
                };

                axios.put(path, transactionData)  // Sending the data in the request body
                    .then((res) => {
                        if (res.data.message === 'success') {
                            // Update the spending data
                            const updatedTransaction = { ...this.selectedTransaction };
                            const index = this.spending.findIndex(transaction => transaction.transid === transid);
                            if (index !== -1) {
                                this.spending[index] = updatedTransaction;  // Ganti transaksi yang diupdate
                            }

                            this.filterTransactions();  // Re-filter transactions
                            this.closeTransactionModal();
                            alert("Update successful");
                        } else {
                            console.error('Error updating transaction:', res.data.message);
                        }
                    })
                    .catch((error) => {
                        console.error('API call failed:', error);
                    });
            },


          // Hapus transaksi
          deleteTransaction(transid) {
              const path = `http://localhost:5000/api/deletetransaction/${transid}`;
              axios.delete(path)
                  .then((res) => {
                    console.log(res.data.message);
                      if (res.data.message === 'success') {
                          // Update the spending data
                          this.spending = this.spending.filter(transaction => transaction.transid !== transid);
                          this.filterTransactions();  // Re-filter transactions
                          // Arahkan ke halaman Workspace setelah login berhasil
                          this.closeTransactionModal();
                          alert("Delete successful");
                      } else {
                          console.error('Error deleting transaction:', res.data.message);
                      }
                  })
                  .catch((error) => {
                      console.error('API call failed:', error);
                  });
          },

          showTransactionModal(transaction) {
              // Logika untuk memunculkan modal dan mengisi data transaksi
              this.selectedTransaction = transaction;
              this.showModal = true;
          },
          closeTransactionModal() {
              // Logika untuk menutup modal
              this.selectedTransaction = null;
              this.showModal = false;
          },
          saveCategoryLimits() {
            const path = 'http://localhost:5000/savecategorylimits';
            const limitsData = this.categories.map(category => ({
                name: category.name,
                limit: category.limit
            }));
            
            axios.post(path, { categories: limitsData })
                .then(res => {
                    if (res.data.status === 'success') {
                        this.successMessage = 'Category limits updated successfully!';
                        setTimeout(() => {
                            this.successMessage = '';
                        }, 3000);
                    } else {
                        console.error('Error saving limits:', res.data.message);
                    }
                })
                .catch(error => {
                    console.error('API call failed:', error);
                });
        },
        addTransaction() {
            this.$router.push('/newtransaction');
        },
        editTransaction(transid) {
            this.$router.push(`/edittransaction/${transid}`);
        },
        getSpending() {
            const path = 'http://localhost:5000/workspace';
            axios.get(path)
                .then((res) => {
                    if (res.data.status === 'success') {
                        this.spending = res.data.spending; // Ambil data transaksi
                        this.filterTransactions(); // Filter data setelah fetching
                    } else {
                        console.error('API status is not success');
                    }
                })
                .catch((error) => {
                    console.error('Error fetching data:', error);
                });
        },
        filterTransactions() {
            this.filteredSpending = this.spending.filter(transaction => {
                const transactionDate = new Date(transaction.date);
                const start = this.startDate ? new Date(this.startDate) : null;
                const end = this.endDate ? new Date(this.endDate) : null;

                // Validasi jika transaksi berada di rentang tanggal
                const isWithinDateRange = (!start || transactionDate >= start) &&
                                          (!end || transactionDate <= end);

                // Validasi jika transaksi memiliki kategori yang dipilih
                const isWithinCategory = !this.selectedCategories.length || 
                    this.selectedCategories.map(c => c.toLowerCase().trim())
                    .includes(transaction.category.toLowerCase().trim());

                return isWithinDateRange && isWithinCategory;
            });
        },
        isOverBudget(categoryName, startDate = null, endDate = null) {
            // Cari kategori berdasarkan nama
            const category = this.categories.find(cat => cat.name === categoryName);
            if (!category || !category.limit) return false;

            // Filter transaksi berdasarkan kategori dan rentang tanggal (jika diberikan)
            const filteredTransactions = this.spending.filter(transaction => {
                if (transaction.category !== categoryName) return false;

                // Jika startDate atau endDate disediakan, bandingkan dengan tanggal transaksi
                const transactionDate = new Date(transaction.date);
                if (startDate && transactionDate < new Date(startDate)) return false;
                if (endDate && transactionDate > new Date(endDate)) return false;

                return true;
            });

            // Hitung total pengeluaran dari transaksi yang tersaring
            const total = filteredTransactions.reduce((sum, transaction) => {
                const amount = transaction.amount ? transaction.amount.toString().replace('$', '') : '0';
                return sum + parseFloat(amount);
            }, 0);

            // Return true jika total pengeluaran lebih besar dari limit
            return total > category.limit;
        }

    },
    watch: {
        // Panggil filterTransactions setiap kali filter berubah
        startDate: 'filterTransactions',
        endDate: 'filterTransactions',
        selectedCategories: 'filterTransactions',
    },
    async mounted() {
        await this.getSpending(); // Ambil data transaksi saat komponen dimuat
    }
};
</script>


<style scoped>
.dashboard {
  padding: 16px;
  font-family: Arial, sans-serif;
}

.header {
  font-size: 2rem;
  margin-bottom: 16px;
}

.filters {
  display: flex;
  gap: 10px;
  margin-bottom: 16px;
  flex-wrap: wrap;
  align-items: center;
}

.filters label {
  margin-right: 5px;
}

.filters input,
.filters select {
  padding: 5px;
  font-size: 14px;
}

.checkbox-group {
  display: flex;
  gap: 10px;
}

.action-buttons {
  margin-bottom: 16px;
}

.add-btn {
  padding: 10px 20px;
  font-size: 14px;
  background-color: #004da0;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.add-btn:hover {
  background-color: #004da0;
}

.transaction-table {
  display: flex;
  gap: 16px;
  margin-top: 16px;
}

.transaction-column {
  flex: 1;
}

.transaction-cards {
  display: flex;
  flex-direction: column;
}

.transaction-card {
  padding: 10px;
  border: 1px solid #ddd;
  margin-bottom: 10px;
  border-radius: 4px;
  cursor:pointer;
}

.transaction-card.over-budget {
  background-color: #ffcccc;
}

.transaction-actions {
  margin-top: 10px;
}


.delete-btn {
  padding: 6px 12px;
  font-size: 14px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.delete-btn {
  background-color: #dc3545;
  color: white;
}

.delete-btn:hover {
  background-color: #c82333;
}

.no-transactions {
  color: #777;
  font-size: 1.1rem;
}

.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.6); /* Lebih gelap untuk kontras */
    display: flex;
    align-items: center;
    justify-content: center;
    backdrop-filter: blur(5px); /* Tambahkan efek blur */
    z-index: 1000;
}

.modal {
    background: #ffffff;
    padding: 25px 30px; /* Lebih nyaman */
    border-radius: 10px;
    max-width: 500px;
    width: 90%; /* Responsif untuk layar kecil */
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2); /* Shadow lebih lembut */
    animation: fadeIn 0.3s ease-in-out; /* Tambahkan animasi masuk */
}

.modal h3 {
    margin-bottom: 15px;
    font-size: 20px;
    color: #333;
}

.modal label {
    display: block;
    margin-top: 10px;
    font-size: 14px;
    color: #555;
}

.modal input,
.modal textarea {
    width: 100%;
    margin-top: 5px;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
    font-size: 14px;
    box-sizing: border-box;
    transition: border-color 0.3s;
}

.modal input:focus,
.modal textarea:focus {
    border-color: #007BFF; /* Warna biru saat fokus */
    outline: none;
}

.modal-buttons {
    display: flex;
    justify-content: space-between;
    margin-top: 20px;
    gap: 10px;
}

.update-btn,
.delete-btn {
    flex: 1; /* Lebih proporsional */
    padding: 10px 15px;
    font-size: 14px;
    border: none;
    border-radius: 5px;
    color: #fff;
    cursor: pointer;
    transition: background-color 0.3s, transform 0.2s;
}

.update-btn {
    background-color: #007BFF;
}

.update-btn:hover {
    background-color: #0056b3;
    transform: scale(1.02);
}

.delete-btn {
    background-color: #dc3545;
}

.delete-btn:hover {
    background-color: #a71d2a;
    transform: scale(1.02);
}

.category{
  display: flex;
  /* justify-content: center; */
  margin: 30px 0px 15px 0px;
  font-size: 25px;
  font-weight: 700;
}

.structured{
  display: flex; 
  flex-direction: column;
}

.startDate{
  margin-right: 20px;
}

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: scale(0.95);
    }
    to {
        opacity: 1;
        transform: scale(1);
    }
}


</style>
