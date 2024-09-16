<template>
  <h1>Мои товары</h1>

  <table id="goods">
    <tr>
      <th colspan="3">Продукт</th>
      <th>Цена</th>
      <th>Кол-во</th>
      <th></th>
    </tr>
    <tr v-for="(el, idx) in items" :key="idx">
      <td colspan="3">{{ el.name }}</td>
      <td>{{ el.price }}</td>
      <td rowspan="1" class="count">
        <span class="countBtn" @click="this.changeCount(el.id, el.count - 1)">-</span>
        <span class="countNum">{{ el.count }}</span>
        <span class="countBtn" @click="this.changeCount(el.id, el.count + 1)">+</span>
      </td>
      <td class="removeItem" @click="this.removeItem(el.id)">Удалить</td>
    </tr>
  </table>

  <div class="statusBlock_wrapper"></div>
</template>

<script>
import axios from "axios";

export default {
  name: "ProfileView",

  data() {
    return {
      items: [],
    };
  },

  async created() {
    const token = localStorage.getItem('token');

    await axios.get("http://localhost:8000/user/items", {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
      .then(response => {
        this.items = response.data;
      })
      .catch(error => {
        if (error.response) {
          // Запрос был сделан, и сервер ответил с кодом статуса, который выходит за пределы 2xx
          console.error(`Error: ${error.response.data.detail}`);
          console.error(`Status: ${error.response.status}`);

          if (error.response.status === 401) {
            this.$router.push('/auth');
          } else if (error.response.status === 404) {
            this.$router.push('/shop');
          }
        } else if (error.request) {
          console.error('No response received:', error.request);
        } else {
          console.error('Error', error.message);
        }
      });
  },

  methods: {
    async removeItem(idx) {
      const token = localStorage.getItem('token');

      await axios.delete("http://localhost:8000/user/items/" + idx, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
        .then(response => {
          console.log(response);
          this.items = response.data.items;
          this.itemStatus("Товар удален", "d68686", "#ce5050");
        })
        .catch(error => {
          if (error.response) {
            console.error(`Error: ${error.response.data.detail}`);
            console.error(`Status: ${error.response.status}`);

            if (error.response.status === 401) {
              this.$router.push('/auth');
            } else if (error.response.status === 404) {
              this.$router.push('/shop');
            }
          } else if (error.request) {
            console.error('No response received:', error.request);
          } else {
            console.error('Error', error.message);
          }
        });
    },

    itemStatus(text, blockColor, textColor) {
      let div = document.createElement("div");
      div.innerHTML = `
          <div>
            ${text}
          </div>
      `;
      div.setAttribute(
        "style",
        `
        background-color: ${blockColor};

        border-radius: 10px;
        
        color: ${textColor};

        padding: 15px 20px;
        margin-top: 20px;

        animation: blockAppearance 700ms ease;
      `
      );

      let wrapper = document.getElementsByClassName("statusBlock_wrapper")[0];

      wrapper.append(div);

      setTimeout(() => div.remove(), 600);
    },

    async changeCount(idx, count) {
      if (count <= 0)
        return;

      const token = localStorage.getItem('token');

      await axios.put("http://localhost:8000/user/items/" + idx + '/' + count, {}, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
        .then(response => {
          console.log(response);
          this.items = response.data.items;
          this.itemStatus("Товар изменен", '#5e9269','#2c3e50');
        })
        .catch(error => {
          if (error.response) {
            console.error(`Error: ${error.response.data.detail}`);
            console.error(`Status: ${error.response.status}`);

            if (error.response.status === 401) {
              this.$router.push('/auth');
            } else if (error.response.status === 404) {
              this.$router.push('/shop');
            }
          } else if (error.request) {
            console.error('No response received:', error.request);
          } else {
            console.error('Error', error.message);
          }
        });
    },
  }
};
</script>

<style lang="scss">
.statusBlock_wrapper {
  display: flex;
  flex-direction: column;
  justify-content: end;
  align-items: center;

  font-family: "Inter", sans-serif;

  position: absolute;
  right: 50px;
  bottom: 30px;
}

h1 {
  text-align: center;
}

#goods {
  border-collapse: collapse;

  margin: 50px auto;

  width: 30%;

  tr {
    height: 40px;

    td {
      text-align: center;
    }

    .count {
      .countNum {
        margin: 0 30px;
      }

      .countBtn {
        cursor: pointer;
        opacity: 0;

        transition: all 300ms ease;
      }
    }

    .count:hover {
      .countBtn {
        opacity: 1;
      }
    }

    .removeItem {
      cursor: pointer;

      transition: all 300ms ease;
    }

    .removeItem:hover {
      color: hsl(0, 56%, 56%);
    }
  }
}
</style>
